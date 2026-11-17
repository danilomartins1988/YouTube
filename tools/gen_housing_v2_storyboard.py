"""Generates projects/why-americans-can-no-longer-afford-a-home/deliverables/documentary/storyboard.yaml
(Episode 58: Why Americans Can No Longer Afford a Home; supersedes Ep 31).

OWNER DIRECTION (as Ep 56): feel like an actual episode of a prime-time animated TV sitcom. Genre level only; everything
original. TV structure: cold open gag (a Saturday open house with a bidding war) -> channel intro (our "theme") -> show
TITLE CARD ("STARTER HOME") with a typed joke subtitle -> five acts, each opened by a BUMPER whose STARTER HOME keeps
shrinking (house -> shed -> doghouse -> birdhouse -> mailbox: the running gag) -> the basement -> end card -> button joke.
Recurring cast (fictional, the sitcom `toon` rig with new looks): MAYA (first-time buyer), REX (her dad, locked into a
cheap mortgage), DEEDEE (realtor). Bespoke day sets (CartoonStage/housing.tsx): openhouse, ratecoaster (track = Freddie Mac
weekly 30-year rate, supplied data), lockstreet, shrinker, emptylot, zoningboard, basement.
Signature animations: the open-house bidding war (s01), the rate rollercoaster (s11), the padlock street (s17), the
Shrink-O-Matic (s08), the zoning map turning yellow (s28), the empty lot that builds/stalls (s22).
Presenter boards: p09 (bars), p13 (income bars + gap), p24 (2 boxes + arrow), p30 (lots: 1, 2, 4 homes).
No logos; no real people; our calculations/estimates labelled; jokes never change a number.
Run: python tools/gen_housing_v2_storyboard.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

ROOT = Path(__file__).resolve().parents[1]
PROJ = ROOT / "projects/why-americans-can-no-longer-afford-a-home"
OUT = PROJ / "deliverables/documentary/storyboard.yaml"
PMMS = json.loads((PROJ / "pmms_weekly_sample.json").read_text())   # Freddie Mac PMMS weekly 30-yr, sampled (see sources.yaml)
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
LOCKS = ["< 4%"] * 5


def toon(x, at=0.0, **kw):
    if "xk" in kw:
        x = kw.pop("xk")
    return it("toon", x=x, at=at, **kw)


def MAYA(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.3)
    return toon(x, at, who="shopper", v=10, skin=2, hair=1, hairStyle=4, color="#26A69A", glasses=True, hat="", scarf="", **kw)


def REX(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.25)
    return toon(x, at, who="shopper", v=4, skin=0, hair=6, hairStyle=5, color="#5C6BC0", glasses=True, hat="", scarf="", **kw)


def DEE(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.3)
    return toon(x, at, who="shopper", v=3, skin=4, hair=3, hairStyle=3, color="#F06292", glasses=False, hat="", scarf="#FFC93C", **kw)


def EXTRA(v, x, at=0.0, **kw):
    kw.setdefault("scale", 1.15)
    return toon(x, at, who="shopper", v=v, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def chart(bars_, at=0.2, **kw):
    kw.setdefault("panel", True)
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


# ---- rate coaster geometry (mirrors housing.tsx ratecoaster defaults) so the camera can follow the car
F, GX0, GX1, Y0, Y1, RMIN, YS, BASE = 860, 200, 2600, 2019, 2027, 2, 88, 70
_P = [(GX0 + (y - Y0) / (Y1 - Y0) * (GX1 - GX0), F - BASE - (r - RMIN) * YS) for y, r in PMMS]
_S = [0.0]
for k in range(1, len(_P)):
    _S.append(_S[-1] + math.hypot(_P[k][0] - _P[k - 1][0], _P[k][1] - _P[k - 1][1]))


def u_at(year):
    """track progress (0..1) of the point nearest to `year`"""
    k = min(range(len(PMMS)), key=lambda q: abs(PMMS[q][0] - year))
    return round(_S[k] / _S[-1], 4)


def xy_at(year):
    k = min(range(len(PMMS)), key=lambda q: abs(PMMS[q][0] - year))
    return _P[k]


def bumper(id_, seg, num, act, title, caption, color, gag, gsign="STARTER HOME"):
    items = [it("minihome", x=1560, y=1010, type=gag, sign=gsign, scale=0.62, at=0.7),
             MAYA(xk=[[0.9, -250], [3.2, 1330]], at=0.9, y=1075, scale=0.8, face="love", pose="run",
                  faces=[[0, "love"], [3.2, "shock"]], poses=[[0, "run"], [3.2, "armsup"]], takes=[3.25]),
             DEE(xk=[[1.6, 2300], [3.0, 1800]], at=1.6, y=1075, scale=0.8, face="grin", pose="run", poses=[[0, "run"], [3.0, "wave"]]),
             it("placard", x=[[1.6, 2300], [3.0, 1800]], y=[[0, 820]], at=1.7, text="SOLD!", size=34, scale=0.8, color="#E53950", textColor="#FFFFFF")]
    stage(id_, seg, {**W1("bumper", num=num, act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "sitcom",
                     "min_seconds": 4.2, "items": items}, sfx=[{"kind": "hit", "at": 0.15, "gain": 0.3}, {"kind": "whoosh", "at": 0.05, "gain": 0.25}])


# ====================================================================== COLD OPEN (Saturday open house)
stage("s01_open", "co_open", {
    **W1("openhouse", houseX=1250, signX=560, crowd=1.0, queue=8, soldAt=C("in cash", 0.2)),
    "cam": cam((0, 1250, 380, 0.95), (C("Three bedrooms"), 1250, 430, 1.25, 1.6), (C("a lawn the size"), 1350, 600, 1.15, 1.4),
               (C("Half the town"), 1250, 420, 1.3, WHIP), (C("Someone just offered"), 1100, 470, 0.95, 1.2), (C("And Maya"), 700, 520, 1.25, WHIP),
               (C("just says"), 700, 470, 1.5, 1.0)), "drift": 3,
    "items": [it("toonwords", text="SATURDAY · OPEN HOUSE", x=1250, y=110, at=0.2, until=C("Three bedrooms", 0.6), size=60),
              sign("3 BED · 1 BATH", 1250, 160, C("Three bedrooms"), color="#FFF8E1", size=34, until=C("Half the town")),
              it("bubble", text="IT'S... COZY!", x=1650, y=380, at=C("a lawn the size"), until=C("Half the town"), tail=[1700, 600], size=32),
              DEE(1720, 0.3, hold="clipboard", pose="talk", face="grin", label="DEEDEE · REALTOR", labelUntil=C("Half the town"),
                  talk=[[C("Three bedrooms"), C("parking space", 0.4)]], faces=[[0, "grin"], [C("in cash"), "dollar"]], hops=[C("in cash", 0.3)]),
              it("paddles", raises=[[C("Someone just offered"), "OVER ASKING!"], [C("more than the asking"), "WAIVE INSPECTION"], [C("in cash"), "ALL CASH!"]],
                 x0=900, x1=1650, y=330, at=C("Someone just offered", -0.1), until=C("And Maya", -0.2)),
              MAYA([[0, 300], [C("And Maya", -0.6), 300], [C("And Maya"), 700]], C("Half the town", 0.5), pose="stand", face="worry", label="MAYA · FIRST-TIME BUYER",
                   labelUntil=C("just says", 0.5), poses=[[0, "stand"], [C("is holding up"), "armsup"]], faces=[[0, "happy"], [C("in cash"), "shock"], [C("is holding up"), "worry"]],
                   takes=[C("in cash", 0.2)]),
              it("placard", x=700, y=[[0, 420], [C("is holding up"), 400]], at=C("is holding up"), text="PLEASE", size=46, scale=1.0),
              it("savejar", x=300, y=860, at=C("saving since forever"), level=[[0, 0.15], [C("saving since forever", 1.5), 0.3]], scale=0.6, text="SAVINGS")]},
    sfx=[{"kind": "hit", "cue": "in cash", "gain": 0.35}])
stage("s02_hook", "co_hook", {
    **W1("openhouse", houseX=1350, signX=700, crowd=1.0, queue=10, soldAt=0.0, soldText="SOLD!"),
    "cam": cam((0, 1150, 420, 0.92), (C("The typical household"), 1150, 450, 1.0, 1.6), (C("And with mortgage rates"), 1150, 470, 1.05, 1.6),
               (C("has run right past"), 1150, 480, 1.25, WHIP)), "drift": 4,
    "items": [it("counter", x=1150, y=180, at=C("The typical existing home"), prefix="$", decimals=0,
                 steps=[[0, 0], [C("The typical existing home"), 0], [C("in October", -0.3), 416700]], text="MEDIAN EXISTING-HOME PRICE, OCT 2026 (NAR)", until=C("The typical household", 1.2)),
              it("counter", x=1150, y=180, at=C("The typical household", 1.3), prefix="$", decimals=0,
                 steps=[[0, 0], [C("The typical household", 1.3), 0], [C("a record", -0.2), 87460]], text="MEDIAN HOUSEHOLD INCOME, 2025 (CENSUS)", until=C("And with mortgage rates", 0.6)),
              sign("30-YR MORTGAGE: 7.11% (FREDDIE MAC, NOV 12)", 1150, 160, C("And with mortgage rates", 0.7), color="#FFCDD2", size=32, until=C("has run right past", 1.5)),
              MAYA([[0, 450], [C("has run right past"), 450], [C("the paycheck most", 0.5), 750]], 0.2, face="worry", hold="box", boxText="PAYCHECK", pose="stand",
                   faces=[[0, "worry"], [C("has run right past"), "panic"]]),
              it("bigtag", x=[[0, 1700], [C("has run right past"), 1700], [C("the paycheck most"), 1150]], y=320, at=C("the paycheck you need"), was="NEEDED", now="PAYCHECK", scale=0.8),
              it("toonwords", text="ZOOM!", x=1450, y=420, at=C("has run right past"), until=C("the paycheck most", 1.5), size=110, color="#FFC93C"),
              DEE(1900, 0.3, face="dollar", hold="clipboard", pose="stand")]},
    sources=["nar_ehs", "census_inc", "pmms"])
# promise: a whip-pan tour of the episode's worlds
stage("s03_promise", "co_promise", {
    "zones": [Z("openhouse", -1600, 1700, houseX=600, signX=150, crowd=1, queue=4),
              Z("ratecoaster", 1700, 4800, gx0=2200, gx1=4300, ys=70, pts=[[2019 + (y - 2019), r] for y, r in PMMS], car=[[0, 0.1], [12, 0.9]], wheelX=4700, boothX=1950),
              Z("lockstreet", 4800, 7600, locks=["< 4%"] * 4, firstX=5300, gap=600, lockAt=C("the owners who", -0.3)),
              Z("emptylot", 7600, 10400, lotX=9000, build=0.3, tumble=True, sign="COMING... SOMEDAY"),
              Z("zoningboard", 10400, 13400, daisX=11800, mapX=12700, podX=11000, mapAt=C("the room where", 0.2), mapDur=1.6, gavelAt=[C("decided", 0.1)])],
    "worldW": 13400,
    "cam": cam((0, 1100, 520, 0.8), (C("Let's follow the money"), 600, 520, 0.85, 1.0), (C("The price that outran"), 600, 480, 0.95, 0.8),
               (C("the rate that rode"), 3250, 470, 0.6, WHIP), (C("the owners who"), 6200, 520, 0.72, WHIP), (C("the homes we never"), 9000, 520, 0.8, WHIP),
               (C("the room where"), 11900, 470, 0.66, WHIP)), "drift": 4,
    "items": [it("toonwords", text="FOLLOW THE MONEY", x=600, y=150, at=C("Let's follow the money"), until=C("the rate that rode"), size=64),
              sign("1 · THE PRICE", 600, 160, C("The price that outran", 0.3), color="#FFCDD2", size=34, until=C("the rate that rode", 0.5)),
              sign("2 · THE RATE", 3250, 130, C("the rate that rode", 0.2), color="#FFF59D", size=40),
              sign("3 · THE LOCK-IN", 6200, 160, C("the owners who", 0.2), color="#BBDEFB", size=38),
              sign("4 · THE MISSING HOMES", 9000, 160, C("the homes we never", 0.2), color="#C8E6C9", size=38),
              sign("5 · THE ROOM", 11900, 120, C("the room where", 0.2), color="#E1BEE7", size=40),
              MAYA([[0, 300], [3, 700]], 0.2, face="happy", pose="stand", scale=1.1),
              REX(6300, 0.1, face="smug", scale=1.1), DEE(9300, 0.1, face="worry", hold="clipboard", scale=1.1)]},
    sfx=[{"kind": "whoosh", "cue": "the rate that rode", "gain": 0.25}, {"kind": "whoosh", "cue": "the owners who", "gain": 0.25},
         {"kind": "whoosh", "cue": "the homes we never", "gain": 0.25}, {"kind": "whoosh", "cue": "the room where", "gain": 0.25}])
stage("s04_title", "title_card", {
    **W1("titlecard", title="STARTER HOME", sub="WHY NOBODY CAN AFFORD ONE", subs=[[2.0, "Tonight: “Three Bedrooms, One Bath, Forty Bidders”"]]), "cam": STILL(), "drift": 0, "min_seconds": 5.8,
    "items": [MAYA(250, 2.4, scale=1.2, face="love", pose="cheer", hops=[2.8, 4.2]), DEE(1690, 2.6, scale=1.2, face="grin", pose="wave", hold="clipboard"),
              REX(1480, 3.0, scale=1.1, face="smug", pose="stand", hops=[3.6])]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}, {"kind": "hit", "at": 1.6, "gain": 0.25}])

# ====================================================================== ACT 1: the price tag
bumper("s05_b1", "a1_card", "1", "ACT ONE", "THE PRICE TAG", "Some assembly required. House not included.", "#E53950", "house")
stage("s06_ratio", "a1_ratio", {
    **W1("lockstreet", locks=[], firstX=-2000, gap=600),
    "cam": cam((0, 1000, 480, 1.0), (C("In the nineteen-nineties"), 1050, 470, 1.05, 1.4), (C("an all-time high"), 1100, 450, 1.15, WHIP), (C("And in twenty"), 1050, 480, 1.0, 1.4)), "drift": 4,
    "items": [it("toonwords", text="THE SIMPLEST TEST", x=1000, y=110, at=0.2, until=C("divides the price"), size=66),
              sign("HOME PRICE ÷ HOUSEHOLD INCOME", 1000, 120, C("divides the price"), color="#FFF8E1", size=34, sub="EXISTING SINGLE-FAMILY · HARVARD JCHS", until=C("In the nineteen-nineties", 0.3)),
              it("calendar", x=1650, y=250, at=C("In the nineteen-nineties"), pages=[[0, "1990s"], [C("By twenty nineteen"), "2019"], [C("In twenty twenty-two"), "2022"], [C("And in twenty"), "2025"]], text="YEAR", scale=0.8),
              it("counter", x=1000, y=170, at=C("In the nineteen-nineties"), suffix="×", decimals=1,
                 steps=[[0, 0], [C("In the nineteen-nineties"), 0], [C("years of income"), 3.2], [C("By twenty nineteen", 0.6), 4.1], [C("an all-time high of five"), 5.0], [C("still"), 4.7]],
                 text="YEARS OF INCOME TO BUY A HOME (JCHS)"),
              MAYA(520, 0.3, hold="box", boxText="1 YEAR PAY", pose="stand", face="happy", faces=[[0, "happy"], [C("By twenty nineteen"), "worry"], [C("an all-time high"), "panic"]], takes=[C("an all-time high")]),
              it("bigtag", x=1380, y=[[0, 560], [C("By twenty nineteen"), 500], [C("an all-time high"), 420]], at=C("divides the price", 0.5), was="HOME", now="PRICE", scale=[[0, 0.7], [C("an all-time high"), 1.0]]),
              DEE(1950, 0.4, face="dollar", hold="clipboard", hops=[C("an all-time high", 0.3)])]},
    sources=["jchs"])
stage("s07_income", "a1_income", {
    **W1("emptylot", lotX=1500, build=1.0, sign="SOLD"),
    "cam": cam((0, 1000, 500, 1.0), (C("But prices sprinted"), 1100, 420, 0.95, 1.4), (C("The paycheck jogged"), 700, 560, 1.2, WHIP), (C("The price tag took"), 1300, 340, 1.05, WHIP)), "drift": 4,
    "items": [sign("MEDIAN HOUSEHOLD INCOME 2025: $87,460 · A RECORD", 1000, 140, C("The Census Bureau"), color="#C8E6C9", size=30, sub="CENSUS BUREAU, REAL (INFLATION-ADJUSTED)", until=C("But prices sprinted")),
              it("toonwords", text="+54% SINCE 2020", x=1100, y=120, at=C("rose"), size=80, until=C("The paycheck jogged", 1.0)),
              sign("HOME PRICES NATIONWIDE (HARVARD JCHS)", 1100, 250, C("rose", 0.5), color="#FFF8E1", size=26, until=C("The paycheck jogged", 1.0)),
              MAYA([[0, 200], [C("The paycheck jogged"), 300], [C("The price tag took"), 650]], 0.2, hold="box", boxText="PAYCHECK", pose="walk", face="worry",
                   faces=[[0, "happy"], [C("The price tag took"), "shock"]]),
              it("bigtag", x=1300, y=[[0, 700], [C("The price tag took"), 640], [C("took the elevator", 1.2), 120]], at=0.3, was="PRICE", now="↑ ↑ ↑", scale=0.9),
              it("toonwords", text="DING!", x=1600, y=80, at=C("took the elevator", 1.0), size=90, color="#FFFFFF")]},
    sources=["census_inc", "jchs_pr"])
stage("s08_shrink", "a1_shrink", {
    **W1("shrinker", machX=650, houseX=1450, size=[[0, 1.0], [C("In March twenty nineteen"), 1.0], [C("By March twenty twenty-six"), 1.0], [C("just"), 0.5]],
         gauge=[[0, 0.5], [C("about"), 0.5], [C("By March twenty twenty-six"), 0.5], [C("just"), 0.23]],
         gaugeText=[[C("about", 0.3), "49% (2019)"], [C("just", 0.3), "23% (2026)"]], zaps=[C("quietly shrank"), C("just", -0.4)]),
    "cam": cam((0, 1050, 480, 0.95), (C("In March twenty nineteen"), 700, 420, 1.15, 1.4), (C("By March twenty twenty-six"), 1050, 470, 1.0, WHIP), (C("Less than one in four"), 1450, 560, 1.3, 1.2)), "drift": 3,
    "items": [sign("LISTINGS AFFORDABLE AT ≤ $75,000 INCOME", 1050, 60, C("affordable to a household"), color="#FFF8E1", size=30, sub="HARVARD JCHS · MARCH 2019 vs MARCH 2026"),
              MAYA(1950, 0.3, face="worry", pose="stand", faces=[[0, "worry"], [C("just"), "shock"]], takes=[C("just", 0.2)]),
              it("toonwords", text="< 1 IN 4", x=1450, y=200, at=C("Less than one in four"), size=96, color="#FFC93C")]},
    sources=["jchs"])
add("p09_ratio", "a1_draw", "engine_draw", {
    "title": "Years of income to buy a home (JCHS)", "board": BOARD, "draw_start": C("Let me draw it"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 820 L 1500 820", "color": "ink", "width": 5, "start": C("Let me draw it")},
        {"d": "M 650 820 L 650 570 L 810 570 L 810 820 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("The nineties"), "label": lbl("1990s · 3.2×", 730, 550, 24, "accent3")},
        {"d": "M 860 820 L 860 500 L 1020 500 L 1020 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Twenty nineteen"), "label": lbl("2019 · 4.1×", 940, 480, 24, "accent2")},
        {"d": "M 1070 820 L 1070 430 L 1230 430 L 1230 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("peak"), "label": lbl("2022 PEAK · 5.0×", 1150, 410, 24, "risk")},
        {"d": "M 1280 820 L 1280 453 L 1440 453 L 1440 820 Z", "color": "accent", "width": 3, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("four point seven"), "label": lbl("2025 · 4.7×", 1360, 433, 24, "accent")},
        {"d": dot(1050, 880), "color": "muted", "width": 1, "start": C("Every extra step"), "label": lbl("EXISTING SINGLE-FAMILY PRICE ÷ MEDIAN HOUSEHOLD INCOME · HARVARD JCHS 2026", 1050, 880, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Every extra step", 0.2), "dur": 1.6, "target": [1150, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["jchs"])

# ====================================================================== ACT 2: the rate rollercoaster
bumper("s10_b2", "a2_card", "2", "ACT TWO", "THE RATE ROLLERCOASTER", "Please keep your wallet inside the ride at all times", "#2F6FD1", "shed")
x21, y21 = xy_at(2021.02); x22, y22 = xy_at(2022.82); x26, y26 = xy_at(2026.77); x27, y27 = xy_at(2026.86); x19, y19 = xy_at(2019.0)
stage("s11_coaster", "a2_coaster", {
    **W1("ratecoaster", pts=PMMS, boothText="THE 30-YR",
         car=[[0, 0.0], [C("Freddie Mac tracks"), 0.0], [C("record low"), u_at(2021.02)], [C("above seven"), u_at(2022.82)], [C("This October"), u_at(2026.6)],
              [C("climbed back"), u_at(2026.77)], [C("last week"), u_at(2026.86)]],
         reveal=[[0, 0.02], [C("Freddie Mac tracks"), 0.02], [C("every week"), 1.0]],
         hl=[[C("record low"), 2021.02, "2.65% · RECORD LOW"], [C("above seven"), 2022.82, "ABOVE 7%"], [C("climbed back", 0.3), 2026.77, "7.40% · OCT"], [C("last week", 0.3), 2026.86, "7.11%"]]),
    "cam": cam((0, 1350, 460, 0.6), (C("Freddie Mac tracks"), 1350, 470, 0.62, 1.0), (C("every week"), x19 + 300, y19 - 60, 0.9, 1.6),
               (C("record low"), x21, y21 - 80, 1.0, 1.8), (C("above seven"), x22, y22, 0.95, 1.4), (C("This October"), x26, y26 + 40, 1.0, 1.8),
               (C("last week"), x27 - 100, y27 + 60, 1.05, 0.8), (C("still", 0.8), 1500, 470, 0.62, 1.4)), "drift": 2,
    "items": [it("toonwords", text="THE REAL PRICE IS THE LOAN", x=1350, y=40, at=C("so the real price"), until=C("Freddie Mac tracks", 0.6), size=60),
              sign("FREDDIE MAC PMMS · WEEKLY 30-YEAR FIXED AVERAGE", 1350, 40, C("Freddie Mac tracks", 0.7), color="#FFF8E1", size=30, until=C("every week", 2.5)),
              MAYA(-150, 0.2, face="worry", pose="stand", faces=[[0, "worry"], [C("climbed back"), "panic"]])]},
    sources=["pmms"], sfx=[{"kind": "whoosh", "cue": "above seven", "gain": 0.25}])
stage("s12_payment", "a2_payment", {
    **W1("openhouse", houseX=1550, signX=2150, crowd=0.3, queue=0, signText="FOR SALE"),
    "cam": cam((0, 1000, 470, 0.95), (C("At two point six five"), 900, 430, 1.05, 1.4), (C("Same house"), 1450, 470, 1.0, WHIP), (C("more, every month"), 1000, 430, 1.15, 1.2)), "drift": 4,
    "items": [sign("OUR CALCULATION · $416,700 · 20% DOWN · 30 YEARS", 1000, 60, C("by our own calculation"), color="#FFF8E1", size=28, sub="PRINCIPAL + INTEREST ONLY · NO TAXES OR INSURANCE"),
              it("bigtag", x=650, y=300, at=C("At two point six five"), was="AT 2.65%", now="$1,343/MO", nowAt=C("principal and interest"), scale=0.95),
              it("bigtag", x=1350, y=300, at=C("At seven point one one"), was="AT 7.11%", now="$2,243/MO", nowAt=C("At seven point one one", 1.0), scale=0.95),
              it("toonwords", text="+$900 A MONTH", x=1000, y=560, at=C("more, every month", -0.6), size=84, color="#FF5A5F"),
              MAYA(350, 0.3, face="worry", pose="stand", faces=[[0, "happy"], [C("At seven point one one", 1.0), "shock"], [C("for thirty years"), "dizzy"]], takes=[C("At seven point one one", 1.0)]),
              DEE(1850, 0.3, face="grin", pose="talk", hold="clipboard", talk=[[C("Same house"), C("tiny lawn", 0.3)]]),
              it("bubble", text="SAME TINY\nLAWN!", x=2000, y=420, at=C("same tiny lawn"), until=C("more, every month"), tail=[1880, 600], size=30)]},
    sources=["nar_ehs", "pmms"])
add("p13_income", "a2_draw", "engine_draw", {
    "title": "The income test (our calculation)", "board": BOARD, "draw_start": C("Let me draw the income test"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 820 L 1400 820", "color": "ink", "width": 5, "start": C("Let me draw the income test")},
        {"d": dot(1010, 380), "color": "accent2", "width": 1, "start": C("a quarter"), "label": lbl("RULE: P&I ≤ 25% OF INCOME (NAR METHOD)", 1010, 380, 24, "accent2")},
        {"d": "M 700 820 L 700 460 L 900 460 L 900 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("that means earning"), "label": lbl("NEEDED ≈ $107,600", 800, 440, 26, "risk")},
        {"d": "M 1100 820 L 1100 528 L 1300 528 L 1300 820 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("Now the median household"), "label": lbl("MEDIAN HOUSEHOLD $87,460", 1200, 508, 24, "accent3")},
        {"d": "M 1330 460 L 1360 460 L 1360 528 L 1330 528", "color": "risk", "width": 5, "start": C("one gap"), "label": lbl("GAP ≈ $20K", 1440, 500, 26, "risk")},
        {"d": dot(1010, 880), "color": "muted", "width": 1, "start": C("This is our calculation"), "label": lbl("OUR CALCULATION · $2,243/MO × 12 ÷ 25% · CENSUS 2025 INCOME", 1010, 880, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("one gap", 0.2), "dur": 1.5, "target": [1345, 495]}],
    "scale": 0.86, "floor": 1040}, sources=["pmms", "nar_ehs", "nar_hai", "census_inc"])
stage("s14_hai", "a2_hai", {
    **W1("ratecoaster", pts=PMMS, car=0.98, boothX=900, boothText="RIDE ENTRANCE", gx0=1900, gx1=4300, wheelX=-500),
    "cam": cam((0, 1000, 470, 1.0), (C("In October it read"), 1050, 450, 1.05, 1.4), (C("Barely over the line"), 900, 520, 1.25, WHIP)), "drift": 3,
    "items": [it("toonwords", text="AFFORDABILITY INDEX", x=1000, y=90, at=0.2, until=C("equals one"), size=62),
              sign("100 = MEDIAN-INCOME FAMILY JUST QUALIFIES", 1000, 90, C("equals one"), color="#FFF8E1", size=30, sub="NAR · 20% DOWN · P&I ≤ 25% OF INCOME", until=C("In October it read", 0.3)),
              it("counter", x=1000, y=110, at=C("In October it read"), decimals=1, steps=[[0, 107.3], [C("In October it read"), 107.3], [C("a year earlier", -0.2), 100.7]], text="NAR HOUSING AFFORDABILITY INDEX · OCT 2026 (OCT 2025: 107.3)"),
              sign("YOU MUST BE THIS RICH TO RIDE", 1400, 300, C("Barely over the line", -0.6), color="#FFE0B2", size=30),
              MAYA(900, 0.3, face="worry", pose="stand", faces=[[0, "worry"], [C("Barely over the line"), "grin"], [C("the down payment"), "shock"]], takes=[C("the down payment")]),
              it("savejar", x=600, y=860, at=C("only if you have"), level=0.12, scale=0.55, text="DOWN PAYMENT")]},
    sources=["nar_ehs", "nar_hai"])
stage("s15_harvard", "a2_harvard", {
    **W1("shrinker", machX=650, houseX=1450, gaugeLabel="INCOME NEEDED", size=[[0, 0.5], [C("up from"), 0.5], [C("five years earlier"), 0.35]],
         gauge=[[0, 0.3], [C("The income needed"), 0.3], [C("at the end of"), 0.85], [C("up from"), 0.85]], gaugeText=[[C("at the end of", -0.3), "$120,800"], [C("up from", 0.5), "WAS $68,700"]],
         zaps=[C("five years earlier", -0.5)]),
    "cam": cam((0, 900, 480, 0.95), (C("The income needed"), 650, 400, 1.25, 1.4), (C("up from"), 1000, 470, 1.0, WHIP)), "drift": 3,
    "items": [sign("HARVARD JCHS · INCLUDES TAXES & INSURANCE · END OF 2025 vs 2020", 1050, 60, C("adding taxes"), color="#FFF8E1", size=26),
              MAYA(1950, 0.3, face="shock", pose="armsup", faces=[[0, "worry"], [C("at the end of"), "shock"]])]},
    sources=["jchs"])

# ====================================================================== ACT 3: the great lock-in
bumper("s16_b3", "a3_card", "3", "ACT THREE", "THE GREAT LOCK-IN", "Your move is important to us. Please hold.", "#7E57C2", "dog")
stage("s17_lock", "a3_lock", {
    **W1("lockstreet", locks=LOCKS, firstX=300, gap=620, lockAt=C("below four percent", -0.6)),
    "cam": cam((0, 1100, 480, 0.9), (C("Meet Rex"), 950, 520, 1.2, WHIP), (C("And he is not alone"), 1200, 470, 0.85, 1.6)), "drift": 4,
    "items": [it("toonwords", text="FROZEN", x=1100, y=120, at=C("They froze"), until=C("Meet Rex"), size=110, color="#BBDEFB"),
              REX(920, C("Meet Rex", -0.3), face="smug", pose="stand", label="REX · MAYA'S DAD", labelUntil=C("And he is not alone"),
                  faces=[[0, "smug"], [C("near the bottom"), "happy"]], hops=[C("near the bottom", 0.2)]),
              it("bubble", text="I REFINANCED\nAT THE BOTTOM!", x=1180, y=320, at=C("Rex refinanced"), until=C("And he is not alone"), tail=[980, 560], size=28),
              sign("HALF OF ALL MORTGAGES BELOW 4% (LATE 2025)", 1200, 100, C("of all outstanding"), color="#FFF59D", size=32, sub="HARVARD JCHS")]},
    sources=["jchs"], sfx=[{"kind": "hit", "cue": "below four percent", "gain": 0.3}])
stage("s18_cage", "a3_cage", {
    **W1("lockstreet", locks=["< 4%"], firstX=1300, gap=620, lockAt=0.0, emptyText="NOPE"),
    "cam": cam((0, 1100, 470, 1.0), (C("His kids have moved out"), 1300, 420, 0.9, 1.4), (C("And he stays anyway"), 1000, 520, 1.25, WHIP), (C("The golden handcuffs"), 1050, 470, 1.05, 1.0)), "drift": 4,
    "items": [REX(900, 0.2, face="worry", pose="stand", faces=[[0, "worry"], [C("And he stays anyway"), "deadpan"], [C("The golden handcuffs"), "smug"]]),
              it("bubble", text="NEW LOAN: 7%+?!", x=650, y=330, at=C("takes a new one"), until=C("His kids have moved out"), tail=[860, 520], size=34, shout=True),
              sign("EMPTY NEST · 4 BEDROOMS", 1700, 160, C("His kids have moved out"), color="#FFE0B2", size=30),
              MAYA([[C("The house is too big"), 2500], [C("And he stays anyway"), 1700]], C("The house is too big", -0.3), face="love", pose="run", poses=[[0, "run"], [C("And he stays anyway"), "stand"]],
                   faces=[[0, "love"], [C("And he stays anyway", 0.3), "panic"]]),
              it("padlock", x=1300, y=330, at=C("lock-in effect", -0.6), lockAt=C("lock-in effect"), text="MY OLD RATE", chainTo=900, scale=0.9),
              it("toonwords", text="GOLDEN HANDCUFFS", x=1050, y=110, at=C("The golden handcuffs"), size=80, color="#FFC93C")]},
    sources=["pmms"])
stage("s19_fhfa", "a3_fhfa", {
    **W1("lockstreet", locks=LOCKS, firstX=-200, gap=620, lockAt=0.0),
    "cam": cam((0, 1150, 470, 0.95), (C("Between mid twenty"), 1150, 450, 1.0, 1.6), (C("And by keeping homes"), 1200, 480, 1.05, 1.4)), "drift": 5,
    "items": [sign("FHFA WORKING PAPER (2024) · ESTIMATES", 1150, 40, C("Economists at the Federal"), color="#FFF8E1", size=28),
              sign("EACH +1 PT (MARKET RATE − YOUR RATE): CHANCE OF SELLING −18.1%", 1150, 130, C("For every percentage point"), color="#BBDEFB", size=28, until=C("Between mid twenty")),
              it("counter", x=1150, y=180, at=C("Between mid twenty"), suffix="M", decimals=2, steps=[[0, 0], [C("Between mid twenty"), 0], [C("home sales"), 1.33]], text="SALES PREVENTED BY LOCK-IN, 2022Q2–2023Q4 (FHFA EST.)", until=C("And by keeping homes", 0.5)),
              chart([{"label": "LOCK-IN: PRICES", "value": 5.7, "color": "#E53950", "at": C("pushed prices"), "display": "+5.7%"},
                     {"label": "HIGHER RATES: PRICES", "value": 3.3, "color": "#2F6FD1", "at": C("more than higher rates"), "display": "−3.3%"}],
                    at=C("And by keeping homes", 0.5), max=7, title="EFFECT ON HOME PRICES (FHFA WORKING PAPER)", x=650, y=170, w=1000, h=420),
              DEE(2000, 0.3, face="worry", hold="clipboard", faces=[[0, "worry"], [C("pushed prices"), "panic"]])]},
    sources=["fhfa"])
stage("s20_sales", "a3_sales", {
    **W1("openhouse", houseX=1250, signX=650, crowd=0.0, queue=0),
    "cam": cam((0, 1100, 480, 0.95), (C("Harvard says"), 1100, 450, 0.95, 1.4), (C("And in October"), 1000, 470, 1.05, WHIP)), "drift": 4,
    "items": [DEE(950, 0.2, face="worry", pose="wave", hold="clipboard", faces=[[0, "worry"], [C("And in October"), "deadpan"]]),
              it("bubble", text="ANYONE?", x=1180, y=320, at=0.4, until=C("Harvard says"), tail=[1000, 560], size=40),
              chart([{"label": "2021", "value": 6.1, "color": "#2E9E5B", "at": C("two thirds of the pace", 0.2), "display": "6.1M"},
                     {"label": "2025", "value": 4.1, "color": "#E53950", "at": C("were stuck at"), "display": "4.1M"}],
                    at=C("Harvard says"), max=7, title="EXISTING-HOME SALES (HARVARD JCHS)", x=1300, y=150, w=700, h=420, until=C("And in October", 0.8)),
              sign("30-YEAR LOW", 1650, 640, C("a thirty-year low"), color="#FFCDD2", size=30, until=C("And in October", 0.8)),
              it("counter", x=1500, y=220, at=C("And in October", 0.9), suffix="M", decimals=2, steps=[[0, 0], [C("And in October", 0.9), 0], [C("an annual pace"), 3.75]], text="OCT 2026 ANNUAL PACE (NAR, SEAS. ADJ.)"),
              it("drone", x=[[0, 2500], [14, -400]], y=200, at=0.5, carry="TUMBLEWEED?", scale=0.6)]},
    sources=["jchs", "nar_ehs"])

# ====================================================================== ACT 4: the homes we never built
bumper("s21_b4", "a4_card", "4", "ACT FOUR", "THE HOMES WE NEVER BUILT", "Some assembly required. Lots of it.", "#2E9E5B", "bird", "STARTER HOME")
stage("s22_bust", "a4_bust", {
    **W1("emptylot", lotX=1250, build=[[0, 0.75], [C("builders went quiet"), 0.75], [C("builders went quiet", 1.2), 0.12]], tumble=True, sign="ON HOLD"),
    "cam": cam((0, 1150, 470, 0.9), (C("By our count"), 1100, 470, 0.95, 1.6), (C("In twenty eleven"), 1250, 520, 1.15, WHIP)), "drift": 4,
    "items": [it("toonwords", text="SUPPLY", x=1150, y=110, at=C("Supply"), until=C("By our count"), size=110),
              chart([{"label": "2000s", "value": 15.64, "color": "#2E9E5B", "at": C("in the two thousands", -0.5), "display": "15.6M"},
                     {"label": "2010s", "value": 9.15, "color": "#E53950", "at": C("in the twenty-tens", -0.5), "display": "9.2M"}],
                    at=C("By our count"), max=18, title="NEW HOMES COMPLETED PER DECADE (OUR SUMS, CENSUS)", x=300, y=150, w=860, h=440, until=C("In twenty eleven", 0.5)),
              it("counter", x=1250, y=200, at=C("In twenty eleven"), suffix="K", decimals=0, steps=[[0, 0], [C("In twenty eleven"), 0], [C("the lowest year"), 585]], text="COMPLETIONS IN 2011 · LOWEST SINCE 1968 (CENSUS)"),
              DEE(1900, 0.3, face="deadpan", pose="stand", hold="clipboard", faces=[[0, "worry"], [C("In twenty eleven"), "deadpan"]])]},
    sources=["completions"])
stage("s23_shortage", "a4_shortage", {
    **W1("emptylot", lotX=1300, build=[[0, 0.12], [C("Not enough"), 0.4]], sign="COMING SOON"),
    "cam": cam((0, 1100, 470, 0.95), (C("Harvard says"), 1100, 450, 1.0, 1.4), (C("These are"), 1150, 480, 1.05, 1.4), (C("Not enough"), 1300, 560, 1.25, WHIP)), "drift": 4,
    "items": [it("toonwords", text="HOW MANY ARE MISSING?", x=1100, y=100, at=0.2, until=C("Harvard says"), size=58),
              sign("ESTIMATES: 1.2M – 5.5M HOMES SHORT", 1100, 100, C("put the shortage"), color="#FFF59D", size=38, sub="RANGE OF ESTIMATES CITED BY HARVARD JCHS (2026)"),
              sign("UP FOR GROWTH: ≈ 3.8M (2023)", 1100, 260, C("Up for Growth"), color="#C8E6C9", size=32),
              sign("DIFFERENT METHODS · DIFFERENT ANSWERS", 1100, 380, C("These are"), color="#FFE0B2", size=28),
              MAYA(450, 0.3, face="worry", pose="shrug", faces=[[0, "worry"], [C("Not enough"), "panic"]]),
              it("toonwords", text="NOT ENOUGH", x=1300, y=520, at=C("Not enough"), size=90, color="#FF5A5F")]},
    sources=["jchs", "upforgrowth", "nahb"])
add("p24_gap", "a4_draw", "engine_draw", {
    "title": "Why shortage estimates differ (simplified)", "board": BOARD, "draw_start": C("Box one"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 470, 300, 220), "color": "accent2", "width": 6, "kind": "box", "start": C("Box one"), "label": lbl("HOMES WE HAVE", 710, 580, 30, "accent2")},
        {"d": rect(1150, 420, 380, 320), "color": "accent3", "width": 7, "kind": "box", "start": C("Box two"), "label": lbl("HOMES WE'D NEED", 1340, 490, 28, "accent3")},
        {"d": dot(1340, 560), "color": "ink", "width": 1, "start": C("for every"), "label": lbl("+ EVERY NEW HOUSEHOLD", 1340, 560, 22, "ink")},
        {"d": dot(1340, 620), "color": "ink", "width": 1, "start": C("plus a healthy number"), "label": lbl("+ HEALTHY VACANCY TO MOVE", 1340, 620, 22, "ink")},
        {"d": arrow((870, 580), (1140, 580), 0.12), "color": "risk", "width": 7, "kind": "arrow", "start": C("The arrow between them"), "label": lbl("THE GAP", 1005, 520, 28, "risk")},
        {"d": dot(1050, 840), "color": "muted", "width": 1, "start": C("Change"), "label": lbl("ASSUMPTIONS → 1.2M–5.5M (ESTIMATES)", 1050, 840, 24, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("The arrow between them", 0.4), "dur": 1.4, "target": [1005, 580]}],
    "scale": 0.86, "floor": 1040}, sources=["jchs"])
stage("s25_cost", "a4_cost", {
    **W1("emptylot", lotX=1300, build=[[0, 0.4], [C("about"), 0.8]], sign="PERMIT PENDING"),
    "cam": cam((0, 1100, 470, 0.95), (C("The home builders'"), 1150, 450, 1.0, 1.4), (C("It's also a clue"), 1100, 500, 1.15, WHIP)), "drift": 4,
    "items": [it("counter", x=1100, y=180, at=C("Harvard says"), prefix="+", suffix="%", decimals=0, steps=[[0, 0], [C("Harvard says"), 0], [C("since January"), 40]], text="CONSTRUCTION INPUT PRICES SINCE JAN 2020 (JCHS)", until=C("The home builders'", 0.5)),
              sign("REGULATION ≈ 26.4% OF A NEW HOME'S PRICE", 1100, 100, C("regulation makes up"), color="#FFF59D", size=34, sub="≈ $131,734 ON A $499,500 NEW HOME · NAHB (BUILDERS' TRADE GROUP) ESTIMATE"),
              it("docs", x=500, y=860, at=C("regulation makes up"), text="PERMITS", scale=0.85, stamp="PENDING", stampAt=C("That's the builders'")),
              it("forklift", x=[[0, 2400], [C("The home builders'"), 1950]], at=0.3, load=["LUMBER", "STEEL"], lift=[[0, 0.1], [C("about"), 0.3]], scale=0.85, flip=True, face="happy"),
              it("toonwords", text="FOLLOW THE CLUE →", x=1100, y=330, at=C("It's also a clue"), size=60)]},
    sources=["jchs", "nahb"])

# ====================================================================== ACT 5: the zoning board
bumper("s26_b5", "a5_card", "5", "ACT FIVE", "THE ZONING BOARD", "Public comment is limited to three hours", "#FF8A1F", "mailbox", "STARTER HOME?")
stage("s27_room", "a5_room", {
    **W1("zoningboard", daisX=1100, mapX=1950, podX=300, gavelAt=[C("One house", 0.1), C("on one lot", 0.1)]),
    "cam": cam((0, 1100, 300, 0.7), (C("Not a bank"), 1300, 380, 0.85, 1.2), (C("The local zoning board"), 1100, 380, 0.8, WHIP), (C("Zoning decides"), 1700, 280, 1.0, 1.6), (C("One house"), 1100, 400, 1.05, WHIP)), "drift": 2,
    "items": [it("toonwords", text="THE MOST POWERFUL ROOM", x=1100, y=-10, at=0.2, until=C("Not a bank"), size=60),
              it("toonwords", text="NOT A BANK. NOT CONGRESS.", x=1100, y=-10, at=C("Not a bank"), until=C("The local zoning board"), size=54, color="#FFFFFF"),
              sign("ZONING = WHAT MAY BE BUILT ON EACH LOT", 1500, -40, C("Zoning decides"), color="#FFF8E1", size=30, until=C("One house", -0.2)),
              it("toonwords", text="ONE HOUSE · ONE LOT", x=1100, y=-20, at=C("One house"), size=70)]})
stage("s28_berkeley", "a5_berkeley", {
    **W1("zoningboard", daisX=700, mapX=1500, podX=-300, mapAt=C("found that about"), mapDur=2.2, mapTitle="RESIDENTIAL LAND (SHARE)"),
    "cam": cam((0, 1300, 330, 0.95), (C("found that about"), 1500, 290, 1.15, 1.4), (C("That's one region"), 1300, 380, 0.9, 1.4)), "drift": 2,
    "items": [it("counter", x=2150, y=150, at=C("found that about"), prefix="≈", suffix="%", decimals=0, steps=[[0, 0], [C("found that about"), 0], [C("single-family homes only"), 78]], text="SINGLE-FAMILY ONLY"),
              sign("GREATER LOS ANGELES · UC BERKELEY (2022)", 1500, -20, C("Researchers at UC Berkeley"), color="#FFF8E1", size=28),
              sign("ONE REGION, NOT THE WHOLE COUNTRY", 1500, 610, C("That's one region"), color="#FFE0B2", size=28),
              MAYA(2250, C("But it shows", -0.4), face="shock", pose="stand", scale=1.1)]},
    sources=["berkeley"])
stage("s29_hearing", "a5_hearing", {
    **W1("zoningboard", daisX=1300, mapX=2150, podX=520, protestAt=C("worried"), gavelAt=[C("hardest to build", 0.1)], mapAt=0.0, mapDur=0.01, share=0.78),
    "cam": cam((0, 700, 430, 1.05), (C("You may need a variance"), 1000, 420, 0.85, 1.4), (C("worried"), 900, 600, 0.85, WHIP), (C("Together"), 1300, 400, 0.95, 1.4)), "drift": 3,
    "items": [MAYA(420, 0.2, face="happy", pose="talk", talk=[[0.2, C("stands", 0.4)]], faces=[[0, "happy"], [C("worried"), "panic"], [C("hardest to build"), "dizzy"]]),
              it("placard", x=560, y=330, at=0.3, until=C("You may need a variance", 1.5), text="4 HOMES\nHERE?", size=36),
              sign("VARIANCE · HEARING · PUBLIC COMMENT", 1300, 30, C("You may need a variance"), color="#FFF8E1", size=30, until=C("Parking rules")),
              sign("PARKING RULES · HEIGHT LIMITS · MINIMUM LOT SIZES", 1300, 30, C("Parking rules"), color="#FFE0B2", size=30),
              it("toonwords", text="CHEAPEST = HARDEST", x=1300, y=170, at=C("Together"), size=70, color="#FF5A5F")]},
    sfx=[{"kind": "hit", "cue": "hardest to build", "gain": 0.35}])
add("p30_lots", "a5_draw", "engine_draw", {
    "title": "One lot, three ways (illustrative)", "board": BOARD, "draw_start": C("Let me draw one lot"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 500, 240, 240), "color": "accent", "width": 6, "kind": "box", "start": C("One lot, one house"), "label": lbl("1 HOUSE", 680, 625, 28, "accent")},
        {"d": dot(680, 790), "color": "accent", "width": 1, "start": C("pays for all the land"), "label": lbl("LAND ÷ 1", 680, 790, 26, "accent")},
        {"d": rect(880, 500, 240, 240), "color": "accent2", "width": 6, "kind": "box", "start": C("with a duplex"), "label": lbl("DUPLEX", 1000, 540, 24, "accent2")},
        {"d": "M 1000 560 L 1000 730", "color": "accent2", "width": 5, "start": C("Two"), "label": lbl("2 HOMES", 1000, 650, 24, "accent2")},
        {"d": dot(1000, 790), "color": "accent2", "width": 1, "start": C("share the land"), "label": lbl("LAND ÷ 2", 1000, 790, 26, "accent2")},
        {"d": rect(1200, 500, 240, 240), "color": "accent3", "width": 6, "kind": "box", "start": C("A fourplex"), "label": lbl("FOURPLEX", 1320, 540, 24, "accent3")},
        {"d": "M 1320 560 L 1320 730 M 1210 645 L 1430 645", "color": "accent3", "width": 5, "start": C("four homes"), "label": lbl("4 HOMES", 1320, 700, 22, "accent3")},
        {"d": dot(1320, 790), "color": "accent3", "width": 1, "start": C("cut to a quarter"), "label": lbl("LAND ÷ 4", 1320, 790, 26, "accent3")},
        {"d": dot(1000, 870), "color": "muted", "width": 1, "start": C("That's what's at stake"), "label": lbl("ILLUSTRATIVE · SAME LOT, SAME LAND COST", 1000, 870, 20, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("cut to a quarter", 0.2), "dur": 1.4, "target": [1320, 790]}],
    "scale": 0.86, "floor": 1040})

# ====================================================================== THE BASEMENT + PAYOFF + TEASER + BUTTON
stage("s31_basement", "a6_basement", {
    **W1("basement", bulbX=1000, futonX=1250, stairsX=1900, boxX=540, winX=500, doorAt=C("Forty", -0.3)),
    "cam": cam((0, 1150, 470, 0.95), (C("In the National"), 1100, 440, 1.0, 1.6), (C("And the typical"), 1150, 470, 1.05, 1.4), (C("Forty"), 1250, 560, 1.3, WHIP)), "drift": 3,
    "items": [it("toonwords", text="THE FIRST-TIME BUYER", x=1100, y=110, at=0.3, until=C("In the National"), size=62),
              sign("FIRST-TIME BUYERS: 22% OF PURCHASES", 1100, 100, C("first-timers made up"), color="#FFF59D", size=34, sub="NAR PROFILE OF HOME BUYERS AND SELLERS 2026 · NORM ≈ 40% BEFORE 2008", until=C("And the typical")),
              it("counter", x=1150, y=170, at=C("And the typical"), decimals=0, steps=[[0, 0], [C("And the typical"), 0], [C("years old"), 40]], text="MEDIAN AGE OF A FIRST-TIME BUYER (NAR 2026, RECORD)"),
              MAYA(1200, 0.2, face="deadpan", pose="sit", y=820, faces=[[0, "deadpan"], [C("Forty"), "shock"]], takes=[C("Forty", 0.1)]),
              it("savejar", x=360, y=860, at=0.5, level=[[0, 0.35], [C("years old"), 0.45]], scale=0.6, text="DOWN PAYMENT"),
              REX([[C("Forty", -0.2), 2350], [C("Forty", 1.2), 2100]], C("Forty", -0.3), y=300, face="happy", pose="wave", scale=1.0),
              it("bubble", text="HAPPY 40th,\nKIDDO!", x=2050, y=80, at=C("Forty", 0.6), tail=[2120, 180], size=30)]},
    sources=["nar_profile"])
stage("s32_payoff", "payoff", {
    "zones": [Z("openhouse", -1600, 2300, houseX=900, signX=300, crowd=0.6, queue=3, signText="STARTER HOME", soldAt=999),
              Z("emptylot", 2300, 5400, lotX=3700, build=[[0, 0.2], [C("Fix them together"), 0.2], [C("comes back"), 1.0]], sign="COMING SOON")],
    "worldW": 5400,
    "cam": cam((0, 1100, 450, 0.82), (C("Prices outran"), 900, 450, 0.85, 1.4), (C("Builders spent"), 3600, 470, 0.85, WHIP), (C("Fix one"), 3300, 460, 0.8, 1.4), (C("comes back"), 3700, 470, 1.0, 1.6)), "drift": 2,
    "items": [it("toonwords", text="NOT ONE VILLAIN", x=1100, y=90, at=C("Not because of one villain"), until=C("Prices outran"), size=70),
              sign("PRICES > PAYCHECKS", 500, 130, C("Prices outran"), color="#FFCDD2", size=30),
              sign("RATES → +$ EVERY MONTH", 1100, 60, C("Rates piled"), color="#FFF59D", size=30),
              sign("OWNERS LOCKED IN", 1600, 160, C("Owners with cheap loans"), color="#BBDEFB", size=30),
              sign("A DECADE OF UNDERBUILDING", 3300, 120, C("Builders spent"), color="#C8E6C9", size=30),
              sign("RULES vs CHEAP HOMES", 3900, 200, C("local rules"), color="#E1BEE7", size=30),
              MAYA([[0, 1400], [C("Fix them together"), 1900], [C("comes back"), 3300]], 0.3, face="worry", pose="stand", faces=[[0, "worry"], [C("comes back"), "love"]], hops=[C("comes back", 0.4)]),
              REX(2900, 0.4, face="smug", pose="stand", faces=[[0, "smug"], [C("comes back"), "happy"]]),
              DEE(4300, 0.5, face="grin", pose="wave", hold="clipboard"),
              it("toonwords", text="THE STARTER HOME, BACK?", x=3700, y=80, at=C("comes back", -0.3), size=58)]})
add("s33_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s34_button", "button", {
    **W1("basement", bulbX=900, futonX=1300, stairsX=1900, boxX=-900, winX=400, doorAt=0.0),
    "cam": cam((0, 1150, 360, 1.5), (2.4, 1150, 480, 0.9, 0.9)), "drift": 0, "min_seconds": 5.6,
    "items": [MAYA(1150, 0.0, face="love", pose="cheer", hops=[0.6, 1.6], faces=[[0, "love"], [2.6, "deadpan"]], poses=[[0, "cheer"], [2.6, "stand"]]),
              it("toonwords", text="MAYA GOT THE KEYS!", x=1150, y=60, at=0.3, until=2.3, size=60),
              it("toonwords", text="...TO THE BASEMENT.", x=1150, y=90, at=2.6, size=64, color="#FFFFFF"),
              it("placard", x=1600, y=420, at=2.9, text="RENT: $0\nLANDLORD: MOM", size=30),
              REX(2200, 2.8, y=300, face="grin", pose="wave", scale=0.9)]},
    sfx=[{"kind": "hit", "at": 2.6, "gain": 0.3}])

write(OUT, "# GENERATED by tools/gen_housing_v2_storyboard.py; edit the generator, not this file.\n"
           "# Episode 58 storyboard (housing v2): sitcom-style episode; bespoke worlds in CartoonStage/housing.tsx; tones from visual_direction.yaml.\n")
