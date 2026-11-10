"""Generates projects/alaska-the-state-that-pays-you-to-live-there/deliverables/documentary/storyboard.yaml
(Episode 48, new topics N8: Alaska: The State That Pays You to Live There).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the snowy north with a pipeline (new `tundra` set) and a giant check (new `bigcheck` item); the northern lights.
- Part 1 (the check): the cabins town, the studio chart, a checks-over-time drawing.
- Part 2 (the fund): the tundra pipeline, the exchange (investments), a two-room vault drawing.
- Part 3 (the cut): the courtroom, Congress-style legislature, a tug-of-war drawing.
- Part 4 (the 2026 check): the legislature at night, the office, a ghost-check drawing.
- Part 5 (what the money does): the supermarket, the hospital, a research-arrows drawing.
No logos, no flags, no real people drawn. Lint: tools/lint_storyboard.py. Run: python tools/gen_alaska_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/alaska-the-state-that-pays-you-to-live-there/deliverables/documentary/storyboard.yaml"
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
    "zones": [Z("tundra")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.15}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("bigcheck", x=1000, y=330, at=0.05, scale=0.9, amount="$1,200", date="2026", payee="EVERY ELIGIBLE RESIDENT"),
              *crowd([500, 600, 1500], "cheer", at=C("Men,"), scale=0.7)]},
    sources=["pfd"])
stage("s02_twist", "h_twist", {
    "zones": [Z("tundra", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("The legislature paid"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="BUT THE FORMULA SAID…", at=0.3, size=54, color="gold"),
              it("bigcheck", x=1000, y=300, at=C("The governor's office"), scale=0.85, amount="$3,650", ghost=True, title="BY THE FORMULA", memo="GOVERNOR'S FY27 BUDGET"),
              it("bigcheck", x=1050, y=470, at=C("The legislature paid"), scale=0.7, amount="$1,200", date="2026")]},
    sources=["court", "pfd"])
stage("s03_question", "h_question", {
    "zones": [Z("vault", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=170, text="WHERE DOES IT COME FROM? WHY DOES IT SHRINK?", at=0.3, size=48, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · OIL → A $90BN FUND", at=C("oil money became"), color="#BBDEFB", size=32),
              it("sign", x=960, y=380, text="2 · THE STATE DEPENDS ON IT", at=C("why the state now"), color="#FFE0B2", size=30),
              it("sign", x=1560, y=380, text="3 · WHAT THE CHECKS DO", at=C("what economists found"), color="#C8E6C9", size=30),
              it("letters", x=960, y=700, text="FOLLOW THE CHECK", at=0.4, size=72, color="gold")]})

# ====================================================================== PART 1: the check
card("s05_c1", "m1_card", "The Check", "Since 1982")
stage("s06_first", "m1_first", {
    "zones": [Z("tundra")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In total"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("bigcheck", x=900, y=330, at=0.3, scale=0.75, amount="$1,000", date="1982"),
              it("counter", x=1700, y=250, at=C("In total"), prefix="≈ $", suffix="M", steps=[[0, 0], [{"cue": "that year"}, 471]], text="PAID OUT IN 1982 (PFD DIVISION)")]},
    sources=["pfd"])
stage("s07_rules", "m1_rules", {
    "zones": [Z("tundra", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In twenty twenty-five"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="THE RULES", at=0.3, size=60, color="gold"),
              it("sign", x=700, y=240, text="LIVE HERE ALL YEAR · INTEND TO STAY", at=C("You must live"), color="#BBDEFB", size=30),
              it("sign", x=700, y=340, text="72 HOURS IN A ROW IN THE STATE", at=C("seventy-two hours"), color="#FFE0B2", size=30),
              it("counter", x=1550, y=300, at=C("In twenty twenty-five"), prefix="", suffix="", steps=[[0, 0], [{"cue": "were paid"}, 618863]], text="PEOPLE PAID IN 2025 (PFD DIVISION)")]},
    sources=["pfd"])
stage("s08_history", "m1_history", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "1982", "value": 1000, "color": "#90A4AE", "at": 0.4, "display": "$1,000"},
                     {"label": "2015", "value": 2072, "color": "#4FC3F7", "at": C("In twenty fifteen"), "display": "$2,072"},
                     {"label": "2022", "value": 3284, "color": "#E53935", "at": C("The\n    largest payment") if False else C("largest payment ever"), "display": "$3,284"},
                     {"label": "2024", "value": 1702, "color": "#4FC3F7", "at": C("In twenty twenty-four"), "display": "$1,702"},
                     {"label": "2025", "value": 1000, "color": "#90A4AE", "at": C("In twenty twenty-five"), "display": "$1,000"}],
                    at=0.2, max=3600, title="PFD PER PERSON, NOMINAL (INCL. ENERGY RELIEF IN 2022, 2024)", x=300, w=1300)]},
    sources=["pfd"])
stage("s09_total", "m1_total", {
    "zones": [Z("tundra")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Someone who collected"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=900, y=250, at=0.3, prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in dividends"}, 31.3]], text="ALL DIVIDENDS, 1982–2025 (PFD DIVISION)", scale=1.2),
              it("counter", x=1550, y=420, at=C("Someone who collected"), prefix="≈ $", suffix="", steps=[[0, 0], [{"cue": "before inflation"}, 52831]], text="ONE PERSON, EVERY CHECK (NOMINAL)")]},
    sources=["pfd"])
add("p10_checks", "m1_draw", "engine_draw", {
    "title": "The checks over time (selected years)", "board": BOARD, "draw_start": C("Here is nineteen eighty-two"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 760 860 L 1500 860", "color": "ink", "width": 4, "start": C("Let me draw the checks")},
        {"d": "M 790 860 L 790 720 L 870 720 L 870 860", "color": "muted", "width": 4, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is nineteen eighty-two"), "label": lbl("1982", 830, 700, 18, "muted")},
        {"d": "M 930 860 L 930 570 L 1010 570 L 1010 860", "color": "accent2", "width": 4, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("A high point"), "label": lbl("2015", 970, 550, 18, "accent2")},
        {"d": "M 1070 860 L 1070 717 L 1150 717 L 1150 860", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("A cut in"), "label": lbl("2016", 1110, 697, 18, "risk")},
        {"d": "M 1210 860 L 1210 400 L 1290 400 L 1290 860", "color": "accent", "width": 4, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("A record"), "label": lbl("2022", 1250, 380, 18, "accent")},
        {"d": "M 1350 860 L 1350 692 L 1430 692 L 1430 860", "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("And today"), "label": lbl("2026", 1390, 672, 18, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("a roller coaster", 0.1), "dur": 1.4, "target": [1250, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["pfd"])
kinetic("s11_t1", "m1_transition", [("Why does the check move so much?", 60, "why the check moves", None, False),
                                    ("…follow it to the vault", 66, "where the money is kept", "gold", False)])

# ====================================================================== PART 2: the fund
card("s12_c2", "m2_card", "The Fund", "Oil money, locked away")
stage("s13_oil", "m2_oil", {
    "zones": [Z("tundra")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 540, "zoom": 1.0}, {"at": C("Later, a state law"), "x": 1300, "y": 540, "zoom": 1.0, "dur": 1.6}], "drift": 3,
    "items": [it("letters", x=1000, y=110, text="1976: A CONSTITUTIONAL AMENDMENT", at=0.3, size=50, color="gold"),
              it("sign", x=800, y=250, text="≥ 25% OF MINERAL ROYALTIES → THE FUND", at=C("At least twenty-five"), color="#FFE0B2", size=30),
              it("sign", x=1500, y=350, text="NEWER LEASES: 50%", at=C("Later, a state law"), color="#BBDEFB", size=34),
              it("barrel", x=[[0, 300], [8, 2200]], at=0.3, scale=0.6)]},
    sources=["law"])
stage("s14_rooms", "m2_rooms", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("At the end of June"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("sign", x=700, y=220, text="ROOM 1: PRINCIPAL — LOCKED", at=C("The principal is locked"), color="#BBDEFB", size=32),
              it("sign", x=1300, y=220, text="ROOM 2: EARNINGS RESERVE — SPENDABLE", at=C("go into a second account"), color="#FFE0B2", size=30),
              it("letters", x=1000, y=110, text="TWO ROOMS", at=0.3, size=60, color="gold"),
              it("sign", x=1300, y=340, text="≈ $10.6BN REALIZED + $4BN FOR NEXT YEAR", at=C("At the end of June"), color="#C8E6C9", size=28)]},
    sources=["apfc"])
stage("s15_size", "m2_size", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In the last fiscal year"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=220, at=0.3, prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "it was worth about"}, 91.9]], text="PERMANENT FUND, JUNE 30, 2026 (APFC)", scale=1.3),
              it("sign", x=700, y=420, text="LOCKED PRINCIPAL ≈ $59.4BN", at=C("fifty-nine"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=420, text="FY26: +12.42% · DRAW $3.8BN", at=C("In the last fiscal year"), color="#C8E6C9", size=30)]},
    sources=["apfc"])
stage("s16_invest", "m2_invest", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="NO LONGER MAINLY AN OIL FUND", at=0.3, size=52, color="gold"),
              it("sign", x=750, y=270, text="ROYALTIES LAST YEAR: ≈ $535M", at=C("Royalties added"), color="#FFE0B2", size=32),
              it("sign", x=1350, y=370, text="DECADES OF INVESTING WORLDWIDE", at=C("Most of its value"), color="#BBDEFB", size=32)]},
    sources=["apfc"])
add("p17_vault", "m2_draw", "engine_draw", {
    "title": "The two-room vault", "board": BOARD, "draw_start": C("Here is the pipeline"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 420 L 720 420 L 720 480", "color": "muted", "width": 10, "start": C("Here is the pipeline"), "label": lbl("OIL ROYALTIES", 640, 400, 20, "muted")},
        {"d": rect(620, 480, 240, 200), "color": "accent2", "width": 6, "kind": "box", "start": C("the locked room"), "label": lbl("PRINCIPAL (LOCKED)", 740, 588, 18, "accent2")},
        {"d": rect(960, 480, 240, 200), "color": "accent", "width": 6, "kind": "box", "start": C("the second room"), "label": lbl("EARNINGS RESERVE", 1080, 588, 18, "accent")},
        {"d": arrow((865, 520), (955, 520)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("The investments grow"), "label": lbl("PROFITS", 910, 500, 16, "accent3")},
        {"d": arrow((1205, 560), (1330, 470)) + " " + arrow((1205, 620), (1330, 720)), "color": "ink", "width": 5, "kind": "arrow", "start": C("the state takes its draw"), "label": lbl("DIVIDEND · BUDGET", 1350, 600, 18, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("and pays the dividend", 0.1), "dur": 1.4, "target": [1080, 580]}],
    "scale": 0.86, "floor": 1040}, sources=["apfc", "law"])
kinetic("s18_t2", "m2_transition", [("The dividend had its own formula…", 60, "its own formula", None, False),
                                    ("…then the state ran short", 64, "ran short of money", "gold", False)])

# ====================================================================== PART 3: the cut
card("s19_c3", "m3_card", "The Cut", "2016 to 2018")
stage("s20_veto", "m3_veto", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The check\n    that year") if False else C("The check"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="2016: OIL PRICES COLLAPSE", at=0.3, size=52, color="gold"),
              it("sign", x=800, y=250, text="DIVIDEND MONEY CUT ≈ IN HALF (VETO)", at=C("cut the money"), color="#FFCDD2", size=32),
              it("bigcheck", x=1450, y=450, at=C("The check"), scale=0.55, amount="$1,022", date="2016")]},
    sources=["court"])
stage("s21_court", "m3_court", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1100, y=150, text="ALASKA SUPREME COURT, 2017", at=0.3, size=50, color="gold"),
              it("sign", x=1150, y=300, text="'MUST COMPETE FOR ANNUAL LEGISLATIVE FUNDING'", at=C("Its words were clear"), color="#FFE0B2", size=30),
              it("gavel", x=1650, y=F - 20, hits=[C("disagreed")], at=0.2)]},
    sources=["court"])
stage("s22_pomv", "m3_pomv", {
    "zones": [Z("parliament", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("That single draw"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="2018: THE 5% DRAW (SB 26)", at=0.3, size=52, color="gold"),
              it("sign", x=1000, y=250, text="5% OF THE AVERAGE VALUE OF PAST YEARS", at=C("Each year, the state may draw"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=360, text="ONE DRAW · TWO USES", at=C("That single draw"), color="#FFE0B2", size=38)]},
    sources=["law"])
stage("s23_budget", "m3_budget", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "PERMANENT FUND", "value": 57.7, "color": "#1E88E5", "at": C("the Permanent Fund supplied"), "display": "≈ 58%"},
                     {"label": "OIL", "value": 30.1, "color": "#424242", "at": C("Oil supplied"), "display": "≈ 30%"}],
                    at=0.2, max=70, title="SHARE OF STATE GENERAL REVENUE, FY2025 (OUR CALC.)", x=300, w=900),
              it("letters", x=1560, y=380, text="THE NEW PAYCHECK", at=C("has replaced oil"), size=44, color="gold")]},
    sources=["rev"])
add("p24_pie", "m3_draw", "engine_draw", {
    "title": "One draw, two hungry sides", "board": BOARD, "draw_start": C("Here is the yearly draw"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 1270 560 m -150 0 a 150 150 0 1 0 300 0 a 150 150 0 1 0 -300 0", "color": "accent", "width": 6, "kind": "stroke", "start": C("Here is the yearly draw"), "label": lbl("THE DRAW", 1270, 568, 24, "accent")},
        {"d": rect(860, 500, 180, 110), "color": "accent3", "width": 5, "kind": "box", "start": C("the dividend checks"), "label": lbl("DIVIDENDS", 950, 562, 20, "accent3")},
        {"d": rect(1500, 500, 200, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("schools, roads"), "label": lbl("SCHOOLS · ROADS", 1600, 562, 18, "accent2")},
        {"d": arrow((1115, 560), (1045, 560)) + " " + arrow((1425, 560), (1495, 560)), "color": "ink", "width": 5, "kind": "arrow", "start": C("Every dollar")},
    ],
    "actions": [{"kind": "point", "at": C("cannot go to the other", 0.1), "dur": 1.4, "target": [1270, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["law", "court"])
kinetic("s25_t3", "m3_transition", [("The same fight…", 72, "Which is exactly", None, False),
                                    ("…again in 2026", 72, "played out again", "gold", False)])

# ====================================================================== PART 4: the 2026 check
card("s26_c4", "m4_card", "The 2026 Check", "Formula versus vote")
stage("s27_formula", "m4_formula", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The legislature chose"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("docs", x=700, y=560, at=0.3, text="GOVERNOR'S FY27 BUDGET", scale=0.7, stamp="$3,650", stampAt=C("about three thousand")),
              it("letters", x=1250, y=150, text="'FULL STATUTORY DIVIDEND'", at=C("proposed a full dividend"), size=50, color="gold"),
              it("sign", x=1350, y=320, text="THE LEGISLATURE: MUCH SMALLER", at=C("The legislature chose"), color="#FFCDD2", size=34)]},
    sources=["court"])
stage("s28_budget", "m4_budget", {
    "zones": [Z("parliament", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It did"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="HB 263 (FY2027 BUDGET)", at=0.3, size=50, color="gold"),
              it("sign", x=750, y=250, text="$1,000 DIVIDEND · ≈ $674M (EST.)", at=C("paid a dividend of"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=350, text="+$200 ENERGY RELIEF IF REVENUE > $6.3BN", at=C("It added"), color="#FFE0B2", size=28),
              it("bigcheck", x=1600, y=560, at=C("It did"), scale=0.45, amount="$1,200", date="2026")]},
    sources=["law", "pfd"])
stage("s29_draw2", "m4_draw2", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("counter", x=1000, y=240, at=0.3, prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "earnings reserve"}, 4.0]], text="DRAWN FROM THE EARNINGS RESERVE (HB 263)", scale=1.2),
              it("sign", x=1000, y=440, text="MOSTLY FOR GOVERNMENT, NOT CHECKS (OUR CALC.)", at=C("By our calculation"), color="#FFE0B2", size=30)]},
    sources=["law"])
stage("s30_skip", "m4_skip", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("This year"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=120, text="INFLATION-PROOFING", at=0.3, size=56, color="gold"),
              it("sign", x=1250, y=280, text="$1.5BN TRANSFER: NOT MADE (APFC)", at=C("This year"), color="#FFCDD2", size=34)]},
    sources=["apfc"])
add("p31_ghost", "m4_draw", "engine_draw", {
    "title": "The ghost check", "board": BOARD, "draw_start": C("Here is the real check"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(700, 600, 360, 150), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is the real check"), "label": lbl("PAID: $1,200", 880, 683, 28, "accent3")},
        {"d": rect(640, 360, 480, 190), "color": "muted", "width": 4, "kind": "box", "start": C("Above it, faint"), "label": lbl("FORMULA: $3,650", 880, 463, 30, "muted")},
        {"d": "M 1160 455 L 1160 675", "color": "risk", "width": 5, "start": C("The gap between them"), "label": lbl("≈ $2,450 KEPT", 1270, 570, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("to run its\n    government") if False else C("run its"), "dur": 1.4, "target": [1160, 570]}],
    "scale": 0.86, "floor": 1040}, sources=["court", "pfd"])
kinetic("s32_t4", "m4_transition", [("What does a yearly check do?", 62, "So what does", None, False),
                                    ("…economists have studied it", 62, "studied that question", "gold", False)])

# ====================================================================== PART 5: what the money does
card("s33_c5", "m5_card", "What the Money Does", "The research")
stage("s34_jobs", "m5_jobs", {
    "zones": [Z("warehouse")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Part-time work"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="DOES FREE MONEY STOP WORK?", at=0.3, size=54, color="gold"),
              it("sign", x=800, y=270, text="EMPLOYMENT: NO EFFECT (JONES & MARINESCU)", at=C("They found no effect"), color="#C8E6C9", size=30),
              it("sign", x=1450, y=370, text="PART-TIME WORK: +1.8 POINTS", at=C("Part-time work"), color="#BBDEFB", size=32),
              *crowd([600, 1700], "walk", at=0.4, scale=0.7)]},
    sources=["research"])
stage("s35_spend", "m5_spend", {
    "zones": [Z("supermarket")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And\n    one study") if False else C("one study of crime"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="WHAT THE RESEARCH FOUND", at=0.3, size=50, color="gold"),
              it("sign", x=700, y=250, text="≈ 25% SPENT WITHIN 3 MONTHS (KUENG)", at=C("about a quarter"), color="#BBDEFB", size=28),
              it("sign", x=1300, y=250, text="BIRTH WEIGHT: +17.7 G PER $1,000", at=C("birth weights"), color="#C8E6C9", size=28),
              it("sign", x=1000, y=360, text="CRIME: SUBSTANCE +14% (DAY AFTER) · PROPERTY −8%", at=C("one study of crime"), color="#FFE0B2", size=28)]},
    sources=["research"])
add("p36_arrows", "m5_draw", "engine_draw", {
    "title": "What the research says (simplified)", "board": BOARD, "draw_start": C("Here is the check arriving"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(760, 520, 220, 100), "color": "accent", "width": 6, "kind": "box", "start": C("Here is the check arriving"), "label": lbl("THE CHECK", 870, 578, 24, "accent")},
        {"d": arrow((985, 540), (1240, 420)), "color": "accent2", "width": 5, "kind": "arrow", "start": C("to jobs"), "label": lbl("JOBS: ≈ NO CHANGE", 1340, 410, 20, "accent2")},
        {"d": arrow((985, 570), (1240, 570)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("to spending"), "label": lbl("SPENDING: ≈ 1/4 IN 3 MONTHS", 1360, 575, 18, "accent3")},
        {"d": arrow((985, 600), (1240, 720)), "color": "muted", "width": 4, "kind": "arrow", "start": C("a few small arrows"), "label": lbl("HEALTH · SAFETY: SMALL", 1340, 735, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("without walking away", 0.1), "dur": 1.4, "target": [1240, 570]}],
    "scale": 0.86, "floor": 1040}, sources=["research"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("tundra", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("But once the state"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=120, text="OIL MONEY FOR EVERYONE, LOCKED AWAY", at=0.3, size=50, color="gold"),
              it("sign", x=1000, y=260, text="NOT SHRINKING BY ACCIDENT · SHRINKING BY VOTE", at=C("The check is not shrinking"), color="#FFCDD2", size=32)]},
    sources=["court", "apfc"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_alaska_storyboard.py; edit the generator, not this file.\n"
           "# Episode 48 storyboard (Alaska dividend): one visual language per part; tones from visual_direction.yaml.\n")
