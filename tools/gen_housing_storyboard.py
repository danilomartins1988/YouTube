"""Generates projects/why-american-homes-became-so-expensive/deliverables/documentary/storyboard.yaml (Episode 31,
US batch #03: Why American Homes Became So Expensive).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: a suburban street (new `suburb` set) and a house whose for-sale sign keeps repricing (new `home` item).
- Part 1 (the price tag): the suburb by day + full-screen charts of the price-to-income ratio.
- Part 2 (the rate shock): a mortgage-rate screen (tradescreen), a bank office, and the suburb at night with padlocked doors.
- Part 3 (the missing homes): a construction site with timber frames that never finish + completions chart.
- Part 4 (the rules on the land): city hall and a top-down zoning map (new `zonemap` item).
- Part 5 (locked out): an evidence board and the suburb at night with buyers outside.
No real people, logos or brands. Lint: tools/lint_storyboard.py.
Run: python tools/gen_housing_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-american-homes-became-so-expensive/deliverables/documentary/storyboard.yaml"
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


def home(x=960, **kw):
    return it("home", x=x, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("suburb")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("counter", x=1000, y=170, at=0.05, prefix="$", suffix="", steps=[[0.05, 0], [1.6, 120800]], text="INCOME NEEDED FOR THE TYPICAL HOME, END 2025 (HARVARD JCHS)", scale=1.3),
              home(1050, at=0.3, scale=0.85, sign="$$$", signX=-360, color="#E3F2FD", roof="#5C6BC0")]},
    sources=["jchs"])
stage("s02_twist", "h_twist", {
    "zones": [Z("hills")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The same home simply"), "x": 1100, "y": 520, "zoom": 1.08, "dur": 1.5}], "drift": 1,
    "items": [home(900, at=0.2, scale=0.8, sign="$68,700", pages=[[0, "$68,700"], [C("a whole extra salary"), "$120,800"]], signHead="INCOME NEEDED"),
              it("letters", x=1350, y=330, text="5 YEARS EARLIER", at=0.4, size=60, color="white"),
              it("letters", x=1350, y=430, text="SAME HOUSE", at=C("The houses did not get bigger"), size=56, color="gold"),
              it("letters", x=1350, y=530, text="+1 WHOLE SALARY", at=C("a whole extra salary"), size=64, color="risk")]},
    sources=["jchs"])
stage("s03_question", "h_question", {
    "zones": [Z("suburb", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [home(1000, at=0.1, scale=0.85, night=True, lockAt=C("slip out of reach")),
              *crowd([360, 450, 1640], "worry", at=0.3, scale=0.7),
              it("letters", x=1000, y=150, text="OUT OF REACH?", at=0.4, size=84, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE PRICE", at=0.3, color="#BBDEFB", size=44),
              it("sign", x=750, y=380, text="2 · THE LOAN", at=C("The price, the loan"), color="#FFCDD2", size=44),
              it("sign", x=1170, y=380, text="3 · MISSING HOMES", at=C("the homes that were"), color="#FFE0B2", size=44),
              it("sign", x=1590, y=380, text="4 · THE RULES", at=C("and the rules"), color="#C8E6C9", size=44),
              it("letters", x=960, y=700, text="FOUR FORCES", at=C("the four forces"), size=72, color="gold")]})

# ====================================================================== PART 1: the price tag (suburb by day + charts)
card("s05_c1", "m1_card", "The Price Tag", "Years of income for one home")
stage("s06_ratio", "m1_ratio", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "1990s AVG", "value": 3.2, "color": "#90A4AE", "at": C("In the nineteen nineties"), "display": "3.2×"},
                     {"label": "2019", "value": 4.1, "color": "#FFB74D", "at": C("In twenty nineteen"), "display": "4.1×"},
                     {"label": "2022 PEAK", "value": 5.0, "color": "#B71C1C", "at": C("just below the all-time high"), "display": "5.0×"},
                     {"label": "2025", "value": 4.7, "color": "#E53935", "at": C("In twenty twenty-five"), "display": "4.7×"}],
                    at=0.2, max=5.6, title="HOME PRICE ÷ HOUSEHOLD INCOME (HARVARD JCHS)", x=360, w=1200)]},
    sources=["jchs"])
stage("s07_jump", "m1_jump", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Wages rose too"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [home(800, at=0.2, scale=0.75, sign="PRICE", pages=[[0, "PRICE"], [1.2, "+54%"]], color="#FCE4EC", roof="#26A69A"),
              it("stack", x=1500, h=[[0, 60], [{"cue": "Wages rose too", "offset": 1}, 140]], at=C("Wages rose too"), text="WAGES", color="#23995A"),
              it("stack", x=1750, h=[[0, 60], [{"cue": "home prices rose", "offset": 1}, 380]], at=0.4, text="HOME PRICES", color="#E53935"),
              it("letters", x=1620, y=180, text="+54% SINCE 2020", at=C("nationwide"), size=56, color="risk")]},
    sources=["jchs_pr"])
stage("s08_new", "m1_new", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In the summer of twenty twenty-six"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [home(1000, at=0.2, scale=0.8, sign="$168,800", pages=[[0, "$168,800"], [C("In the summer of twenty twenty-six"), "$393,300"]], signHead="NEW HOME", color="#F1F8E9", roof="#8D6E63"),
              it("letters", x=1550, y=330, text="2000 → 2026", at=0.6, size=60, color="white"),
              it("letters", x=1550, y=430, text="MORE THAN DOUBLED", at=C("but the price more than doubled"), size=50, color="gold"),
              it("letters", x=1550, y=510, text="(not adjusted for inflation)", at=C("These are dollars of the day"), size=30, color="white")]},
    sources=["mspus"])
add("p09_blocks", "m1_draw", "engine_draw", {
    "title": "Years of income per home", "board": BOARD, "draw_start": C("Here is one year"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("Here is one year")},
        {"d": rect(600, 760, 180, 100), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is one year", 0.4), "label": lbl("1 YEAR", 690, 818, 22, "accent3")},
        {"d": "M 900 860 L 900 560 L 1080 560 L 1080 860 M 900 760 L 1080 760 M 900 660 L 1080 660", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.25, "kind": "bar", "start": C("In the nineties"), "label": lbl("1990s ≈ 3", 990, 540, 24, "accent2")},
        {"d": "M 1140 860 L 1140 460 L 1320 460 L 1320 860 M 1140 760 L 1320 760 M 1140 660 L 1320 660 M 1140 560 L 1320 560", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.25, "kind": "bar", "start": C("By twenty nineteen"), "label": lbl("2019 ≈ 4", 1230, 440, 24, "accent")},
        {"d": "M 1380 860 L 1380 390 L 1460 390 L 1460 860", "color": "risk", "width": 7, "fill": "risk", "fillOpacity": 0.25, "kind": "bar", "start": C("Today, almost five"), "label": lbl("TODAY ≈ 5", 1420, 370, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Every extra block", 0.3), "dur": 1.4, "target": [1420, 420]}],
    "scale": 0.86, "floor": 1040}, sources=["jchs"])
kinetic("s10_t1", "m1_transition", [("Nobody pays cash", 60, "almost nobody pays", None, True), ("…the price of borrowing", 58, "the price of borrowing", "gold", False)])

# ====================================================================== PART 2: the rate shock (rate screen + bank office + night suburb)
card("s11_c2", "m2_card", "The Rate Shock", "Mortgage rates and the lock-in")
stage("s12_rates", "m2_rates", {
    "zones": [Z("office")], "worldW": 2000,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("Then inflation arrived"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("tradescreen", x=1000, y=470, at=0.2, scale=1.15, text="30-YR MORTGAGE RATE (FREDDIE MAC)", decimals=2, max=8, min=0, hot=6.5, lamp=False, suffix="%",
                 price=[[0, 3.1], [{"cue": "fell to"}, 2.65], [{"cue": "Then inflation arrived"}, 3.2], [{"cue": "and interest rates"}, 6.9], [{"cue": "In early November"}, 7.18]])]},
    sources=["pmms"])
stage("s13_payment", "m2_payment", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "END 2020", "value": 1240, "color": "#90A4AE", "at": C("At the end of twenty twenty"), "display": "$1,240"},
                     {"label": "NOW (MORTGAGE)", "value": 2420, "color": "#E53935", "at": C("reached"), "display": "$2,420"},
                     {"label": "+ INSURANCE, TAXES", "value": 3120, "color": "#B71C1C", "at": C("Add insurance"), "display": "$3,120"}],
                    at=0.2, max=3500, title="MONTHLY COST OF THE MEDIAN-PRICED HOME (HARVARD JCHS)", x=420, w=1080)]},
    sources=["jchs"])
stage("s14_lockin", "m2_lockin", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So many owners"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.5}], "drift": 2,
    "items": [home(700, at=0.2, scale=0.65, night=True, text="LOAN < 4%", textc="#FFE082", lockAt=C("simply stay put")),
              home(1300, at=0.3, scale=0.65, night=True, color="#E3F2FD", roof="#5C6BC0", text="LOAN < 4%", textc="#FFE082", lockAt=C("simply stay put", 0.4)),
              it("letters", x=1000, y=150, text="HALF OF ALL MORTGAGES BELOW 4%", at=C("Half of all outstanding"), size=50, color="gold"),
              it("letters", x=1500, y=280, text="NEW LOAN ≈ 7%", at=C("take a new one"), size=54, color="risk")]},
    sources=["jchs"])
stage("s15_frozen", "m2_frozen", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("counter", x=520, y=300, at=0.3, suffix="%", decimals=1, steps=[[0, 0], [{"cue": "fell to a record low", "offset": 1}, 11.2]], text="AMERICANS WHO MOVED IN A YEAR, 2024 (RECORD LOW)"),
              chart([{"label": "2021", "value": 6.1, "color": "#90A4AE", "at": C("about two thirds"), "display": "6.1M"},
                     {"label": "2025", "value": 4.1, "color": "#E53935", "at": C("existing home sales"), "display": "4.1M"}],
                    at=0.2, max=7, dark=True, title="EXISTING HOME SALES (HARVARD JCHS)", x=980, y=240, w=760, h=520)]},
    sources=["jchs"])
add("p16_lock", "m2_draw", "engine_draw", {
    "title": "The rate lock", "board": BOARD, "draw_start": C("Here is an owner"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 400, 240, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is an owner"), "label": lbl("OWNER · 3%", 680, 468, 24, "accent3")},
        {"d": rect(1200, 400, 240, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the house"), "label": lbl("NEXT HOUSE", 1320, 468, 24, "accent2")},
        {"d": arrow((810, 460), (1190, 460), 0.0), "color": "ink", "width": 4, "start": C("Between them")},
        {"d": rect(900, 420, 200, 80), "color": "risk", "width": 7, "kind": "box", "start": C("a new loan at seven"), "label": lbl("NEW LOAN 7%", 1000, 468, 22, "risk")},
        {"d": "M 600 600 L 760 600 M 620 580 L 620 640 L 740 640 L 740 580", "color": "accent", "width": 6, "start": C("So the owner stays"), "label": lbl("STAYS", 680, 690, 24, "accent")},
        {"d": "M 1220 640 L 1420 640", "color": "risk", "width": 6, "start": C("see fewer homes"), "label": lbl("FEWER LISTINGS", 1320, 690, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("a new loan at seven", 0.3), "dur": 1.4, "target": [1000, 460]}],
    "scale": 0.86, "floor": 1040}, sources=["jchs"])
kinetic("s17_t2", "m2_transition", [("Rates explain the last few years", 54, "Rates explain", None, True), ("…the homes never built", 64, "the homes that America", "gold", False)])

# ====================================================================== PART 3: the missing homes (construction site + chart)
card("s18_c3", "m3_card", "The Missing Homes", "A decade of too little building")
stage("s19_crash", "m3_crash", {
    "zones": [Z("site")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By our calculation"), "x": 1400, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("crane", x=900, at=0.2, progress=[[0, 0.6], [6, 0.2]], scale=0.8, text="2008: BUST"),
              home(1250, at=0.3, scale=0.6, frameAt=999),
              home(1750, at=0.4, scale=0.6, frameAt=999),
              it("letters", x=1650, y=300, text="CONSTRUCTION COLLAPSED", at=C("construction collapsed"), size=54, color="risk"),
              it("letters", x=1650, y=390, text="2011: 585,000 · LOWEST SINCE 1968", at=C("In twenty eleven alone"), size=40, color="white")]},
    sources=["completions"])
stage("s20_decades", "m3_gap", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2000–2009", "value": 15.6, "color": "#2F6FD1", "at": 0.5, "display": "15.6M"},
                     {"label": "2010–2019", "value": 9.2, "color": "#E53935", "at": 1.2, "display": "9.2M"}],
                    at=0.2, max=18, title="NEW HOMES COMPLETED (OUR SUM OF CENSUS DATA)", x=320, w=880),
              *crowd([1450, 1550, 1650, 1750], "walk", at=C("Millennials"), scale=0.55),
              it("letters", x=1600, y=300, text="MORE HOUSEHOLDS", at=C("the number of households"), size=46, color="gold")]},
    sources=["completions"])
stage("s21_shortage", "m3_shortage", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.1}, {"at": C("Either way"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 600, "y": 360, "text": "1.2M", "sub": "low estimate", "at": 0.3, "w": 420, "color": "#C8E6C9", "size": 60},
                {"x": 1600, "y": 360, "text": "5.5M", "sub": "high estimate", "at": C("range"), "w": 420, "color": "#FFCDD2", "size": 60},
                {"x": 1100, "y": 660, "text": "≈ 3.8M", "sub": "Up for Growth estimate", "at": C("Up for Growth"), "w": 420, "color": "#FFF59D", "size": 56}],
              links=[[0, 2, C("Up for Growth", 0.4)], [1, 2, C("Up for Growth", 0.6)]],
              stamp="MILLIONS MISSING", stampAt=C("Either way")),
              it("letters", x=1100, y=150, text="SHORTAGE ESTIMATES (CITED BY HARVARD JCHS)", at=0.3, size=40, color="white")]},
    sources=["jchs", "upforgrowth"])
stage("s22_recovery", "m3_recovery", {
    "zones": [Z("site")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But filling a hole"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [home(700, at=0.2, scale=0.6, frameAt=0.4, doneAt=3.5, color="#FFFDE7", roof="#EF6C00"),
              home(1300, at=0.3, scale=0.6, frameAt=1.4, doneAt=4.5),
              it("crane", x=1900, at=0.3, progress=[[0, 0.3], [12, 0.8]], scale=0.75, text="BUILDING AGAIN"),
              it("letters", x=1200, y=330, text="≈ 1.5 MILLION COMPLETED IN 2025", at=C("Completions came back"), size=48, color="gold")]},
    sources=["completions"])
add("p23_gap", "m3_draw", "engine_draw", {
    "title": "The gap (schematic)", "board": BOARD, "draw_start": C("Here is the line of new households"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860 M 560 860 L 560 380", "color": "ink", "width": 4, "start": C("Here is the line of new households")},
        {"d": "M 580 700 L 1440 520", "color": "accent2", "width": 7, "start": C("rising steadily"), "label": lbl("NEW HOUSEHOLDS", 1300, 500, 22, "accent2")},
        {"d": "M 580 705 L 900 640", "color": "accent3", "width": 7, "start": C("Here is the line of new homes"), "label": lbl("NEW HOMES", 760, 620, 22, "accent3")},
        {"d": "M 900 640 L 1000 780 L 1440 720", "color": "accent3", "width": 7, "start": C("the homes line dropped")},
        {"d": "M 1100 600 L 1100 760 M 1250 570 L 1250 740 M 1400 540 L 1400 725", "color": "risk", "width": 5, "start": C("is the shortage"), "label": lbl("SHORTAGE", 1250, 820, 26, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Higher prices", 0.1), "dur": 1.4, "target": [1250, 660]}],
    "scale": 0.86, "floor": 1040}, sources=["completions", "jchs"])
kinetic("s24_t3", "m3_transition", [("Why not just build more?", 66, "why not just build", None, False), ("…it's written in the rules", 60, "written in the rules", "gold", False)])

# ====================================================================== PART 4: the rules on the land (city hall + zoning map)
card("s25_c4", "m4_card", "The Rules on the Land", "Zoning and regulation")
stage("s26_zoning", "m4_zoning", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Researchers at the University"), "x": 1250, "y": 500, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("docs", x=820, y=560, at=0.3, text="ZONING CODE", scale=0.7, stamp="ONE HOUSE PER LOT", stampAt=C("one house per lot")),
              it("zonemap", x=1450, y=440, at=C("Researchers at the University"), fillAt=C("They found that"), fillDur=3.0, share=0.78, cols=10, rows=6, cell=62,
                 title="GREATER LOS ANGELES (UC BERKELEY)", label="SINGLE-FAMILY ONLY ≈ 78%", label2="OTHER HOMES")]},
    sources=["berkeley"])
stage("s27_meaning", "m4_meaning", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Even where demand"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.5}], "drift": 2,
    "items": [home(1000, at=0.2, scale=0.75, color="#FFF3E0"),
              it("sign", x=500, y=260, text="NO APARTMENTS", at=C("no apartments"), color="#FFCDD2", size=40),
              it("sign", x=1500, y=260, text="NO TOWNHOUSES", at=C("no townhouses"), color="#FFCDD2", size=40),
              it("sign", x=1000, y=130, text="NO DUPLEX", at=C("no small duplex"), color="#FFCDD2", size=40)]},
    sources=["berkeley"])
stage("s28_regulation", "m4_regulation", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("estimates that regulation"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("docs", x=650, y=560, at=0.2, text="PERMITS · FEES · CODES", scale=0.75, stamp="DELAYED", stampAt=C("and delays")),
              it("counter", x=1450, y=260, at=C("estimates that regulation"), suffix="%", decimals=1, steps=[[0, 0], [{"cue": "of the price of", "offset": 0}, 26.4]], text="REGULATION, SHARE OF A NEW HOME'S PRICE (NAHB, BUILDERS' GROUP)"),
              it("letters", x=1450, y=440, text="≈ $132,000 PER HOME", at=C("On an average new home"), size=46, color="gold")]},
    sources=["nahb"])
stage("s29_debate", "m4_debate", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("balance", x=1000, at=0.2, left="SAFETY", lsub="environment", right="COST", rsub="delay", tilt=0, to=10, balanceAt=C("But the direction")),
              it("letters", x=1000, y=150, text="INDUSTRY ESTIMATE", at=0.4, size=50, color="white"),
              it("clock", x=1750, y=330, at=C("slower and more expensive"), period=0.6, text="SLOWER")]},
    sources=["nahb"])
add("p30_block", "m4_draw", "engine_draw", {
    "title": "One block, two rules (illustration)", "board": BOARD, "draw_start": C("Here are eight lots"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": " ".join(rect(560 + 110 * k, 380, 90, 90) for k in range(4)) + " " + " ".join(rect(560 + 110 * k, 500, 90, 90) for k in range(4)), "color": "ink", "width": 4, "start": C("Here are eight lots")},
        {"d": " ".join(f"M {585 + 110 * k} {r + 60} L {585 + 110 * k} {r + 35} L {605 + 110 * k} {r + 20} L {625 + 110 * k} {r + 35} L {625 + 110 * k} {r + 60}" for k in range(4) for r in (380, 500)), "color": "accent", "width": 4, "start": C("each lot gets one house"), "label": lbl("8 HOMES", 755, 650, 30, "accent")},
        {"d": " ".join(rect(1060 + 110 * k, 380, 90, 90) for k in range(4)) + " " + " ".join(rect(1060 + 110 * k, 500, 90, 90) for k in range(4)), "color": "ink", "width": 4, "start": C("Now allow small apartment")},
        {"d": " ".join(rect(1075 + 110 * k, r + 12, 60, 66) + f" M {1075 + 110 * k} {r + 45} L {1135 + 110 * k} {r + 45} M {1105 + 110 * k} {r + 12} L {1105 + 110 * k} {r + 78}" for k in range(4) for r in (380, 500)), "color": "accent2", "width": 4, "start": C("Four homes on each"), "label": lbl("32 HOMES", 1255, 650, 30, "accent2")},
        {"d": "M 560 720 L 1440 720", "color": "risk", "width": 5, "start": C("The land did not change"), "label": lbl("SAME LAND · DIFFERENT RULE", 1000, 770, 26, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Thirty-two homes", 0.2), "dur": 1.4, "target": [1255, 480]}],
    "scale": 0.86, "floor": 1040}, sources=["berkeley"])
kinetic("s31_t4", "m4_transition", [("Prices · loans · missing homes · rules", 48, "High prices", None, True), ("Someone ends up locked outside", 60, "locked", "risk", False)])

# ====================================================================== PART 5: locked out (evidence board + night suburb)
card("s32_c5", "m5_card", "Locked Out", "First-time buyers")
stage("s33_age", "m5_age", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("First-time buyers made up"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("person", x=700, pose="stand", at=0.2, scale=0.85, hair=5, skin=2),
              it("counter", x=1000, y=230, at=0.3, prefix="AGE ", suffix="", steps=[[0, 29], [{"cue": "years old", "offset": 0}, 40]], text="TYPICAL FIRST-TIME BUYER (NAR, RECORD HIGH)"),
              home(1650, at=0.3, scale=0.65, sign="22%", signHead="FIRST-TIMERS", signX=-330),
              it("letters", x=1650, y=130, text="≈ HALF THE PRE-2008 NORM (40%)", at=C("about half the historical"), size=38, color="gold")]},
    sources=["nar"])
stage("s34_listings", "m5_listings", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "MARCH 2019", "value": 49, "color": "#23995A", "at": 0.5, "display": "49%"},
                     {"label": "MARCH 2026", "value": 23, "color": "#E53935", "at": C("By March twenty twenty-six"), "display": "23%"}],
                    at=0.2, max=55, dark=True, title="LISTINGS AFFORDABLE ON $75,000 OR LESS (HARVARD JCHS)", x=520, w=880)]},
    sources=["jchs"])
stage("s35_metros", "m5_metros", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 480, "zoom": 1.05}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 650, "y": 420, "text": "31 METROS", "sub": "need > $100k income (2020)", "at": 0.3, "w": 420, "color": "#C8E6C9", "size": 54},
                {"x": 1550, "y": 420, "text": "169 METROS", "sub": "need > $100k income (2025)", "at": C("In twenty twenty-five"), "w": 440, "color": "#FFCDD2", "size": 54}],
              links=[[0, 1, C("In twenty twenty-five", 0.4)]], stamp="NOT JUST THE COASTS", stampAt=C("and sixty-nine"))]},
    sources=["jchs"])
add("p36_four", "m5_draw", "engine_draw", {
    "title": "Four forces, one door", "board": BOARD, "draw_start": C("The price, almost five"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(1180, 380, 220, 420), "color": "ink", "width": 7, "kind": "box", "start": C("Let me put the four forces"), "label": lbl("DOOR", 1290, 360, 26, "ink")},
        {"d": arrow((600, 420), (1160, 470), 0.0), "color": "accent2", "width": 6, "start": C("The price, almost five"), "label": lbl("PRICE ≈ 5 YRS INCOME", 720, 400, 20, "accent2")},
        {"d": arrow((600, 530), (1160, 550), 0.0), "color": "risk", "width": 6, "start": C("The loan, at around seven"), "label": lbl("LOAN ≈ 7%", 700, 515, 20, "risk")},
        {"d": arrow((600, 640), (1160, 630), 0.0), "color": "accent", "width": 6, "start": C("The missing homes"), "label": lbl("MILLIONS MISSING", 710, 625, 20, "accent")},
        {"d": arrow((600, 750), (1160, 710), 0.0), "color": "accent3", "width": 6, "start": C("And the rules on the land"), "label": lbl("THE RULES", 690, 735, 20, "accent3")},
        {"d": "M 1460 820 L 1460 700 M 1440 720 L 1460 700 L 1480 720", "color": "ink", "width": 5, "start": C("the people still outside"), "label": lbl("FIRST-TIME BUYERS", 1460, 860, 20, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("pushes the door", 0.2), "dur": 1.4, "target": [1290, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["jchs", "pmms", "nar"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("suburb", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("For owners who bought early"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [home(1000, at=0.2, scale=0.8, night=True, sign="$$$", signX=-340),
              it("letters", x=1000, y=130, text="NOT ONE VILLAIN", at=C("Not because of one villain"), size=60, color="gold"),
              it("letters", x=560, y=250, text="EARLY OWNERS: A WINDFALL", at=C("For owners who bought early"), size=36, color="green"),
              it("letters", x=1440, y=250, text="EVERYONE ELSE: HIGHER PRICE TAG", at=C("For everyone else"), size=36, color="risk")]},
    sources=["completions", "jchs", "pmms"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_housing_storyboard.py; edit the generator, not this file.\n"
           "# Episode 31 storyboard (US housing costs): one visual language per part; tones from visual_direction.yaml.\n")
