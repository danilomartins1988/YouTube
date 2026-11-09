"""Generates projects/when-tokyos-land-was-worth-more-than-entire-countries/deliverables/documentary/storyboard.yaml (Episode 23, Japan's bubble).

Bespoke worlds (tones from visual_direction.yaml: spectacle -> strategy -> crisis -> reflective): a neon Ginza night where a
single square meter carries a giant price tag, the new `balance` item (a huge scale with the Imperial Palace garden on
one pan and California on the other, settling level) as the through-line, a central-bank room where the rate dial
climbs, the stock board falling, golf-club memberships, and a 2024 trading floor finally passing the old record.
Presenter: the land-loan machine (boxes + arrows), the US vs Japan land value (bars), the machine in reverse (boxes + arrows).
No logos, no flags, no likeness of real people (names in text only); no yen symbols on screen (dollars only).
Run: python tools/gen_tokyo_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/when-tokyos-land-was-worth-more-than-entire-countries/deliverables/documentary/storyboard.yaml"
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


def scale_item(x=1000, **kw):
    kw.setdefault("textc", "#FFFFFF")
    return it("balance", x=x, left="IMPERIAL PALACE", lsub="Tokyo · one walled garden", right="CALIFORNIA", rsub="the whole state", lsize=1.3, rsize=1.3, **kw)


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": 3.5, "x": 1000, "y": 520, "zoom": 0.9, "dur": 3.0}], "drift": 2,
    "items": [scale_item(1000, at=0.2, scale=1.3, tilt=-16, balanceAt=4.0)],
    "callouts": [co("One garden = one American state?", 960, 120, C("How can a garden"), "gold", screen=True, size=42)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("district", night=True)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 0.95}, {"at": C("Japan's land as a whole"), "x": 1900, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("Then it all came down"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [scale_item(900, at=0.2, scale=0.85, tilt=-14, balanceAt=C("was worth as much as")),
              it("tower", x=1700, text="ALL US LAND", color="#1565C0", h=140, at=C("Japan's land as a whole"), scale=0.8),
              it("tower", x=2050, text="JAPAN'S LAND", color="#C62828", h=[[0, 40], [{"cue": "all the land in the United States", "offset": 1}, 560]], at=C("Japan's land as a whole"), scale=0.8),
              it("chart", x=2400, y=420, w=420, h=260, at=C("Then it all came down"), dur=2.5, text="NIKKEI", pts=[0.9, 0.5, 0.4, 0.3, 0.35], color="risk")],
    "callouts": [co("Palace land = California or Canada (est.)", 960, 960, C("At neighbouring land prices"), "gold", screen=True, size=38, sub="Shiryaev, Zhitlukhin & Ziemba (LSE)", until=C("Japan's land as a whole", -0.3)),
                 co("Japan's land ≈ 4.1× all US land", 960, 960, C("Japan's land as a whole"), "white", screen=True, size=40, until=C("Then it all came down", -0.3)),
                 co("Then: 34 years to regain the stock-market peak", 960, 960, C("Then it all came down"), "risk", screen=True, size=36, sub="AP")]},
    sources=["lse", "ap_2024"])

# ====================================================================== PART 1: money with nowhere to go
card("s03_c1", "m1_card", "Money With Nowhere to Go", "1985-1989")
stage("s04_q1", "m1_question", {
    "zones": [Z("vault")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vaultdoor", x=960, at=0.2, openAt=1.0, scale=0.8), it("coins", **{"from": [960, 500], "to": [2200, 300]}, at=1.5, rate=7)],
    "callouts": [co("Where did the money come from?", 960, 150, C("Where did"), "gold", screen=True, size=44)]})
stage("s05_roots", "m1_roots", {
    "zones": [Z("city")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("And from around"), "x": 1800, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("chart", x=900, y=420, w=520, h=320, at=C("Between nineteen fifty-five"), dur=3, text="BIG-CITY LAND vs CONSUMER PRICES", pts=[0.05, 0.15, 0.3, 0.55, 0.95], color="green"),
              it("letters", x=900, y=180, text="20× FASTER", at=C("faster than consumer prices"), size=64, color="gold"),
              *[it("building", x=1600 + 220 * k, at=C("prices in central Tokyo", 0.4 * k), text=["BANK", "BROKER", "FUND"][k], scale=0.55) for k in range(3)]],
    "callouts": [co("1955-1990: big-city land rose 20× faster than prices", 960, 960, C("Between nineteen fifty-five"), "white", screen=True, size=34, sub="LSE paper", until=C("And from around", -0.3)),
                 co("From ≈ 1983: foreign finance floods into Tokyo", 960, 960, C("And from around"), "gold", screen=True, size=36, sub="Ministry of Finance Japan")]},
    sources=["lse", "mof"])
stage("s06_plaza", "m1_plaza", {
    "zones": [Z("parliament")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Japan's currency soared"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=0.2, pages=[[0, "SEP", "1985"]], scale=0.8),
              *[it("person", x=800 + 130 * k, pose="stand", at=C("the Group of Five", 0.2 * k), scale=0.6, hair=k + 1, skin=k % 4) for k in range(5)],
              it("contract", x=1100, y=420, at=C("Plaza Accord"), text="PLAZA ACCORD", sub="push the dollar down", scale=0.6),
              it("chart", x=1800, y=420, w=460, h=280, at=C("Japan's currency soared"), dur=2.5, text="JAPAN'S CURRENCY vs DOLLAR", pts=[0.2, 0.45, 0.7, 0.85, 0.9], color="green"),
              it("arrow", **{"from": [1800, 650], "to": [2200, 760]}, at=C("began cutting interest rates"))],
    "callouts": [co("Sept 1985: the Plaza Accord", 960, 960, C("In September"), "white", screen=True, size=40, sub="Ministry of Finance Japan", until=C("Japan's currency soared", -0.3)),
                 co("Strong currency → fear of recession → rate cuts", 960, 960, C("Japan's currency soared"), "gold", screen=True, size=38)]},
    sources=["mof"])
stage("s07_cheap", "m1_cheap", {
    "zones": [Z("exchange")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Japan's Ministry of Finance says"), "x": 1800, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=900, y=220, at=C("By February"), suffix="%", decimals=1, steps=[[0, 5.0], [{"cue": "the official interest rate", "offset": 1.5}, 2.5]], text="OFFICIAL DISCOUNT RATE"),
              it("stack", x=900, h=[[0, 40], [{"cue": "Companies had more cash", "offset": 1.5}, 300]], at=C("Companies had more cash"), text="CASH", sub="nowhere to go"),
              it("letters", x=1800, y=200, text="ZAITECH", at=C("a new word appeared"), size=90, color="gold"),
              it("conveyor", x=1800, y=F - 40, at=C("Companies started making money"), n=5, speed=1.2, goods="box")],
    "callouts": [co("Feb 1987 - May 1989: 2.5%, the lowest ever", 960, 960, C("By February"), "white", screen=True, size=38, sub="Ministry of Finance Japan", until=C("Japan's Ministry of Finance says", -0.3)),
                 co("'Zaitech': making money from money", 960, 960, C("Japan's Ministry of Finance says"), "gold", screen=True, size=40)]},
    sources=["mof"])
add("p08_machine", "m1_draw", "engine_draw", {
    "title": "The land-loan machine", "board": BOARD, "draw_start": C("A company owns land"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(580, 360, 240, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("A company owns land"), "label": lbl("LAND", 700, 428, 28, "accent3")},
        {"d": rect(1060, 360, 240, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("The bank lends"), "label": lbl("BANK LOAN", 1180, 428, 26, "accent2")},
        {"d": rect(820, 620, 240, 120), "color": "accent", "width": 6, "kind": "box", "start": C("buy more land, or shares"), "label": lbl("BUY MORE", 940, 688, 26, "accent")},
        {"d": arrow((830, 420), (1050, 420), 0.1), "color": "ink", "width": 5, "start": C("The bank lends", 0.5)},
        {"d": arrow((1180, 490), (1000, 610), -0.2), "color": "ink", "width": 5, "start": C("uses the loan")},
        {"d": arrow((820, 640), (700, 490), -0.2), "color": "ink", "width": 5, "start": C("That pushes prices up"), "label": lbl("prices ↑", 660, 600, 24, "risk")},
        {"d": "M 1360 420 Q 1440 560 1360 700", "color": "risk", "width": 5, "start": C("Round and round"), "label": lbl("feels safe…", 1420, 760, 22, "risk", "start")},
    ],
    "actions": [{"kind": "point", "at": C("Round and round", 0.2), "dur": 1.4, "target": [940, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["mof"])
stage("s09_firewood", "m1_firewood", {
    "zones": [Z("parliament", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But ordinary prices"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 2,
    "items": [it("stack", x=900, h=[[0, 80], [{"cue": "And the pile kept growing", "offset": 2}, 420]], at=0.2, text="MONEY", sub="'dry firewood'", color="#8D6E63"),
              it("paper", x=1500, y=380, at=C("quotes a saying"), text="'Dry firewood piled up goes up in flames'", name="MOF HISTORY", scale=0.7),
              it("pricetag", x=1900, y=300, at=C("But ordinary prices"), pages=[[0, "SHOP PRICES: STABLE"]], sub="no alarm")],
    "callouts": [co("'Dry firewood piled up goes up in flames'", 960, 960, C("Dry firewood"), "gold", screen=True, size=38, sub="Ministry of Finance Japan", until=C("But ordinary prices", -0.3)),
                 co("Stable shop prices hid the danger", 960, 960, C("But ordinary prices"), "white", screen=True, size=40)]},
    sources=["mof"])
kinetic("s10_t1", "m1_transition", [("By the end of the decade", 60, "By the end of the decade", None, False), ("the numbers stopped making sense", 54, "stopped making sense", "risk", False)])

# ====================================================================== PART 2: the price of a square meter
card("s11_c2", "m2_card", "The Price of a Square Meter", "Tokyo, 1989")
stage("s12_q2", "m2_question", {
    "zones": [Z("district", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("pricetag", x=960, y=380, at=0.3, pages=[[0, "1 m²"], [2.5, "$ ? ? ?"]], sub="Ginza, Tokyo")],
    "callouts": [co("How expensive did Tokyo get?", 960, 150, C("How expensive"), "gold", screen=True, size=44)]})
stage("s13_ginza", "m2_ginza", {
    "zones": [Z("district", night=True)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("Office space"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("Even simple houses"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("pricetag", x=900, y=330, at=C("one square meter"), pages=[[0, "1 m²"], [{"cue": "was worth"}, "$200,000+"]], sub="Ginza"),
              it("desk", x=900, at=C("about the size of a small table"), scale=0.8),
              it("pricetag", x=1350, y=300, at=C("Choice land downtown"), pages=[[0, "≈ $1BN / ACRE"]], sub="downtown"),
              it("building", x=1750, at=C("Office space"), text="OFFICE · $75,000 / FT²", scale=0.7),
              it("building", x=2300, at=C("Even simple houses"), text="HOUSE · $10,000+ / MONTH", scale=0.55)],
    "callouts": [co("Ginza: one square meter, $200,000+", 960, 960, C("one square meter"), "gold", screen=True, size=40, sub="LSE paper", until=C("Office space", -0.3)),
                 co("Office space ≈ $75,000 per square foot", 960, 960, C("Office space"), "white", screen=True, size=38, until=C("Even simple houses", -0.3)),
                 co("Simple houses: $10,000+ a month in rent", 960, 960, C("Even simple houses"), "risk", screen=True, size=38)]},
    sources=["lse"])
stage("s14_total", "m2_total", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In just four years"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=1000, y=220, at=C("all the land in Japan"), prefix="$", suffix="tn", decimals=1, steps=[[0, 0], [{"cue": "all the land in Japan was worth", "offset": 2}, 15.2]], text="ALL JAPANESE LAND, END-1989 (H.10)"),
              it("tower", x=1500, text="1985", color="#78909C", h=250, at=C("In just four years"), scale=0.7),
              it("tower", x=1800, text="1989", color="#C62828", h=[[0, 40], [{"cue": "had", "offset": 1}, 520]], at=C("In just four years"), scale=0.7)],
    "callouts": [co("End-1989: ≈ {{landvalue.display}} of land", 960, 960, C("By the end of"), "gold", screen=True, size=40, sub="LSE paper; converted at H.10 (143.80 per $)", until=C("In just four years", -0.3)),
                 co("More than doubled since 1985", 960, 960, C("In just four years"), "risk", screen=True, size=40)]},
    sources=["lse", "fred_jpy"])
stage("s15_banks", "m2_banks", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Land was the collateral"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("magnifier", x=[[0, 700], [6, 1000]], y=[[0, 520], [6, 480]], at=C("When the Ministry of Finance inspected"), scale=0.8),
              it("docs", x=1000, y=580, at=C("inspected them"), text="BANK INSPECTION", scale=0.6, stamp="LAND LOANS ↑", stampAt=C("significantly increased")),
              it("docs", x=1700, y=580, at=C("checks on those land loans"), text="LOAN CHECKS", scale=0.6, stamp="INCOMPLETE", stampAt=C("were incomplete"))],
    "callouts": [co("MOF inspections: land and zaitech loans soared", 960, 960, C("When the Ministry"), "white", screen=True, size=36, sub="Ministry of Finance Japan", until=C("Land was the collateral", -0.3)),
                 co("Land: the collateral behind almost everything", 960, 960, C("Land was the collateral"), "gold", screen=True, size=38)]},
    sources=["mof"])
add("p16_compare", "m2_draw", "engine_draw", {
    "title": "Japan vs America", "board": BOARD, "draw_start": C("Here is the United States"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(760, 330, 300, 170) + " " + rect(1200, 400, 60, 30), "color": "muted", "width": 4, "start": C("Here is the United States"), "label": lbl("AREA: US ≈ 25× JAPAN", 1010, 540, 22, "muted")},
        {"d": "M 760 840 L 1480 840 M 760 840 L 760 570", "color": "ink", "width": 4, "start": C("Here is the value")},
        {"d": "M 820 840 L 820 790 L 960 790 L 960 840", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.4, "kind": "bar", "start": C("Here is the value"), "label": lbl("US LAND VALUE", 890, 880, 20, "accent2")},
        {"d": "M 1320 840 L 1320 600 L 1460 600 L 1460 840", "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("value of Japan's land"), "label": lbl("JAPAN ≈ 4.1×", 1390, 580, 22, "risk")},
        {"d": "M 1000 700 L 1180 700", "color": "accent", "width": 5, "start": C("a hundred times"), "label": lbl("1 acre: 100×", 1090, 680, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("About four times bigger", 0.2), "dur": 1.4, "target": [1390, 640]}],
    "scale": 0.86, "floor": 1040}, sources=["lse"])
stage("s17_palace", "m2_palace", {
    "zones": [Z("district", night=True)], "worldW": 2600, "night": True, "min_seconds": 20,
    "cam": [{"at": 0, "x": 1100, "y": 480, "zoom": 1.1}, {"at": C("Valued at the price"), "x": 1200, "y": 520, "zoom": 0.92, "dur": 2.6}], "drift": 1,
    "items": [scale_item(1200, at=0.2, scale=1.45, tilt=-18, balanceAt=C("worth as much as all of California")),
              it("letters", x=1200, y=130, text="ON PAPER", at=C("But on paper"), size=64, color="gold")],
    "callouts": [co("The Imperial Palace: a walled garden in central Tokyo", 960, 960, C("The Imperial Palace sits"), "white", screen=True, size=34, until=C("Valued at the price", -0.3)),
                 co("At neighbouring prices: worth all of California (est.)", 960, 960, C("Valued at the price"), "gold", screen=True, size=34, sub="LSE paper", until=C("It was never for sale", -0.3)),
                 co("Never for sale. Priceless on paper.", 960, 960, C("It was never for sale"), "risk", screen=True, size=40)]},
    sources=["lse"])
kinetic("s18_t2", "m2_transition", [("The last trading day of 1989", 56, "the last trading day", None, True), ("The stock market peaks", 64, "hit its peak", "gold", False)])

# ====================================================================== PART 3: the pin
card("s19_c3", "m3_card", "The Pin", "1989-1990")
stage("s20_q3", "m3_question", {
    "zones": [Z("parliament")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("burst", x=960, y=420, at=3.5), it("letters", x=960, y=420, text="?", at=0.5, until=3.4, size=140, color="gold")],
    "callouts": [co("What pops a bubble this big?", 960, 150, C("What pops"), "gold", screen=True, size=44)]})
stage("s21_rates", "m3_rates", {
    "zones": [Z("parliament")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In just over a year"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=1000, y=230, at=C("Interest rates"), suffix="%", decimals=2, steps=[[0, 2.5], [{"cue": "began to raise them", "offset": 0.5}, 3.25], [{"cue": "Then again in October"}, 3.75], [{"cue": "Christmas Day"}, 4.25], [{"cue": "In March"}, 5.25], [{"cue": "the rate reached", "offset": 0.5}, 6.0]], text="OFFICIAL DISCOUNT RATE (BOJ)"),
              it("calendar", x=1600, y=320, at=C("In May"), pages=[[0, "MAY", "1989"], [{"cue": "Then again in October"}, "OCT", "1989"], [{"cue": "Christmas Day"}, "DEC 25", "1989"], [{"cue": "In March"}, "MAR", "1990"], [{"cue": "in August"}, "AUG", "1990"]], scale=0.8),
              it("letters", x=1500, y=620, text="2.5% → 6%", at=C("In just over a year"), size=70, color="risk")],
    "callouts": [co("May 1989 → Aug 1990: five rate rises", 960, 960, C("In May"), "white", screen=True, size=38, sub="BOJ data, Ministry of Finance Japan", until=C("In just over a year", -0.3)),
                 co("The price of money more than doubled", 960, 960, C("In just over a year"), "risk", screen=True, size=40)]},
    sources=["mof"])
stage("s22_warning", "m3_warning", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And Yamaichi's top management"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("chart", x=900, y=420, w=500, h=300, at=C("His model"), dur=2.5, text="BOND YIELD vs EARNINGS YIELD", pts=[0.3, 0.4, 0.6, 0.8, 0.95], color="risk"),
              it("letters", x=900, y=180, text="DANGER: APRIL 1989", at=C("flashed a danger signal"), size=54, color="risk"),
              *crowd([1600, 1720, 1840], "stand", at=C("And Yamaichi's top management"), scale=0.7),
              it("docs", x=1750, y=560, at=C("did not listen"), text="WARNING", scale=0.55, stamp="IGNORED", stampAt=C("did not listen", 0.3))],
    "callouts": [co("April 1989: a crash signal, but not a date", 960, 960, C("His model"), "gold", screen=True, size=38, sub="LSE paper (Ziemba)", until=C("And Yamaichi's top management", -0.3)),
                 co("Yamaichi's bosses did not listen", 960, 960, C("And Yamaichi's top management"), "risk", screen=True, size=40)]},
    sources=["lse"])
stage("s23_crash", "m3_crash", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By October"), "x": 1500, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=1000, y=220, at=C("the Nikkei index closed"), steps=[[0, 38916], [{"cue": "it fell", "offset": 0.5}, 38916], [{"cue": "By October", "offset": 2}, 20222]], text="NIKKEI 225"),
              it("chart", x=1000, y=500, w=600, h=300, at=C("From the very first"), dur=4, text="1990", pts=[0.95, 0.8, 0.7, 0.55, 0.5], color="risk"),
              it("letters", x=1700, y=300, text="−48%", at=C("it had lost"), size=120, color="risk"),
              *crowd([1600, 1720, 1840], "worry", at=C("By October"), scale=0.7)],
    "callouts": [co("Peak: 38,916 at the end of 1989", 960, 960, C("On the last trading day"), "white", screen=True, size=40, sub="LSE paper", until=C("By October", -0.3)),
                 co("Oct 1, 1990: 20,222 (−48%)", 960, 960, C("By October"), "risk", screen=True, size=42)]},
    sources=["lse"])
stage("s24_soros", "m3_soros", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A bubble can stay"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=600, y=300, at=C("in nineteen eighty-eight"), pages=[[0, "1988", "TOO EARLY"]], scale=0.8),
              it("arrow", **{"from": [800, 300], "to": [1300, 600]}, at=C("bet against the Japanese market")),
              it("stack", x=1500, h=[[0, 300], [{"cue": "and lost", "offset": 1.5}, 40]], at=C("bet against"), text="−$1BN", sub="too early", color="#C62828"),
              it("clock", x=1900, y=330, at=C("A bubble can stay"), period=1.6)],
    "callouts": [co("Soros shorted too early (1988): ≈ −$1bn", 960, 960, C("Even famous investors"), "risk", screen=True, size=38, sub="LSE paper", until=C("A bubble can stay", -0.3)),
                 co("Being right too early = being wrong", 960, 960, C("A bubble can stay"), "gold", screen=True, size=40)]},
    sources=["lse"])
stage("s25_land", "m3_land", {
    "zones": [Z("parliament")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("So in March"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [*crowd([700, 820, 940], "cheer", at=C("the public stayed bullish"), scale=0.7),
              it("docs", x=1600, y=560, at=C("So in March"), text="'SŌRYŌ KISEI' · MAR 1990", scale=0.6, stamp="LIMIT LAND LOANS", stampAt=C("It told banks")),
              it("barrier", x=2100, at=C("The flow of new money"), closeAt=C("was cut off"), scale=0.9)],
    "callouts": [co("Land held on: the public stayed bullish", 960, 960, C("Land held on"), "white", screen=True, size=38, sub="Ministry of Finance Japan", until=C("So in March", -0.3)),
                 co("March 1990: caps on real-estate lending", 960, 960, C("So in March"), "gold", screen=True, size=40)]},
    sources=["mof"])
kinetic("s26_t3", "m3_transition", [("First the shares fell", 60, "First the shares fell", None, False), ("Then the golf clubs. Then the land.", 54, "Then the golf clubs", "risk", False)])

# ====================================================================== PART 4: the long fall
card("s27_c4", "m4_card", "The Long Fall", "1991-2010s")
stage("s28_q4", "m4_question", {
    "zones": [Z("city")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("chart", x=960, y=420, w=600, h=320, at=0.3, dur=5, text="LAND PRICES", pts=[0.95, 0.85, 0.7, 0.55, 0.45], color="risk")],
    "callouts": [co("When land stops going up…", 960, 150, C("What happens"), "gold", screen=True, size=44)]})
stage("s29_golf", "m4_golf", {
    "zones": [Z("hills")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("It fell after"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("sign", x=800, y=300, text="GOLF CLUB MEMBERSHIP", sub="traded like a share", at=C("memberships of golf clubs"), color="#C8E6C9", size=30),
              it("chart", x=1600, y=420, w=520, h=300, at=C("that market was an even bigger bubble"), dur=3, text="GOLF MEMBERSHIPS vs NIKKEI", pts=[0.2, 0.6, 0.95, 0.5, 0.2], color="green"),
              it("letters", x=1600, y=180, text="1991: LAND TURNS", at=C("from nineteen ninety-one"), size=54, color="risk")],
    "callouts": [co("Golf memberships: a bigger bubble than stocks", 960, 960, C("according to the researchers"), "gold", screen=True, size=38, sub="LSE paper", until=C("Then, from", -0.3)),
                 co("From 1991: land begins a long decline", 960, 960, C("Then, from"), "risk", screen=True, size=40)]},
    sources=["lse"])
add("p30_reverse", "m4_draw", "engine_draw", {
    "title": "The machine in reverse", "board": BOARD, "draw_start": C("Here is the loop from before"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(580, 360, 240, 120), "color": "risk", "width": 6, "kind": "box", "start": C("Land prices fall"), "label": lbl("LAND ↓", 700, 428, 28, "risk")},
        {"d": rect(1060, 360, 240, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("The banks are left with bad loans"), "label": lbl("BAD LOANS", 1180, 428, 26, "accent2")},
        {"d": rect(820, 620, 240, 120), "color": "accent", "width": 6, "kind": "box", "start": C("Companies cannot borrow"), "label": lbl("FORCED SALES", 940, 688, 24, "accent")},
        {"d": arrow((830, 420), (1050, 420), 0.1), "color": "ink", "width": 5, "start": C("worth less")},
        {"d": arrow((1180, 490), (1000, 610), -0.2), "color": "ink", "width": 5, "start": C("they stop lending")},
        {"d": arrow((820, 640), (700, 490), -0.2), "color": "ink", "width": 5, "start": C("That pushes prices down again"), "label": lbl("prices ↓", 660, 600, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("takes it apart", 0.2), "dur": 1.4, "target": [940, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["lse"])
stage("s31_lost", "m4_lost", {
    "zones": [Z("city", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Some of the biggest names"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 2,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "1990s", "LOST"], [3.0, "2000s", "LOST"], [6.0, "2010s", "LOST"]], scale=0.8),
              *crowd([900, 1020, 1140], "worry", at=C("a lost generation"), scale=0.7),
              it("building", x=1800, at=C("Some of the biggest names"), text="YAMAICHI SECURITIES", scale=0.7),
              it("docs", x=1800, y=600, at=C("was bankrupt"), text="1990s", scale=0.5, stamp="BANKRUPT", stampAt=C("was bankrupt", 0.3))],
    "callouts": [co("'Two decades of deflation… a lost generation'", 960, 960, C("The researchers describe"), "white", screen=True, size=36, sub="LSE paper", until=C("Some of the biggest names", -0.3)),
                 co("Yamaichi, once Japan's no. 4 broker: bankrupt", 960, 960, C("Some of the biggest names"), "risk", screen=True, size=36)]},
    sources=["lse"])
kinetic("s32_t4", "m4_transition", [("And the stock market waited", 58, "the stock market waited", None, False), ("and waited", 70, "and waited, for", "gold", False)])

# ====================================================================== PART 5: thirty-four years
card("s33_c5", "m5_card", "Thirty-Four Years", "1989-2024")
stage("s34_q5", "m5_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("clock", x=960, y=380, at=0.3, period=1.2)],
    "callouts": [co("How long does recovery take?", 960, 150, C("How long"), "gold", screen=True, size=44)]})
stage("s35_record", "m5_record", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A whole generation"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=0.2, pages=[[0, "FEB 22", "2024"]], scale=0.8),
              it("counter", x=1000, y=220, at=C("the Nikkei finally closed"), decimals=2, steps=[[0, 38915.87], [{"cue": "It had taken", "offset": -0.5}, 39098.68]], text="NIKKEI 225 CLOSE"),
              it("burst", x=1000, y=400, at=C("It had taken")),
              *[it("person", x=1500 + 140 * k, pose="stand", at=C("A whole generation", 0.3 * k), scale=0.55 + 0.08 * k, hair=k + 1, skin=k % 4) for k in range(4)]],
    "callouts": [co("Feb 22, 2024: 39,098.68 beats the 1989 record", 960, 960, C("On February"), "gold", screen=True, size=38, sub="AP", until=C("A whole generation", -0.3)),
                 co("34 years: a whole generation", 960, 960, C("A whole generation"), "white", screen=True, size=40)]},
    sources=["ap_2024"])
stage("s36_compare", "m5_compare", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1100, "y": 500, "zoom": 1.0}, {"at": C("When cheap money meets"), "x": 1200, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 2,
    "items": [scale_item(1100, at=0.2, scale=1.3, tilt=0, to=22, balanceAt=0.8),
              it("letters", x=1100, y=130, text="PRICE = HOW MUCH YOU CAN BORROW", at=C("They start measuring"), size=44, color="gold")],
    "callouts": [co("Today, nobody believes the comparison", 960, 960, C("Today, nobody thinks"), "white", screen=True, size=38, until=C("When cheap money meets", -0.3)),
                 co("Cheap money + 'can never fall' = bubble", 960, 960, C("When cheap money meets"), "gold", screen=True, size=38)]},
    sources=["lse"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("district", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("When the borrowing stopped"), "x": 1500, "y": 520, "zoom": 0.9, "dur": 2.6}], "drift": 2,
    "items": [it("pricetag", x=900, y=330, at=0.2, pages=[[0, "$15 TRILLION"], [{"cue": "When the borrowing stopped"}, "?"]], sub="on paper"),
              it("coins", **{"from": [-200, 300], "to": [900, 450]}, at=C("kept borrowing", -2), rate=6, until=C("When the borrowing stopped")),
              scale_item(1800, at=C("Every bubble since"), scale=0.7, tilt=-12, balanceAt=C("The trick is"))],
    "callouts": [co("Real on paper, impossible in practice", 960, 150, C("That a price can be real"), "white", screen=True, size=40, until=C("When the borrowing stopped", -0.3)),
                 co("No borrowing, no belief", 960, 150, C("When the borrowing stopped"), "risk", screen=True, size=42, until=C("Every bubble since", -0.3)),
                 co("Every bubble has its 'palace = California'", 960, 150, C("Every bubble since"), "gold", screen=True, size=38)]},
    sources=["lse"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_tokyo_storyboard.py; edit the generator, not this file.\n"
           "# Episode 23 storyboard (Japan's bubble): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
