"""Generates projects/how-one-flooded-factory-ran-america-short-of-iv-fluids/deliverables/documentary/storyboard.yaml
(Episode 44, new topics N4: How One Flooded Factory Ran America Short of IV Fluids).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the valley factory by the river (new `riverplant` set); the hospital corridor with an emptying IV bag.
- Part 1 (the factory): the valley plant, the studio, a supply-line drawing.
- Part 2 (the flood): the river rising over the levee (floodAt), the plant at night, a levee drawing.
- Part 3 (the rationing): the hospital corridor, IV bags (new `ivbag` item), charts, an allocation drawing.
- Part 4 (the airlift): the airport with planes, the plant restarting, a recovery timeline.
- Part 5 (why one factory): the office, the studio charts, a trade-off drawing.
No company logos (names in text only), no real people drawn. Lint: tools/lint_storyboard.py.
Run: python tools/gen_ivfluids_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-one-flooded-factory-ran-america-short-of-iv-fluids/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def chart(bars_, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("riverplant")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.15}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1000, y=170, at=0.05, prefix="≈ ", suffix="%", steps=[[0.05, 0], [1.5, 60]], text="OF U.S. IV SOLUTIONS, ONE PLANT (AHA ESTIMATE)", scale=1.4)]},
    sources=["aha"])
stage("s02_twist", "h_twist", {
    "zones": [Z("hospital")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("Within days"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=140, text="SEPT 2024: HURRICANE HELENE", at=0.3, size=56, color="gold"),
              it("ivbag", x=1300, y=360, at=0.3, scale=0.9, text="IV", level=[[0, 0.9], [{"cue": "a fraction"}, 0.25]]),
              it("sign", x=760, y=330, text="ORDERS: A FRACTION OF NORMAL", at=C("a fraction"), color="#FFCDD2", size=34)]},
    sources=["baxter"])
stage("s03_question", "h_question", {
    "zones": [Z("riverplant", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=170, text="ONE BUILDING. A BAG OF SALT WATER.", at=0.3, size=58, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · INSIDE THE FACTORY", at=C("what happened inside"), color="#BBDEFB", size=32),
              it("sign", x=960, y=380, text="2 · KEEPING PATIENTS SUPPLIED", at=C("kept\n    patients") if False else C("regulators kept"), color="#FFE0B2", size=30),
              it("sign", x=1560, y=380, text="3 · THE ECONOMICS", at=C("the economics of cheap"), color="#C8E6C9", size=32),
              it("letters", x=960, y=700, text="FOLLOW THE BAG", at=0.4, size=70, color="gold")]})

# ====================================================================== PART 1: the factory
card("s05_c1", "m1_card", "The Factory", "North Cove, Marion, North Carolina")
stage("s06_bag", "m1_bag", {
    "zones": [Z("hospital")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Hospitals use it"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("ivbag", x=800, y=380, at=0.3, scale=1.0, text="IV", level=0.85),
              it("letters", x=1350, y=170, text="STERILE WATER + A LITTLE SALT OR SUGAR", at=0.3, size=40, color="gold"),
              it("sign", x=1350, y=300, text="HYDRATION · DRUGS · SURGERY · ER", at=C("Hospitals use it"), color="#BBDEFB", size=32),
              it("sign", x=1350, y=400, text="COMMON · AND CHEAP", at=C("one of the cheapest"), color="#C8E6C9", size=34)]})
stage("s07_site", "m1_site", {
    "zones": [Z("riverplant")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And it calls it"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=900, y=180, text="NORTH COVE · BAXTER'S LARGEST PLANT", at=0.3, color="#FFE0B2", size=34),
              it("counter", x=1500, y=300, at=C("with"), prefix="", suffix="+", steps=[[0, 0], [{"cue": "employees"}, 2500]], text="EMPLOYEES (BAXTER)"),
              it("letters", x=1300, y=440, text="LARGEST U.S. MAKER OF IV + DIALYSIS SOLUTIONS", at=C("And it calls it"), size=34, color="gold")]},
    sources=["baxter"])
stage("s08_output", "m1_output", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("counter", x=620, y=330, at=0.3, prefix="", suffix="M+", steps=[[0, 0], [{"cue": "every single"}, 1]], text="IV SOLUTIONS A DAY (BAXTER)", scale=1.3),
              it("counter", x=1320, y=330, at=C("The hospital association"), prefix="≈ ", suffix="%", steps=[[0, 0], [{"cue": "used in the country"}, 60]], text="OF U.S. DAILY USE (AHA ESTIMATE)", scale=1.3),
              it("letters", x=960, y=640, text="BAXTER GAVE NO PERCENTAGE", at=C("never gave a percentage"), size=46, color="gold")]},
    sources=["baxter", "aha"])
stage("s09_size", "m1_size", {
    "zones": [Z("riverplant")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": C("It is not a small"), "x": 1300, "y": 520, "zoom": 0.95, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=1000, y=380, text="THE BUILDING ITSELF", at=0.3, until=C("It is not a small"), size=54, color="gold"),
              it("sign", x=800, y=170, text="1.4M+ SQ FT", at=C("one point four million"), color="#BBDEFB", size=40),
              it("sign", x=1400, y=170, text="$500M+ INVESTED SINCE 2017", at=C("five hundred million"), color="#FFE0B2", size=36),
              it("letters", x=1300, y=300, text="BUILT TO BE EFFICIENT", at=C("It is not a small"), size=50, color="gold")]},
    sources=["baxter"])
stage("s10_few", "m1_few", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="WHO ELSE MAKES THEM? (ICU MEDICAL 10-K)", at=0.3, size=44, color="gold"),
              it("sign", x=650, y=280, text="BAXTER", at=C("compete in the U.S."), color="#FFCDD2", size=44),
              it("sign", x=1000, y=280, text="B. BRAUN", at=C("compete in the U.S.", 0.5), color="#BBDEFB", size=44),
              it("sign", x=1350, y=280, text="ICU MEDICAL", at=C("compete in the U.S.", 1.0), color="#C8E6C9", size=44),
              it("letters", x=1000, y=420, text="THREE MAKERS · ONE GIANT PLANT", at=C("Three companies"), size=44, color="white")]},
    sources=["rivals"])
add("p11_supply", "m1_draw", "engine_draw", {
    "title": "The supply line (illustration)", "board": BOARD, "draw_start": C("Here is one big factory"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(780, 330, 260, 120), "color": "risk", "width": 6, "kind": "box", "start": C("Here is one big factory"), "label": lbl("BIG PLANT", 910, 398, 26, "risk")},
        {"d": rect(1220, 330, 150, 60), "color": "muted", "width": 4, "kind": "box", "start": C("two smaller makers"), "label": lbl("MAKER 2", 1295, 368, 18, "muted")},
        {"d": rect(1220, 410, 150, 60), "color": "muted", "width": 4, "kind": "box", "start": C("two smaller makers", 0.4), "label": lbl("MAKER 3", 1295, 448, 18, "muted")},
        {"d": rect(700, 560, 180, 70), "color": "accent2", "width": 4, "kind": "box", "start": C("trucks go out to distributors"), "label": lbl("DISTRIBUTOR", 790, 603, 18, "accent2")},
        {"d": rect(960, 560, 180, 70), "color": "accent2", "width": 4, "kind": "box", "start": C("trucks go out to distributors", 0.4), "label": lbl("DISTRIBUTOR", 1050, 603, 18, "accent2")},
        {"d": arrow((880, 455), (790, 555)) + " " + arrow((940, 455), (1050, 555)), "color": "risk", "width": 5, "kind": "arrow", "start": C("trucks go out", 0.6)},
        {"d": " ".join(rect(640 + k * 110, 740, 70, 50) for k in range(7)), "color": "accent3", "width": 3, "kind": "stroke", "start": C("to thousands of hospitals"), "label": lbl("HOSPITALS", 990, 830, 22, "accent3")},
        {"d": arrow((790, 635), (700, 735)) + " " + arrow((800, 635), (900, 735)) + " " + arrow((1050, 635), (1010, 735)) + " " + arrow((1060, 635), (1230, 735)), "color": "ink", "width": 3, "kind": "arrow", "start": C("to thousands of hospitals", 0.5)},
    ],
    "actions": [{"kind": "point", "at": C("Most of the arrows", 0.1), "dur": 1.4, "target": [910, 400]}],
    "scale": 0.86, "floor": 1040}, sources=["baxter", "rivals"])
kinetic("s12_t1", "m1_transition", [("For years, that shape worked…", 62, "that shape worked fine", None, False),
                                    ("…then the rain came", 70, "the rain came", "gold", False)])

# ====================================================================== PART 2: the flood
card("s13_c2", "m2_card", "The Flood", "Hurricane Helene, September 2024")
stage("s14_storm", "m2_storm", {
    "zones": [Z("riverplant", floodAt=C("Rivers rose fast"))], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("At North Cove"), "x": 1200, "y": 560, "zoom": 1.05, "dur": 2.0}], "drift": 3,
    "items": [it("storm", x=1000, y=120, at=0.2, scale=1.0),
              it("letters", x=1000, y=260, text="'A LEVEE BREACH' (BAXTER)", at=C("triggered a levee breach"), size=54, color="gold")]},
    sources=["baxter"])
stage("s15_closed", "m2_closed", {
    "zones": [Z("riverplant", night=True, floodAt=0)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The bridges"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="SEPT 29: 'CLOSED FOR PRODUCTION'", at=0.3, size=52, color="gold"),
              it("sign", x=1300, y=270, text="BRIDGES TO THE SITE DAMAGED", at=C("The bridges"), color="#FFCDD2", size=34),
              it("barrier", x=700, at=C("could not easily reach"), scale=0.8)]},
    sources=["baxter"])
stage("s16_inside", "m2_inside", {
    "zones": [Z("fab")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A flooded line"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=130, text="STERILE IS NOT ORDINARY", at=0.3, size=56, color="gold"),
              it("sign", x=800, y=270, text="CLEAN · CHECK · PROVE SAFE", at=C("Every production line"), color="#BBDEFB", size=34),
              it("sign", x=1400, y=270, text="NO 'JUST DRY IT AND RESTART'", at=C("A flooded line"), color="#FFCDD2", size=34)]})
add("p17_levee", "m2_draw", "engine_draw", {
    "title": "The levee (illustration)", "board": BOARD, "draw_start": C("Here is the river"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 760 Q 760 730 960 760 T 1360 760", "color": "accent2", "width": 8, "kind": "stroke", "start": C("Here is the river"), "label": lbl("RIVER", 620, 800, 22, "accent2")},
        {"d": "M 880 740 L 940 640 L 1000 740", "color": "muted", "width": 7, "kind": "stroke", "start": C("Here is the levee"), "label": lbl("LEVEE", 940, 620, 22, "muted")},
        {"d": rect(1060, 520, 260, 220), "color": "ink", "width": 6, "kind": "box", "start": C("Here is the factory"), "label": lbl("FACTORY", 1190, 640, 26, "ink")},
        {"d": "M 560 700 Q 760 660 960 690 T 1360 690", "color": "accent2", "width": 6, "kind": "stroke", "start": C("The water rises")},
        {"d": "M 930 650 L 950 690 L 925 720 M 960 660 L 975 700", "color": "risk", "width": 7, "kind": "stroke", "start": C("The levee breaks"), "label": lbl("BREACH", 960, 600, 24, "risk")},
        {"d": arrow((1000, 700), (1120, 680), 0.2), "color": "accent2", "width": 6, "kind": "arrow", "start": C("The levee breaks", 0.5)},
    ],
    "actions": [{"kind": "point", "at": C("one break in one place", 0.1), "dur": 1.4, "target": [950, 680]}],
    "scale": 0.86, "floor": 1040}, sources=["baxter"])
kinetic("s18_t2", "m2_transition", [("Within days…", 72, "Within days", None, False),
                                    ("…hospitals felt it", 72, "felt it", "gold", False)])

# ====================================================================== PART 3: the rationing
card("s19_c3", "m3_card", "The Rationing", "Hospitals on allocation")
stage("s20_alloc", "m3_alloc", {
    "zones": [Z("hospital")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("On October ninth"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="'ALLOCATION': A SET SHARE OF NORMAL ORDERS", at=0.3, size=42, color="gold"),
              it("sign", x=750, y=290, text="DIRECT CUSTOMERS: 40%", at=C("At first"), color="#FFE0B2", size=34),
              it("sign", x=750, y=390, text="DISTRIBUTORS: 10%", at=C("For distributors"), color="#FFCDD2", size=34),
              it("sign", x=1450, y=310, text="OCT 9: BOTH → 60%", at=C("On October ninth"), color="#C8E6C9", size=38),
              it("ivbag", x=1750, y=520, at=0.4, scale=0.7, pole=False, text="IV", level=[[0, 0.4], [{"cue": "On October ninth"}, 0.6]])]},
    sources=["baxter"])
stage("s21_survey", "m3_survey", {
    "zones": [Z("hospital", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="PHARMACISTS' SURVEY (ASHP, OCT 2024)", at=0.3, size=44, color="gold"),
              it("counter", x=700, y=300, at=C("of respondents") if False else C("In a survey"), prefix="", suffix="%", steps=[[0, 0], [{"cue": "moderate or critical"}, 84]], text="MODERATE OR CRITICAL IMPACT", scale=1.2),
              it("counter", x=1400, y=300, at=C("almost half"), prefix="", suffix="%", steps=[[0, 0], [{"cue": "two weeks of fluids"}, 47]], text="≤ 2 WEEKS OF FLUIDS LEFT", scale=1.2)]},
    sources=["ashp"])
stage("s22_saving", "m3_saving", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Pharmacists, doctors"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=800, y=200, text="FDA: TEMPORARY COMPOUNDING GUIDANCE", at=C("The FDA issued"), color="#BBDEFB", size=32),
              it("letters", x=1300, y=330, text="EVERY BAG HAD TO COUNT", at=C("every single bag"), size=52, color="gold"),
              *[it("ivbag", x=600 + k * 350, y=560, at=0.3 + 0.2 * k, scale=0.55, pole=False, level=0.5 - 0.1 * k) for k in range(4)]]},
    sources=["fda"])
add("p23_alloc", "m3_draw", "engine_draw", {
    "title": "The allocation (Baxter percentages)", "board": BOARD, "draw_start": C("Here is a normal order"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 760 860 L 1500 860", "color": "ink", "width": 4, "start": C("Let me draw the allocation")},
        {"d": "M 820 860 L 820 400 L 980 400 L 980 860", "color": "muted", "width": 5, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is a normal order"), "label": lbl("NORMAL · 100", 900, 380, 22, "muted")},
        {"d": "M 1060 860 L 1060 584 L 1220 584 L 1220 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("a direct customer gets"), "label": lbl("DIRECT · 60", 1140, 564, 22, "accent")},
        {"d": "M 1300 860 L 1300 814 L 1460 814 L 1460 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("A distributor"), "label": lbl("DISTRIBUTOR · 10 (AT FIRST)", 1380, 794, 18, "risk")},
        {"d": "M 820 400 L 1460 400", "color": "risk", "width": 3, "kind": "stroke", "start": C("The gap between"), "label": lbl("THE GAP", 1300, 380, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("where hospitals had to", 0.1), "dur": 1.4, "target": [1300, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["baxter"])
kinetic("s24_t3", "m3_transition", [("Where could America find…", 62, "Where could America", None, False),
                                    ("…millions of extra bags, fast?", 62, "millions of extra bags", "gold", False)])

# ====================================================================== PART 4: the airlift
card("s25_c4", "m4_card", "The Airlift", "Fluids flown across oceans")
stage("s26_fda", "m4_fda", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And it helped"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("docs", x=700, y=560, at=0.3, text="FDA SHORTAGE LIST", scale=0.7, stamp="ADDED", stampAt=C("shortage list")),
              it("counter", x=1450, y=280, at=C("And it helped"), prefix="", suffix="", steps=[[0, 0], [{"cue": "different IV and dialysis"}, 23]], text="FLUIDS CLEARED FOR IMPORT, FROM 5 BAXTER PLANTS (FDA)", scale=1.2)]},
    sources=["fda"])
stage("s27_planes", "m4_planes", {
    "zones": [Z("airport")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Water,"), "x": 1300, "y": 500, "zoom": 1.0, "dur": 2.0}], "drift": 3,
    "items": [it("plane", x=1250, y=620, at=0.2, scale=1.3),
              it("plane", x=[[0.3, -300], [6, 2400]], y=[[0.3, 300], [6, 200]], at=0.3, scale=0.9),
              it("plane", x=[[{"cue": "airplanes"}, -300], [{"cue": "Water,"}, 2400]], y=260, at=C("airplanes"), scale=0.7),
              it("counter", x=800, y=200, at=C("According to Baxter"), prefix="≈ ", suffix="", steps=[[0, 0], [{"cue": "airplanes"}, 200]], text="FLIGHTS BY END OF 2024 (BAXTER)"),
              it("counter", x=1500, y=200, at=C("airplanes"), prefix="≈ ", suffix="", steps=[[0, 0], [{"cue": "of fluids"}, 18000]], text="TONS OF PRODUCT (BAXTER)")]},
    sources=["baxter"])
stage("s28_rivals", "m4_rivals", {
    "zones": [Z("warehouse")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But neither could"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("pallet", x=[[0, 300], [6, 900]], at=0.2, rows=3, scale=0.8),
              it("sign", x=800, y=200, text="B. BRAUN: +20% OUTPUT (CA, FL)", at=0.3, color="#BBDEFB", size=34),
              it("sign", x=1500, y=300, text="ICU MEDICAL: HIGHER DEMAND, LATE 2024", at=C("ICU Medical reported"), color="#C8E6C9", size=32),
              it("letters", x=1250, y=440, text="NO ONE COULD REPLACE IT OVERNIGHT", at=C("But neither could"), size=44, color="gold")]},
    sources=["rivals"])
stage("s29_restart", "m4_restart", {
    "zones": [Z("riverplant")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By late January"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="LINE BY LINE", at=0.3, size=60, color="gold"),
              it("sign", x=950, y=250, text="OCT 31: FIRST LINE (≈ 25% OF OUTPUT)", at=C("Baxter restarted its first line"), color="#BBDEFB", size=28),
              it("sign", x=1600, y=250, text="NOV 21: FIRST BAGS RELEASED", at=C("released its first bags"), color="#FFE0B2", size=28),
              it("sign", x=1050, y=350, text="JAN 28: ALL 10 LINES", at=C("all ten lines"), color="#C8E6C9", size=30),
              it("sign", x=1600, y=350, text="FEB 17: PRE-STORM OUTPUT", at=C("On February seventeenth"), color="#C8E6C9", size=30)]},
    sources=["baxter"])
stage("s30_bill", "m4_bill", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "LOST SALES (EST.)", "value": 110, "color": "#90A4AE", "at": C("cut its sales"), "display": "$110M"},
                     {"label": "CLEANUP + IDLE + FREIGHT", "value": 317, "color": "#E53935", "at": C("It recorded"), "display": "$317M"},
                     {"label": "INSURANCE", "value": 251, "color": "#43A047", "at": C("offset by"), "display": "−$251M"}],
                    at=0.2, max=350, title="WHAT THE FLOOD COST BAXTER IN 2024 (10-K)", x=300, w=1200)]},
    sources=["tenk"])
add("p31_recovery", "m4_draw", "engine_draw", {
    "title": "Eight months, flood to normal (Baxter)", "board": BOARD, "draw_start": C("Here is the flood"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 740 640 L 1600 640", "color": "ink", "width": 5, "start": C("Let me draw the recovery")},
        {"d": rect(740, 500, 150, 70), "color": "risk", "width": 5, "kind": "box", "start": C("Here is the flood"), "label": lbl("SEP: FLOOD", 815, 543, 18, "risk")},
        {"d": rect(910, 680, 150, 70), "color": "accent2", "width": 4, "kind": "box", "start": C("The first line"), "label": lbl("OCT: LINE 1", 985, 723, 18, "accent2")},
        {"d": rect(1080, 500, 150, 70), "color": "accent2", "width": 4, "kind": "box", "start": C("All ten\n    lines") if False else C("at the end of January"), "label": lbl("JAN: 10 LINES", 1155, 543, 18, "accent2")},
        {"d": rect(1250, 680, 150, 70), "color": "accent3", "width": 4, "kind": "box", "start": C("Full output"), "label": lbl("FEB: FULL", 1325, 723, 18, "accent3")},
        {"d": rect(1420, 500, 160, 70), "color": "accent3", "width": 5, "kind": "box", "start": C("almost every product"), "label": lbl("MAY: NORMAL", 1500, 543, 18, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("Eight months", 0.1), "dur": 1.4, "target": [1180, 640]}],
    "scale": 0.86, "floor": 1040}, sources=["baxter"])
kinetic("s32_t4", "m4_transition", [("The fluids came back…", 64, "The fluids came back", None, False),
                                    ("…why one building?", 70, "one building carrying", "gold", False)])

# ====================================================================== PART 5: why one factory
card("s33_c5", "m5_card", "Why One Factory", "The economics of cheap medicine")
stage("s34_cheap", "m5_cheap", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In the year"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="ROOT CAUSE #1: 'LACK OF INCENTIVES' (FDA, 2019)", at=C("listed the first root cause"), size=40, color="gold"),
              it("counter", x=760, y=300, at=C("Of the shortage drugs"), prefix="", suffix="%", steps=[[0, 0], [{"cue": "sterile injectables"}, 63]], text="OF SHORTAGE DRUGS: STERILE INJECTABLES"),
              it("counter", x=1500, y=300, at=C("In the year"), prefix="$", suffix="", decimals=2, steps=[[0, 0], [{"cue": "just"}, 8.73]], text="MEDIAN PRICE PER UNIT"),
              it("letters", x=1000, y=520, text="THE FDA'S STUDY", at=0.3, until=C("listed the first root cause"), size=56, color="gold")]},
    sources=["roots"])
stage("s35_margin", "m5_margin", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("When margins are thin"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("sign", x=900, y=220, text="GAO, 2014: 'LOW PROFIT MARGINS HAVE LIMITED INFRASTRUCTURE INVESTMENTS'", at=0.3, color="#FFE0B2", size=26),
              it("letters", x=1250, y=360, text="THIN MARGINS → ONE HUGE PLANT", at=C("When margins are thin"), size=48, color="gold")]},
    sources=["roots"])
stage("s36_maria", "m5_maria", {
    "zones": [Z("tropic")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Two\n    storms") if False else C("seven years apart"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("storm", x=1000, y=120, at=0.2, scale=0.9),
              it("sign", x=900, y=270, text="2017: HURRICANE MARIA · SALINE PLANT, PUERTO RICO", at=0.3, color="#FFE0B2", size=30),
              it("letters", x=1250, y=400, text="TWO STORMS · SEVEN YEARS · SAME LESSON", at=C("seven years apart"), size=42, color="gold")]},
    sources=["maria"])
add("p37_tradeoff", "m5_draw", "engine_draw", {
    "title": "The trade-off (illustration)", "board": BOARD, "draw_start": C("On one side, one big plant"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 1080 380 L 1080 860", "color": "muted", "width": 3, "start": C("Let me draw the trade-off")},
        {"d": rect(780, 440, 240, 160), "color": "risk", "width": 6, "kind": "box", "start": C("On one side, one big plant"), "label": lbl("ONE BIG PLANT", 900, 528, 22, "risk")},
        {"d": "M 780 680 L 1020 680", "color": "risk", "width": 1, "start": C("Cheaper per bag"), "label": lbl("CHEAPER · ONE WEAK POINT", 900, 700, 18, "risk")},
        {"d": " ".join(rect(1140 + (k % 3) * 100, 440 + (k // 3) * 90, 80, 70) for k in range(6)), "color": "accent3", "width": 4, "kind": "stroke", "start": C("many smaller\n    plants") if False else C("On the other, many smaller"), "label": lbl("MANY PLANTS", 1290, 660, 22, "accent3")},
        {"d": "M 1140 720 L 1430 720", "color": "accent3", "width": 1, "start": C("More expensive"), "label": lbl("COSTLIER · RESILIENT", 1290, 740, 18, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("the market keeps", 0.1), "dur": 1.4, "target": [900, 520]}],
    "scale": 0.86, "floor": 1040}, sources=["roots"])

# ====================================================================== PAYOFF
stage("s38_payoff", "payoff", {
    "zones": [Z("riverplant", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("The system is efficient"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=130, text="NOBODY IS PAID TO BUILD A BACKUP", at=0.3, size=54, color="gold"),
              it("sign", x=800, y=270, text="EFFICIENT ON A NORMAL DAY", at=C("The system is efficient"), color="#C8E6C9", size=32),
              it("sign", x=1400, y=270, text="FRAGILE ON A BAD ONE", at=C("fragile on a bad one"), color="#FFCDD2", size=32)]},
    sources=["roots", "baxter"])
add("s39_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_ivfluids_storyboard.py; edit the generator, not this file.\n"
           "# Episode 44 storyboard (IV fluids): one visual language per part; tones from visual_direction.yaml.\n")
