"""Generates projects/who-actually-gets-the-tariff-refund/deliverables/documentary/storyboard.yaml
(Episode 41, new topics N1: Who Actually Gets the $166 Billion Tariff Refund?).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the container port with a giant counter; the supermarket aisle; Washington.
- Part 1 (the ruling): the courtroom, the port, a chain diagram.
- Part 2 (who really paid): the warehouse with pallets, pass-through charts, the store.
- Part 3 (the refund machine): office screens at night, Treasury numbers, the trade court.
- Part 4 (where the money lands): the exchange floor (company results), the store, the warehouse.
- Part 5 (the fight): the courtroom at night, Congress, the port again.
No company logos (names in text only), no real people drawn. Lint: tools/lint_storyboard.py.
Run: python tools/gen_tariff_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/who-actually-gets-the-tariff-refund/deliverables/documentary/storyboard.yaml"
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
    "zones": [Z("port")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1000, y=200, at=0.05, prefix="$", suffix="BN", steps=[[0.05, 0], [1.5, 166]], text="IEEPA TARIFFS CHARGED (CBP ESTIMATE)", scale=1.4),
              it("letters", x=1000, y=420, text="RULED UNLAWFUL BY THE SUPREME COURT", at=C("later said the President had no power"), size=44, color="gold")]},
    sources=["cit", "scotus"])
stage("s02_twist", "h_twist", {
    "zones": [Z("supermarket")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("But almost none of it"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=250, at=0.3, prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in refunds"}, 127.7]], text="REFUNDS SENT FOR PAYMENT BY OCT 23 (INCL. INTEREST)"),
              *crowd([800, 900, 1500], "walk", at=0.2, scale=0.6),
              it("sign", x=1400, y=440, text="SHOPPERS: ≈ $0 FROM THE GOVERNMENT", at=C("But almost none of it"), color="#FFCDD2", size=36)]},
    sources=["cit", "cbp"])
stage("s03_question", "h_question", {
    "zones": [Z("port", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=170, text="WHO PAID? WHO GETS IT BACK?", at=0.3, size=66, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · PORT → CART", at=C("from a port to your shopping cart"), color="#BBDEFB", size=34),
              it("sign", x=960, y=380, text="2 · THE REFUND MACHINE", at=C("the refund"), color="#FFE0B2", size=34),
              it("sign", x=1560, y=380, text="3 · WHY NOT YOU", at=C("not to you"), color="#C8E6C9", size=34),
              it("letters", x=960, y=700, text="FOLLOW THE TARIFF DOLLAR", at=0.4, size=68, color="gold")]})

# ====================================================================== PART 1: the ruling
card("s05_c1", "m1_card", "The Ruling", "February 20, 2026")
stage("s06_case", "m1_case", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Learning Resources"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("sign", x=1400, y=330, text="AN EMERGENCY POWERS LAW: IEEPA", at=0.3, color="#FFE0B2", size=40),
              it("docs", x=700, y=560, at=C("Importers sued"), text="LEARNING RESOURCES v. TRUMP", scale=0.7, stamp="6–3", stampAt=C("by a vote of")),
              it("gavel", x=1650, y=F - 20, hits=[C("by a vote of")], at=0.2)]},
    sources=["scotus"])
stage("s07_held", "m1_held", {
    "zones": [Z("court", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}], "drift": 0,
    "items": [it("letters", x=960, y=200, text="'IEEPA DOES NOT AUTHORIZE", at=0.3, size=56, color="white"),
              it("letters", x=960, y=290, text="THE PRESIDENT TO IMPOSE TARIFFS'", at=0.3, size=56, color="gold"),
              it("letters", x=960, y=420, text="MAJORITY: ROBERTS · DISSENT: THOMAS, ALITO, KAVANAUGH", at=C("Chief Justice Roberts"), size=30, color="white")]},
    sources=["scotus"])
stage("s08_mess", "m1_mess", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And he added a line"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="REFUNDS? THE COURT 'SAYS NOTHING'", at=0.3, size=48, color="gold"),
              it("sign", x=900, y=300, text="'LIKELY TO BE A MESS'", at=C("likely be a mess"), color="#FFCDD2", size=40),
              it("letters", x=1300, y=450, text="'SOME IMPORTERS MAY HAVE ALREADY PASSED ON COSTS TO CONSUMERS'", at=C("Some importers may have"), size=28, color="white")]},
    sources=["scotus"])
stage("s09_scale", "m1_scale", {
    "zones": [Z("port")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("paid by"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 3,
    "items": [it("counter", x=900, y=260, at=0.3, prefix="", suffix="M", steps=[[0, 0], [{"cue": "import shipments"}, 53]], text="IMPORT ENTRIES (CBP ESTIMATE)"),
              it("counter", x=1600, y=260, at=C("paid by"), prefix="≈ ", suffix="K", steps=[[0, 0], [{"cue": "different importers"}, 330]], text="IMPORTERS OF RECORD")]},
    sources=["cit"])
add("p10_chain", "m1_draw", "engine_draw", {
    "title": "Who pays a tariff", "board": BOARD, "draw_start": C("Here is a factory abroad"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 420, 170, 80), "color": "muted", "width": 5, "kind": "box", "start": C("Here is a factory abroad"), "label": lbl("FACTORY", 645, 468, 22, "muted")},
        {"d": rect(800, 420, 170, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("the American company"), "label": lbl("IMPORTER", 885, 468, 22, "accent2")},
        {"d": rect(1040, 420, 170, 80), "color": "accent", "width": 5, "kind": "box", "start": C("Then the goods go to a store"), "label": lbl("STORE", 1125, 468, 22, "accent")},
        {"d": rect(1260, 420, 170, 80), "color": "accent3", "width": 5, "kind": "box", "start": C("and to you"), "label": lbl("YOU", 1345, 468, 22, "accent3")},
        {"d": arrow((735, 460), (795, 460)) + " " + arrow((975, 460), (1035, 460)) + " " + arrow((1215, 460), (1255, 460)), "color": "ink", "width": 4, "kind": "arrow", "start": C("the American company", 0.5)},
        {"d": rect(800, 600, 170, 80), "color": "risk", "width": 5, "kind": "box", "start": C("the importer pays it to customs"), "label": lbl("CUSTOMS", 885, 648, 22, "risk")},
        {"d": arrow((885, 505), (885, 595)), "color": "risk", "width": 5, "kind": "arrow", "start": C("the importer pays it to customs", 0.4), "label": lbl("DUTY", 940, 555, 18, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("The law sees", 0.1), "dur": 1.4, "target": [885, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["cbp"])
kinetic("s11_t1", "m1_transition", [("The legal question: settled…", 62, "The legal question", None, False),
                                    ("…who actually paid?", 72, "Who actually paid", "gold", False)])

# ====================================================================== PART 2: who really paid
card("s12_c2", "m2_card", "Who Really Paid", "Pass-through, in estimates")
stage("s13_importer", "m2_importer", {
    "zones": [Z("warehouse")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The government never sends you"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("pallet", x=[[0, 300], [6, 900]], at=0.2, rows=3, scale=0.8),
              it("letters", x=1000, y=160, text="ON PAPER: THE IMPORTER PAYS", at=0.3, size=54, color="gold"),
              it("pricetag", x=1500, y=360, at=C("before customs releases it"), text="+ DUTY", scale=1.0),
              it("letters", x=1500, y=560, text="NO BILL TO YOU", at=C("The government never sends you"), size=48, color="white")]},
    sources=["cbp"])
stage("s14_pass", "m2_pass", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "LOW ESTIMATE", "value": 46, "color": "#90A4AE", "at": C("Researchers at the Yale"), "display": "46%"},
                     {"label": "HIGH ESTIMATE", "value": 86, "color": "#E53935", "at": C("showed\n    up") if False else C("depending on how"), "display": "86%"}],
                    at=0.2, max=100, title="TARIFFS PASSED INTO CORE GOODS PRICES (YALE BUDGET LAB ESTIMATE)", x=300, w=800),
              it("letters", x=1550, y=380, text="'PASS-THROUGH'", at=C("called pass-through"), size=60, color="gold")]},
    sources=["yale"])
stage("s15_nyfed", "m2_nyfed", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=150, text="NEW YORK FED RESEARCHERS", at=0.3, size=48, color="gold"),
              it("counter", x=960, y=300, at=C("They estimate that"), prefix="≈ ", suffix="%", steps=[[0, 0], [{"cue": "passed through into the prices"}, 90]], text="INTO IMPORT PRICES, 2025 TARIFFS (NY FED RESEARCHERS)", scale=1.3),
              it("letters", x=960, y=600, text="STORE PRICES: SLOWER, OVER MONTHS", at=C("built up more gradually"), size=48, color="gold")]},
    sources=["nyfed"])
stage("s16_split", "m2_split", {
    "zones": [Z("supermarket")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("Exactly how much"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=270, text="THE COST WAS SHARED", at=0.3, size=64, color="gold"),
              it("sign", x=900, y=420, text="IMPORTERS PAID FIRST", at=C("Importers paid customs first"), color="#BBDEFB", size=38),
              it("sign", x=1500, y=420, text="MUCH PASSED ON", at=C("passed a large"), color="#FFE0B2", size=38)]},
    sources=["yale", "nyfed"])
add("p17_dollar", "m2_draw", "engine_draw", {
    "title": "A tariff dollar (illustration)", "board": BOARD, "draw_start": C("One dollar goes to customs"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1440 860", "color": "ink", "width": 4, "start": C("Let me draw a tariff dollar")},
        {"d": "M 600 860 L 600 400 L 740 400 L 740 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("One dollar goes to customs"), "label": lbl("$1 TO CUSTOMS", 670, 380, 20, "risk")},
        {"d": "M 820 860 L 820 700 L 960 700 L 960 860", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("stays with the importer"), "label": lbl("IMPORTER KEEPS", 890, 680, 18, "accent2")},
        {"d": "M 1040 860 L 1040 560 L 1180 560 L 1180 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("moves down the chain"), "label": lbl("PASSED ON", 1110, 540, 18, "accent")},
        {"d": arrow((1190, 600), (1330, 520), 0.2), "color": "ink", "width": 4, "kind": "arrow", "start": C("By the time it reaches"), "label": lbl("YOUR RECEIPT", 1340, 500, 20, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("hidden inside", 0.1), "dur": 1.4, "target": [1110, 650]}],
    "scale": 0.86, "floor": 1040}, sources=["yale", "nyfed"])
kinetic("s18_t2", "m2_transition", [("Now run the chain backwards…", 62, "run that chain backwards", None, False),
                                    ("…where does the money land?", 64, "where does it land", "gold", False)])

# ====================================================================== PART 3: the refund machine
card("s19_c3", "m3_card", "The Refund Machine", "Customs pays importers back")
stage("s20_cape", "m3_cape", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And in October"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="A NEW REFUND SYSTEM (CBP)", at=0.3, size=54, color="gold"),
              it("sign", x=1000, y=260, text="APRIL: RECENT SHIPMENTS", at=C("First, in April"), color="#BBDEFB", size=32),
              it("sign", x=1000, y=360, text="JUNE: COMPLEX CASES", at=C("Then, in June"), color="#FFE0B2", size=32),
              it("sign", x=1000, y=460, text="OCTOBER: OLDEST, WITH A COURT ORDER", at=C("And in October"), color="#FFCDD2", size=30)]},
    sources=["cit", "cbp"])
stage("s21_court", "m3_court", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("counter", x=1000, y=240, at=0.3, prefix="", suffix="+", steps=[[0, 0], [{"cue": "four thousand cases"}, 4000]], text="REFUND CASES AT THE TRADE COURT (OCT 2026)", scale=1.2),
              it("gavel", x=1650, y=F - 20, hits=[C("four thousand cases")], at=0.2)]},
    sources=["cit"])
stage("s22_flow", "m3_flow", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "BY JULY 31", "value": 100, "color": "#90CAF9", "at": C("By the end of July"), "display": "≈ $100BN"},
                     {"label": "BY OCT 23", "value": 127.7, "color": "#1E88E5", "at": C("By late October"), "display": "$127.7BN"}],
                    at=0.2, max=150, title="REFUNDS SENT TO TREASURY FOR PAYMENT, INCL. INTEREST (CBP)", x=300, w=900),
              it("letters", x=1550, y=420, text="OF ≈ $166BN", at=C("the total reached"), size=56, color="gold")]},
    sources=["cit"])
stage("s23_treasury", "m3_treasury", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "MAY", "value": 21.97, "color": "#4FC3F7", "at": 0.5, "display": "$22.0B"},
                     {"label": "JUNE", "value": 49.18, "color": "#E53935", "at": C("In June"), "display": "$49.2B"},
                     {"label": "JULY", "value": 33.38, "color": "#4FC3F7", "at": C("In June", 1.0), "display": "$33.4B"},
                     {"label": "AUG", "value": 10.54, "color": "#4FC3F7", "at": C("In June", 1.5), "display": "$10.5B"},
                     {"label": "SEP", "value": 19.36, "color": "#4FC3F7", "at": C("In June", 2.0), "display": "$19.4B"}],
                    at=0.2, max=55, dark=True, title="CUSTOMS REFUNDS PER MONTH, 2026 (TREASURY)", x=300, w=1100),
              it("letters", x=1640, y=420, text="NET: NEGATIVE MAY–JULY", at=C("went negative"), size=34, color="risk")]},
    sources=["mts"])
stage("s24_held", "m3_held", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("counter", x=1000, y=280, at=0.3, prefix="≈ $", suffix="M", steps=[[0, 0], [{"cue": "on hold"}, 990]], text="WAITING FOR BANK DETAILS (CBP)", scale=1.2),
              it("letters", x=1000, y=540, text="OWED, BUT UNCLAIMED", at=C("bank details"), size=54, color="gold")]},
    sources=["cit"])
add("p25_pipe", "m3_draw", "engine_draw", {
    "title": "The refund pipe", "board": BOARD, "draw_start": C("On the left, the customs agency"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 440, 220, 100), "color": "risk", "width": 5, "kind": "box", "start": C("On the left, the customs agency"), "label": lbl("CUSTOMS", 670, 498, 24, "risk")},
        {"d": rect(890, 440, 220, 100), "color": "accent", "width": 5, "kind": "box", "start": C("In the middle, the Treasury"), "label": lbl("TREASURY", 1000, 498, 24, "accent")},
        {"d": rect(1220, 440, 220, 100), "color": "accent2", "width": 5, "kind": "box", "start": C("the importer's bank account"), "label": lbl("IMPORTER", 1330, 498, 24, "accent2")},
        {"d": arrow((785, 490), (885, 490)) + " " + arrow((1115, 490), (1215, 490)), "color": "ink", "width": 5, "kind": "arrow", "start": C("In the middle, the Treasury", 0.4)},
        {"d": rect(1220, 680, 220, 90), "color": "muted", "width": 4, "kind": "box", "start": C("There is no pipe"), "label": lbl("SHOPPER", 1330, 733, 22, "muted")},
        {"d": "M 1330 550 L 1330 670 M 1290 590 L 1370 650 M 1370 590 L 1290 650", "color": "risk", "width": 6, "start": C("There is no pipe", 0.4)},
    ],
    "actions": [{"kind": "point", "at": C("only that company", 0.1), "dur": 1.4, "target": [1330, 490]}],
    "scale": 0.86, "floor": 1040}, sources=["cbp", "cit"])
kinetic("s26_t3", "m3_transition", [("The checks land in company accounts…", 58, "landing in corporate", None, False),
                                    ("…here is what they did with them", 60, "what some of those", "gold", False)])

# ====================================================================== PART 4: where the money lands
card("s27_c4", "m4_card", "Where the Money Lands", "From the companies' own filings")
stage("s28_rule", "m4_rule", {
    "zones": [Z("port", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("If you paid more"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=160, text="WHO CAN GET A REFUND?", at=0.3, until=C("importer of record"), size=52, color="gold"),
              it("letters", x=1000, y=160, text="'ONLY ... THE IMPORTER OF RECORD' (CBP)", at=C("importer of record"), size=46, color="gold"),
              it("sign", x=1300, y=320, text="NO CONSUMER REFUND · NO FORM TO FILL OUT", at=C("If you paid more"), color="#FFCDD2", size=34)]},
    sources=["cbp"])
stage("s29_target", "m4_target", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In plain words"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="THE RETAILERS' OWN FILINGS", at=0.3, size=44, color="white"),
              it("counter", x=1000, y=240, at=C("Target reported"), prefix="$", suffix="M", steps=[[0, 0], [{"cue": "of tariff refunds in one quarter"}, 994]], text="TARGET: TARIFF REFUNDS BOOKED (10-Q)", scale=1.2),
              it("letters", x=1300, y=480, text="LOWER COSTS → HIGHER PROFIT", at=C("In plain words"), size=48, color="gold")]},
    sources=["filings"])
stage("s30_costco", "m4_costco", {
    "zones": [Z("warehouse")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The clothing maker"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1200, y=90, text="REFUNDS IN COMPANY FILINGS", at=0.3, size=42, color="white"),
              it("sign", x=800, y=200, text="COSTCO: PAID ≈ $500M · BACK ≈ $339M", at=C("Costco said"), color="#BBDEFB", size=34),
              it("sign", x=800, y=320, text="'PART ... INVESTED IN REDUCING PRICES'", at=C("invested in lower prices"), color="#FFF9C4", size=28),
              it("sign", x=1600, y=200, text="LULULEMON: $134.5M → +5.6 PTS MARGIN", at=C("lululemon received"), color="#FFE0B2", size=32),
              it("sign", x=1600, y=320, text="MATTEL: $88M → ≈ 55% MARGIN", at=C("the toy maker Mattel"), color="#C8E6C9", size=32)]},
    sources=["filings"])
stage("s31_fedex", "m4_fedex", {
    "zones": [Z("port")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1100, y=130, text="THE MOST DIRECT CASE: FEDEX", at=0.3, size=50, color="gold"),
              it("counter", x=760, y=280, at=C("FedEx said"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in refunds"}, 3.3]], text="FEDEX: REFUNDS RECEIVED (10-Q)"),
              it("counter", x=1500, y=280, at=C("and recorded about"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "as money owed back"}, 2.7]], text="OWED BACK TO ITS CUSTOMERS")]},
    sources=["filings"])
add("p32_three", "m4_draw", "engine_draw", {
    "title": "Three ways a refund can go (from the filings)", "board": BOARD, "draw_start": C("Some becomes profit"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 360, 280, 90), "color": "ink", "width": 6, "kind": "box", "start": C("Let me draw three ways"), "label": lbl("REFUND", 1000, 413, 26, "ink")},
        {"d": rect(560, 620, 240, 90), "color": "accent", "width": 5, "kind": "box", "start": C("Some becomes profit"), "label": lbl("PROFIT", 680, 673, 24, "accent")},
        {"d": rect(880, 620, 240, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("Some goes back to"), "label": lbl("BUSINESS CUSTOMERS", 1000, 673, 18, "accent2")},
        {"d": rect(1200, 620, 240, 90), "color": "accent3", "width": 5, "kind": "box", "start": C("may turn into lower prices"), "label": lbl("LOWER PRICES?", 1320, 673, 22, "accent3")},
        {"d": arrow((900, 455), (700, 615)) + " " + arrow((1000, 455), (1000, 615)) + " " + arrow((1100, 455), (1300, 615)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Some becomes profit", 0.3)},
    ],
    "actions": [{"kind": "point", "at": C("up\n    to each company") if False else C("each company"), "dur": 1.4, "target": [1000, 660]}],
    "scale": 0.86, "floor": 1040}, sources=["filings"])
kinetic("s33_t4", "m4_transition", [("Which is exactly why…", 64, "Which is exactly why", None, False),
                                    ("…shoppers are going to court", 64, "going to court", "gold", False)])

# ====================================================================== PART 5: the fight
card("s34_c5", "m5_card", "The Fight", "Lawsuits and new tariffs")
stage("s35_suits", "m5_suits", {
    "zones": [Z("court", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("FedEx disclosed fourteen"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="CONSUMER CLASS ACTIONS", scale=0.7, stamp="ALLEGATIONS", stampAt=C("These\n    are allegations") if False else C("are allegations")),
              it("sign", x=1150, y=330, text="COSTCO: 4 SUITS", at=C("Costco disclosed four"), color="#FFE0B2", size=38),
              it("sign", x=1650, y=330, text="FEDEX: 14 SUITS", at=C("FedEx disclosed fourteen"), color="#BBDEFB", size=38)]},
    sources=["filings"])
stage("s36_class", "m5_class", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1000, y=150, text="CERTIFIED: A CLASS OF IMPORTERS", at=C("certified a class of importers"), size=52, color="gold"),
              it("letters", x=1000, y=250, text="(TRADE COURT, OCT 2026)", at=0.3, size=36, color="white"),
              it("gavel", x=1650, y=F - 20, hits=[C("certified a class")], at=0.2)]},
    sources=["cit"])
stage("s37_after", "m5_after", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The Tax Foundation"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1250, y=110, text="THE TARIFFS DID NOT DISAPPEAR", at=0.3, size=48, color="gold"),
              it("sign", x=800, y=230, text="SECTION 122: 10% FOR 150 DAYS", at=C("Section\n    one twenty-two") if False else C("one twenty-two"), color="#FFE0B2", size=34),
              it("sign", x=1500, y=230, text="THEN SECTION 301: 60 ECONOMIES", at=C("three oh one"), color="#FFCDD2", size=34),
              it("sign", x=1150, y=340, text="≈ $820 PER HOUSEHOLD IN 2026 (TAX FOUNDATION ESTIMATE)", at=C("The Tax Foundation"), color="#FFF9C4", size=30)]},
    sources=["crs"])
add("p38_loop", "m5_draw", "engine_draw", {
    "title": "The tariff loop", "board": BOARD, "draw_start": C("Tariffs go in at the port"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(1090, 340, 280, 80), "color": "risk", "width": 5, "kind": "box", "start": C("Tariffs go in at the port"), "label": lbl("TARIFF AT THE PORT", 1230, 388, 20, "risk")},
        {"d": rect(1410, 520, 260, 80), "color": "accent", "width": 5, "kind": "box", "start": C("Prices rise on the shelf"), "label": lbl("PRICES RISE", 1540, 568, 22, "accent")},
        {"d": rect(1090, 700, 280, 80), "color": "ink", "width": 5, "kind": "box", "start": C("The court says"), "label": lbl("COURT: ILLEGAL", 1230, 748, 22, "ink")},
        {"d": rect(790, 520, 260, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("Refunds come out"), "label": lbl("REFUND → IMPORTERS", 920, 568, 18, "accent2")},
        {"d": arrow((1370, 400), (1470, 515), 0.2) + " " + arrow((1530, 605), (1370, 710), 0.2) + " " + arrow((1090, 720), (950, 605), 0.2) + " " + arrow((930, 515), (1090, 400), 0.2), "color": "ink", "width": 4, "kind": "arrow", "start": C("new tariffs start the loop")},
    ],
    "actions": [{"kind": "point", "at": C("under a new law", 0.1), "dur": 1.4, "target": [1230, 380]}],
    "scale": 0.86, "floor": 1040}, sources=["crs", "cit"])

# ====================================================================== PAYOFF
stage("s39_payoff", "payoff", {
    "zones": [Z("port", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("The money left"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=150, text="WHO GETS THE REFUND?", at=0.3, until=C("The companies that paid"), size=60, color="gold"),
              it("letters", x=1000, y=150, text="THE COMPANIES THAT PAID AT THE BORDER", at=C("The companies that paid"), size=46, color="gold"),
              it("letters", x=1000, y=260, text="OUT THROUGH THE PORT · BACK THROUGH THE SAME DOOR", at=C("The money left"), size=36, color="white")]},
    sources=["cbp", "yale"])
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_tariff_storyboard.py; edit the generator, not this file.\n"
           "# Episode 41 storyboard (tariff refunds): one visual language per part; tones from visual_direction.yaml.\n")
