"""Generates projects/how-one-company-made-diamonds-a-symbol-of-love/deliverables/documentary/storyboard.yaml (Episode 24, De Beers).

Bespoke worlds (tones from visual_direction.yaml: spectacle -> strategy -> crisis -> reflective): a 1870s mining field
of Kimberley, a London sorting room with the selling box, a 1940s advertising office where four words are typed, a
1950s jewellery window with a price tag, a courtroom, a lab with grown stones, and a boardroom for the sale.
The new `gem` item (a brilliant-cut diamond that sparkles, and greys out as its price story fades) is the through-line.
Presenter: the cartel box (boxes + arrows), the two halves of the machine (boxes + arrows), the price gap (bars / lines).
No De Beers logo or real ads (the slogan is quoted as text), no likeness of real people (names in text only).
Run: python tools/gen_debeers_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-one-company-made-diamonds-a-symbol-of-love/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
LAB = "#E1BEE7"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("vault", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 3.0, "x": 1000, "y": 500, "zoom": 1.0, "dur": 3.0}], "drift": 1,
    "items": [it("gem", x=1000, y=430, at=0.2, scale=1.3)],
    "callouts": [co("Love → a small, clear stone. Who decided?", 960, 960, C("Why does a promise"), "gold", screen=True, size=40)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("vault", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 500, "zoom": 1.0}, {"at": C("And in"), "x": 1500, "y": 500, "zoom": 1.05, "dur": 2.4},
            {"at": C("Today, the company"), "x": 2100, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 2,
    "items": [it("counter", x=800, y=220, at=C("it controlled"), suffix="%", steps=[[0, 0], [{"cue": "of the world's rough diamonds", "offset": 0.5}, 80]], text="SHARE OF ROUGH SALES (UP TO)"),
              it("gem", x=800, y=520, at=0.2, scale=0.8),
              it("letters", x=1500, y=300, text="A DIAMOND IS FOREVER", at=C("A diamond is forever"), size=60, color="gold"),
              it("pricetag", x=2100, y=320, at=C("Today, the company"), pages=[[0, "FOR SALE"]], sub="2026"),
              it("gem", x=2100, y=560, at=C("Today, the company"), scale=0.6, dimAt=C("being sold off"))],
    "callouts": [co("De Beers controlled 75–80% of rough diamond sales", 960, 960, C("it controlled"), "white", screen=True, size=36, sub="GIA", until=C("And in", -0.3)),
                 co("1947: four words", 960, 960, C("And in"), "gold", screen=True, size=42, sub="Adweek", until=C("Today, the company", -0.3)),
                 co("Today: the diamond king is for sale", 960, 960, C("Today, the company"), "risk", screen=True, size=40, sub="Anglo American")]},
    sources=["gia", "adweek", "anglo_2025"])

# ====================================================================== PART 1: the cartel
card("s03_c1", "m1_card", "The Cartel", "Kimberley, 1870s-1929")
stage("s04_q1", "m1_question", {
    "zones": [Z("site")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("gem", x=960, y=640, at=0.3, n=5, gap=180, scale=0.6)],
    "callouts": [co("Too many diamonds, how to keep them valuable?", 960, 150, C("How do you keep"), "gold", screen=True, size=38)]})
stage("s05_kimberley", "m1_kimberley", {
    "zones": [Z("site")], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Two rivals"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("Both men agreed"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("crane", x=700, at=0.2, progress=0.3, scale=0.7),
              it("chart", x=900, y=360, w=460, h=260, at=C("prices swung wildly"), dur=2.5, text="DIAMOND PRICES", pts=[0.8, 0.3, 0.9, 0.2, 0.7], color="risk"),
              *[it("person", x=1450 + 250 * k, pose="stand", at=C("Two rivals", 0.4 * k), scale=0.75, hair=k + 1, skin=k) for k in range(2)],
              it("sign", x=1575, y=280, text="RHODES vs BARNATO", sub="the fight for Kimberley", at=C("Two rivals"), color="#FFE082", size=30),
              it("calendar", x=2000, y=300, at=C("Rhodes won"), pages=[[0, "1888", "KIMBERLEY"]], scale=0.8),
              it("letters", x=2300, y=600, text="CONTROL SUPPLY", at=C("Both men agreed"), size=64, color="gold")],
    "callouts": [co("Early 1870s: diamond rush at Kimberley", 960, 960, C("In the early"), "white", screen=True, size=40, sub="GIA", until=C("Two rivals", -0.3)),
                 co("1888: De Beers Consolidated Mines", 960, 960, C("Rhodes won"), "gold", screen=True, size=40, until=C("Both men agreed", -0.3)),
                 co("The rule: control how many come out of the ground", 960, 960, C("Both men agreed"), "white", screen=True, size=34)]},
    sources=["gia"])
stage("s06_syndicate", "m1_syndicate", {
    "zones": [Z("office")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("It sorted the stones"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [*[it("person", x=500 + 110 * k, pose="read", at=C("ten diamond dealers", 0.1 * k), scale=0.5, hair=k % 5, skin=k % 4) for k in range(10)],
              it("contract", x=1100, y=330, at=C("signed a deal"), text="BUY ALL PRODUCTION", sub="London syndicate", scale=0.55),
              it("conveyor", x=1700, y=F - 40, at=C("It sorted the stones"), n=6, speed=1.0, goods="box"),
              it("gem", x=1700, y=420, at=C("thousands of categories"), n=4, gap=150, scale=0.4),
              it("letters", x=2300, y=220, text="PRICES IT SET", at=C("at prices it set"), size=56, color="gold")],
    "callouts": [co("Ten London dealers buy everything", 960, 960, C("So De Beers signed"), "white", screen=True, size=40, sub="GIA", until=C("It sorted the stones", -0.3)),
                 co("'Sights': fixed prices, approved buyers only", 960, 960, C("It sorted the stones"), "gold", screen=True, size=38)]},
    sources=["gia"])
stage("s07_anglo", "m1_anglo", {
    "zones": [Z("exchange")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("With American backers"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("Remember that name"), "x": 2200, "y": 500, "zoom": 1.1, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "1907", "CRASH"], [{"cue": "First World War"}, "1914-18", "WAR"]], scale=0.8),
              it("storm", x=900, y=220, at=C("nearly collapsed twice"), scale=0.6),
              it("building", x=1600, at=C("he created a mining firm"), text="ANGLO AMERICAN", scale=0.75),
              it("arrow", **{"from": [1750, 450], "to": [2150, 450]}, at=C("to take over")),
              it("building", x=2300, at=C("to take over"), text="DE BEERS", scale=0.75),
              it("letters", x=2300, y=180, text="1929", at=C("By"), size=80, color="gold")],
    "callouts": [co("Oppenheimer builds Anglo American", 960, 960, C("With American backers"), "white", screen=True, size=40, sub="GIA", until=C("Remember that name", -0.3)),
                 co("Remember the name: it will sell De Beers", 960, 960, C("Remember that name"), "gold", screen=True, size=38)]},
    sources=["gia"])
add("p08_cartel", "m1_draw", "engine_draw", {
    "title": "How the cartel worked", "board": BOARD, "draw_start": C("Here are the mines"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 330, 180, 90) + " " + rect(560, 460, 180, 90) + " " + rect(560, 590, 180, 90), "color": "accent3", "width": 5, "kind": "box", "start": C("Here are the mines"), "label": lbl("MINES", 650, 310, 24, "accent3")},
        {"d": rect(900, 420, 260, 170), "color": "accent", "width": 7, "fill": "accent", "fillOpacity": 0.2, "kind": "box", "start": C("into one box"), "label": lbl("THE SELLING BOX", 1030, 512, 22, "accent")},
        {"d": arrow((750, 375), (890, 470), 0.1) + " " + arrow((750, 505), (890, 505), 0.0) + " " + arrow((750, 635), (890, 545), -0.1), "color": "ink", "width": 4, "kind": "arrow", "start": C("All their stones flow")},
        {"d": rect(1300, 460, 180, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("approved buyers"), "label": lbl("BUYERS", 1390, 512, 22, "accent2")},
        {"d": arrow((1170, 505), (1290, 505), 0.0), "color": "ink", "width": 4, "start": C("From there")},
        {"d": rect(940, 700, 180, 80), "color": "risk", "width": 5, "kind": "box", "start": C("the box simply kept the diamonds"), "label": lbl("STOCKPILE", 1030, 748, 22, "risk")},
        {"d": "M 1030 600 L 1030 690", "color": "risk", "width": 4, "start": C("the box simply kept the diamonds", 0.3)},
        {"d": "M 1300 800 L 1340 760 L 1380 720 L 1420 700 L 1460 680", "color": "accent3", "width": 5, "start": C("never came down"), "label": lbl("price: only up", 1380, 820, 22, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("And here is the trick", 0.2), "dur": 1.4, "target": [1030, 740]}],
    "scale": 0.86, "floor": 1040}, sources=["gia"])
stage("s09_share", "m1_share", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("It did not need"), "x": 1500, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("tower", x=800, text="OWN MINES ≈ 45%", color="#78909C", h=[[0, 20], [{"cue": "by value", "offset": 1}, 230]], at=C("De Beers' own mines"), scale=0.8),
              it("tower", x=1150, text="CONTROLLED ≈ 80%", color="#FFB300", h=[[0, 20], [{"cue": "around eighty percent", "offset": 1}, 410]], at=C("But through its contracts"), scale=0.8),
              it("gem", x=1800, y=420, at=C("It did not need"), scale=0.9, label="ONE PLACE TO SELL", textc="#FFFFFF")],
    "callouts": [co("1980s: mined ≈ 45%, controlled ≈ 80%", 960, 960, C("By the nineteen eighties"), "gold", screen=True, size=40, sub="GIA", until=C("It did not need", -0.3)),
                 co("Own the market, not the mines", 960, 960, C("It did not need"), "white", screen=True, size=40)]},
    sources=["gia"])
kinetic("s10_t1", "m1_transition", [("Supply was half the job", 60, "half the job", None, False), ("The other half: demand", 64, "creating demand", "gold", False)])

# ====================================================================== PART 2: a diamond is forever
card("s11_c2", "m2_card", "A Diamond Is Forever", "1938-1957")
stage("s12_q2", "m2_question", {
    "zones": [Z("shop")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("gem", x=960, y=440, at=0.3, scale=1.0), *crowd([500, 1420], "stand", at=1.0, scale=0.7)],
    "callouts": [co("How do you make people want a stone?", 960, 150, C("How do you make"), "gold", screen=True, size=42)]})
stage("s13_1938", "m2_1938", {
    "zones": [Z("city")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("He traveled to Philadelphia"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=0.2, pages=[[0, "SEP", "1938"]], scale=0.8),
              it("chart", x=900, y=400, w=440, h=260, at=C("diamond prices were falling"), dur=2.5, text="DIAMOND PRICES", pts=[0.8, 0.6, 0.45, 0.3, 0.2], color="risk"),
              it("plane", x=[[0, 1100], [{"cue": "He traveled", "offset": 4}, 1600]], y=[[0, 300], [{"cue": "He traveled", "offset": 4}, 260]], at=C("decided the company's future"), scale=0.55, text="TO AMERICA"),
              it("building", x=1800, at=C("He traveled to Philadelphia"), text="N.W. AYER & SON · PHILADELPHIA", scale=0.7),
              it("gem", x=2300, y=420, at=C("draped diamonds"), scale=0.6)],
    "callouts": [co("1938: prices falling, war coming", 960, 960, C("In September"), "risk", screen=True, size=40, sub="Adweek", until=C("He traveled to Philadelphia", -0.3)),
                 co("The bet: sell diamonds to America", 960, 960, C("He traveled to Philadelphia"), "gold", screen=True, size=40)]},
    sources=["adweek"])
stage("s14_gerety", "m2_gerety", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True, "min_seconds": 16,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("A diamond is forever"), "x": 1100, "y": 480, "zoom": 1.2, "dur": 2.4}], "drift": 1,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "1947", "N.W. AYER"]], scale=0.8),
              it("desk", x=1000, at=0.3, scale=0.9),
              it("person", x=1250, pose="read", at=0.4, scale=0.8, hair=6, skin=0),
              it("paper", x=1000, y=380, at=C("a photo of a honeymooning couple"), text="A DIAMOND IS FOREVER", name="COPY · 1947", scale=0.8),
              it("gem", x=1700, y=420, at=C("De Beers adopted the line"), scale=0.8)],
    "callouts": [co("Copywriter Frances Gerety, 1947", 960, 960, C("a young copywriter"), "white", screen=True, size=40, sub="Adweek", until=C("A diamond is forever", -0.3)),
                 co("'A Diamond Is Forever'", 960, 960, C("A diamond is forever"), "gold", screen=True, size=48)]},
    sources=["adweek"])
stage("s15_meaning", "m2_meaning", {
    "zones": [Z("shop")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And since grooms"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("gem", x=900, y=420, at=0.2, scale=0.9, label="A PROMISE"),
              it("letters", x=900, y=160, text="NOT A GEM. A PROMISE.", at=C("A diamond stopped being a gem"), size=50, color="gold"),
              it("counter", x=1700, y=220, at=C("And since grooms"), suffix="%", steps=[[0, 0], [{"cue": "nine out of ten", "offset": 1}, 90]], text="DIAMOND BUYERS WHO ARE GROOMS"),
              *crowd([1600, 1720, 1840], "stand", at=C("the ads spoke straight to them"), scale=0.7)],
    "callouts": [co("Not beauty, not wealth: love that lasts", 960, 960, C("The genius was"), "white", screen=True, size=40, until=C("And since grooms", -0.3)),
                 co("Grooms: 9 in 10 diamond buyers", 960, 960, C("And since grooms"), "gold", screen=True, size=40, sub="Adweek")]},
    sources=["adweek"])
stage("s16_price", "m2_price", {
    "zones": [Z("shop")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("At the time"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "1957", "AD"]], scale=0.8),
              it("pricetag", x=1000, y=320, at=C("listed a one carat diamond"), pages=[[0, "1 CARAT: $600–$1,210"]], sub="1957 ad"),
              it("gem", x=1000, y=600, at=C("listed a one carat"), scale=0.6),
              it("stack", x=1700, h=[[0, 40], [{"cue": "a month", "offset": 1}, 140]], at=C("At the time"), text="$417 / MONTH", sub="average take-home pay")],
    "callouts": [co("1957: one carat for $600–$1,210", 960, 960, C("A De Beers advertisement"), "gold", screen=True, size=40, sub="Adweek", until=C("At the time", -0.3)),
                 co("…when men took home $417 a month", 960, 960, C("At the time"), "white", screen=True, size=40)]},
    sources=["adweek"])
add("p17_halves", "m2_draw", "engine_draw", {
    "title": "The two halves of the machine", "board": BOARD, "draw_start": C("On one side, the cartel"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 260, 130), "color": "accent2", "width": 6, "kind": "box", "start": C("On one side, the cartel"), "label": lbl("CARTEL: SUPPLY ↓", 690, 432, 22, "accent2")},
        {"d": rect(1220, 360, 260, 130), "color": "accent", "width": 6, "kind": "box", "start": C("On the other side, the slogan"), "label": lbl("SLOGAN: DEMAND ↑", 1350, 432, 22, "accent")},
        {"d": rect(890, 600, 260, 130), "color": "risk", "width": 7, "fill": "risk", "fillOpacity": 0.15, "kind": "box", "start": C("the price in the middle rises"), "label": lbl("PRICE ↑", 1020, 672, 30, "risk")},
        {"d": arrow((700, 500), (890, 640), 0.15), "color": "ink", "width": 5, "start": C("Supply down")},
        {"d": arrow((1340, 500), (1150, 640), -0.15), "color": "ink", "width": 5, "start": C("demand up")},
        {"d": "M 1180 760 Q 1300 820 1440 780", "color": "muted", "width": 4, "start": C("nobody wanted to sell theirs back"), "label": lbl("no resale", 1450, 820, 22, "muted", "start")},
    ],
    "actions": [{"kind": "point", "at": C("the price in the middle rises", 0.3), "dur": 1.4, "target": [1020, 660]}],
    "scale": 0.86, "floor": 1040}, sources=["gia", "adweek"])
kinetic("s18_t2", "m2_transition", [("The machine worked for decades", 56, "worked almost perfectly", None, False), ("Then the world changed", 64, "the world changed", "risk", False)])

# ====================================================================== PART 3: cracks
card("s19_c3", "m3_card", "Cracks", "1994-2003")
stage("s20_q3", "m3_question", {
    "zones": [Z("vault")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vaultdoor", x=960, at=0.2, openAt=2.5, scale=0.8), it("gem", x=960, y=430, at=3.0, n=3, gap=200, scale=0.5)],
    "callouts": [co("Can a cartel outlive its world?", 960, 150, C("Can a cartel"), "gold", screen=True, size=42)]})
stage("s21_usa", "m3_usa", {
    "zones": [Z("court")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Only in two thousand four"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=C("In nineteen ninety-four"), pages=[[0, "1994", "INDICTED"], [{"cue": "Only in two thousand four"}, "2004", "PLEA"]], scale=0.8),
              it("docs", x=1000, y=580, at=C("indicted the company"), text="INDICTMENT: PRICE FIXING", scale=0.6, stamp="NO JURISDICTION", stampAt=C("the court had no hold")),
              it("gavel", x=1600, y=420, hits=[C("finally plead guilty", 0.3)]),
              it("stack", x=2100, h=[[0, 40], [{"cue": "pay a fine of", "offset": 1}, 180]], at=C("pay a fine of"), text="$10M FINE", sub="2004 guilty plea")],
    "callouts": [co("1994: US indictment (industrial diamonds)", 960, 960, C("In nineteen ninety-four"), "white", screen=True, size=38, sub="US DOJ", until=C("Only in two thousand four", -0.3)),
                 co("2004: guilty plea, $10 million fine", 960, 960, C("Only in two thousand four"), "risk", screen=True, size=40, sub="US DOJ")]},
    sources=["doj_2004"])
stage("s22_soviet", "m3_soviet", {
    "zones": [Z("site")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("In nineteen ninety-eight"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("barrier", x=800, at=0.2, closeAt=0.3, openAt=C("Moscow lost its tight grip"), scale=1.0),
              it("gem", x=[[0, 700], [{"cue": "Moscow lost", "offset": 5}, 1300]], y=600, at=C("Moscow lost"), n=3, gap=120, scale=0.4),
              it("crane", x=1800, at=C("Canada opened"), progress=0.8, scale=0.7),
              it("sign", x=1800, y=250, text="CANADA'S FIRST DIAMOND MINE", sub="1998 · sells most stones itself", at=C("Canada opened"), color="#BBDEFB", size=26),
              it("arrow", **{"from": [2000, 500], "to": [2500, 500]}, at=C("without passing through De Beers"))],
    "callouts": [co("Soviet breakup: supply escapes", 960, 960, C("When the Soviet Union"), "white", screen=True, size=40, sub="GIA", until=C("In nineteen ninety-eight", -0.3)),
                 co("Canada sells around the cartel", 960, 960, C("In nineteen ninety-eight"), "gold", screen=True, size=40)]},
    sources=["gia"])
stage("s23_stockpile", "m3_stockpile", {
    "zones": [Z("vault")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("By two thousand three"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("vaultdoor", x=800, at=0.2, openAt=C("It sold off its great stockpile"), scale=0.7),
              it("coins", **{"from": [800, 500], "to": [1600, 300]}, at=C("It sold off", 0.5), rate=6, until=C("By two thousand three")),
              it("tower", x=1600, text="1900s ≈ 80%", color="#FFB300", h=410, at=C("By two thousand three"), scale=0.7),
              it("tower", x=1900, text="2003: 65%", color="#C62828", h=[[0, 410], [{"cue": "had fallen to", "offset": 1}, 330]], at=C("By two thousand three"), scale=0.7),
              it("chart", x=2400, y=420, w=420, h=260, at=C("as more stones were sold at auction"), dur=2.5, text="ROUGH PRICES", pts=[0.5, 0.8, 0.3, 0.7, 0.4], color="risk")],
    "callouts": [co("The stockpile is sold; supply no longer held back", 960, 960, C("So De Beers changed"), "white", screen=True, size=36, sub="GIA", until=C("By two thousand three", -0.3)),
                 co("2003: 65% share · prices 'extremely volatile'", 960, 960, C("By two thousand three"), "gold", screen=True, size=36, sub="GIA")]},
    sources=["gia"])
kinetic("s24_t3", "m3_transition", [("The biggest threat was not a mine", 52, "did not come from a mine", None, False), ("It came from a laboratory", 60, "from a laboratory", "risk", False)])

# ====================================================================== PART 4: diamonds from a machine
card("s25_c4", "m4_card", "Diamonds From a Machine", "2018-2025")
stage("s26_q4", "m4_question", {
    "zones": [Z("fab")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("gem", x=700, y=430, at=0.3, scale=0.7, label="MINED"), it("gem", x=1250, y=430, at=1.5, scale=0.7, color=LAB, label="GROWN")],
    "callouts": [co("If anyone can make one, what is 'forever' worth?", 960, 150, C("What happens"), "gold", screen=True, size=38)]})
stage("s27_lab", "m4_lab", {
    "zones": [Z("fab")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("In twenty eighteen"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("conveyor", x=900, y=F - 40, at=0.2, n=6, speed=1.2, goods="box"),
              it("gem", x=900, y=420, at=C("grown in factories"), n=3, gap=160, scale=0.45, color=LAB),
              it("pricetag", x=1700, y=320, at=C("launched a lab-grown jewellery brand"), pages=[[0, "$800 / CARAT"]], sub="Lightbox, 2018"),
              it("letters", x=1700, y=620, text="CHEAP · DIFFERENT", at=C("a cheap, different product"), size=56, color="gold")],
    "callouts": [co("Same carbon, grown in a factory", 960, 960, C("Diamonds can now"), "white", screen=True, size=40, until=C("In twenty eighteen", -0.3)),
                 co("2018: De Beers' own lab brand, $800 a carat", 960, 960, C("In twenty eighteen"), "gold", screen=True, size=38, sub="De Beers Group")]},
    sources=["debeers_2025"])
stage("s28_cook", "m4_cook", {
    "zones": [Z("shop")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Lightbox was meant"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("gem", x=1000, y=420, at=0.2, scale=0.8, color=LAB),
              it("pricetag", x=1000, y=170, at=C("synthetics were selling for"), pages=[[0, "THOUSANDS OF $"]], sub="2018"),
              it("paper", x=1700, y=380, at=C("As De Beers' chief executive"), text="'almost as much as natural diamonds'", name="AL COOK, DE BEERS", scale=0.7)],
    "callouts": [co("2018: lab stones sold for thousands of dollars", 960, 960, C("At first"), "white", screen=True, size=38, sub="National Jeweler", until=C("Lightbox was meant", -0.3)),
                 co("Lightbox: show they deserve far less", 960, 960, C("Lightbox was meant"), "gold", screen=True, size=40)]},
    sources=["nj_2025"])
stage("s29_collapse", "m4_collapse", {
    "zones": [Z("fab")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("In twenty twenty-five"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=900, y=220, at=C("wholesale prices"), suffix="%", steps=[[0, 0], [{"cue": "fell by", "offset": 1}, -90]], text="LAB-GROWN WHOLESALE PRICE (DE BEERS)"),
              it("chart", x=900, y=520, w=520, h=280, at=C("collapsed"), dur=3, text="LAB DIAMOND PRICE", pts=[0.95, 0.7, 0.4, 0.2, 0.08], color="risk"),
              it("docs", x=1700, y=580, at=C("In twenty twenty-five"), text="LIGHTBOX", scale=0.6, stamp="CLOSED", stampAt=C("close Lightbox altogether")),
              it("conveyor", x=2200, y=F - 40, at=C("Factories could simply make more"), n=8, speed=2.0, goods="box")],
    "callouts": [co("Lab-grown wholesale prices: −90%", 960, 960, C("According to De Beers"), "risk", screen=True, size=42, sub="De Beers Group, May 2025", until=C("In twenty twenty-five", -0.3)),
                 co("2025: De Beers closes Lightbox", 960, 960, C("In twenty twenty-five"), "white", screen=True, size=40)]},
    sources=["debeers_2025"])
add("p30_gap", "m4_draw", "engine_draw", {
    "title": "The price of the story", "board": BOARD, "draw_start": C("Here is the price line"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 820 L 1460 820 M 560 820 L 560 330", "color": "ink", "width": 4, "start": C("Here is the price line")},
        {"d": "M 600 420 L 800 410 L 1000 430 L 1200 440 L 1400 450", "color": "accent", "width": 6, "start": C("Here is the price line", 0.5), "label": lbl("MINED STONE", 1400, 420, 22, "accent")},
        {"d": "M 600 470 L 800 600 L 1000 700 L 1200 760 L 1400 790", "color": "accent2", "width": 6, "start": C("Here is the line of a lab diamond"), "label": lbl("LAB STONE", 1400, 770, 22, "accent2")},
        {"d": "M 1280 440 L 1280 780 L 1330 780 L 1330 440", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.2, "kind": "bar", "start": C("the gap between them"), "label": lbl("THE STORY", 1305, 620, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("the price of the story", 0.2), "dur": 1.4, "target": [1305, 620]}],
    "scale": 0.86, "floor": 1040}, sources=["debeers_2025"])
kinetic("s31_t4", "m4_transition", [("And then the numbers", 66, "And then the numbers", None, False), ("reached the owner", 66, "reached the owner", "risk", False)])

# ====================================================================== PART 5: for sale
card("s32_c5", "m5_card", "For Sale", "2011-2026")
stage("s33_q5", "m5_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("gem", x=960, y=430, at=0.2, scale=1.0), it("pricetag", x=1400, y=300, at=1.2, pages=[[0, "$ ?"]], sub="today")],
    "callouts": [co("What is the diamond king worth now?", 960, 150, C("What is the diamond king"), "gold", screen=True, size=42)]})
stage("s34_2011", "m5_2011", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("That put a value"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=0.2, pages=[[0, "NOV", "2011"]], scale=0.8),
              it("contract", x=900, y=430, at=C("paid the Oppenheimer family"), text="40% OF DE BEERS", sub="$5.1bn cash", scale=0.6),
              it("counter", x=1700, y=220, at=C("That put a value"), prefix="≈ $", suffix="bn", decimals=2, steps=[[0, 0], [{"cue": "on the whole company", "offset": 0.5}, 12.75]], text="IMPLIED VALUE, 100%"),
              it("tower", x=1700, text="2011", color="#FFB300", h=520, at=C("That put a value"), scale=0.7)],
    "callouts": [co("2011: Anglo pays $5.1bn for 40%", 960, 960, C("In twenty eleven"), "gold", screen=True, size=40, sub="Anglo American", until=C("That put a value", -0.3)),
                 co("≈ $12.75bn for the whole company", 960, 960, C("That put a value"), "white", screen=True, size=40)]},
    sources=["anglo_2011"])
stage("s35_writedown", "m5_writedown", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It is now trying to sell"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("docs", x=1000, y=580, at=C("In its results"), text="ANGLO AMERICAN · FY2025", scale=0.6, stamp="$2.3BN IMPAIRMENT", stampAt=C("booked an impairment")),
              it("gem", x=1600, y=420, at=0.3, scale=0.8, dimAt=C("as diamond markets weakened")),
              it("pricetag", x=1600, y=180, at=C("It is now trying to sell"), pages=[[0, "FOR SALE"]], sub="2026")],
    "callouts": [co("FY2025: $2.3bn impairment on De Beers", 960, 960, C("In its results"), "risk", screen=True, size=40, sub="Anglo American, Feb 2026", until=C("It is now trying to sell", -0.3)),
                 co("Now: selling the diamond king", 960, 960, C("It is now trying to sell"), "white", screen=True, size=40)]},
    sources=["anglo_2025"])
stage("s36_sale", "m5_sale", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("But even as a rough guide"), "x": 1500, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("paper", x=900, y=380, at=C("Bloomberg reported"), text="'about $1 billion' (reported)", name="JULY 2026", scale=0.7),
              it("tower", x=1500, text="2011 ≈ $12.75BN", color="#FFB300", h=560, at=C("But even as a rough guide"), scale=0.7),
              it("tower", x=1850, text="2026 ≈ $1BN?", color="#C62828", h=[[0, 20], [{"cue": "Perhaps one billion", "offset": 0.5}, 60]], at=C("Perhaps one billion"), scale=0.7)],
    "callouts": [co("Reported: ≈ $1bn for Anglo's stake (unconfirmed)", 960, 960, C("Bloomberg reported"), "white", screen=True, size=36, sub="JCK, citing Bloomberg", until=C("But even as a rough guide", -0.3)),
                 co("≈ $13bn then · ≈ $1bn now (rough guide)", 960, 960, C("But even as a rough guide"), "gold", screen=True, size=38)]},
    sources=["jck_2026", "anglo_2011"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("vault", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.05}, {"at": C("The slogan still works"), "x": 1300, "y": 500, "zoom": 1.0, "dur": 2.6}], "drift": 1,
    "items": [it("gem", x=1000, y=430, at=0.2, scale=1.2, dimAt=C("But a story can only hold")),
              it("letters", x=1000, y=150, text="SUPPLY + STORY = PRICE", at=C("It is about who controls"), size=50, color="gold")],
    "callouts": [co("Not rarity alone: who controls supply, and the story", 960, 960, C("That a price"), "white", screen=True, size=34, until=C("The slogan still works", -0.3)),
                 co("A story holds a price until people ask", 960, 960, C("The slogan still works"), "gold", screen=True, size=40)]},
    sources=["gia", "adweek"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_debeers_storyboard.py; edit the generator, not this file.\n"
           "# Episode 24 storyboard (De Beers): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
