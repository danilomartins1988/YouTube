"""Generates projects/the-stamp-that-could-break-asmls-monopoly/deliverables/documentary/storyboard.yaml (Episode 15, C2).

Bespoke worlds for the challengers to ASML (tones from visual_direction.yaml: tech -> strategy -> thriller -> tech -> reflective):
ASML's EUV machine in a clean room (with the tin light source and a double-decker comparison), the new `imprint` item
(Canon's nanoimprint machine: inkjet resist, quartz mold pressing down, UV flash, step and repeat, a dust defect), a
Japanese R&D office, a secret night lab in Shenzhen with a giant prototype that glows but prints nothing, the new
`beamsrc` item (an X-ray accelerator in San Francisco, a helium-atom source on a Norwegian fjord), and a final clean room
where the challengers line up. Presenter: the moat, the speed problem, why China does not care about speed.
No logos (company names in text only), no smiling sun, no generic city, no real people drawn.
Run: python tools/gen_nanoimprint_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-stamp-that-could-break-asmls-monopoly/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
ASML, CANON, CHINA, SUB, LACE = "#1E7FD8", "#C62828", "#FF4B3E", "#26A69A", "#FFB300"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": k + 1, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("fab", label="yellow")], "worldW": 2400,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.2}, {"at": C("rubber stamp"), "x": 1350, "y": 520, "zoom": 0.95, "dur": 2.6}], "drift": 0,
    "items": [it("litho", x=640, at=0.2, fireAt=0.6, text="THE MOST EXPENSIVE MACHINE", scale=0.8),
              it("imprint", x=1750, at=C("something that works"), rate=0.6, text="…OR A STAMP?", scale=0.55),
              it("letters", x=1200, y=200, text="VS", at=C("rubber stamp"), size=110, color="gold")],
    "callouts": [co("The most expensive machine in chipmaking…", 960, 150, C("most expensive"), "white", screen=True, size=40, until=C("rubber stamp", -0.3)),
                 co("…replaced by a stamp?", 960, 150, C("rubber stamp"), "gold", screen=True, size=46)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("fab", -1600, 1500, label="yellow"), Z("office", 1500, 3200, night=True), Z("sciencepark", 3200, 7000)], "worldW": 4400,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("camera company"), "x": 2300, "y": 520, "zoom": 0.95, "dur": 2.2},
            {"at": C("two startups"), "x": 3500, "y": 520, "zoom": 0.95, "dur": 2.2}], "drift": 0,
    "items": [it("litho", x=760, at=0.2, fireAt=0.4, text="ASML · EUV", scale=0.75, color=ASML),
              it("counter", x=760, y=180, at=C("Its newest machine"), prefix="$", suffix="M", steps=[[0, 0], [{"cue": "Its newest machine", "offset": 2.2}, 400]], text="NEWEST MACHINE"),
              it("imprint", x=2000, at=C("camera company"), rate=0.6, text="CANON", scale=0.45),
              it("sign", x=2700, y=330, text="SECRET LAB", sub="Shenzhen", at=C("a secret lab"), color="#FFCDD2", size=34),
              it("beamsrc", x=3400, y=520, at=C("two startups"), mode="xray", scale=0.55, text="STARTUP 1", color=SUB),
              it("beamsrc", x=3850, y=520, at=C("two startups", 0.4), mode="atoms", scale=0.55, text="STARTUP 2", color=LACE)],
    "callouts": [co("One company prints every top chip: ASML", 960, 960, C("Every one of"), "white", screen=True, until=C("Its newest machine", -0.3)),
                 co("Newest machine: {{high_na.display}}. Nobody else can build one.", 960, 960, C("Its newest machine"), "gold", screen=True, size=40, sub="MIT Technology Review", until=C("camera company", -0.3)),
                 co("Four challengers, four different ways", 960, 960, C("camera company"), "risk", screen=True, size=40)]},
    sources=["mit_asml", "reuters_cn_euv"], sfx=[{"kind": "hit", "cue": "Nobody else", "gain": 0.3}])

# ====================================================================== PART 1: the machine nobody else can build
card("s03_c1", "m1_card", "The Machine Nobody Else Can Build", "How one company got there")
stage("s04_q1", "m1_question", {
    "zones": [Z("dutch")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 4,
    "items": [it("litho", x=1300, at=0.3, fireAt=1.0, text="ASML", scale=0.6, color=ASML),
              it("tower", x=560, text="#1", color=ASML, h=420, at=0.6, scale=0.8)],
    "callouts": [co("How did one company end up alone at the top?", 960, 150, C("How did one"), "gold", screen=True, size=40)]})
stage("s05_print", "m1_print", {
    "zones": [Z("fab", label="yellow")], "worldW": 3400,
    "cam": [{"at": 0, "x": 760, "y": 500, "zoom": 1.05}, {"at": C("The smaller the light"), "x": 1700, "y": 500, "zoom": 1.0, "dur": 2.4},
            {"at": C("ASML makes that light"), "x": 2650, "y": 500, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("wafer", x=700, y=420, r=200, at=C("a disc of silicon"), spin=6, revealAt=C("print billions"), fail=0.0),
              it("mirrors", x=1700, y=480, at=C("The smaller the light", -0.6), beamAt=C("The smaller the light"), dur=3.2, scale=0.7),
              it("letters", x=1700, y=150, text="EUV", at=C("extreme ultraviolet"), size=110, color="purple"),
              it("tinsource", x=2650, y=480, at=C("ASML makes that light", -0.4), laserAt=C("firing lasers"), plasmaAt=C("molten tin"), rate=1.0, scale=0.7, text="TIN DROPS + LASER (slowed down)")],
    "callouts": [co("Light prints the circuits, layer by layer", 960, 960, C("shine light"), "white", screen=True, until=C("The smaller the light", -0.3)),
                 co("Smaller wavelength → smaller circuits", 960, 960, C("The smaller the light"), "gold", screen=True, until=C("ASML makes that light", -0.3)),
                 co("Lasers hit molten tin, tens of thousands of times a second", 960, 960, C("ASML makes that light"), "white", screen=True, size=36, sub="MIT Technology Review")]},
    sources=["mit_asml"])
stage("s06_bet", "m1_bet", {
    "zones": [Z("dutch", -1600, 1500), Z("office", 1500, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("Two Japanese giants"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.2},
            {"at": C("ASML kept going"), "x": 900, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "2001", "THE BET"], [{"cue": "before the first machines"}, "2017", "ON SALE"]], scale=0.8),
              it("tower", x=900, text="ASML", color=ASML, h=[[0, 300], [{"cue": "ASML kept going"}, 300], [{"cue": "ASML kept going", "offset": 4}, 560]], at=0.4, scale=0.9),
              it("tower", x=2000, text="NIKON", color="#78909C", h=[[0, 420], [{"cue": "Both dropped out"}, 420], [{"cue": "Both dropped out", "offset": 1.4}, 60]], at=C("Two Japanese giants"), scale=0.85),
              it("tower", x=2400, text="CANON", color=CANON, h=[[0, 420], [{"cue": "Both dropped out", "offset": 0.3}, 420], [{"cue": "Both dropped out", "offset": 1.7}, 60]], at=C("Two Japanese giants", 0.3), scale=0.85),
              it("counter", x=1300, y=230, at=C("It took"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "in research", "offset": -1}, 10]], text="R&D"),
              it("letters", x=1300, y=420, text="16 YEARS", at=C("It took", 0.5), size=60, color="gold")],
    "callouts": [co("Nikon and Canon dropped out", 960, 960, C("Both dropped out"), "risk", screen=True, until=C("ASML kept going", 1.2)),
                 co("{{euv_history.years_display}} and {{euv_history.display}} of research", 960, 960, C("It took"), "gold", screen=True, size=40, sub="MIT Technology Review", until=C("before the first machines", -0.2)),
                 co("2017: first EUV machines, {{euv_history.first_display}} each", 960, 960, C("before the first machines"), "white", screen=True)]},
    sources=["mit_asml"], sfx=[{"kind": "hit", "cue": "Both dropped out", "gain": 0.25}])
stage("s07_money", "m1_money", {
    "zones": [Z("datacenter", -1600, 1400), Z("fab", 1400, 3000, label="yellow"), Z("port", 3000, 7000)], "worldW": 4200,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.0}, {"at": C("A standard EUV machine"), "x": 2200, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("because of export rules"), "x": 3400, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("hbm", x=700, y=520, at=0.3, scale=0.6, dur=3, text="AI CHIP"),
              it("counter", x=700, y=180, at=C("In twenty twenty-five"), suffix=" EUV", steps=[[0, 0], [{"cue": "In twenty twenty-five", "offset": 2}, 50]], text="SOLD IN 2025 (NEARLY)"),
              it("coins", **{"from": [700, 300], "to": [1900, 300]}, at=C("brought in"), rate=5, until=C("A standard EUV machine", 2)),
              it("litho", x=1900, at=C("A standard EUV machine", -0.4), fireAt=C("A standard EUV machine"), text="EUV", sub="≈ $250M", scale=0.6),
              it("litho", x=2550, at=C("high-NA version", -0.3), fireAt=C("high-NA version"), text="HIGH-NA EUV", sub="$400M", scale=0.68, color="#7E57C2"),
              it("barrier", x=3400, text="NO EUV TO CHINA", at=C("because of export rules", -0.3), closeAt=C("no EUV machine")),
              it("ship", type="cargo", x=[[0, 3000], [{"cue": "no EUV machine"}, 3200]], at=C("because of export rules"), scale=0.6)],
    "callouts": [co("2025: {{euv_history.sold_display}} EUV machines, {{euv_history.rev_display}} revenue", 960, 960, C("In twenty twenty-five"), "gold", screen=True, size=38, sub="MIT Technology Review", until=C("A standard EUV machine", -0.3)),
                 co("EUV {{euv_price.display}} · High-NA {{high_na.display}}", 960, 960, C("A standard EUV machine"), "white", screen=True, size=40, sub="Reuters · MIT Technology Review", until=C("because of export rules", -0.3)),
                 co("No EUV machine ever sold to a customer in China", 960, 960, C("no EUV machine"), "risk", screen=True, size=38, sub="ASML to Reuters")]},
    sources=["mit_asml", "reuters_cn_euv"])
add("p08_moat", "m1_draw", "engine_draw", {
    "title": "Why the monopoly is so hard to attack", "board": BOARD, "draw_start": C("On one side"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 330, 300, 120), "color": "accent", "width": 5, "start": C("On one side"), "label": lbl("DECADES OF R&D", 690, 395, 24, "accent")},
        {"d": rect(540, 480, 300, 120), "color": "accent", "width": 5, "start": C("billions of dollars"), "label": lbl("$ BILLIONS", 690, 545, 28, "accent")},
        {"d": rect(940, 380, 260, 180), "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.18, "kind": "box", "start": C("In the middle"), "label": lbl("ONE MACHINE", 1070, 475, 26, "accent2")},
        {"d": arrow((850, 465), (930, 465)), "color": "ink", "width": 4, "start": C("only one company")},
        {"d": rect(1300, 320, 200, 70) + " " + rect(1300, 420, 200, 70) + " " + rect(1300, 520, 200, 70), "color": "accent3", "width": 4, "start": C("every chipmaker"), "label": lbl("CHIPMAKERS", 1400, 640, 24, "accent3")},
        {"d": arrow((1210, 465), (1290, 465)), "color": "ink", "width": 4, "start": C("every chipmaker", 0.3)},
        {"d": "M 560 700 Q 900 640 1240 700", "color": "risk", "width": 7, "start": C("cross that whole gap"), "label": lbl("CROSS IT ALL AT ONCE…", 900, 760, 26, "risk")},
        {"d": "M 560 820 Q 900 940 1240 820", "color": "accent3", "width": 6, "start": C("find a way around"), "label": lbl("…OR GO AROUND IT", 900, 840, 26, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("find a way around", 0.3), "dur": 1.4, "target": [900, 880]}],
    "scale": 0.86, "floor": 1040}, sources=["mit_asml"])
kinetic("s09_t1", "m1_transition", [("One of the companies that dropped out", 48, "One of the companies", None, True), ("decided to go around it", 72, "go around it", "accent", False)])

# ====================================================================== PART 2: the stamp
card("s10_c2", "m2_card", "The Stamp", "Printing a chip without a light source")
stage("s11_q2", "m2_question", {
    "zones": [Z("office")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.3}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("imprint", x=960, at=0.3, rate=0.45, text="CANON · NANOIMPRINT", scale=0.75, color=CANON)],
    "callouts": [co("Print a chip without light?", 960, 150, C("Can you print"), "gold", screen=True, size=44)]})
stage("s12_how", "m2_how", {
    "zones": [Z("fab", label="red")], "worldW": 1920, "min_seconds": 20,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.2}, {"at": C("Then it presses"), "x": 960, "y": 620, "zoom": 1.3, "dur": 2.6},
            {"at": C("Canon says it can print"), "x": 960, "y": 580, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("imprint", x=960, at=0.2, rate=0.32, text="NANOIMPRINT (slowed down)", scale=1.0, color=CANON),
              it("letters", x=1650, y=200, text="14 nm", at=C("Canon says it can print"), size=80, color="gold")],
    "callouts": [co("1 · The circuit is carved into a quartz mold", 960, 150, C("carves the circuit"), "white", screen=True, size=36, until=C("Then it presses", -0.3)),
                 co("2 · Pressed onto liquid resin, like a stamp", 960, 150, C("Then it presses"), "gold", screen=True, size=36, until=C("A flash", -0.3)),
                 co("3 · A mercury lamp's UV hardens it (1970s light)", 960, 150, C("A flash"), "white", screen=True, size=36, until=C("The mold lifts", -0.2)),
                 co("4 · Lift: the pattern stays. Lines {{nil_how.display}} wide", 960, 150, C("The mold lifts"), "gold", screen=True, size=36, sub="Canon: like the 5 nm process (IEEE Spectrum, The Register)")]},
    sources=["ieee_nil", "register_nil"])
stage("s13_road", "m2_road", {
    "zones": [Z("office", -1600, 1500), Z("sciencepark", 1500, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("It took"), "x": 1300, "y": 520, "zoom": 0.95, "dur": 2.2},
            {"at": C("Canon shipped"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "2004", "START"], [{"cue": "in twenty fourteen"}, "2014", "BUYS MII"], [{"cue": "Canon shipped"}, "2024", "FIRST SALE"]], scale=0.8),
              it("sign", x=900, y=330, text="MOLECULAR IMPRINTS", sub="Austin, Texas · bought 2014", at=C("Molecular Imprints"), color="#FFE0B2", size=34),
              it("letters", x=1300, y=170, text="20 YEARS", at=C("It took"), size=80, color="gold"),
              it("imprint", x=2200, at=C("Canon shipped", -0.3), rate=0.5, text="FIRST COMMERCIAL NIL", sub="Texas Institute for Electronics", scale=0.55, color=CANON),
              it("ramstick", x=2850, y=560, at=C("Kioxia"), scale=0.5, label="PROTOTYPE")],
    "callouts": [co("{{nil_how.years_display}} from start to market", 960, 960, C("It took"), "gold", screen=True, until=C("Canon shipped", -0.3)),
                 co("{{nil_ship.display}}: first machine, to a research consortium", 960, 960, C("Canon shipped"), "white", screen=True, size=38, until=C("Kioxia", -0.3)),
                 co("Kioxia tests it for prototype memory chips", 960, 960, C("Kioxia"), "white", screen=True, sub="IEEE Spectrum")]},
    sources=["ieee_nil", "register_nil"])
stage("s14_pitch", "m2_pitch", {
    "zones": [Z("fab", label="red")], "worldW": 3400,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("With no"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.2},
            {"at": C("And it is smaller"), "x": 2300, "y": 540, "zoom": 0.8, "dur": 2.6}], "drift": 3,
    "items": [it("pricetag", x=760, y=300, at=0.3, pages=[[0, "EUV $$$"], [{"cue": "one digit less"}, "÷ 10?"]], sub="Canon: 'one digit less' (not final)"),
              it("counter", x=1500, y=260, at=C("With no"), suffix="%", steps=[[0, 100], [{"cue": "uses about", "offset": 0.5}, 10]], text="ENERGY (CANON ESTIMATE)"),
              it("bus", x=1900, at=C("double-decker bus"), text="≈ 200 m³ · EUV", scale=0.9),
              it("imprint", x=2650, at=C("Four of Canon's", -0.2), rate=0.6, text="NIL", scale=0.3, color=CANON),
              it("imprint", x=2850, at=C("Four of Canon's"), rate=0.6, text="NIL", scale=0.3, color=CANON),
              it("imprint", x=3050, at=C("Four of Canon's", 0.2), rate=0.6, text="NIL", scale=0.3, color=CANON),
              it("imprint", x=3250, at=C("Four of Canon's", 0.4), rate=0.6, text="NIL", scale=0.3, color=CANON)],
    "callouts": [co("Price: 'one digit less' than EUV", 960, 960, C("Fujio Mitarai"), "gold", screen=True, size=40, sub="Canon's CEO to Bloomberg, 2023 · no final price", until=C("With no", -0.3)),
                 co("Energy: about {{nil_energy.display}} (Canon's estimate)", 960, 960, C("With no"), "white", screen=True, size=40, sub="IEEE Spectrum", until=C("And it is smaller", -0.3)),
                 co("4 Canon machines < half an EUV's space", 960, 960, C("Four of Canon's"), "gold", screen=True, size=40)]},
    sources=["jt_mitarai", "tf_nil", "ieee_nil"])
kinetic("s15_t2", "m2_transition", [("Cheaper, smaller and greener", 60, "Cheaper", None, False), ("So why is every chipmaker not buying one?", 46, "So why", "accent", True)])

# ====================================================================== PART 3: the catch
card("s16_c3", "m3_card", "The Catch", "Why a stamp is hard")
stage("s17_q3", "m3_question", {
    "zones": [Z("fab", label="red")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.4}, {"at": 3.0, "x": 960, "y": 520, "zoom": 1.05, "dur": 3.0}], "drift": 2,
    "items": [it("imprint", x=960, at=0.2, rate=0.5, text="NANOIMPRINT", scale=0.8, color=CANON),
              it("magnifier", x=[[0, 600], [7, 1300]], y=[[0, 500], [7, 620]], at=0.8, scale=0.9)],
    "callouts": [co("What's the problem with a stamp?", 960, 150, C("What is the problem"), "gold", screen=True, size=44)]})
stage("s18_touch", "m3_touch", {
    "zones": [Z("fab", label="red")], "worldW": 1920, "min_seconds": 20,
    "shake": [{"at": C("ruin the chips"), "dur": 1.0, "amp": 8}],
    "cam": [{"at": 0, "x": 960, "y": 600, "zoom": 1.05}, {"at": C("a single speck"), "x": 960, "y": 680, "zoom": 1.5, "dur": 2.2},
            {"at": C("Canon had to invent"), "x": 960, "y": 600, "zoom": 1.05, "dur": 2.4}], "drift": 0,
    "items": [it("imprint", x=960, at=0.2, rate=0.5, text="NANOIMPRINT", scale=1.0, color=CANON, defectAt=C("a single speck"), defectCell=6),
              it("letters", x=1560, y=200, text="DEFECT", at=C("ruin the chips"), size=80, color="risk")],
    "callouts": [co("Light never touches the wafer. A stamp does.", 960, 150, C("Light never touches"), "white", screen=True, size=38, until=C("a single speck", -0.3)),
                 co("One speck of dust → ruined chips", 960, 150, C("a single speck"), "risk", screen=True, size=40, until=C("Canon had to invent", -0.3)),
                 co("Air bubbles · inkjet resin · layer alignment", 960, 150, C("Canon had to invent"), "white", screen=True, size=38, until=C("Gartner", -0.3)),
                 co("Gartner: 'a big gap' from lab to high volume", 960, 150, C("Gartner"), "gold", screen=True, size=38, sub="The Register")]},
    sources=["thw_nil_price", "ieee_nil", "register_nil"], sfx=[{"kind": "hit", "cue": "ruin the chips", "gain": 0.3}])
add("p19_speed", "m3_draw", "engine_draw", {
    "title": "The speed problem", "board": BOARD, "draw_start": C("An EUV machine prints"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 760 L 1400 760", "color": "ink", "width": 4, "start": C("An EUV machine prints")},
        {"d": "M 620 760 L 620 360 L 760 360 L 760 760", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar",
         "start": C("An EUV machine prints", 0.3), "label": lbl("EUV ≈ 200 / h", 690, 340, 24, "accent2")},
        {"d": "M 860 760 L 860 600 L 1000 600 L 1000 760", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar",
         "start": C("Canon's comparison"), "label": lbl("NIL 80 / h", 930, 580, 24, "accent")},
        {"d": "M 860 560 L 1000 560", "color": "accent", "width": 3, "start": C("with a target of"), "label": lbl("target 100", 930, 540, 20, "accent")},
        {"d": rect(1120, 380, 120, 80), "color": "accent3", "width": 5, "start": C("every mold wears out"), "label": lbl("MOLD COPY", 1180, 430, 20, "accent3")},
        {"d": arrow((1250, 420), (1380, 420)), "color": "ink", "width": 4, "start": C("One copy of the mold")},
        {"d": rect(1390, 380, 140, 80), "color": "accent3", "width": 4, "start": C("One copy of the mold", 0.4), "label": lbl("≈ 2,000 WAFERS", 1460, 500, 22, "accent3")},
        {"d": "M 1130 600 L 1520 690 M 1520 600 L 1130 690", "color": "risk", "width": 6, "start": C("has to be replaced"), "label": lbl("then replace it", 1325, 740, 24, "risk")},
        {"d": "M 600 860 L 1520 860", "color": "risk", "width": 5, "start": C("every slow step"), "label": lbl("slow steps + worn molds = cost", 1060, 910, 26, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Canon's comparison", 0.4), "dur": 1.4, "target": [930, 620]}],
    "scale": 0.86, "floor": 1040}, sources=["ieee_nil", "mit_asml"])
stage("s20_niche", "m3_niche", {
    "zones": [Z("office", -1600, 1500), Z("fab", 1500, 6000, label="yellow")], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("Compare that"), "x": 1600, "y": 520, "zoom": 0.85, "dur": 2.4},
            {"at": C("like memory"), "x": 2400, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("sign", x=760, y=330, text="'NOT TO OVERTAKE EUV'", sub="Canon's CEO, 2023", at=C("Mitarai said"), color="#FFCDD2", size=32),
              it("tower", x=1300, text="CANON GOAL 10-20/yr", color=CANON, h=[[0, 40], [{"cue": "Its target", "offset": 1.5}, 110]], at=C("Its target"), scale=0.8),
              it("tower", x=1750, text="ASML EUV 2025 ≈ 50", color=ASML, h=[[0, 40], [{"cue": "Compare that", "offset": 1.5}, 460]], at=C("Compare that"), scale=0.8),
              it("ramstick", x=2400, y=540, at=C("like memory"), scale=0.7, label="MEMORY"),
              it("imprint", x=2900, at=C("like memory", 0.3), rate=0.9, text="REPEATING PATTERNS", scale=0.4, color=CANON)],
    "callouts": [co("Canon's goal: {{nil_sales.display}} within five years", 960, 960, C("Its target"), "gold", screen=True, size=40, sub="a target, not sales (The Register)", until=C("Compare that", -0.3)),
                 co("Not the throne: chips that don't need it", 960, 960, C("not trying to take"), "white", screen=True, size=40)]},
    sources=["thw_nil_price", "register_nil", "mit_asml"])
kinetic("s21_t3", "m3_transition", [("One country cannot wait", 60, "But one country", None, False), ("It is building EUV itself, in secret", 48, "in secret", "risk", True)])

# ====================================================================== PART 4: the secret lab
card("s22_c4", "m4_card", "The Secret Lab", "Copying the hardest machine")
stage("s23_q4", "m4_question", {
    "zones": [Z("fab", night=True, label="red")], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.3}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("litho", x=960, at=0.3, fireAt=1.2, text="COPY?", scale=0.75, color=CHINA),
              it("magnifier", x=[[0, 500], [7, 1400]], y=[[0, 380], [7, 520]], at=0.6, scale=0.9)],
    "callouts": [co("Can a country copy the hardest machine?", 960, 150, C("Can a country"), "gold", screen=True, size=42)]})
stage("s24_lab", "m4_lab", {
    "zones": [Z("fab", -1600, 6000, night=True, label="red")], "worldW": 3400, "night": True,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.05}, {"at": C("former ASML engineers"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.2},
            {"at": C("It fills nearly"), "x": 2200, "y": 520, "zoom": 0.7, "dur": 3.0}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "DEC", "2025"]], scale=0.8),
              it("sign", x=820, y=330, text="REUTERS", sub="a prototype in a Shenzhen lab", at=C("Reuters reported"), color="#FFCDD2", size=40),
              *crowd([1300, 1420, 1540], "read", at=C("former ASML engineers"), tie=False),
              it("sign", x=1750, y=300, text="USED ASML PARTS", sub="bought on secondary markets", at=C("secondary"), color="#FFE0B2", size=30),
              it("litho", x=2100, at=C("It fills nearly", -0.3), fireAt=C("makes EUV light"), text="PROTOTYPE", scale=0.95, color=CHINA),
              it("litho", x=2750, at=C("It fills nearly", 0.2), fireAt=C("makes EUV light"), text="PROTOTYPE", scale=0.95, color=CHINA),
              it("letters", x=2400, y=170, text="0 CHIPS", at=C("not made a single chip"), size=90, color="risk")],
    "callouts": [co("According to two people with knowledge of the project", 960, 960, C("According to two"), "white", screen=True, size=36, sub="Reuters", until=C("It fills nearly", -0.3)),
                 co("It makes EUV light…", 960, 960, C("makes EUV light"), "gold", screen=True, size=42, until=C("not made a single chip", -0.3)),
                 co("…but no chips yet", 960, 960, C("not made a single chip"), "risk", screen=True, size=44)]},
    sources=["reuters_cn_euv", "engadget_cn_euv"], sfx=[{"kind": "hit", "cue": "not made a single chip", "gain": 0.3}])
stage("s25_gap", "m4_gap", {
    "zones": [Z("fab", -1600, 1500, night=True, label="red"), Z("dutch", 1500, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("ASML's production machines"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.2},
            {"at": C("The government's goal"), "x": 1400, "y": 520, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=700, y=420, at=C("one Chinese team"), suffix=" W", steps=[[0, 0], [{"cue": "one Chinese team", "offset": 2}, 100]], text="ONE CHINESE LIGHT SOURCE"),
              it("tinsource", x=2300, y=480, at=C("ASML's production machines", -0.3), laserAt=C("ASML's production machines"), rate=1.2, scale=0.6, text="≈ 600 W"),
              it("calendar", x=1400, y=260, at=C("The government's goal"), pages=[[0, "2028", "GOAL"], [{"cue": "more realistic"}, "2030", "MORE LIKELY?"]], scale=0.85),
              it("calendar", x=2300, y=260, at=C("Remember"), pages=[[0, "2001", "ASML PROTOTYPE"], [{"cue": "nearly two decades"}, "2019", "FIRST CHIPS"]], scale=0.75)],
    "callouts": [co("Light: {{cn_light.display}} vs ASML {{cn_light.asml_display}}", 960, 960, C("one Chinese team"), "risk", screen=True, size=40, sub="Tom's Hardware", until=C("The government's goal", -0.3)),
                 co("Goal: chips by 2028 · insiders: 2030 more realistic", 960, 960, C("The government's goal"), "gold", screen=True, size=36, sub="Reuters · goals, not facts", until=C("Remember", -0.3)),
                 co("ASML: prototype 2001 → chips nearly two decades later", 960, 960, C("Remember"), "white", screen=True, size=36)]},
    sources=["thw_cn_tools", "reuters_cn_euv", "engadget_cn_euv"])
stage("s26_duv", "m4_duv", {
    "zones": [Z("fab", -1600, 1600, label="red"), Z("fab", 1600, 6000, label="yellow")], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 0.95}, {"at": C("ASML deploys"), "x": 2200, "y": 520, "zoom": 0.9, "dur": 2.2},
            {"at": C("So for now"), "x": 900, "y": 500, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [*[it("litho", x=420 + k * 200, at=C("are expected to deliver", k * 0.25), fireAt=C("are expected to deliver", k * 0.25 + 0.4), text="DUV", scale=0.28, color=CHINA) for k in range(5)],
              it("counter", x=2300, y=200, at=C("ASML deploys"), steps=[[0, 0], [{"cue": "ASML deploys", "offset": 2}, 130]], text="ASML IMMERSION / YEAR"),
              *[it("litho", x=1800 + (k % 6) * 170, at=C("ASML deploys", 0.1 * k), fireAt=C("ASML deploys", 0.1 * k + 0.3), text="", scale=0.2, color=ASML) for k in range(12)],
              it("plane", x=[[0, 3200], [{"cue": "come from Japan", "offset": 3}, 600]], y=200, at=C("come from Japan"), text="PARTS FROM JAPAN"),
              it("wafer", x=900, y=380, r=150, at=C("So for now"), spin=4, revealAt=C("printing the same layer"), fail=0.05)],
    "callouts": [co("China: about 5 DUV machines this year", 960, 960, C("are expected to deliver"), "risk", screen=True, size=40, sub="Tom's Hardware", until=C("ASML deploys", -0.3)),
                 co("ASML: about 130 a year", 960, 960, C("ASML deploys"), "white", screen=True, size=40, until=C("So for now", -0.3)),
                 co("Print the same layer several times", 960, 960, C("printing the same layer"), "gold", screen=True, size=40, sub="multi-patterning")]},
    sources=["thw_cn_tools", "mit_asml"])
add("p27_china", "m4_draw", "engine_draw", {
    "title": "Why China may not care about speed", "board": BOARD, "draw_start": C("A Western chipmaker"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 340, 360, 140), "color": "accent2", "width": 5, "start": C("A Western chipmaker"), "label": lbl("WESTERN FAB", 740, 400, 26, "accent2")},
        {"d": "M 600 450 L 880 450", "color": "accent2", "width": 3, "start": C("earns money"), "label": lbl("must earn money", 740, 455, 20, "accent2")},
        {"d": "M 960 410 L 1100 410 M 1070 390 L 1100 410 L 1070 430", "color": "ink", "width": 4, "start": C("hundreds of wafers")},
        {"d": dot(1180, 410), "color": "accent2", "width": 1, "start": C("hundreds of wafers", 0.2), "label": lbl("200 / h", 1250, 420, 28, "accent2", "start")},
        {"d": rect(560, 560, 360, 140), "color": "risk", "width": 5, "start": C("A country cut off"), "label": lbl("CUT-OFF COUNTRY", 740, 620, 26, "risk")},
        {"d": "M 600 670 L 880 670", "color": "risk", "width": 3, "start": C("only needs one that works"), "label": lbl("only needs it to work", 740, 675, 20, "risk")},
        {"d": "M 960 630 L 1100 630 M 1070 610 L 1100 630 L 1070 650", "color": "ink", "width": 4, "start": C("very happy")},
        {"d": dot(1180, 630), "color": "risk", "width": 1, "start": C("very happy", 0.3), "label": lbl("1 / h", 1250, 640, 28, "risk", "start")},
        {"d": " ".join(rect(1120 + (k % 10) * 36, 740 + (k // 10) * 30, 26, 20) for k in range(30)), "color": "accent", "width": 2,
         "start": C("a thousand of them"), "label": lbl("× 1,000", 1300, 860, 30, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("very happy", 0.6), "dur": 1.4, "target": [1180, 630]}],
    "scale": 0.86, "floor": 1040}, sources=["mit_asml"])
kinetic("s28_t4", "m4_transition", [("Canon is changing the method. China is copying the light.", 40, "Canon is changing", None, True), ("Two startups want to change the light itself", 50, "Two startups", "accent", True)])

# ====================================================================== PART 5: new kinds of light
card("s29_c5", "m5_card", "New Kinds of Light", "After extreme ultraviolet")
stage("s30_q5", "m5_question", {
    "zones": [Z("sciencepark")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("beamsrc", x=700, y=520, at=0.3, mode="xray", scale=0.6, text="?", color=SUB),
              it("beamsrc", x=1250, y=520, at=0.8, mode="atoms", scale=0.6, text="?", color=LACE)],
    "callouts": [co("What comes after EUV?", 960, 150, C("What comes after"), "gold", screen=True, size=44)]})
stage("s31_substrate", "m5_substrate", {
    "zones": [Z("sciencepark", -1600, 1600), Z("site", 1600, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("It wants to build"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("It even predicts"), "x": 1500, "y": 520, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [it("beamsrc", x=760, y=500, at=0.3, mode="xray", fireAt=C("X-rays"), scale=0.8, text="SUBSTRATE · X-RAYS", color=SUB, sub="San Francisco"),
              it("crane", x=2300, text="OWN FAB · GOAL 2030", at=C("It wants to build"), progress=[[0, 0.15], [25, 0.5]], scale=0.8),
              it("pricetag", x=1500, y=280, at=C("It even predicts"), pages=[[0, "$100,000"], [{"cue": "about a tenth"}, "$10,000"]], sub="per wafer · Substrate's prediction"),
              it("letters", x=1500, y=560, text="?", at=C("shared few details"), size=150, color="risk")],
    "callouts": [co("No machines for sale: its own factory, goal {{substrate.display}}", 960, 960, C("It does not plan"), "white", screen=True, size=36, sub="MIT Technology Review", until=C("It even predicts", -0.3)),
                 co("A wafer for {{substrate.wafer_display}}? (its prediction)", 960, 960, C("It even predicts"), "gold", screen=True, size=40, until=C("shared few details", -0.3)),
                 co("Few details · an ASML author: 'probably unachievable'", 960, 960, C("shared few details"), "risk", screen=True, size=36, sub="Marc Hijink, MIT Technology Review")]},
    sources=["mit_asml"])
stage("s32_lace", "m5_lace", {
    "zones": [Z("fjord", -1600, 1700), Z("fab", 1700, 6000, label="yellow")], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("It says the atoms"), "x": 900, "y": 460, "zoom": 1.2, "dur": 2.2},
            {"at": C("ASML is not standing still"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("beamsrc", x=760, y=500, at=0.3, mode="atoms", fireAt=C("helium atoms"), scale=0.8, text="LACE · HELIUM ATOMS", color=LACE, sub="Norway"),
              it("letters", x=1300, y=200, text="0.1 nm", at=C("It says the atoms"), size=80, color="gold"),
              it("calendar", x=1350, y=480, at=C("ready to sell"), pages=[[0, "2029-30", "GOAL"]], scale=0.75),
              it("litho", x=2300, at=C("ASML is not standing still", -0.3), fireAt=C("already shipping"), text="HIGH-NA EUV", sub="shipping now", scale=0.75, color="#7E57C2")],
    "callouts": [co("A beam of helium atoms instead of light", 960, 960, C("fires a beam"), "white", screen=True, size=40, until=C("It says the atoms", -0.3)),
                 co("Precision 0.1 nm · machines by {{lace.display}}", 960, 960, C("It says the atoms"), "gold", screen=True, size=38, sub="the company's goal (MIT Technology Review)", until=C("ASML is not standing still", -0.3)),
                 co("Meanwhile: high-NA EUV is already shipping", 960, 960, C("ASML is not standing still"), "white", screen=True, size=38)]},
    sources=["mit_asml"])

# ====================================================================== PAYOFF
stage("s33_payoff", "payoff", {
    "zones": [Z("fab", label="yellow")], "worldW": 3000,
    "cam": [{"at": 0, "x": 1500, "y": 520, "zoom": 0.75}, {"at": C("And that is the real lesson"), "x": 900, "y": 520, "zoom": 1.0, "dur": 3},
            {"at": C("Breaking it will take"), "x": 1500, "y": 520, "zoom": 0.8, "dur": 3}], "drift": 2,
    "items": [it("litho", x=900, at=0.2, fireAt=0.4, text="ASML", scale=0.75, color=ASML),
              it("imprint", x=1650, at=C("Canon's machine works"), rate=0.6, text="CANON", sub="niche chips, for now", scale=0.35, color=CANON),
              it("litho", x=2100, at=C("China's prototype"), fireAt=C("makes light"), text="CHINA", sub="light, no chips", scale=0.42, color=CHINA),
              it("beamsrc", x=2550, y=560, at=C("The startups have goals"), mode="xray", scale=0.45, text="STARTUPS", color=SUB),
              it("calendar", x=900, y=190, at=C("a bet held for"), pages=[[0, "16", "YEARS"]], scale=0.7)],
    "callouts": [co("Could a stamp break the monopoly? Not soon.", 960, 150, C("So could a stamp"), "white", screen=True, size=40, until=C("And that is the real lesson", -0.3)),
                 co("The monopoly was never just a machine", 960, 150, C("And that is the real lesson"), "gold", screen=True, size=42, until=C("Breaking it will take", -0.3)),
                 co("It was a bet held while everyone else gave up", 960, 150, C("Breaking it will take"), "gold", screen=True, size=40)]},
    sources=["mit_asml", "ieee_nil", "reuters_cn_euv"])
add("s34_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_nanoimprint_storyboard.py; edit the generator, not this file.\n"
           "# Episode 15 storyboard (chip series C2): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
