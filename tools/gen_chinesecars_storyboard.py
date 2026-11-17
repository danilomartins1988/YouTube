"""Generates projects/why-are-chinese-cars-so-cheap/deliverables/documentary/storyboard.yaml
(Episode 61: Why Are Chinese Cars So Cheap — And So Advanced?).

OWNER DIRECTION: premium business documentary with cartoon energy (house style of Ep 56): cold open -> channel intro -> show
TITLE CARD with a typed subtitle -> six parts opened by bumpers (a generic car zooms through; VOLTY the battery cell's price tag
drops each time: the running gag, all BNEF 2025 figures) -> verdict -> end card -> button.
Narrative device: THE FOUR SUSPECTS lineup board (efficiency, subsidies, financial engineering, cash burn), stamped at the verdict.
Cast (toon rig, fictional): JUNE (American car shopper), MEI (battery-line engineer: a competent professional), MORGAN (a Western
automaker's finance chief). Real people: Wang Chuanfu (BYD) and Lei Jun (Xiaomi) as respectful busts (signature traits, name label).
Bespoke sets (CartoonStage/cars.tsx): evshow, costlab, gigaline, cellplant, chainvalley, cashworks, pricestreet, carport, tariffgate,
c61title, c61bumper. Signature animations: the $25,000 car (p08 + s09), the battery supply chain (p21 + s20/s22), the subsidy
experiment (p15), the cash burn machine (s31 + p32), the global price war (s39 + p41 + s43/s44).
All cars are generic originals; no logos; no flags; jokes never change a number. Run: python tools/gen_chinesecars_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-are-chinese-cars-so-cheap/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
GOLD, BLUE, RED, GREEN, NAVY, TEAL = "#FFB627", "#1E88E5", "#E5484D", "#2E9E5B", "#13223A", "#26C6DA"


def toon(x, at=0.0, **kw):
    if "xk" in kw:
        x = kw.pop("xk")
    return it("toon", x=x, at=at, **kw)


def JUNE(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.3)
    return toon(x, at, who="shopper", v=2, skin=0, hair=2, hairStyle=3, color="#FF7043", glasses=False, scarf="#FFB627", **kw)


def MEI(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.3)
    return toon(x, at, who="shopper", v=1, skin=4, hair=1, hairStyle=4, color=TEAL, glasses=True, scarf="#FFFFFF", **kw)


def MORGAN(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.3)
    return toon(x, at, who="shopper", v=3, skin=2, hair=6, hairStyle=1, color="#37474F", glasses=True, scarf=RED, **kw)


def VOLTY(x, at=0.0, **kw):
    kw.setdefault("scale", 0.9)
    return it("cellbot", x=x, at=at, **kw)


def car(x, at=0.0, **kw):
    return it("evcar", x=x, at=at, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def chart(bars_, at=0.2, **kw):
    kw.setdefault("panel", True)
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


def bust(who, x, at, label, **kw):
    kw.setdefault("scale", 0.42)
    return it("bust", who=who, x=x, y=kw.pop("y", 900), at=at, label=label, **kw)


SUSP = ["EFFICIENCY", "SUBSIDIES", "FINANCIAL ENGINEERING", "CASH BURN"]


def bumper(id_, seg, num, title, caption, color, tag):
    items = [VOLTY([[0.6, -200], [2.4, 1650]], 0.5, y=900, scale=0.75, tags=[[1.4, tag]], hops=[2.6], faces=[[0, "happy"], [2.6, "worry"]])]
    stage(id_, seg, {**W1("c61bumper", num=num, act=f"PART {['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX'][int(num) - 1]}", title=title, caption=caption, color=color),
                     "cam": STILL(), "drift": 0, "min_seconds": 3.8, "items": items},
          sfx=[{"kind": "whoosh", "at": 0.05, "gain": 0.25}, {"kind": "hit", "at": 0.2, "gain": 0.3}])


# ====================================================================== COLD OPEN
stage("s01_open", "co_open", {
    **W1("evshow", carX=900, scanAt=C("laser scanner"), chargeAt=C("charges from ten"), lidar=True, screenAt=C("big touchscreen", -0.3)),
    "cam": cam((0, 900, 560, 1.35), (C("big touchscreen"), 1350, 420, 1.5, 1.4), (C("laser scanner"), 1100, 470, 1.2, 1.4), (C("charges from ten"), 900, 500, 1.15, 1.2),
               (C("Now, the price"), 900, 420, 0.95, WHIP)), "drift": 3,
    "items": [it("toonwords", text="BRAND-NEW. ELECTRIC.", x=900, y=180, at=0.2, until=C("big touchscreen"), size=70),
              sign("DRIVER ASSIST · LIDAR", 1500, 210, C("laser scanner", 0.3), color="#BBDEFB", size=28, until=C("charges from ten")),
              JUNE(-300, 0.3, xk=[[0, -300], [C("A big touchscreen"), 380]], face="happy", hold="phone", faces=[[0, "happy"], [C("Now, the price"), "shock"]], takes=[C("Now, the price", 0.3)])]},
    sources=["seagull"], sfx=[{"kind": "whoosh", "cue": "Now, the price", "gain": 0.25}])
stage("s02_hook", "co_hook", {
    **W1("evshow", carX=900, lidar=True, price="$9,900", priceSub="SEAGULL (2ND GEN) · CHINA LIST ¥65,900 · OCT 2026 · INCL. VAT", priceAt=C("That's about nine"),
         rivalAt=C("The average new electric car"), rivalX=1800, rivalPrice="$56,220", rivalSub="AVERAGE NEW EV SOLD · U.S. · OCT 2026 (KBB)"),
    "cam": cam((0, 900, 420, 1.0), (C("That's about nine"), 900, 380, 1.05, 1.0), (C("The average new electric car"), 1300, 480, 0.82, 1.6)), "drift": 3,
    "items": [it("counter", x=900, y=140, at=C("starts at", -0.2), prefix="¥", decimals=0, steps=[[0, 0], [C("starts at"), 0], [C("nine hundred yuan"), 65900]], text="CHINA LIST PRICE · OCT 2026", until=C("That's about nine", 0.3)),
              JUNE(300, 0.0, face="shock", hold="phone", faces=[[0, "shock"], [C("The average new electric car"), "worry"]], takes=[C("That's about nine", 0.2)]),
              it("toonwords", text="SAME KIND OF CAR?", x=1300, y=60, at=C("in October"), size=48)]},
    sources=["seagull", "cnevpost_seagull", "h10", "kbb"], sfx=[{"kind": "hit", "cue": "That's about nine", "gain": 0.35}])
stage("s03_contra", "co_contra", {
    **W1("gigaline", board="MEANWHILE, IN THE WEST", speed=60),
    "cam": cam((0, 1000, 500, 1.0), (C("Is China just better"), 1100, 420, 0.95, 1.4)), "drift": 4,
    "items": [it("counter", x=900, y=180, at=C("lost"), prefix="−$", suffix="B", decimals=1, steps=[[0, 0], [C("lost"), 0], [C("billion dollars last year"), 4.8]], text="FORD MODEL e (EV UNIT), 2025 EBIT", until=C("Is China just better")),
              MORGAN(1500, 0.2, face="worry", pose="clipboard", hold="clipboard", label="MORGAN · WESTERN CARMAKER CFO", labelUntil=C("Is China just better"), takes=[C("lost", 0.4)]),
              it("suspects", x=1000, y=420, at=C("Is China just better", -0.2), scale=0.85,
                 his=[[C("Is China just better"), 0], [C("Is the government paying"), 1], [C("Are the books"), 2], [C("burning cash"), 3]])]},
    sources=["ford"], sfx=[{"kind": "hit", "cue": "lost", "gain": 0.3}])
stage("s04_promise", "co_promise", {
    **W1("gigaline", board="THE INVESTIGATION", speed=90),
    "cam": cam((0, 1000, 420, 0.95), (C("take the car apart"), 1100, 520, 1.05, 1.2), (C("price war"), 1300, 500, 1.0, 1.2)), "drift": 5,
    "items": [it("suspects", x=1000, y=320, at=0.0, scale=0.7, until=C("To find the culprit", 0.5), his=[[0, -1]]),
              sign("1 · TAKE THE CAR APART", 520, 200, C("take the car apart"), color="#FFE0B2", size=30),
              sign("2 · FOLLOW THE BATTERY", 980, 120, C("follow the battery"), color="#BBDEFB", size=30),
              sign("3 · READ THE CASH FLOW", 1440, 200, C("read the cash flow"), color="#C8E6C9", size=30),
              sign("4 · THE PRICE WAR", 1720, 330, C("price war"), color="#FFCDD2", size=30),
              VOLTY(300, C("follow the battery"), hops=[C("follow the battery", 0.3)], tags=[[C("follow the battery", 0.4), "$108/kWh"]]),
              JUNE(1750, 0.2, face="grin", hold="phone")]},
    sfx=[{"kind": "whoosh", "cue": "take the car apart", "gain": 0.2}])
stage("s05_title", "title_card", {
    **W1("c61title", subs=[[2.1, "Tonight: “The Price Is Right. The Profit Is… Pending.”"]]), "cam": STILL(), "drift": 0, "min_seconds": 5.6, "items": []},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}, {"kind": "hit", "at": 1.4, "gain": 0.25}])

# ====================================================================== PART 1: the impossible car
bumper("s06_b1", "a1_card", "1", "THE IMPOSSIBLE CAR", "Batteries included. Explanations extra.", BLUE, "$108/kWh")
stage("s07_fair", "a1_fair", {
    **W1("evshow", carX=700, price="$9,900", priceSub="CHINA · INCL. 13% VAT · + 5% NEV PURCHASE TAX (2026)", priceAt=0.0, priceX=700,
         rivalAt=C("Its European cousin", -0.2), rivalX=1650, rivalPrice="$25,900", rivalSub="DOLPHIN SURF · GERMANY LIST €23,490 · INCL. 19% VAT"),
    "cam": cam((0, 900, 500, 1.1), (C("small city car"), 700, 520, 1.2, 1.2), (C("Its European cousin"), 1200, 470, 0.88, 1.6)), "drift": 3,
    "items": [it("toonwords", text="FAIR WARNING", x=900, y=120, at=0.1, until=C("small city car"), size=80),
              sign("SMALL CITY CAR · 4.2 M LONG", 700, 640, C("small city car"), color="#FFF8E1", size=26, until=C("Its European cousin")),
              sign("EU: 10% DUTY + 17.0% BYD COUNTERVAILING DUTY", 1650, 120, C("different taxes"), color="#FFCDD2", size=24),
              JUNE(250, 0.2, face="worry", hold="phone", pose="talk", talk=[[0.3, 1.8]])]},
    sources=["nevtax", "seagull", "h10", "eu_cvd"])
stage("s08_real", "a1_real", {
    **W1("pricestreet", start=["¥ EV", "¥ EV", "¥ GAS"], names=["EV", "EV", "GASOLINE"], margin=0.5, gauge=False),
    "cam": cam((0, 900, 420, 0.95), (C("nearly seventy percent"), 950, 460, 1.0, 1.4)), "drift": 3,
    "items": [it("counter", x=1700, y=220, at=C("nearly seventy percent", -0.3), suffix="%", steps=[[0, 0], [C("nearly seventy percent"), 0], [C("were cheaper"), 70]], text="CHINA 2025: EVs CHEAPER THAN GAS EQUIVALENT (IEA)"),
              sign("BEFORE ANY INCENTIVE", 1700, 470, C("Before incentives"), color="#C8E6C9", size=32),
              car([[0, -400], [C("something real remains"), 2600]], 0.0, carKind="hatch", color="#2E9E5B", lights=True)]},
    sources=["iea_gevo"])
stage("s09_scale", "a1_scale", {
    **W1("gigaline", board="2025: ~16M OF ~22M ELECTRIC CARS MADE IN CHINA (IEA)", speed=200),
    "cam": cam((0, 900, 480, 1.0), (C("BYD alone"), 1100, 470, 1.0, 1.4)), "drift": 5,
    "items": [it("counter", x=1500, y=170, at=C("BYD alone"), suffix="M", decimals=1, steps=[[0, 0], [C("BYD alone"), 0], [C("million vehicles"), 4.6]], text="BYD VEHICLES SOLD, 2025"),
              sign("#1 IN BATTERY-ELECTRIC CARS, AHEAD OF TESLA", 1500, 400, C("more fully electric"), color="#FFF59D", size=26),
              sign("VW GROUP OPERATING MARGIN 2025: 2.8%", 500, 160, C("more fully electric", 0.8), color="#FFCDD2", size=26),
              MEI(420, 0.2, face="happy", hold="clipboard", pose="clipboard", label="MEI · BATTERY LINE ENGINEER", labelUntil=C("BYD alone"))]},
    sources=["iea_gevo", "byd_sales", "byd_ar25", "vw"])
add("p10_cost", "a1_draw", "engine_draw", {
    "title": "A hypothetical $25,000 EV (not company data)", "board": BOARD, "draw_start": C("Let me draw"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 640 640 Q 640 565 705 552 L 805 540 Q 885 462 1005 456 Q 1125 462 1185 540 L 1290 556 Q 1340 566 1338 640 Z", "color": "ink", "width": 6, "kind": "stroke", "start": C("Let me draw")},
        {"d": "M 700 645 a 42 42 0 1 0 84 0 a 42 42 0 1 0 -84 0", "color": "ink", "width": 6, "kind": "stroke", "start": C("where a car's money", 0.3)},
        {"d": "M 1190 645 a 42 42 0 1 0 84 0 a 42 42 0 1 0 -84 0", "color": "ink", "width": 6, "kind": "stroke", "start": C("where a car's money", 0.6)},
        {"d": dot(990, 360), "color": "muted", "width": 1, "start": C("A hypothetical"), "label": lbl("HYPOTHETICAL $25,000 EV · NOT ANY COMPANY'S DATA", 990, 360, 22, "muted")},
        {"d": "M 760 600 L 1220 600 L 1220 640 L 760 640 Z", "color": "accent", "width": 4, "fill": "accent", "fillOpacity": 0.6, "kind": "bar", "start": C("The biggest part"), "label": lbl("BATTERY", 990, 628, 24, "ink")},
        {"d": arrow((1420, 760), (1180, 650), -0.15), "color": "risk", "width": 5, "kind": "arrow", "start": C("average pack price")},
        {"d": dot(1460, 800), "color": "risk", "width": 1, "start": C("average pack price", 0.3), "label": lbl("60 kWh × $99/kWh (BNEF 2025 AVG)", 1460, 800, 22, "risk")},
        {"d": dot(1460, 850), "color": "risk", "width": 1, "start": C("five thousand nine hundred"), "label": lbl("≈ $5,900 ≈ 24% OF THE PRICE (OUR CALC.)", 1460, 850, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("The biggest part", 0.3), "dur": 1.4, "target": [990, 620]}],
    "scale": 0.86, "floor": 1040}, sources=["bnef"])
SLICES = [[C("The biggest", -99), "BATTERY", 5900, GOLD, "≈ $5,900 · BNEF AVG × 60 kWh"], [C("motor and electronics"), "MOTOR & ELECTRONICS", 2500, BLUE, "ILLUSTRATIVE"],
          [C("Screens, chips"), "SCREENS, CHIPS, SOFTWARE", 2500, "#7E57C2", ""], [C("Body, steel"), "BODY, STEEL, GLASS", 5500, "#90A4AE", ""],
          [C("Labor and the factory"), "LABOR & FACTORY", 2500, "#26A69A", ""], [C("Shipping and the dealer"), "SHIPPING & DEALER", 2500, "#FF7043", ""],
          [C("Taxes"), "TAXES", 2000, "#B0BEC5", ""], [C("the slice the company keeps"), "MARGIN", 1600, RED, "THIN"]]
SLICES[0][0] = 0.3
stage("s11_slices", "a1_slices", {
    **W1("costlab", explodeAt=0.0, slices=SLICES, note="HYPOTHETICAL · ONLY THE BATTERY SLICE IS CALCULATED"),
    "cam": cam((0, 960, 520, 1.0), (C("the slice the company keeps"), 1150, 300, 1.25, 1.4), (C("It's thin"), 1100, 330, 1.35, WHIP)), "drift": 2,
    "items": [it("toonwords", text="$25,000 · HYPOTHETICAL", x=1080, y=60, at=0.1, until=C("Body, steel"), size=44),
              it("toonwords", text="IT'S THIN.", x=1100, y=180, at=C("It's thin"), size=70, color=RED)]},
    sources=["bnef"])
stage("s12_turn", "a1_turn", {
    **W1("gigaline", board="WHO IS MAKING THE SLICES CHEAPER?", speed=60),
    "cam": cam((0, 1000, 420, 0.95), (C("the government"), 1000, 400, 1.15, WHIP)), "drift": 2,
    "items": [it("suspects", x=1000, y=380, at=0.0, scale=0.85, his=[[0, -1], [C("The first suspect"), 1]])]})

# ====================================================================== PART 2: the subsidy suspect
bumper("s13_b2", "a2_card", "2", "THE SUBSIDY SUSPECT", "Follow the money. Then read the receipt.", RED, "$99/kWh")
stage("s14_csis", "a2_csis", {
    **W1("carport", lot=[[0, 0.3], [6, 0.8]], board="SUPPORT FOR EVs, 2009–2023 (CSIS ESTIMATE)"),
    "cam": cam((0, 900, 480, 1.0), (C("Beijing spent"), 800, 460, 1.0, 1.4)), "drift": 4,
    "items": [it("toonwords", text="EXHIBIT A", x=900, y=120, at=0.1, until=C("Beijing spent"), size=70),
              it("counter", x=900, y=200, at=C("Beijing spent"), prefix="≈ $", suffix="B", decimals=1, steps=[[0, 0], [C("Beijing spent"), 0], [C("backing electric cars"), 230.9]], text="CSIS ESTIMATE (CALLED CONSERVATIVE)"),
              it("coinrain", x=900, y=330, at=C("Beijing spent"), until=C("twenty twenty-three"), n=16, w=500, fall=420)]},
    sources=["csis"])
stage("s15_where", "a2_where", {
    **W1("evshow", carX=1100, price="REBATE + TAX BREAK", priceSub="MOSTLY PAID TO BUYERS, NOT CARMAKERS (CSIS)", priceAt=C("most of it went to buyers"), priceX=1100),
    "cam": cam((0, 1000, 470, 0.95), (C("And it shrank"), 1300, 440, 1.0, 1.4)), "drift": 3,
    "items": [JUNE([[0, -300], [C("most of it went"), 500]], 0.1, face="happy", hold="card", faces=[[0, "happy"], [C("And it shrank"), "worry"]]),
              chart([{"label": "2018", "value": 13860, "color": BLUE, "at": C("And it shrank", -0.2), "display": "$13,860"},
                     {"label": "2023", "value": 4800, "color": RED, "at": C("per car by"), "display": "< $4,800"}],
                    at=C("And it shrank", -0.4), max=15000, title="SUPPORT PER EV (CSIS)", x=1350, y=170, w=560, h=420)]},
    sources=["csis"])
stage("s16_hidden", "a2_hidden", {
    **W1("gigaline", board="2020 · HEFEI-LED INVESTORS → NIO CHINA", speed=80),
    "cam": cam((0, 1000, 470, 1.0), (C("An investment"), 1100, 450, 1.1, 1.2)), "drift": 4,
    "items": [sign("NOT IN THE COUNT: CHEAP LAND · CHEAP LOANS · CITY STAKES", 1000, 140, 0.3, color="#FFF8E1", size=26, until=C("Hefei-led")),
              it("counter", x=1000, y=170, at=C("Hefei-led"), prefix="≈ $", suffix="B", decimals=1, steps=[[0, 0], [C("Hefei-led"), 0], [C("into NIO's"), 1.0]], text="¥7B FOR A 24.1% STAKE IN NIO CHINA (2020)"),
              sign("EQUITY, NOT A GRANT", 1500, 420, C("An investment"), color="#C8E6C9", size=34),
              MORGAN(400, 0.3, face="smug", hold="clipboard", pose="clipboard", faces=[[0, "smug"], [C("money a startup"), "worry"]])]},
    sources=["csis", "nio_hefei", "h10_2020"])
stage("s17_grants", "a2_grants", {
    **W1("evshow", carX=700, carColor="#1E88E5", price="≈ $1.8B", priceSub="BYD GOVERNMENT GRANTS IN 2025 PROFIT (¥12.6B, ANNUAL REPORT)", priceAt=C("BYD's own annual report"), priceX=1150),
    "cam": cam((0, 1000, 470, 0.95), (C("BYD's own annual report"), 1150, 420, 1.0, 1.4)), "drift": 3,
    "items": [VOLTY(200, 0.1, scale=0.7),
              it("docs", x=1480, y=760, at=C("Kiel Institute"), text="KIEL POLICY BRIEF 173", scale=0.8, stamp="BYD 2022: €2.1B ≈ $2.2B", stampAt=C("for BYD")),
              it("docs", x=420, y=760, at=C("BYD's own annual report"), text="BYD ANNUAL REPORT 2025", scale=0.8, stamp="GRANTS ¥12.6B", stampAt=C("of grants"))]},
    sources=["kiel", "g5a", "byd_ar25"])
add("p18_subsidy", "a2_draw", "engine_draw", {
    "title": "The subsidy experiment (BYD 2025 ratios; our calculation)", "board": BOARD, "draw_start": C("run an experiment"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1500 860", "color": "ink", "width": 5, "start": C("run an experiment")},
        {"d": "M 620 860 L 620 420 L 820 420 L 820 860 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("On a twenty thousand"), "label": lbl("CAR PRICE $20,000 (EXAMPLE)", 720, 400, 22, "accent2")},
        {"d": "M 860 860 L 860 853 L 1000 853 L 1000 860 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.9, "kind": "bar", "start": C("a sliver"), "label": lbl("GRANTS ≈ 1.6% ≈ $320", 930, 820, 22, "risk")},
        {"d": arrow((930, 800), (930, 845)), "color": "risk", "width": 4, "kind": "arrow", "start": C("a sliver", 0.3)},
        {"d": "M 1140 860 L 1140 560 L 1300 560 L 1300 860 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("But they're"), "label": lbl("NET PROFIT", 1220, 540, 22, "accent3")},
        {"d": "M 1320 860 L 1320 744 L 1460 744 L 1460 860 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.8, "kind": "bar", "start": C("two-fifths"), "label": lbl("GRANTS ≈ 2/5", 1390, 724, 22, "risk")},
        {"d": dot(1040, 930), "color": "muted", "width": 1, "start": C("by our calculation"), "label": lbl("BYD AR 2025: GRANTS ¥12.6B · REVENUE ¥804B · NET PROFIT ¥32.6B (GRANTS PRE-TAX)", 1040, 930, 18, "muted")},
        {"d": dot(1040, 330), "color": "ink", "width": 1, "start": C("They can't make a car cheap"), "label": lbl("PROFITABLE? YES. CHEAP? NO.", 1040, 330, 30, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("a sliver", 0.2), "dur": 1.4, "target": [930, 850]}, {"kind": "react", "at": C("two-fifths", 0.4)}],
    "scale": 0.86, "floor": 1040}, sources=["byd_ar25"])
stage("s19_eu", "a2_eu", {
    **W1("tariffgate", wallAt=999, euAt=0.3, euLines=["10% EU CAR DUTY", "+ 17.0% BYD", "+ 18.8% GEELY", "+ 35.3% SAIC"], euX=900),
    "cam": cam((0, 1350, 500, 1.0), (C("China disputes"), 1300, 480, 1.05, 1.2)), "drift": 3,
    "items": [sign("SINCE OCT 30, 2024 · EU ANTI-SUBSIDY DUTIES", 1300, 110, 0.4, color="#FFF8E1", size=28),
              sign("EU FINDINGS · CHINA DISPUTES THEM", 1300, 760, C("China disputes"), color="#FFCDD2", size=30),
              car([[0, 300], [C("seventeen percent more"), 700], [C("China disputes"), 780]], 0.0, carKind="hatch", color=TEAL, tag="+17.0%", tagColor="#FFCDD2")]},
    sources=["eu_cvd"])
stage("s20_turn", "a2_turn", {
    **W1("carport", lot=[[0, 0.4], [C("grew almost"), 0.95]], board="CHINESE-MADE EVs SOLD IN EUROPE, 2025: ≈ 940,000 (IEA)"),
    "cam": cam((0, 1000, 480, 1.0), (C("grew almost"), 900, 520, 1.05, 1.2)), "drift": 3,
    "items": [it("toonwords", text="DID THE DUTIES WORK?", x=900, y=120, at=0.1, until=C("grew almost"), size=60),
              it("counter", x=900, y=200, at=C("grew almost"), prefix="+", suffix="%", steps=[[0, 0], [C("grew almost"), 0], [C("grew almost", 1.6), 50]], text="CHINESE-MADE EV SALES IN EUROPE, 2025 (IEA, ≈)")]},
    sources=["iea_gevo"])

# ====================================================================== PART 3: the machine
bumper("s21_b3", "a3_card", "3", "THE MACHINE", "Some assembly required. Most of it nearby.", GREEN, "$84/kWh")
stage("s22_battery", "a3_battery", {
    **W1("gigaline", board="FOUNDED 1995 AS A BATTERY COMPANY", speed=90),
    "cam": cam((0, 960, 500, 1.0), (C("It still makes its own"), 900, 520, 1.05, 1.4)), "drift": 3,
    "items": [bust("wangcf", 1560, 0.3, "WANG CHUANFU · BYD FOUNDER", y=880, scale=0.4, expr="happy", exprs=[[0, "happy"], [C("It still makes"), "smug"]], dir=-1),
              sign("BYD ANNUAL REPORT 2025: INCORPORATED FEB 1995 (BYD BATTERY)", 820, 120, C("founded BYD"), color="#FFF8E1", size=24),
              MEI(300, 0.3, face="happy", pose="point", poses=[[0, "stand"], [C("battery is a car's"), "point"]])]},
    sources=["byd_ar25"])
stage("s23_lfp", "a3_lfp", {
    **W1("cellplant", fill=[[0, 0.8], [9, 1.0]], jarsAt=C("lithium iron phosphate"), tagsAt=C("packs averaged"), jarX=1350, packX=600, board="CHEMISTRY CHOICE"),
    "cam": cam((0, 1000, 500, 1.0), (C("lithium iron phosphate"), 1500, 520, 1.05, 1.4), (C("packs averaged"), 1500, 470, 1.1, 1.2)), "drift": 3,
    "items": [sign("BLOOMBERGNEF 2025 SURVEY · AVERAGE PACK PRICES", 1500, 110, C("packs averaged"), color="#FFF8E1", size=24),
              VOLTY([[0, 2300], [C("needs no nickel"), 1000]], 0.2, tags=[[C("packs averaged"), "$81/kWh"]], hops=[C("packs averaged", 0.2)])]},
    sources=["bnef"])
stage("s24_blade", "a3_blade", {
    **W1("cellplant", fill=[[0, 0.1], [C("skipping a layer"), 1.0]], board="CELL-TO-PACK (NO MODULES)", packX=860),
    "cam": cam((0, 860, 520, 1.15), (C("Neither chemistry"), 960, 480, 0.95, 1.4)), "drift": 3,
    "items": [sign("NMC: MORE ENERGY PER POUND", 400, 160, C("Neither chemistry"), color="#E1BEE7", size=26),
              sign("LFP: CHEAPER, NO NICKEL OR COBALT", 1500, 160, C("Neither chemistry", 0.4), color="#C8E6C9", size=26),
              it("toonwords", text="CHEAP + GOOD ENOUGH", x=960, y=300, at=C("for an affordable car"), size=60, color=GOLD),
              MEI(1700, 0.2, face="grin", pose="talk", talk=[[C("Neither chemistry"), C("good enough wins", 0.5)]])]})
add("p25_chain", "a3_chain", "engine_draw", {
    "title": "The battery's journey (China's share, 2025)", "board": BOARD, "draw_start": C("Let me draw"), "speed": 1600, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        *[{"d": rect(520 + k * 215, 520, 160, 90), "color": "ink", "width": 5, "kind": "box", "start": C(cu), "label": lbl(nm, 600 + k * 215, 572, 22, "ink")}
          for k, (nm, cu) in enumerate([("MINE", "Minerals are mined"), ("REFINE", "refined"), ("POWDERS", "turned into powders"), ("CELLS", "made into cells"), ("PACK", "packed"), ("CAR", "put in a car")])],
        *[{"d": arrow((680 + k * 215, 565), (733 + k * 215, 565)), "color": "accent2", "width": 4, "kind": "arrow", "start": C(cu, 0.2)}
          for k, cu in enumerate(["refined", "turned into powders", "made into cells", "packed", "put in a car"])],
        {"d": rect(950, 620, 160, 60), "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.5, "kind": "bar", "start": C("eighty-five percent"), "label": lbl("CATHODE ≈ 85%", 1030, 700, 20, "risk")},
        {"d": rect(950, 680, 160, 0), "color": "risk", "width": 1, "kind": "stroke", "start": C("ninety percent"), "label": lbl("ANODE > 90%", 1030, 730, 20, "risk")},
        {"d": rect(1165, 620, 160, 60), "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.5, "kind": "bar", "start": C("more than eighty percent of the cells"), "label": lbl("CELLS > 80%", 1245, 700, 20, "risk")},
        {"d": dot(1460, 440), "color": "accent", "width": 1, "start": C("CATL and BYD"), "label": lbl("CATL 39.2% + BYD 16.4% OF EV BATTERIES (SNE, 2025)", 1250, 440, 22, "accent")},
        {"d": dot(1040, 820), "color": "muted", "width": 1, "start": C("shade China's share"), "label": lbl("SHARES OF WORLD PRODUCTION, 2025 (IEA GEVO 2026)", 1040, 820, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("eighty-five percent", 0.1), "dur": 1.4, "target": [1030, 650]}, {"kind": "point", "at": C("CATL and BYD", 0.2), "dur": 1.4, "target": [1350, 565], "laser": True}],
    "scale": 0.86, "floor": 1040}, sources=["iea_gevo", "sne"])
stage("s26_price", "a3_price", {
    **W1("chainvalley", lit=[[0, 0], [5, 5]], shades=[[C("thirty percent less"), 4, 0.3, "−30% VS N. AMERICA"], [C("thirty-five percent less"), 5, 0.35, "−35% VS EUROPE"]],
         caption="BATTERY PACK PRICES IN CHINA, 2025 (IEA)"),
    "cam": cam((0, 1000, 470, 0.95), (C("thirty percent less"), 1350, 430, 1.0, 1.4)), "drift": 3,
    "items": [VOLTY([[0, -200], [5, 900]], 0.2, scale=0.7, tags=[[C("thirty percent less"), "−30%"]])]},
    sources=["iea_gevo"])
stage("s27_cluster", "a3_cluster", {
    **W1("gigaline", board="SUPPLIERS A SHORT DRIVE AWAY", speed=140),
    "cam": cam((0, 1000, 480, 1.0), (C("A problem gets fixed"), 1200, 500, 1.05, 1.2)), "drift": 4,
    "items": [*[it("drone", x=[[0, -300 - k * 200], [9 + k, 2400]], y=110 + k * 60, at=0.2 + k * 0.4, carry=t_, scale=0.75) for k, t_ in enumerate(["MOTORS", "CHIPS", "SEATS"])],
              sign("SEE ALSO: OUR FILM ON CHINESE FACTORIES", 1000, 330, C("our film"), color="#BBDEFB", size=28),
              it("toonwords", text="A TRUCK, NOT A SHIP", x=1200, y=250, at=C("A problem gets fixed"), size=60)]})
stage("s28_speed", "a3_speed", {
    **W1("gigaline", board="NEW MODEL DEVELOPMENT TIME (ALIXPARTNERS, 2024)", speed=220),
    "cam": cam((0, 960, 480, 1.0),), "drift": 3,
    "items": [chart([{"label": "CHINESE EV MAKERS", "value": 20, "color": RED, "at": C("about twenty months"), "display": "~20 MO"},
                     {"label": "TRADITIONAL", "value": 40, "color": "#90A4AE", "at": C("about half the time"), "display": "~40 MO"}],
                    at=0.2, max=45, title="MONTHS TO DEVELOP A NEW MODEL (EST.)", x=420, y=170, w=1080, h=420)]},
    sources=["alix"])
stage("s29_xiaomi", "a3_xiaomi", {
    **W1("evshow", carX=800, carColor="#FF7043", carKind="sedan", price="411,082", priceSub="XIAOMI CARS DELIVERED IN 2025 (XIAOMI)", priceAt=C("Last year it delivered"), priceX=800),
    "cam": cam((0, 1000, 470, 0.95),), "drift": 3,
    "items": [bust("leijun", 1600, 0.3, "LEI JUN · XIAOMI FOUNDER", y=900, scale=0.4, expr="happy", dir=-1),
              sign("2021: XIAOMI ANNOUNCES ITS CAR BUSINESS", 800, 110, C("launched its car business"), color="#FFF8E1", size=26)]},
    sources=["xiaomi_2021", "xiaomi_ar25"])
stage("s30_scale", "a3_scale", {
    **W1("gigaline", board="2025: 16 MILLION ELECTRIC CARS MADE IN CHINA (IEA)", speed=320),
    "cam": cam((0, 900, 480, 0.9), (C("That's why one new"), 1200, 460, 1.05, 1.4), (C("that's an ecosystem"), 1000, 470, 0.95, 1.2)), "drift": 4,
    "items": [MORGAN([[0, 2300], [C("That's why one new"), 1500]], 0.2, face="worry", hold="clipboard", pose="clipboard", faces=[[0, "worry"], [C("that's an ecosystem"), "shock"]]),
              sign("THE CHEAP BATTERY", 600, 160, C("The cheap battery"), color="#FFE0B2", size=28),
              sign("THE SUPPLIERS NEXT DOOR", 1000, 100, C("the suppliers next door"), color="#BBDEFB", size=28),
              sign("THE EXPERIENCED ENGINEERS", 1400, 160, C("the experienced engineers"), color="#C8E6C9", size=28),
              it("toonwords", text="AN ECOSYSTEM, NOT A BUILDING", x=1000, y=300, at=C("not a building", -0.5), size=54)]},
    sources=["iea_gevo"])
stage("s31_caution", "a3_caution", {
    **W1("evshow", carX=900, screenAt=0.0),
    "cam": cam((0, 1400, 420, 1.3), (C("Features show up"), 1000, 480, 1.0, 1.4)), "drift": 3,
    "items": [it("toonwords", text="FEATURES ≠ QUALITY", x=1300, y=150, at=0.3, size=70, color=RED),
              sign("DAY ONE: FEATURES", 600, 220, C("Features show up"), color="#BBDEFB", size=30),
              sign("YEARS LATER: SAFETY & RELIABILITY (INDEPENDENT TESTS)", 1200, 320, C("Safety and reliability"), color="#FFF59D", size=26),
              JUNE(300, 0.2, face="worry", hold="phone")]})

# ====================================================================== PART 4: follow the cash
bumper("s32_b4", "a4_card", "4", "FOLLOW THE CASH", "Profit is an opinion. Cash is a fact.", "#7E57C2", "$81 (LFP)")
stage("s33_byd", "a4_byd", {
    **W1("gigaline", board="BYD · YEAR ENDED DEC 31, 2025 (ANNUAL REPORT)", speed=120),
    "cam": cam((0, 960, 480, 1.0), (C("Its car business"), 1100, 470, 1.0, 1.4)), "drift": 3,
    "items": [VOLTY(1700, 0.1, scale=0.7, faces=[[0, "happy"]]),
              chart([{"label": "REVENUE", "value": 111.9, "color": BLUE, "at": C("on revenue"), "display": "≈ $111.9B"},
                     {"label": "NET PROFIT", "value": 4.5, "color": GREEN, "at": C("it earned"), "display": "≈ $4.5B (−19%)"}],
                    at=C("BYD is"), max=120, title="BYD 2025, WHOLE COMPANY", x=260, y=150, w=760, h=420, until=C("Its car business", 1.0)),
              sign("CAR SEGMENT PROFIT BEFORE TAX ≈ $4.0B", 1450, 160, C("Its car business"), color="#C8E6C9", size=28),
              it("toonwords", text="≈ $860 PER VEHICLE", x=1450, y=330, at=C("a vehicle", -0.6), size=56, color=GOLD),
              sign("OUR ROUGH CALC: SEGMENT ALSO SELLS BATTERIES, SOLAR, RAIL", 1450, 450, C("by our rough math"), color="#FFF8E1", size=20)]},
    sources=["byd_ar25", "g5a"])
stage("s34_machine", "a4_machine", {
    **W1("cashworks", mx=760, stages=[[C("Revenue pours in"), 0], [C("gross profit"), 1], [C("operating profit"), 2], [C("Then timing"), 3], [C("free cash flow"), 4]],
         levels={"0": 0.9, "1": 0.55, "2": 0.35, "3": [[0, 0.3], [C("when suppliers get paid"), 0.45]], "4": 0.25}),
    "cam": cam((0, 900, 420, 0.95), (C("Then timing"), 1000, 560, 1.0, 1.4), (C("free cash flow"), 1000, 640, 1.05, 1.2)), "drift": 2,
    "items": [it("toonwords", text="PROFIT ≠ CASH", x=1500, y=120, at=0.2, until=C("Revenue pours in", 1.0), size=70, color=RED),
              MORGAN(1600, 0.3, face="worry", pose="point", hold="clipboard", poses=[[0, "clipboard"], [C("Revenue pours in"), "point"]], label="ILLUSTRATIVE MACHINE · NO REAL DATA", labelUntil=C("gross profit"))]})
add("p35_two", "a4_draw", "engine_draw", {
    "title": "Two hypothetical carmakers, same profit", "board": BOARD, "draw_start": C("Take two hypothetical"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1500 860", "color": "ink", "width": 5, "start": C("Take two hypothetical")},
        {"d": "M 620 860 L 620 700 L 760 700 L 760 860 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.35, "kind": "bar", "start": C("same profit"), "label": lbl("A · PROFIT", 690, 680, 20, "accent3")},
        {"d": "M 1080 860 L 1080 700 L 1220 700 L 1220 860 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.35, "kind": "bar", "start": C("same profit", 0.4), "label": lbl("B · PROFIT", 1150, 680, 20, "accent3")},
        {"d": dot(690, 900), "color": "ink", "width": 1, "start": C("two months"), "label": lbl("PAYS SUPPLIERS IN 2 MONTHS", 760, 900, 20, "ink")},
        {"d": dot(1150, 900), "color": "ink", "width": 1, "start": C("takes six"), "label": lbl("PAYS IN 6 MONTHS", 1220, 900, 20, "ink")},
        {"d": "M 780 860 L 780 760 L 900 760 L 900 860 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.4, "kind": "bar", "start": C("In the bank"), "label": lbl("A · CASH", 840, 740, 20, "accent2")},
        {"d": "M 1240 860 L 1240 520 L 1360 520 L 1360 860 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.4, "kind": "bar", "start": C("B looks richer"), "label": lbl("B · CASH", 1300, 500, 20, "accent2")},
        {"d": arrow((1430, 540), (1430, 820)), "color": "risk", "width": 6, "kind": "arrow", "start": C("Until it has to pay up"), "label": lbl("PAY UP", 1480, 690, 24, "risk")},
        {"d": dot(1040, 360), "color": "muted", "width": 1, "start": C("interest free"), "label": lbl("SUPPLIERS' MONEY = AN INTEREST-FREE LOAN", 1040, 360, 24, "muted")},
        {"d": dot(1040, 960), "color": "muted", "width": 1, "start": C("On paper"), "label": lbl("HYPOTHETICAL · NO REAL COMPANY", 1040, 960, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("B looks richer", 0.2), "dur": 1.4, "target": [1300, 600]}, {"kind": "react", "at": C("Until it has to pay up", 0.3)}],
    "scale": 0.86, "floor": 1040})
stage("s36_pledge", "a4_pledge", {
    **W1("gigaline", board="JUNE 2025 · THE 60-DAY PLEDGE", speed=80),
    "cam": cam((0, 1000, 480, 1.0),), "drift": 3,
    "items": [it("counter", x=1000, y=170, at=C("seventeen"), steps=[[0, 0], [C("seventeen"), 0], [C("major carmakers"), 17]], text="CARMAKERS PLEDGING TO PAY SUPPLIERS IN 60 DAYS (MIIT-BACKED)"),
              it("calendar", x=1650, y=300, at=C("within sixty days", -0.5), pages=[[0, "60"]], text="DAYS", scale=0.8),
              *[it("toon", who="shopper", v=5 + k, x=[[0, -300 - k * 150], [C("promised to pay"), 300 + k * 160]], at=0.3, face="happy", hold="box", scale=1.05) for k in range(3)]]},
    sources=["pledge", "pledge_mii"])
stage("s37_unwind", "a4_unwind", {
    **W1("cashworks", mx=700, labels=["REVENUE", "GROSS PROFIT", "OPERATING PROFIT", "OPERATING CASH", "FREE CASH FLOW"],
         levels={"0": 0.9, "1": 0.5, "2": 0.3, "3": [[0, 0.75], [C("Cash from operations dropped"), 0.75], [C("eight point two billion"), 0.33]], "4": [[0, 0.3], [C("Free cash flow"), -0.3]]},
         negAt=C("minus thirteen"), negText="≈ −$13.6B"),
    "cam": cam((0, 1000, 560, 1.0), (C("Free cash flow"), 960, 600, 1.04, 1.4)), "drift": 2,
    "items": [sign("BYD 2025 (ANNUAL REPORT) · OUR CALCULATIONS", 1520, 60, 0.2, color="#FFF8E1", size=24),
              sign("OWED TO SUPPLIERS: −≈$4.8B", 1400, 180, C("What it owed suppliers"), color="#FFE0B2", size=28),
              sign("OPERATING CASH: $18.5B (2024) → $8.2B", 1520, 300, C("Cash from operations"), color="#BBDEFB", size=28),
              sign("FACTORIES & EQUIPMENT: ≈$21.8B", 1520, 420, C("It spent"), color="#FFCDD2", size=28),
              sign("BORROWINGS: ≈$4.0B → ≈$15.8B", 1520, 540, C("borrowed more"), color="#E1BEE7", size=28),
              it("toonwords", text="PROFITABLE. AND BURNING CASH.", x=1100, y=880, at=C("Profitable, and burning"), size=50, color=RED)]},
    sources=["byd_ar25", "g5a"])
stage("s38_others", "a4_others", {
    **W1("evshow", carX=700, carColor="#FF7043", carKind="sedan", price="≈ $34,900", priceSub="XIAOMI AVERAGE EV SELLING PRICE, 2025", priceAt=C("its average car"), priceX=700),
    "cam": cam((0, 1000, 470, 0.95),), "drift": 3,
    "items": [chart([{"label": "2024", "value": -0.86, "color": RED, "at": C("in twenty twenty-four"), "display": "−$0.86B"},
                     {"label": "2025", "value": 0.125, "color": GREEN, "at": C("first operating profit"), "display": "+$0.13B"}],
                    at=0.2, min=-1, max=0.4, title="XIAOMI EV SEGMENT", x=1150, y=170, w=700, h=420),
              sign("2024: ADJ. NET LOSS · 2025: OPERATING PROFIT", 1500, 760, C("first operating profit"), color="#FFF8E1", size=22),
              it("toonwords", text="NOT EVERY CHINESE CAR IS CHEAP", x=1000, y=60, at=C("Not every Chinese car"), size=48)]},
    sources=["xiaomi_ar25", "xiaomi_24", "g5a"])
stage("s39_nio", "a4_nio", {
    **W1("gigaline", board="NIO · FY2025 RESULTS", speed=60),
    "cam": cam((0, 960, 480, 1.0), (C("A low price"), 1000, 470, 1.05, 1.2)), "drift": 3,
    "items": [it("counter", x=900, y=170, at=0.2, prefix="−$", suffix="B", decimals=1, steps=[[0, 0], [0.3, 0], [C("last year"), 2.1]], text="NIO NET LOSS, 2025 (≈, ¥14.9B)", until=C("A low price")),
              sign("Q4 2025: FIRST QUARTERLY OPERATING PROFIT (NON-GAAP)", 900, 420, C("first quarterly"), color="#C8E6C9", size=26, until=C("A low price", -0.2)),
              sign("LOW PRICE ≠ LOSS", 700, 380, C("A low price"), color="#FFF59D", size=34),
              sign("ONE GOOD QUARTER ≠ A LASTING BUSINESS", 1200, 520, C("one good quarter"), color="#FFCDD2", size=30),
              MORGAN(1700, 0.3, face="worry", hold="clipboard")]},
    sources=["nio_q4", "g5a"])

# ====================================================================== PART 5: the price war
bumper("s40_b5", "a5_card", "5", "THE PRICE WAR", "Everything must go. Including the margin.", "#FF7043", "SALE?!")
stage("s41_glut", "a5_glut", {
    **W1("carport", lot=[[0, 0.4], [C("more electric cars"), 1.0]], board="2025: PRODUCTION 20% ABOVE CHINA'S OWN DEMAND (IEA)"),
    "cam": cam((0, 900, 480, 1.0), (C("prices fall"), 600, 520, 1.1, 1.2)), "drift": 3,
    "items": [car([[0, -300], [6, 2600]], 0.1, carKind="suv", color=GOLD),
              it("toonwords", text="TOO MANY CARS", x=700, y=250, at=C("more electric cars"), size=64, color=RED)]},
    sources=["iea_gevo"])
stage("s42_margin", "a5_margin", {
    **W1("pricestreet", cuts=[[C("And they did"), 0, "$27,900"], [C("And they did", 0.5), 1, "$26,500"], [C("And they did", 1.0), 2, "$27,000"]], margin=0.3, gauge=False, sx=220, gap=440),
    "cam": cam((0, 960, 470, 1.0), (C("four point one"), 1100, 450, 0.98, 1.4)), "drift": 3,
    "items": [MORGAN(300, 0.1, face="worry", hold="clipboard"),
              chart([{"label": "2024", "value": 4.3, "color": BLUE, "at": C("four point one", -0.4), "display": "4.3%"},
                     {"label": "2025", "value": 4.1, "color": "#FF7043", "at": C("four point one"), "display": "4.1%"},
                     {"label": "H1 2026", "value": 3.8, "color": RED, "at": C("three point eight"), "display": "3.8%"}],
                    at=C("four point one", -0.6), max=5, title="CHINA AUTO MARGIN (NBS)", x=1280, y=150, w=560, h=380)]},
    sources=["nbs25", "nbs26"])
add("p43_war", "a5_draw", "engine_draw", {
    "title": "How a price war squeezes (illustrative)", "board": BOARD, "draw_start": C("price war squeezes"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 860 L 1500 860 M 600 860 L 600 380", "color": "ink", "width": 5, "start": C("price war squeezes")},
        {"d": "M 620 440 L 820 440 L 860 520 L 1040 520 L 1080 600 L 1260 600 L 1300 660 L 1480 660", "color": "risk", "width": 7, "start": C("This line is the price"), "label": lbl("PRICE", 660, 420, 24, "risk")},
        {"d": "M 620 700 L 1480 740", "color": "accent2", "width": 7, "start": C("This one, the cost"), "label": lbl("COST", 660, 680, 24, "accent2")},
        {"d": arrow((720, 450), (720, 690)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("The gap is the margin"), "label": lbl("MARGIN", 790, 580, 22, "accent3")},
        {"d": dot(840, 500), "color": "risk", "width": 1, "start": C("One company cuts"), "label": lbl("CUT", 900, 490, 20, "risk")},
        {"d": dot(1060, 580), "color": "risk", "width": 1, "start": C("Rivals follow"), "label": lbl("CUT", 1110, 570, 20, "risk")},
        {"d": arrow((1400, 670), (1400, 735)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("The gap shrinks"), "label": lbl("THIN", 1450, 705, 22, "accent3")},
        {"d": dot(1050, 330), "color": "ink", "width": 1, "start": C("The strongest"), "label": lbl("STRONG: SURVIVE ON THIN MARGINS · WEAK: CAN'T", 1050, 330, 24, "ink")},
        {"d": dot(1050, 920), "color": "muted", "width": 1, "start": C("Costs fall too"), "label": lbl("ILLUSTRATIVE · NO REAL DATA", 1050, 920, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("The gap shrinks", 0.2), "dur": 1.4, "target": [1400, 700]}],
    "scale": 0.86, "floor": 1040})
stage("s44_fail", "a5_fail", {
    **W1("pricestreet", start=["CLOSED", "$24,900", "CLOSED"], cuts=[[C("Hozon"), 1, "CLOSED"]], margin=0.15, gaugeText="WEAKEST MAKERS"),
    "cam": cam((0, 1000, 470, 0.95), (C("Price wars help buyers"), 900, 520, 1.05, 1.2)), "drift": 3,
    "items": [sign("WM MOTOR: BANKRUPTCY REORGANIZATION (OCT 2023)", 600, 120, C("WM Motor"), color="#FFCDD2", size=24),
              sign("HOZON (NETA): BANKRUPTCY PROCEEDINGS (JUN 2025)", 1250, 200, C("Hozon"), color="#FFCDD2", size=24),
              JUNE([[0, 2400], [C("Price wars help buyers"), 1500]], 0.2, face="grin", hold="phone", faces=[[0, "grin"], [C("They bury"), "worry"]])]},
    sources=["wm", "neta"])
stage("s45_export", "a5_export", {
    **W1("carport", lot=[[0, 0.9], [C("running more than"), 1.0]], board="CHINA EV EXPORTS, 2025: > 2.5 MILLION (IEA)"),
    "cam": cam((0, 1000, 480, 1.0), (C("running more than"), 400, 560, 1.15, 1.4)), "drift": 4,
    "items": [car([[0, 2600], [7, -300]], 0.1, carKind="hatch", color=RED, flip=True),
              it("counter", x=1300, y=170, at=C("exports doubled"), suffix="M+", decimals=1, steps=[[0, 0], [C("exports doubled"), 0], [C("half million"), 2.5]], text="ELECTRIC CAR EXPORTS, 2025 (IEA)", until=C("running more than")),
              sign("EXPORTS > OVERSEAS SALES BY 25%+ (IEA EST.)", 400, 160, C("running more than"), color="#FFCDD2", size=28),
              it("toonwords", text="SHIPPED FASTER THAN SOLD", x=600, y=330, at=C("Cars shipped faster"), size=54)]},
    sources=["iea_gevo"])
stage("s46_walls", "a5_walls", {
    **W1("tariffgate", wallAt=C("America set"), euAt=C("Europe now offers", -0.4), minAt=C("minimum-price deals"), usText="U.S. · 100%",
         usSub="+ CONNECTED-CAR SOFTWARE BAN FROM MY2027", euLines=["10% EU CAR DUTY", "+ 17.0% BYD", "+ 35.3% SAIC"]),
    "cam": cam((0, 600, 470, 1.0), (C("Europe now offers"), 1100, 470, 0.9, 1.4)), "drift": 3,
    "items": [sign("SECTION 301 · SEP 2024 (USTR)", 600, 120, C("America set", 0.4), color="#FFF8E1", size=24),
              car([[0, -300], [C("America set", 0.5), 200]], 0.0, carKind="hatch", color=TEAL, flip=False)]},
    sources=["fr_301_2024", "bis_cv", "eu_pu"])
stage("s47_abroad", "a5_abroad", {
    **W1("gigaline", board="CHINESE CARMAKERS' PLANTS ABROAD, 2025: ~1.7M CARS/YR (IEA)", speed=100),
    "cam": cam((0, 960, 480, 1.0), (C("Every government"), 1000, 470, 1.0, 1.2)), "drift": 3,
    "items": [chart([{"label": "ABROAD", "value": 1.7, "color": GOLD, "at": C("cars a year"), "display": "~1.7M"},
                     {"label": "IN CHINA", "value": 29, "color": BLUE, "at": C("so far"), "display": "29M"}],
                    at=0.2, max=30, title="CAPACITY, 2025 (IEA)", x=300, y=150, w=700, h=400, until=C("Every government", 0.5)),
              sign("TARIFFS: PROTECT JOBS & SUPPLY CHAINS", 1450, 200, C("tariffs protect jobs"), color="#C8E6C9", size=26),
              sign("ALSO: KEEP CHEAPER CARS FROM DRIVERS", 1450, 330, C("keep cheaper cars"), color="#FFCDD2", size=26),
              JUNE(600, C("Every government"), face="worry", hold="phone"), MORGAN(1700, 0.3, face="worry", hold="clipboard")]},
    sources=["iea_gevo"])

# ====================================================================== PART 6: the verdict
bumper("s48_b6", "a6_card", "6", "THE VERDICT", "All rise. Except the margins.", NAVY, "PRICELESS?")
VBASE = {**W1("gigaline", board="THE VERDICT", speed=60), "drift": 2}
stage("s49_eff", "a6_eff", {**VBASE, "cam": cam((0, 960, 520, 1.0), (C("Efficiency"), 960, 500, 1.04, 1.2)),
    "items": [it("suspects", x=960, y=420, at=0.0, scale=0.95, his=[[C("Efficiency"), 0]], stamps=[[C("guilty"), 0, "GUILTY", RED]]),
              it("toonwords", text="MAIN REASON · STRUCTURAL", x=960, y=820, at=C("the main reason"), size=48)]})
stage("s50_sub", "a6_sub", {**VBASE, **W1("evshow", carX=900), "cam": cam((0, 960, 520, 1.0), (C("an accomplice"), 960, 500, 1.04, 2.0)),
    "items": [it("suspects", x=960, y=420, at=-1, scale=0.95, his=[[0, 1]], stamps=[[-1, 0, "GUILTY", RED], [C("an accomplice"), 1, "ACCOMPLICE", "#FF7043"]]),
              it("toonwords", text="MATTERS MORE TO PROFIT THAN PRICE", x=960, y=820, at=C("matters more to profit"), size=54)]}, sources=["byd_ar25", "csis"])
stage("s51_fin", "a6_fin", {**VBASE, **W1("cashworks", mx=500), "cam": cam((0, 960, 520, 1.0), (C("real, and being unwound"), 960, 500, 1.04, 2.0)),
    "items": [it("suspects", x=960, y=420, at=-1, scale=0.95, his=[[0, 2]], stamps=[[-1, 0, "GUILTY", RED], [-1, 1, "ACCOMPLICE", "#FF7043"], [C("real, and being unwound"), 2, "UNWINDING", "#7E57C2"]])]},
    sources=["pledge", "byd_ar25"])
stage("s52_burn", "a6_burn", {**VBASE, **W1("pricestreet", margin=0.2), "cam": cam((0, 960, 520, 1.0), (C("And the price war"), 960, 500, 1.05, 1.4)),
    "items": [it("suspects", x=960, y=420, at=-1, scale=0.95, his=[[0, 3]], stamps=[[-1, 0, "GUILTY", RED], [-1, 1, "ACCOMPLICE", "#FF7043"], [-1, 2, "UNWINDING", "#7E57C2"], [C("depends who"), 3, "SOME", RED]])]},
    sources=["byd_ar25", "nio_q4"])
stage("s53_payoff", "payoff", {
    **W1("carport", lot=[[0, 0.8], [12, 1.0]], board="CHEAP CARS: HERE TO STAY · CARMAKERS: FEWER"),
    "cam": cam((0, 1000, 470, 0.9), (C("What isn't real yet"), 900, 480, 1.0, 1.6), (C("Expect the cars"), 1000, 470, 0.88, 1.6)), "drift": 2,
    "items": [it("toonwords", text="THE CHEAP CAR IS REAL", x=1000, y=150, at=C("The cheap Chinese car"), until=C("What isn't real yet"), size=60),
              it("toonwords", text="THE PROFIT? NOT YET.", x=1000, y=150, at=C("What isn't real yet"), until=C("Expect the cars"), size=60, color=RED),
              it("toonwords", text="CHEAP CARS. FEWER CARMAKERS.", x=1000, y=150, at=C("Expect the cars"), size=56, color=GOLD),
              JUNE(400, 0.2, face="happy", hold="phone"), MEI(800, 0.3, face="happy", hold="clipboard"), MORGAN(1500, 0.4, face="worry", hold="clipboard", faces=[[0, "worry"], [C("Expect the cars"), "smug"]]),
              VOLTY(1150, 0.5, tags=[[0.6, "$81/kWh"]])]})
add("s54_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s55_button", "button", {
    **W1("evshow", carX=900, price="$0.00", priceSub="THIS VIDEO · NO SUBSIDY · NO TARIFF", priceAt=0.4), "cam": cam((0, 900, 420, 1.0), (2.6, 900, 380, 1.15, WHIP)), "drift": 0, "min_seconds": 5.2,
    "items": [VOLTY(400, 0.0, scale=1.0, tags=[[0.2, "$81"], [2.6, "FREE?!"]], hops=[2.7], faces=[[0, "happy"], [2.6, "worry"]]),
              JUNE(1500, 0.1, face="grin", faces=[[0, "grin"], [2.6, "shock"]], takes=[2.6]),
              it("toonwords", text="BEST PRICE ON THE LOT", x=900, y=120, at=2.7, size=66, color=GOLD)]},
    sfx=[{"kind": "hit", "at": 2.6, "gain": 0.3}])

write(OUT, "# GENERATED by tools/gen_chinesecars_storyboard.py; edit the generator, not this file.\n"
           "# Episode 61 storyboard (Chinese cars): premium business doc with cartoon energy; worlds in CartoonStage/cars.tsx; tones from visual_direction.yaml.\n")
