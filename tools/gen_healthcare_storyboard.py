"""Generates projects/why-americans-pay-so-much-for-healthcare/deliverables/documentary/storyboard.yaml (Episode 29,
US batch #01: Why Americans Pay So Much for Healthcare).

Built on the diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md): one visual language per part.
- Hook: an itemized medical bill unrolling (new `medbill` item) over a hospital corridor (new `hospital` set).
- Part 1 (the bill): full-screen data charts in the studio.
- Part 2 (less care, higher prices): the hospital corridor with few patients and the price on top.
- Part 3 (the hospital): two patients, one hospital, two bills.
- Part 4 (the pharmacy): a pharmacy shop with pill bottles and swinging price tags (new `pills` item).
- Part 5 (the paperwork): an evidence board tracing where the premium goes.
Five presenter boards (bars, equation boxes, two patients, three pills, premium flow); text mostly on objects or at the top.
No hospital, insurer or drug-maker logos; no likeness of real people.
Run: python tools/gen_healthcare_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-americans-pay-so-much-for-healthcare/deliverables/documentary/storyboard.yaml"
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


def chart(bars, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars, at=at, **kw)


# ====================================================================== HOOK (4 beats)
stage("s01_open", "h_open", {
    "zones": [Z("hospital")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.25}, {"at": 1.0, "x": 960, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("medbill", x=960, y=120, at=0.05, scale=1.05, title="FAMILY HEALTH PLAN · 1 YEAR",
                 lines=[{"text": "Your share", "amount": "$7,471", "at": 1.0}, {"text": "Your employer's share", "amount": "$20,832", "at": 1.6}],
                 total={"text": "TOTAL", "amount": "$28,303", "at": 2.4})]},
    sources=["kff_ehbs"])
stage("s02_twist", "h_twist", {
    "zones": [Z("hospital")], "worldW": 2600,
    "cam": [{"at": 0, "x": 950, "y": 520, "zoom": 1.0}, {"at": C("Yet they pay far more"), "x": 1350, "y": 500, "zoom": 0.85, "dur": 1.4}], "drift": 1,
    "items": [it("person", x=700, pose="walk", at=0.2, scale=0.75, hair=2, skin=1),
              it("letters", x=820, y=200, text="½ THE DOCTOR VISITS", at=C("about half as often"), size=70, color="green"),
              it("letters", x=820, y=320, text="FEWER HOSPITAL DAYS", at=C("They spend fewer days"), size=54, color="green"),
              it("letters", x=1750, y=200, text="PAY FAR MORE", at=C("Yet they pay far more"), size=90, color="risk"),
              it("letters", x=1750, y=330, text="LIVE SHORTER LIVES", at=C("they live shorter lives"), size=60, color="risk")]},
    sources=["pkff_prices", "pkff_life"])
stage("s03_question", "h_question", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.15}, {"at": 1.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("coins", **{"from": [600, 500], "to": [1500, 300]}, at=0.2, rate=6),
              it("letters", x=960, y=380, text="WHERE DOES THE MONEY GO?", at=0.3, size=90, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=480, y=360, text="1 · HOSPITAL", at=0.3, color="#B2DFDB", size=52),
              it("sign", x=960, y=360, text="2 · PHARMACY", at=0.8, color="#FFE0B2", size=52),
              it("sign", x=1440, y=360, text="3 · PAPERWORK", at=1.3, color="#E1BEE7", size=52),
              it("letters", x=960, y=650, text="+ WHY THEY'RE SO HARD TO CUT", at=C("and why they are so hard"), size=56, color="risk")]})

# ====================================================================== PART 1: the bill (data language)
card("s05_c1", "m1_card", "The Bill", "2024")
stage("s06_total", "m1_total", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.2}, {"at": C("That is"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 0,
    "items": [it("counter", x=960, y=260, at=0.3, prefix="$", suffix=" TRILLION", decimals=1, steps=[[0, 0], [{"cue": "on health care", "offset": 0}, 5.3]], text="US HEALTH SPENDING, 2024 (CMS)", scale=1.4),
              it("counter", x=600, y=640, at=C("That is"), prefix="$", steps=[[0, 0], [{"cue": "for every man", "offset": 0.5}, 15474]], text="PER PERSON"),
              it("counter", x=1320, y=640, at=C("of everything"), suffix="%", decimals=1, steps=[[0, 0], [{"cue": "economy produced", "offset": 0}, 18.0]], text="OF GDP"),
              it("letters", x=960, y=960, text="+7.2% IN ONE YEAR", at=C("And it grew"), size=56, color="risk")]},
    sources=["cms"])
stage("s07_parts", "m1_parts", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "HOSPITALS", "value": 1634.7, "color": "#2E7D74", "at": C("The biggest piece"), "display": "$1.63tn", "sub": "+8.9%"},
                     {"label": "PRESCRIPTION DRUGS", "value": 467.0, "color": "#E89A00", "at": C("Prescription drugs"), "display": "$467bn", "sub": "+7.9%"}],
                    at=0.2, max=1800, title="TWO BIG PIECES OF THE BILL (2024, CMS)", x=460, w=1000)]},
    sources=["cms"])
stage("s08_peers", "m1_peers", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}, {"at": C("Even Switzerland"), "x": 960, "y": 540, "zoom": 1.0, "dur": 1.5}], "drift": 0,
    "items": [chart([{"label": "PEER AVERAGE", "value": 7860, "color": "#90A4AE", "at": C("The average of comparable")},
                     {"label": "UNITED STATES", "value": 14775, "color": "#E53935", "at": C("the US spent")}],
                    at=0.2, prefix="$", max=16000, dark=True, title="HEALTH SPENDING PER PERSON, 2024 (OECD BASIS)", x=480, w=960),
              it("letters", x=960, y=980, text="SWITZERLAND (#2): ≈ $5,000 LESS", at=C("Even Switzerland"), size=48, color="gold")]},
    sources=["pkff_spend"])
add("p09_peers", "m1_draw", "engine_draw", {
    "title": "More money, shorter lives", "board": BOARD, "draw_start": C("Here is the average rich country"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 640 L 1460 640", "color": "ink", "width": 4, "start": C("Here is the average rich country")},
        {"d": "M 680 640 L 680 540 L 820 540 L 820 640", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("spending about eight thousand"), "label": lbl("PEERS ~$7.9k", 750, 520, 22, "accent2")},
        {"d": "M 920 640 L 920 515 L 1060 515 L 1060 640", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is Switzerland"), "label": lbl("SWITZERLAND", 990, 495, 22, "accent")},
        {"d": "M 1160 640 L 1160 400 L 1300 400 L 1300 640", "color": "risk", "width": 7, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("And here is the United States"), "label": lbl("US ~$14.8k", 1230, 380, 24, "risk")},
        {"d": "M 600 760 L 1460 760", "color": "ink", "width": 3, "start": C("Now look underneath")},
        {"d": "M 1160 760 L 1160 860 L 1300 860 L 1300 760", "color": "risk", "width": 6, "kind": "bar", "start": C("Seventy-nine years"), "label": lbl("US 79 yrs", 1230, 900, 22, "risk")},
        {"d": "M 680 760 L 680 875 L 820 875 L 820 760", "color": "accent3", "width": 6, "kind": "bar", "start": C("Almost eighty-three"), "label": lbl("PEERS 82.7", 750, 915, 22, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("but not the longest lives", 0.2), "dur": 1.4, "target": [1230, 820]}],
    "scale": 0.86, "floor": 1040}, sources=["pkff_spend", "pkff_life"])
stage("s10_life", "m1_life", {
    "zones": [Z("hospital", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("More money"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=900, y=230, at=0.3, suffix=" YEARS", steps=[[0, 70], [{"cue": "in twenty twenty-four", "offset": 0}, 79]], text="US LIFE EXPECTANCY, 2024 (RECORD)"),
              it("letters", x=1450, y=480, text="−3.7 YEARS VS PEERS", at=C("But that is still"), size=60, color="risk"),
              *crowd([500, 640, 1500, 1640], "stand", at=0.4, scale=0.6, old=True)]},
    sources=["pkff_life"])
kinetic("s11_t1", "m1_transition", [("What is the money buying?", 58, "So what is all that money", None, True), ("Not more care.", 76, "It is not more care", "gold", False)])

# ====================================================================== PART 2: less care, higher prices (hospital world)
card("s12_c2", "m2_card", "Less Care, Higher Prices", "The US vs other rich countries")
stage("s13_usage", "m2_usage", {
    "zones": [Z("hospital")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("In other rich countries"), "x": 1400, "y": 520, "zoom": 0.9, "dur": 1.5},
            {"at": C("And an average hospital stay"), "x": 1800, "y": 520, "zoom": 0.9, "dur": 1.5}], "drift": 1,
    "items": [it("letters", x=1000, y=260, text="DOCTOR VISITS: ≈ ½", at=C("They have"), size=64, color="green"),
              it("person", x=700, pose="read", at=C("They have"), scale=0.7, hair=1, skin=2),
              it("letters", x=1450, y=150, text="PEERS: +57% DISCHARGES", at=C("In other rich countries"), size=56, color="white"),
              it("calendar", x=2100, y=300, at=C("And an average hospital stay"), pages=[[0, "6.5", "DAYS (US)"], [{"cue": "against almost ten days"}, "9.7", "DAYS (PEERS)"]], scale=0.85)]},
    sources=["pkff_prices"])
stage("s14_finding", "m2_finding", {
    "zones": [Z("corkboard")], "worldW": 2000,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.2}, {"at": C("In the words of"), "x": 1000, "y": 470, "zoom": 1.0, "dur": 1.8}], "drift": 0,
    "items": [it("pinboard", cards=[
                {"x": 650, "y": 380, "text": "MORE CARE?", "sub": "no", "at": 0.4, "w": 300, "color": "#FFCDD2", "size": 44},
                {"x": 1350, "y": 380, "text": "HIGHER PRICES", "sub": "yes", "at": C("the conclusion keeps"), "w": 380, "color": "#C8E6C9", "size": 44},
                {"x": 1000, "y": 680, "text": "'higher prices … explain the high spending'", "sub": "Peterson-KFF", "at": C("In the words of"), "w": 760, "size": 30}],
              links=[[1, 2, C("In the words of", 0.5)]], stamp="CONFIRMED", stampAt=C("that explain the high spending"))]},
    sources=["pkff_prices", "jama"])
stage("s15_example", "m2_example", {
    "zones": [Z("hospital")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("For a procedure"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.5}], "drift": 1,
    "items": [it("medbill", x=650, y=140, at=C("Take a heart bypass"), scale=0.8, title="HEART BYPASS · US MEDICARE",
                 lines=[{"text": "Average cost", "amount": "$44,149", "at": C("the average cost was")}]),
              it("medbill", x=1350, y=140, at=C("In public insurance schemes"), scale=0.8, title="HEART BYPASS · PEER NATIONS",
                 lines=[{"text": "Average cost", "amount": "$24,847", "at": C("it was about")}]),
              it("letters", x=1000, y=760, text="ANGIOPLASTY: 2.9×", at=C("For a procedure"), size=70, color="risk")]},
    sources=["pkff_prices"])
add("p16_equation", "m2_draw", "engine_draw", {
    "title": "Spending = care × price", "board": BOARD, "draw_start": C("Spending equals"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 380, 240, 120), "color": "ink", "width": 6, "kind": "box", "start": C("Spending equals"), "label": lbl("SPENDING", 660, 448, 26, "ink")},
        {"d": rect(870, 380, 240, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("the amount of care"), "label": lbl("AMOUNT OF CARE", 990, 448, 22, "accent3")},
        {"d": rect(1200, 380, 240, 120), "color": "risk", "width": 6, "kind": "box", "start": C("times the price"), "label": lbl("PRICE", 1320, 448, 28, "risk")},
        {"d": "M 795 440 L 855 440 M 795 455 L 855 455", "color": "ink", "width": 5, "start": C("Spending equals", 0.6)},
        {"d": "M 1135 420 L 1175 470 M 1175 420 L 1135 470", "color": "ink", "width": 5, "start": C("times the price", 0.3)},
        {"d": "M 990 520 L 990 600", "color": "accent3", "width": 5, "start": C("is not unusually high"), "label": lbl("normal", 990, 640, 22, "accent3")},
        {"d": arrow((1320, 620), (1320, 520), 0.0), "color": "risk", "width": 7, "start": C("So the price has to be"), "label": lbl("HIGH", 1320, 660, 28, "risk")},
        {"d": rect(560, 720, 880, 110), "color": "accent", "width": 5, "kind": "box", "start": C("three prices that matter most"), "label": lbl("HOSPITAL · PHARMACY · PAPERWORK", 1000, 785, 28, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("And the paperwork", 0.3), "dur": 1.4, "target": [1000, 775]}],
    "scale": 0.86, "floor": 1040}, sources=["pkff_prices"])
kinetic("s17_t2", "m2_transition", [("Price #1", 70, "Start with the biggest", None, False), ("The hospital", 80, "The hospital", "gold", False)])

# ====================================================================== PART 3: the hospital (two patients, two bills)
card("s18_c3", "m3_card", "Price One: The Hospital", "Same care, different prices")
stage("s19_two", "m3_two", {
    "zones": [Z("hospital")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 500, "zoom": 0.95}], "drift": 1,
    "items": [it("person", x=800, pose="stand", at=C("For older Americans"), scale=0.8, old=True, hair=1, skin=0),
              it("sign", x=800, y=300, text="MEDICARE", sub="price set by government", at=C("For older Americans"), color="#BBDEFB", size=40),
              it("person", x=1800, pose="stand", at=C("For everyone with private"), scale=0.8, hair=3, skin=2),
              it("sign", x=1800, y=300, text="PRIVATE PLAN", sub="price negotiated, insurer by insurer", at=C("For everyone with private"), color="#FFCDD2", size=40),
              it("letters", x=1300, y=150, text="SAME HOSPITAL · MANY PRICES", at=C("It has many"), size=52, color="gold")]},
    sources=["rand_hosp"])
stage("s20_rand", "m3_rand", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "MEDICARE", "value": 100, "color": "#1565C0", "at": 0.5, "display": "100%"},
                     {"label": "PRIVATE PLANS", "value": 254, "color": "#E53935", "at": C("they paid on average"), "display": "254%"},
                     {"label": "OUTPATIENT", "value": 279, "color": "#B71C1C", "at": C("For outpatient"), "display": "279%", "sub": "private plans"}],
                    at=0.2, max=300, title="WHAT HOSPITALS WERE PAID, 2022 (RAND)", x=360, w=1200),
              it("letters", x=960, y=990, text="≈ 2.5× FOR THE SAME CARE", at=C("In other words"), size=56, color="gold")]},
    sources=["rand_hosp"])
stage("s21_caveat", "m3_caveat", {
    "zones": [Z("office")], "worldW": 2000,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}], "drift": 1,
    "items": [it("docs", x=800, y=560, at=0.3, text="RAND ROUND 5.1", scale=0.7, stamp="PART OF MARKET", stampAt=C("covers only part")),
              it("magnifier", x=[[0, 1200], [6, 1500]], y=[[0, 520], [6, 480]], at=C("So treat the exact number"), scale=0.8),
              it("letters", x=1400, y=230, text="DIRECTION: PRICES ARE HIGH", at=C("The direction, though"), size=52, color="gold")]},
    sources=["rand_hosp", "pkff_prices"])
stage("s22_mri", "m3_mri", {
    "zones": [Z("hospital", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Same machine"), "x": 1300, "y": 520, "zoom": 1.05, "dur": 1.5}], "drift": 2,
    "items": [it("device", type="server", x=900, y=F, at=0.3, scale=1.3),
              it("letters", x=900, y=250, text="MRI SCAN", at=0.4, size=70, color="white"),
              it("letters", x=1600, y=300, text="PRIVATE PLAN > 3× MEDICARE", at=C("cost more than three times"), size=54, color="risk")]},
    sources=["pkff_prices"])
add("p23_twopatients", "m3_draw", "engine_draw", {
    "title": "One hospital, two patients", "board": BOARD, "draw_start": C("On the left"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 330, 300, 120), "color": "ink", "width": 6, "kind": "box", "start": C("Let me draw one hospital", 1.0), "label": lbl("ONE HOSPITAL", 1010, 398, 26, "ink")},
        {"d": rect(560, 620, 260, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("On the left"), "label": lbl("MEDICARE: 100", 690, 688, 24, "accent2")},
        {"d": rect(1200, 620, 260, 120), "color": "risk", "width": 6, "kind": "box", "start": C("On the right"), "label": lbl("PRIVATE: ~250", 1330, 688, 24, "risk")},
        {"d": arrow((930, 460), (720, 610), 0.1), "color": "accent2", "width": 5, "start": C("The hospital is paid one hundred")},
        {"d": arrow((1090, 460), (1300, 610), -0.1), "color": "risk", "width": 6, "start": C("The hospital is paid about two hundred")},
        {"d": "M 1330 760 L 1330 860 L 1390 820 M 1330 860 L 1270 820", "color": "risk", "width": 6, "start": C("It comes back"), "label": lbl("HIGHER PREMIUMS", 1330, 900, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("It comes back", 0.3), "dur": 1.4, "target": [1330, 690]}],
    "scale": 0.86, "floor": 1040}, sources=["rand_hosp"])
kinetic("s24_t3", "m3_transition", [("Price #2", 70, "The second price", None, False), ("The pharmacy", 80, "pick up a prescription", "gold", False)])

# ====================================================================== PART 4: the pharmacy
card("s25_c4", "m4_card", "Price Two: The Pharmacy", "Brand-name vs generic")
stage("s26_brand", "m4_brand", {
    "zones": [Z("shop", label="PHARMACY")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("For brand-name drugs"), "x": 1300, "y": 520, "zoom": 1.05, "dur": 1.5}], "drift": 2,
    "items": [it("pills", x=800, at=0.3, label="ALL DRUGS", price="278%", scale=1.0),
              it("pills", x=1500, at=C("For brand-name drugs"), label="BRAND-NAME", price="422%", color="#E53935", scale=1.15),
              it("letters", x=1150, y=930, text="US PRICE vs 33 RICH COUNTRIES (RAND, 2022)", at=0.5, size=40, color="gold")]},
    sources=["rand_drugs"])
stage("s27_generic", "m4_generic", {
    "zones": [Z("shop", label="PHARMACY")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("pills", x=800, at=0.3, label="GENERIC", price="67%", color="#43A047", scale=1.0, sub="cheaper in the US"),
              it("pills", x=1450, at=0.6, label="BRAND-NAME", price="422%", color="#E53935", scale=1.0, sub="patented"),
              it("letters", x=1100, y=930, text="THE PROBLEM: NEW, PATENTED DRUGS", at=C("The problem is not every pill"), size=46, color="gold")]},
    sources=["rand_drugs"])
stage("s28_rebates", "m4_rebates", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "BRAND, LIST", "value": 422, "color": "#E53935", "at": 0.4, "display": "422%"},
                     {"label": "BRAND, AFTER REBATES", "value": 308, "color": "#EF6C00", "at": C("Even after estimating"), "display": "308%"},
                     {"label": "MEDICARE-NEGOTIATED", "value": 280, "color": "#7E57C2", "at": C("And even the prices"), "display": "2.8×", "sub": "vs 11 peers (KFF)"}],
                    at=0.2, max=460, dark=True, title="US BRAND-NAME DRUG PRICES vs OTHER RICH COUNTRIES", x=340, w=1240)]},
    sources=["rand_drugs", "pkff_prices"])
add("p29_pills", "m4_draw", "engine_draw", {
    "title": "The same pill, three prices", "board": BOARD, "draw_start": C("Here is the price in other rich countries"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("Here is the price in other rich countries")},
        {"d": "M 640 860 L 640 780 L 780 780 L 780 860", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("set to one hundred"), "label": lbl("ABROAD 100", 710, 760, 22, "accent2")},
        {"d": "M 880 860 L 880 806 L 1020 806 L 1020 860", "color": "accent3", "width": 6, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is the American generic"), "label": lbl("US GENERIC 67", 950, 786, 22, "accent3")},
        {"d": "M 1120 860 L 1120 520 L 1260 520 L 1260 860", "color": "risk", "width": 7, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("the American brand-name price"), "label": lbl("US BRAND 422", 1190, 500, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Very different price tags", 0.2), "dur": 1.4, "target": [1190, 690]}],
    "scale": 0.86, "floor": 1040}, sources=["rand_drugs"])
kinetic("s30_t4", "m4_transition", [("Price #3", 70, "The third price", None, False), ("The hardest to see", 66, "the hardest to see", "gold", False)])

# ====================================================================== PART 5: the paperwork (evidence board)
card("s31_c5", "m5_card", "Price Three: The Paperwork", "Administration and premiums")
stage("s32_admin", "m5_admin", {
    "zones": [Z("office")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("A major study"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 3,
    "items": [it("docs", x=800, y=560, at=0.3, text="CLAIMS · CODES · APPEALS", scale=0.75, stamp="DENIED?", stampAt=C("argue over every bill")),
              chart([{"label": "US (2016)", "value": 8, "color": "#E53935", "at": C("administration took about"), "display": "8%"},
                     {"label": "OTHER RICH COUNTRIES", "value": 2, "color": "#90A4AE", "at": C("against one to three"), "display": "1–3%"}],
                    at=C("A major study"), max=10, title="ADMINISTRATION, SHARE OF SPENDING (JAMA)", x=1300, w=800, h=480),
              it("letters", x=1700, y=970, text="2024: ≈ 7% (INSURANCE + PROGRAMS)", at=C("More recent figures"), size=40, color="gold")]},
    sources=["jama", "pkff_time"])
stage("s33_premium", "m5_premium", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("Workers themselves"), "x": 1300, "y": 500, "zoom": 1.05, "dur": 1.5}], "drift": 2,
    "items": [it("medbill", x=800, y=140, at=C("In twenty twenty-six"), scale=0.85, title="FAMILY PLAN · 2026",
                 lines=[{"text": "Worker pays", "amount": "$7,471", "at": C("Workers themselves")}, {"text": "Employer pays", "amount": "$20,832", "at": C("The employer paid")}],
                 total={"text": "TOTAL", "amount": "$28,303", "at": C("cost on average")}),
              it("letters", x=1650, y=300, text="+5% IN ONE YEAR", at=C("up five percent"), size=60, color="risk"),
              it("letters", x=1650, y=420, text="WORKERS: +9%", at=C("nine percent more"), size=52, color="risk")]},
    sources=["kff_ehbs"])
add("p34_flow", "m5_draw", "engine_draw", {
    "title": "Where a premium goes", "board": BOARD, "draw_start": C("Into the insurer"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 330, 300, 120), "color": "accent", "width": 6, "kind": "box", "start": C("Into the insurer"), "label": lbl("PREMIUM → INSURER", 1010, 398, 22, "accent")},
        {"d": rect(540, 640, 260, 120), "color": "risk", "width": 6, "kind": "box", "start": C("Out to hospitals"), "label": lbl("HOSPITALS", 670, 708, 24, "risk")},
        {"d": arrow((930, 460), (700, 630), 0.1), "color": "risk", "width": 5, "start": C("Out to hospitals", 0.3), "label": lbl("~2.5× Medicare", 740, 560, 20, "risk")},
        {"d": rect(1220, 640, 260, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Out to the pharmacy"), "label": lbl("PHARMACY", 1350, 708, 24, "accent2")},
        {"d": arrow((1090, 460), (1320, 630), -0.1), "color": "accent2", "width": 5, "start": C("Out to the pharmacy", 0.3), "label": lbl("brand 4×", 1290, 560, 20, "accent2")},
        {"d": rect(900, 560, 220, 90), "color": "accent3", "width": 5, "kind": "box", "start": C("a slice that stays behind"), "label": lbl("PAPERWORK", 1010, 612, 22, "accent3")},
        {"d": arrow((1010, 460), (1010, 550), 0.0), "color": "accent3", "width": 5, "start": C("a slice that stays behind", 0.3)},
    ],
    "actions": [{"kind": "point", "at": C("Three prices, one bill", 0.2), "dur": 1.4, "target": [1010, 400]}],
    "scale": 0.86, "floor": 1040}, sources=["kff_ehbs", "rand_hosp", "rand_drugs", "jama"])
stage("s35_hard", "m5_hard", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.15}, {"at": C("Lowering the price"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 1100, "y": 300, "text": "EVERY PRICE", "sub": "is somebody's income", "at": 0.3, "w": 400, "size": 48},
                {"x": 600, "y": 620, "text": "HOSPITAL BUDGET", "at": C("A hospital's budget"), "w": 340, "size": 32},
                {"x": 1100, "y": 680, "text": "DRUG MAKER PROFIT", "at": C("a drug maker's profit"), "w": 360, "size": 32},
                {"x": 1600, "y": 620, "text": "INSURER REVENUE", "at": C("an insurer's revenue"), "w": 340, "size": 32}],
              links=[[0, 1, C("A hospital's budget", 0.3)], [0, 2, C("a drug maker's profit", 0.3)], [0, 3, C("an insurer's revenue", 0.3)]])]})

# ====================================================================== PAYOFF
stage("s36_payoff", "payoff", {
    "zones": [Z("hospital")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Health care in America"), "x": 1200, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 1,
    "items": [it("letters", x=900, y=220, text="LESS CARE", at=C("They go less"), size=80, color="green"),
              it("medbill", x=1500, y=120, at=C("They pay more"), scale=0.75, title="EACH PIECE OF CARE",
                 lines=[{"text": "Visit", "amount": "$$$", "at": C("each visit")}, {"text": "Scan", "amount": "$$$", "at": C("each scan")},
                        {"text": "Pill", "amount": "$$$", "at": C("each pill")}, {"text": "Claim", "amount": "$$$", "at": C("and each claim")}],
                 total={"text": "PRICE", "amount": "HIGH", "at": C("It is expensive because")})]},
    sources=["pkff_prices"])
add("s37_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_healthcare_storyboard.py; edit the generator, not this file.\n"
           "# Episode 29 storyboard (US healthcare prices): one visual language per part; tones from visual_direction.yaml.\n")
