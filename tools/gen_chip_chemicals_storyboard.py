"""Generates projects/the-chemicals-that-decide-who-makes-chips/deliverables/documentary/storyboard.yaml (Episode 18, C5).

Bespoke worlds for the materials chokepoints (tones from visual_direction.yaml: thriller -> tech -> crisis -> strategy ->
reflective): the new `vessel` item (an amber resist bottle, a neon gas cylinder with a gauge, a stack of gallium bars,
each of which can drain or be padlocked) is the through-line; a clean room where a line stops when the bottle runs
dry, a Japanese chemical plant, a port barrier for 2019, a steel plant and a cylinder whose gauge falls in 2022, a
night port and a price chart for gallium, a boardroom for JSR's buy-out, and a Taiwan plant. Presenter: the cheap
ingredient with the same power as the machine, three kinds of chokepoints.
No flags, no logos (names in text only), no likeness of real people, no smiling sun.
Run: python tools/gen_chip_chemicals_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-chemicals-that-decide-who-makes-chips/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
JP, KR, UA, CN = "#C62828", "#1565C0", "#FFB300", "#B71C1C"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 5, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("fab", label="yellow")], "worldW": 2400,
    "cam": [{"at": 0, "x": 700, "y": 560, "zoom": 1.3}, {"at": C("a missing"), "x": 1200, "y": 540, "zoom": 0.95, "dur": 2.6}], "drift": 0,
    "items": [it("vessel", mode="bottle", x=600, at=0.2, scale=1.2, level=[[0, 0.8], [{"cue": "a missing"}, 0.8], [{"cue": "a missing", "offset": 2}, 0.0]], glow=True),
              it("conveyor", x0=900, x1=2400, y=F - 40, at=0, n=8, speed=140, goods="chip", stopAt=C("a missing", 1.5)),
              it("litho", x=1700, at=0.4, fireAt=0.6, text="EUV MACHINE", scale=0.6)],
    "callouts": [co("Not a broken machine…", 960, 150, C("not by a broken"), "white", screen=True, size=42, until=C("a missing", -0.3)),
                 co("…a missing bottle of liquid", 960, 150, C("a missing"), "gold", screen=True, size=44)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("port")], "worldW": 3200,
    "cam": [{"at": 0, "x": 1600, "y": 560, "zoom": 0.8}, {"at": C("Each time"), "x": 1600, "y": 540, "zoom": 0.9, "dur": 2.6}], "drift": 3,
    "items": [it("vessel", mode="bottle", x=900, at=C("A chemical from Japan"), scale=0.8, label="RESIST", text="JAPAN"),
              it("vessel", mode="tank", x=1600, at=C("a gas from Ukraine"), scale=0.7, label="NEON", text="UKRAINE"),
              it("vessel", mode="ingot", x=2300, at=C("a metal from China"), scale=0.9, label="GALLIUM", text="CHINA"),
              it("litho", x=3000, at=C("a machine worth"), fireAt=C("a machine worth", 0.3), text="$ HUNDREDS OF MILLIONS", scale=0.55)],
    "callouts": [co("A chemical, a gas, a metal", 960, 960, C("A chemical from Japan"), "white", screen=True, size=42, until=C("Each time", -0.3)),
                 co("The weakest link fits in a truck", 960, 960, C("something that fits"), "gold", screen=True, size=42)]},
    sources=["ihs_2019", "reg_neon", "usgs_ga"])

# ====================================================================== PART 1: the liquid
card("s03_c1", "m1_card", "The Liquid That Draws Circuits", "Photoresist")
stage("s04_q1", "m1_question", {
    "zones": [Z("fab", label="yellow")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.35}, {"at": 3.0, "x": 960, "y": 560, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vessel", mode="bottle", x=700, at=0.2, scale=0.9, label="?", glow=True),
              it("vessel", mode="tank", x=1000, at=0.5, scale=0.7, label="?"),
              it("vessel", mode="ingot", x=1350, at=0.8, scale=0.8, label="?")],
    "callouts": [co("The most important chemical in a chip factory?", 960, 150, C("What is the most"), "gold", screen=True, size=38)]})
stage("s05_resist", "m1_resist", {
    "zones": [Z("fab", label="yellow")], "worldW": 2600, "min_seconds": 18,
    "cam": [{"at": 0, "x": 700, "y": 560, "zoom": 1.15}, {"at": C("When the lithography machine"), "x": 1400, "y": 500, "zoom": 1.05, "dur": 2.6},
            {"at": C("No resist"), "x": 1300, "y": 520, "zoom": 0.9, "dur": 2.2}], "drift": 2,
    "items": [it("vessel", mode="bottle", x=600, at=0.2, scale=1.0, level=[[0, 0.9], [{"cue": "spread across"}, 0.9], [{"cue": "spread across", "offset": 2}, 0.7]]),
              it("wafer", x=1150, y=420, r=180, at=C("spread across"), spin=10, revealAt=C("Wash it"), fail=0.0),
              it("mirrors", x=1800, y=460, at=C("When the lithography machine", -0.4), beamAt=C("shines its pattern"), dur=2.5, scale=0.55),
              it("letters", x=1300, y=170, text="NO RESIST = NO CHIP", at=C("No resist"), size=60, color="risk")],
    "callouts": [co("Photoresist: a light-sensitive liquid", 960, 960, C("A strong candidate"), "gold", screen=True, size=40, until=C("When the lithography machine", -0.3)),
                 co("Light changes it; washing leaves the circuit", 960, 960, C("When the lithography machine"), "white", screen=True, size=38, until=C("No resist", -0.3)),
                 co("No resist, no pattern. No pattern, no chip.", 960, 960, C("No resist"), "risk", screen=True, size=40)]},
    sources=["thw_jsr"])
stage("s06_recipe", "m1_recipe", {
    "zones": [Z("sciencepark")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("hundreds of test cycles"), "x": 1500, "y": 540, "zoom": 0.9, "dur": 2.4}], "drift": 3,
    "items": [it("vessel", mode="bottle", x=700, at=0.2, scale=0.8, label="RECIPE v1"),
              it("vessel", mode="bottle", x=950, at=C("a new recipe"), scale=0.8, label="RECIPE v2", glow=True),
              it("clock", x=1500, y=360, at=C("hundreds of test cycles"), period=1.2, text="TEST CYCLES"),
              *crowd([1800, 1950], "read", at=C("the resist maker"), scale=0.7),
              it("calendar", x=2200, y=320, at=C("One of the biggest"), pages=[[0, "≈ 2", "YEARS"]], scale=0.8)],
    "callouts": [co("Every generation needs a new recipe", 960, 960, C("Every new generation"), "white", screen=True, size=40, until=C("hundreds of test cycles", -0.3)),
                 co("Hundreds of test cycles, chipmaker and supplier", 960, 960, C("hundreds of test cycles"), "gold", screen=True, size=38, sub="Tom's Hardware", until=C("One of the biggest", -0.3)),
                 co("TOK: a new resist takes up to two years", 960, 960, C("One of the biggest"), "white", screen=True, size=40, sub="Reuters, 2019")]},
    sources=["thw_jsr", "aj_2019"])
stage("s07_japan", "m1_japan", {
    "zones": [Z("carplant", -1600, 1800), Z("fab", 1800, 6000, label="yellow")], "worldW": 3400,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("But it means"), "x": 2300, "y": 540, "zoom": 0.85, "dur": 2.6},
            {"at": C("And this resist sells"), "x": 1200, "y": 540, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("sign", x=900, y=250, text="JAPAN · CHEMICAL PLANTS", at=0.3, color="#FFCDD2", size=34),
              it("tower", x=600, text="TOK", color=JP, h=420, at=C("Tokyo Ohka Kogyo"), scale=0.75),
              it("tower", x=900, text="JSR", color="#AD1457", h=380, at=C("JSR"), scale=0.75),
              it("tower", x=1200, text="SHIN-ETSU", color="#6A1B9A", h=350, at=C("Shin-Etsu"), scale=0.75),
              it("letters", x=900, y=700, text="≈ 90%", at=C("of the world market"), size=90, color="gold"),
              *[it("litho", x=2200 + k * 340, at=C("But it means", 0.3 * k), fireAt=C("But it means", 0.3 * k + 0.4), text=n, scale=0.42) for k, n in enumerate(["TAIWAN", "KOREA", "USA"])],
              it("coins", **{"from": [2500, 600], "to": [900, 600]}, at=C("But it means", 1), rate=4),
              it("pricetag", x=1500, y=300, at=C("And this resist sells"), pages=[[0, "$1,800"]], sub="per gallon (EUV resist)")],
    "callouts": [co("3 Japanese firms: {{euv_share.display}} of EUV resist (estimate)", 960, 960, C("According to the research firm"), "gold", screen=True, size=36, sub="QYResearch via Digital Today", until=C("But it means", -0.3)),
                 co("The top fabs all depend on a few Japanese plants", 960, 960, C("But it means"), "white", screen=True, size=38, until=C("And this resist sells", -0.3)),
                 co("{{euv_share.gal_display}}", 960, 960, C("And this resist sells"), "gold", screen=True, size=44)]},
    sources=["dt_japan", "thw_jsr"])
stage("s08_layers", "m1_layers", {
    "zones": [Z("fab", label="yellow")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("Each layer needs"), "x": 1500, "y": 540, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("hbm", x=800, y=520, at=0.3, scale=0.6, dur=6, layers=10, text="2 nm CHIP"),
              it("counter", x=800, y=200, at=C("adds"), prefix="+", suffix="%", steps=[[0, 0], [{"cue": "adds", "offset": 1.5}, 30]], text="EUV LAYERS vs 3 nm"),
              it("vessel", mode="bottle", x=1500, at=C("Each layer needs"), scale=0.7, level=[[0, 1], [{"cue": "Each layer needs", "offset": 6}, 0.2]]),
              it("sign", x=2000, y=330, text="HOYA · BLANK MASKS", sub="another Japanese specialist", at=C("Hoya"), color="#FFE0B2", size=30),
              it("letters", x=1500, y=160, text="MORE LAYERS, MORE MATERIAL", at=C("The smaller the chip"), size=48, color="gold")],
    "callouts": [co("2 nm: {{layers.display}} vs 3 nm", 960, 960, C("adds"), "gold", screen=True, size=40, sub="Korean industry figures (Digital Today)", until=C("Each layer needs", -0.3)),
                 co("Each layer: resist + a mask on a Hoya blank", 960, 960, C("Each layer needs"), "white", screen=True, size=38)]},
    sources=["dt_japan"])
add("p09_power", "m1_draw", "engine_draw", {
    "title": "Why a tiny market holds so much power", "board": BOARD, "draw_start": C("The machine that prints"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 340, 340, 230), "color": "accent2", "width": 6, "start": C("The machine that prints"), "label": lbl("MACHINE: $ HUNDREDS OF M", 730, 460, 22, "accent2")},
        {"d": rect(1160, 440, 110, 130), "color": "accent", "width": 5, "start": C("The resist on a wafer"), "label": lbl("RESIST: ¢", 1215, 515, 24, "accent")},
        {"d": "M 920 455 L 1140 505", "color": "ink", "width": 4, "start": C("the factory needs both"), "label": lbl("BOTH NEEDED", 1030, 440, 22, "ink")},
        {"d": "M 600 700 L 1440 700", "color": "accent3", "width": 6, "start": C("If either one"), "label": lbl("production line", 1020, 680, 22, "accent3")},
        {"d": "M 980 660 L 1060 740 M 1060 660 L 980 740", "color": "risk", "width": 8, "start": C("the whole line stops"), "label": lbl("STOP", 1020, 790, 30, "risk")},
        {"d": "M 730 600 Q 970 860 1215 600", "color": "accent", "width": 5, "start": C("the same power"), "label": lbl("same power", 970, 880, 26, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("the whole line stops", 0.2), "dur": 1.4, "target": [1020, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["dt_japan"])
kinetic("s10_t1", "m1_transition", [("In 2019", 72, "In twenty nineteen", None, False), ("one country tested exactly that idea", 52, "one country tested", "risk", True)])

# ====================================================================== PART 2: the test (2019)
card("s11_c2", "m2_card", "The Test", "Japan and Korea, 2019")
stage("s12_q2", "m2_question", {
    "zones": [Z("port")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.3}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vessel", mode="bottle", x=700, at=0.2, scale=0.8, lockAt=2.5),
              it("barrier", x=1200, text="EXPORTS", at=0.4, closeAt=2.0)],
    "callouts": [co("What happens when a supplier closes the tap?", 960, 150, C("What happens"), "gold", screen=True, size=40)]})
stage("s13_curbs", "m2_curbs", {
    "zones": [Z("parliament", -1600, 1500), Z("port", 1500, 6000)], "worldW": 3400,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("Fluorinated polyimide"), "x": 2000, "y": 540, "zoom": 0.95, "dur": 2.4},
            {"at": C("Korea is home"), "x": 2700, "y": 540, "zoom": 1.0, "dur": 2.4}, {"at": C("And Japan supplied"), "x": 1900, "y": 540, "zoom": 0.8, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "JUL 1", "2019"]], scale=0.8),
              it("docs", x=850, y=540, at=C("Japan announced"), text="EXPORT RULES", scale=0.7, stamp="RESTRICTED", stampAt=C("restrict exports")),
              it("vessel", mode="bottle", x=1750, at=C("Fluorinated polyimide"), scale=0.6, label="POLYIMIDE", sub="screens", lockAt=C("Photoresist")),
              it("vessel", mode="bottle", x=2000, at=C("Photoresist"), scale=0.6, label="RESIST", lockAt=C("ultra-pure hydrogen")),
              it("vessel", mode="tank", x=2250, at=C("ultra-pure hydrogen"), scale=0.5, label="HF", color="#CFD8DC", lockAt=C("used to clean", 0.5)),
              it("barrier", x=2550, text="TO KOREA", at=C("Japan announced", 1), closeAt=C("restrict exports", 1)),
              it("tower", x=2900, text="SAMSUNG", color=KR, h=460, at=C("Korea is home"), scale=0.75),
              it("tower", x=3200, text="SK HYNIX", color="#FF8A65", h=420, at=C("Korea is home", 0.3), scale=0.75),
              it("letters", x=2000, y=200, text="≈ 70%+", at=C("And Japan supplied"), size=90, color="gold")],
    "callouts": [co("1 July 2019: Japan restricts three materials to Korea", 960, 960, C("Japan announced"), "risk", screen=True, size=36, sub="IHS Markit", until=C("Korea is home", -0.3)),
                 co("Home to Samsung and SK hynix", 960, 960, C("Korea is home"), "white", screen=True, size=40, until=C("And Japan supplied", -0.3)),
                 co("Japan: ≈ 70%+ of world supply (one estimate)", 960, 960, C("And Japan supplied"), "gold", screen=True, size=38, sub="Reuters, 2019")]},
    sources=["ihs_2019", "oled_2019", "aj_2019"], sfx=[{"kind": "hit", "cue": "restrict exports", "gain": 0.3}])
stage("s14_scramble", "m2_scramble", {
    "zones": [Z("sciencepark", -1600, 1600), Z("site", 1600, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("Soulbrain"), "x": 2100, "y": 540, "zoom": 1.0, "dur": 2.4},
            {"at": C("For the first time"), "x": 1500, "y": 540, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [*crowd([500, 650, 800], "read", at=C("Samsung stepped up"), scale=0.7),
              *[it("vessel", mode="bottle", x=1050 + k * 150, at=C("from other suppliers", 0.3 * k), scale=0.45, label=f"TEST {k + 1}") for k in range(3)],
              it("crane", x=2100, text="SOULBRAIN · HF PLANT", at=C("Soulbrain"), progress=[[0, 0.3], [20, 0.8]], scale=0.8),
              it("docs", x=2600, y=540, at=C("case-by-case"), text="LICENCE", scale=0.6),
              it("letters", x=1500, y=200, text="CHEMICALS AS A LEVER", at=C("For the first time"), size=56, color="risk")],
    "callouts": [co("Samsung tests non-Japanese resist and HF", 960, 960, C("Samsung stepped up"), "white", screen=True, size=38, sub="Reuters, 2019", until=C("Soulbrain", -0.3)),
                 co("Soulbrain races to match Japanese purity", 960, 960, C("Soulbrain"), "gold", screen=True, size=38, until=C("For the first time", -0.3)),
                 co("A supply of chemicals turned into a lever", 960, 960, C("For the first time"), "risk", screen=True, size=40)]},
    sources=["aj_2019"])
add("p15_after", "m2_after", "engine_draw", {
    "title": "Did Korea break free?", "board": BOARD, "draw_start": C("Did Korea break free"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 820 L 1500 820 M 560 820 L 560 330", "color": "ink", "width": 4, "start": C("Did Korea break free"), "label": lbl("2019 → today", 1420, 860, 22, "ink")},
        {"d": "M 600 760 Q 900 700 1050 560 Q 1200 440 1450 400", "color": "accent3", "width": 7, "start": C("makes more of the ordinary"), "label": lbl("ORDINARY: MADE IN KOREA", 1250, 380, 22, "accent3")},
        {"d": "M 600 520 Q 800 600 950 560 Q 1150 470 1450 330", "color": "risk", "width": 7, "start": C("But for the most advanced"), "label": lbl("ADVANCED: JAPAN AGAIN", 1250, 310, 22, "risk")},
        {"d": "M 640 810 L 640 700 L 700 700 L 700 810 M 760 810 L 760 620 L 820 620 L 820 810", "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar",
         "start": C("it now makes more of the ordinary"), "label": lbl("home-made share", 730, 595, 18, "accent3")},
        {"d": "M 1300 880 L 1460 880 M 1430 860 L 1460 880 L 1430 900", "color": "accent", "width": 5, "start": C("moves the finish line"), "label": lbl("finish line moves", 1180, 885, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("the more Korea depends", 0.2), "dur": 1.4, "target": [1450, 330]}],
    "scale": 0.86, "floor": 1040}, sources=["dt_japan"])
kinetic("s16_t2", "m2_transition", [("A chemical can be restricted", 60, "A chemical can", None, False), ("A gas can simply disappear", 66, "A gas can", "risk", False)])

# ====================================================================== PART 3: the gas
card("s17_c3", "m3_card", "The Gas", "Neon, 2022")
stage("s18_q3", "m3_question", {
    "zones": [Z("fab", night=True, label="red")], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.3}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vessel", mode="tank", x=960, at=0.2, scale=0.9, label="NEON", glow=True, level=[[0, 1], [9, 0.6]])],
    "callouts": [co("A war in Ukraine, a threat to fabs in Taiwan?", 960, 150, C("Why would a war"), "gold", screen=True, size=38)]})
stage("s19_neon", "m3_neon", {
    "zones": [Z("fab", -1600, 1500, label="yellow"), Z("port", 1500, 6000, night=True)], "worldW": 3200, "night": True,
    "shake": [{"at": C("When Russia invaded"), "dur": 1.4, "amp": 10}],
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.0}, {"at": C("And in early"), "x": 2300, "y": 540, "zoom": 0.95, "dur": 2.6}], "drift": 3,
    "items": [it("tinsource", x=760, y=480, at=0.3, laserAt=C("inside the lasers"), rate=1.1, scale=0.55, text="LITHOGRAPHY LASER"),
              it("vessel", mode="tank", x=1250, at=C("ultra-pure neon"), scale=0.6, label="NEON", glow=True),
              it("megafab", x=2000, w=380, h=160, n=3, progress=1, at=C("Ingas in Mariupol"), text="INGAS · MARIUPOL", color=UA, scale=0.7),
              it("megafab", x=2600, w=380, h=160, n=3, progress=1, at=C("Cryoin in Odessa"), text="CRYOIN · ODESSA", color=UA, scale=0.7),
              it("letters", x=2300, y=200, text="45-54%", at=C("by Reuters' calculation"), size=90, color="gold"),
              it("letters", x=2300, y=360, text="SHUT DOWN", at=C("both shut down"), size=70, color="risk")],
    "callouts": [co("Neon: the gas inside lithography lasers", 960, 960, C("Chipmakers use"), "white", screen=True, size=40, until=C("And in early", -0.3)),
                 co("Two Ukrainian firms: {{neon.display}} of chip neon", 960, 960, C("by Reuters' calculation"), "gold", screen=True, size=38, sub="Reuters calculation (via The Register)", until=C("both shut down", -0.3)),
                 co("Feb 2022: both shut down", 960, 960, C("both shut down"), "risk", screen=True, size=42)]},
    sources=["reg_neon", "cnbc_neon"], sfx=[{"kind": "hit", "cue": "both shut down", "gain": 0.3}])
stage("s20_steel", "m3_steel", {
    "zones": [Z("carplant", -1600, 1600), Z("fab", 1600, 6000, label="yellow")], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("with companies in Ukraine"), "x": 1900, "y": 540, "zoom": 1.0, "dur": 2.4},
            {"at": C("The whole chip industry"), "x": 1500, "y": 540, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [it("sign", x=800, y=250, text="STEEL PLANTS", sub="neon is a by-product", at=0.3, color="#CFD8DC", size=36),
              it("letters", x=800, y=420, text="UP TO 90%", at=C("historically"), size=70, color="gold"),
              it("coins", **{"from": [800, 600], "to": [1900, 520]}, at=C("with companies in Ukraine", -0.5), rate=4),
              it("vessel", mode="tank", x=1900, at=C("ultra-pure gas"), scale=0.6, label="NEON 99.999"),
              it("counter", x=2400, y=220, at=C("The whole chip industry"), suffix=" t", steps=[[0, 0], [{"cue": "The whole chip industry", "offset": 2}, 540]], text="CHIP NEON USED, 2021")],
    "callouts": [co("Historically up to 90%: a by-product of Russian steel", 960, 960, C("historically"), "white", screen=True, size=36, sub="CNBC", until=C("The whole chip industry", -0.3)),
                 co("≈ 540 tonnes a year for all chipmaking (2021)", 960, 960, C("The whole chip industry"), "gold", screen=True, size=38, sub="Techcet via CNBC")]},
    sources=["cnbc_neon"])
stage("s21_stocks", "m3_stocks", {
    "zones": [Z("fab", label="yellow")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("But replacing"), "x": 1600, "y": 540, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [*[it("vessel", mode="tank", x=500 + k * 150, at=C("kept safety stocks", 0.2 * k), scale=0.45, label="STOCK", level=[[0, 1], [{"cue": "But replacing"}, 1], [{"cue": "But replacing", "offset": 8}, 0.3]]) for k in range(4)],
              it("crane", x=1700, text="NEW NEON LINE", at=C("Building new neon"), progress=[[0, 0.1], [25, 0.5]], scale=0.8),
              it("calendar", x=2200, y=320, at=C("could take"), pages=[[0, "9-24", "MONTHS"]], scale=0.8),
              it("letters", x=1300, y=180, text="A WAR IS ENOUGH", at=C("A war is enough"), size=64, color="risk")],
    "callouts": [co("Safety stocks since the 2014 scare", 960, 960, C("They had learned"), "white", screen=True, size=40, until=C("But replacing", -0.3)),
                 co("New neon lines: 9 months to 2 years", 960, 960, C("Building new neon"), "gold", screen=True, size=40, sub="Supplyframe via Reuters", until=C("Neon showed", -0.3)),
                 co("No government needed: a war is enough", 960, 960, C("Neon showed"), "risk", screen=True, size=40)]},
    sources=["reg_neon", "cnbc_neon"])
stage("s22_now", "m3_now", {
    "zones": [Z("port")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 540, "zoom": 0.85}, {"at": C("The lesson had been"), "x": 1300, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("chart", x=1300, y=420, w=620, h=320, at=C("By one"), dur=3, text="SHARE FROM RUSSIA + UKRAINE", pts=[0.9, 0.85, 0.7, 0.55, 0.4], color="green"),
              it("letters", x=1300, y=170, text="≈ 2/5", at=C("only about two-fifths"), size=100, color="gold"),
              it("ship", type="cargo", x=[[0, 300], [20, 2400]], at=0.4, scale=0.6)],
    "callouts": [co("By 2022, only ≈ two-fifths from Russia + Ukraine", 960, 960, C("By one"), "gold", screen=True, size=38, sub="Bain estimate (CNBC)", until=C("The lesson had been", -0.3)),
                 co("Learned once. Learned again.", 960, 960, C("The lesson had been"), "white", screen=True, size=42)]},
    sources=["cnbc_neon"])
kinetic("s23_t3", "m3_transition", [("And then came the metal", 64, "And then came", None, False), ("controlled by the country that wanted it controlled", 42, "controlled by the country", "risk", True)])

# ====================================================================== PART 4: the metal
card("s24_c4", "m4_card", "The Metal", "Gallium")
stage("s25_q4", "m4_question", {
    "zones": [Z("vault")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.3}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vessel", mode="ingot", x=960, at=0.3, scale=1.2, n=6, glow=True, label="GALLIUM")],
    "callouts": [co("One country, almost all of it?", 960, 150, C("What happens"), "gold", screen=True, size=42)]})
stage("s26_gallium", "m4_gallium", {
    "zones": [Z("datacenter", -1600, 1500), Z("vault", 1500, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("And according to"), "x": 2100, "y": 540, "zoom": 0.95, "dur": 2.6}], "drift": 3,
    "items": [it("vessel", mode="ingot", x=500, at=0.2, scale=0.7, n=4, label="GALLIUM"),
              it("device", type="server", x=900, y=F, at=C("telecom equipment")),
              it("device", type="tv", x=1150, y=F, at=C("LEDs")),
              it("letters", x=900, y=230, text="≈ 4 IN 5 → CHIPS", at=C("chips use"), size=54, color="gold"),
              it("vessel", mode="ingot", x=2100, at=C("And according to", 0.3), scale=1.1, n=6, label="99% CHINA", glow=True),
              it("letters", x=2100, y=230, text="99%", at=C("produced"), size=120, color="risk")],
    "callouts": [co("US: ≈ 79% of gallium goes into chips", 960, 960, C("chips use"), "white", screen=True, size=40, sub="USGS", until=C("And according to", -0.3)),
                 co("China: {{gallium.display}} of the world's raw gallium (2024)", 960, 960, C("And according to"), "risk", screen=True, size=38, sub="US Geological Survey")]},
    sources=["usgs_ga"])
stage("s27_controls", "m4_controls", {
    "zones": [Z("port", night=True)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("Prices jumped"), "x": 1600, "y": 520, "zoom": 0.9, "dur": 2.4},
            {"at": C("Then, in December"), "x": 2300, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "AUG", "2023"], [{"cue": "Then, in December"}, "DEC", "2024"]], scale=0.8),
              it("docs", x=800, y=540, at=C("requiring licences"), text="EXPORT LICENCE", scale=0.6, stamp="REQUIRED", stampAt=C("for every gallium")),
              it("chart", x=1600, y=420, w=560, h=300, at=C("Prices jumped"), dur=3, text="RAW GALLIUM IN CHINA ($/kg)", pts=[0.3, 0.4, 0.62, 0.75, 0.85], color="risk"),
              it("counter", x=1600, y=180, at=C("went from about"), prefix="$", steps=[[0, 240], [{"cue": "by October", "offset": -1}, 240], [{"cue": "by October", "offset": 1}, 420]], text="PER KG"),
              it("vessel", mode="ingot", x=2300, at=C("Then, in December", -0.3), scale=0.8, label="TO THE US", lockAt=C("banned gallium exports")),
              it("barrier", x=2700, text="USA", at=C("Then, in December"), closeAt=C("altogether"))],
    "callouts": [co("Aug 2023: licences for every export", 960, 960, C("requiring licences"), "white", screen=True, size=40, sub="USGS", until=C("Prices jumped", -0.3)),
                 co("$240 → $420 a kilogram (mid-2023 → Oct 2024)", 960, 960, C("Prices jumped"), "gold", screen=True, size=38, until=C("Then, in December", -0.3)),
                 co("Dec 2024: exports to the US banned", 960, 960, C("Then, in December"), "risk", screen=True, size=40)]},
    sources=["usgs_ga"], sfx=[{"kind": "hit", "cue": "banned gallium exports", "gain": 0.3}])
stage("s28_pause", "m4_pause", {
    "zones": [Z("port")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 540, "zoom": 1.0}, {"at": C("In other words"), "x": 1300, "y": 540, "zoom": 1.1, "dur": 2.4}], "drift": 3,
    "items": [it("barrier", x=1300, text="LICENCE", at=0.2, closeAt=0.3, openAt=C("suspended that ban")),
              it("vessel", mode="ingot", x=800, at=0.3, scale=0.7, label="GALLIUM"),
              it("calendar", x=1720, y=320, at=C("set to expire"), pages=[[0, "27 NOV", "2026"]], scale=0.8),
              it("clock", x=1720, y=600, at=C("set to expire"), period=2.0, text="PAUSE ENDS", scale=0.8),
              it("letters", x=1300, y=200, text="THE HAND IS STILL ON IT", at=C("In other words"), size=50, color="risk")],
    "callouts": [co("Nov 2025: the US ban is suspended", 960, 960, C("suspended that ban"), "gold", screen=True, size=40, sub="Evertiq / Reuters", until=C("But it only paused", -0.3)),
                 co("Licences still needed; pause ends 27 Nov 2026", 960, 960, C("But it only paused"), "white", screen=True, size=38, until=C("In other words", -0.3)),
                 co("The tap is open. The hand is still on it.", 960, 960, C("In other words"), "risk", screen=True, size=40)]},
    sources=["evertiq_ga"])
add("p29_kinds", "m4_draw", "engine_draw", {
    "title": "Three kinds of chokepoints", "board": BOARD, "draw_start": C("The first is skill"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 340, 280, 340), "color": "accent2", "width": 6, "start": C("The first is skill"), "label": lbl("SKILL", 700, 390, 30, "accent2")},
        {"d": "M 600 470 L 800 470", "color": "accent2", "width": 3, "start": C("Japan makes resist"), "label": lbl("Japan · resist", 700, 520, 22, "accent2")},
        {"d": rect(900, 340, 280, 340), "color": "accent", "width": 6, "start": C("The second is accident"), "label": lbl("ACCIDENT", 1040, 390, 30, "accent")},
        {"d": "M 940 470 L 1140 470", "color": "accent", "width": 3, "start": C("neon ended up"), "label": lbl("Ukraine · neon", 1040, 520, 22, "accent")},
        {"d": rect(1240, 340, 280, 340), "color": "risk", "width": 6, "start": C("The third is policy"), "label": lbl("POLICY", 1380, 390, 30, "risk")},
        {"d": "M 1280 470 L 1480 470", "color": "risk", "width": 3, "start": C("China produces"), "label": lbl("China · gallium", 1380, 520, 22, "risk")},
        {"d": "M 600 760 L 1480 760", "color": "ink", "width": 5, "start": C("Each one is fixed"), "label": lbl("different fixes · none quick", 1040, 810, 26, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("none of them quickly", 0.2), "dur": 1.4, "target": [1040, 760]}],
    "scale": 0.86, "floor": 1040}, sources=["dt_japan", "reg_neon", "usgs_ga"])
kinetic("s30_t4", "m4_transition", [("So what are governments", 60, "So what are", None, False), ("doing about it?", 72, "doing about it", "accent", False)])

# ====================================================================== PART 5: owning the bottle
card("s31_c5", "m5_card", "Owning the Bottle", "Chemicals as strategic assets")
stage("s32_q5", "m5_question", {
    "zones": [Z("office")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.3}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vessel", mode="bottle", x=960, at=0.3, scale=1.0, glow=True, label="NATIONAL?", sub="ASSET")],
    "callouts": [co("Can a country protect its chemicals?", 960, 150, C("Can a country"), "gold", screen=True, size=42)]})
stage("s33_jsr", "m5_jsr", {
    "zones": [Z("exchange", -1600, 1500), Z("office", 1500, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("JSR left the stock market"), "x": 1300, "y": 540, "zoom": 0.95, "dur": 2.2},
            {"at": C("JSR had already bought"), "x": 2200, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "2024", "BUY-OUT"]], scale=0.8),
              it("ticker", y=110, at=0.3, items=["JSR TENDER OFFER COMPLETE", "DELISTED 25 JUNE 2024"]),
              it("contract", x=900, y=430, at=C("bought JSR"), text="JIC BUYS JSR", sub="≈ $6.4bn", scale=0.65),
              it("letters", x=1400, y=250, text="NATIONAL ASSET", at=C("in effect"), size=60, color="gold"),
              it("vessel", mode="bottle", x=2200, at=C("Inpria"), scale=0.8, label="MOR", sub="next-gen EUV", glow=True),
              it("counter", x=2600, y=220, at=C("Inpria"), prefix="$", suffix="M", steps=[[0, 0], [{"cue": "Inpria", "offset": 1.5}, 514]], text="INPRIA (2021)")],
    "callouts": [co("2024: a state-backed fund buys JSR, ≈ {{jsr.display}}", 960, 960, C("bought JSR"), "gold", screen=True, size=38, sub="Tom's Hardware", until=C("JSR had already bought", -0.3)),
                 co("Inpria, 2021: the next resist generation", 960, 960, C("JSR had already bought"), "white", screen=True, size=38)]},
    sources=["thw_jsr"])
stage("s34_mor", "m5_mor", {
    "zones": [Z("fab", label="yellow")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.05}, {"at": C("JSR is now ramping"), "x": 1700, "y": 540, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("vessel", mode="bottle", x=700, at=0.2, scale=0.8, label="ORGANIC", sub="today"),
              it("vessel", mode="bottle", x=1050, at=C("it uses tin oxide"), scale=0.8, label="TIN OXIDE", sub="next", glow=True),
              it("letters", x=1050, y=230, text="≈ 5×", at=C("absorbs extreme"), until=C("JSR is now ramping", 1), size=110, color="gold"),
              it("megafab", x=1800, w=600, h=200, n=4, at=C("JSR is now ramping"), progress=[[0, 0.1], [{"cue": "JSR is now ramping", "offset": 4}, 1]], text="FIRST MOR PLANT · KOREA", glowAt=C("buying tomorrow's"))],
    "callouts": [co("Tin-oxide resist: ≈ 5× more EUV absorbed (Inpria)", 960, 960, C("absorbs extreme"), "gold", screen=True, size=36, sub="company claim (Tom's Hardware)", until=C("JSR is now ramping", -0.3)),
                 co("Defending today's recipe, buying tomorrow's", 960, 960, C("Japan is not only"), "white", screen=True, size=38)]},
    sources=["thw_jsr"])
stage("s35_taiwan", "m5_taiwan", {
    "zones": [Z("site", -1600, 1500), Z("fab", 1500, 6000, label="yellow")], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("Its rivals"), "x": 1800, "y": 540, "zoom": 0.9, "dur": 2.4},
            {"at": C("The reason is speed"), "x": 1400, "y": 540, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [it("crane", x=800, text="JSR · YUNLIN, TAIWAN", at=C("JSR is building"), progress=[[0, 0.2], [20, 0.6]], scale=0.85),
              it("calendar", x=330, y=300, at=C("as early as"), pages=[[0, "2028", "OPENS?"]], scale=0.75),
              it("megafab", x=1900, w=360, h=150, n=3, progress=1, at=C("Tokyo Ohka Kogyo"), text="TOK", color=JP, scale=0.7),
              it("megafab", x=2400, w=360, h=150, n=3, progress=1, at=C("Shin-Etsu"), text="SHIN-ETSU", color="#6A1B9A", scale=0.7),
              it("plane", x=[[0, 2600], [{"cue": "shipping samples", "offset": 4}, 600]], y=[[0, 200], [{"cue": "shipping samples", "offset": 4}, 300]], at=C("shipping samples"), text="SAMPLES · WEEKS", scale=0.55, flip=True)],
    "callouts": [co("At TSMC's request: JSR's first Taiwan plant (2028?)", 960, 960, C("At the request"), "gold", screen=True, size=36, sub="Tom's Hardware", until=C("Its rivals", -0.3)),
                 co("TOK and Shin-Etsu already make resist in Taiwan", 960, 960, C("Its rivals"), "white", screen=True, size=38, until=C("The reason is speed", -0.3)),
                 co("Speed: weeks of shipping per test cycle", 960, 960, C("The reason is speed"), "gold", screen=True, size=40)]},
    sources=["thw_jsr"])
stage("s36_lesson", "m5_lesson", {
    "zones": [Z("port")], "worldW": 3200,
    "cam": [{"at": 0, "x": 1600, "y": 540, "zoom": 0.8}, {"at": C("Every country is building"), "x": 1600, "y": 540, "zoom": 0.75, "dur": 2.6}], "drift": 3,
    "items": [it("vessel", mode="bottle", x=700, at=C("Taiwan gets"), scale=0.6, label="TAIWAN", sub="plants"),
              it("vessel", mode="bottle", x=1100, at=C("Japan keeps"), scale=0.6, label="JAPAN", sub="recipes", glow=True),
              it("vessel", mode="bottle", x=1500, at=C("Korea makes more"), scale=0.6, label="KOREA", sub="ordinary"),
              it("vessel", mode="ingot", x=2000, at=C("America looks"), scale=0.6, n=2, label="USA"),
              it("vessel", mode="ingot", x=2500, at=C("China still"), scale=0.7, n=6, label="CHINA"),
              it("letters", x=1600, y=180, text="NOBODY OWNS ALL OF IT", at=C("Nobody owns"), size=56, color="gold")],
    "callouts": [co("Taiwan: plants · Japan: recipes", 960, 960, C("Taiwan gets"), "white", screen=True, size=40, until=C("Korea makes more", -0.3)),
                 co("Korea: ordinary materials · China: the gallium", 960, 960, C("Korea makes more"), "white", screen=True, size=38, until=C("Every country is building", -0.3)),
                 co("Everyone builds a little. Nobody owns all of it.", 960, 960, C("Every country is building"), "gold", screen=True, size=38)]},
    sources=["thw_jsr", "dt_japan", "usgs_ga"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("fab", label="yellow")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 540, "zoom": 0.8}, {"at": C("The most powerful thing"), "x": 800, "y": 600, "zoom": 1.3, "dur": 3.2}], "drift": 2,
    "items": [it("litho", x=1700, at=0.2, fireAt=0.4, text="THE MACHINE", scale=0.75),
              it("vessel", mode="bottle", x=800, at=C("a liquid most people"), scale=0.9, label="RESIST", glow=True),
              it("vessel", mode="tank", x=1100, at=C("collect a gas"), scale=0.55, label="NEON"),
              it("vessel", mode="ingot", x=2300, at=C("a silver metal"), scale=0.6, n=4, label="GALLIUM")],
    "callouts": [co("Machine makers… and the makers of a liquid, a gas, a metal", 960, 150, C("The machine makers"), "white", screen=True, size=34, until=C("The most powerful thing", -0.3)),
                 co("Sometimes the power is the bottle on the shelf", 960, 150, C("The most powerful thing"), "gold", screen=True, size=40)]},
    sources=["dt_japan", "cnbc_neon", "usgs_ga"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_chip_chemicals_storyboard.py; edit the generator, not this file.\n"
           "# Episode 18 storyboard (chip series C5): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
