"""Generates projects/how-spacex-actually-makes-money/deliverables/documentary/storyboard.yaml
(Episode 51, owner request R1: How SpaceX Actually Makes Money).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the data center at night (the rent), the launch site (new `launchpad` set) with a generic rocket.
- Part 1 (three businesses): the exchange (listing day), the office (the recast filing), the studio (segments), an engines drawing.
- Part 2 (Starlink): low orbit with a satellite constellation (new `constellation` item), the suburb, a subscriber bar drawing.
- Part 3 (the rockets): the launch site by day and night, a booster landing (new `rocket` item, `landAt`), a launches drawing.
- Part 4 (the landlord): the data center, the exchange at night, the office, a Q3 bar drawing.
- Part 5 (who's in charge): the bank hall (vote certificates), the office, parliament, a control drawing.
No logos or markings on rockets or satellites; no real people drawn (names in text only). Lint: tools/lint_storyboard.py.
Run: python tools/gen_spacex_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-spacex-actually-makes-money/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}


def chart(bars_, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


def pad(night=False):
    return {"zones": [Z("launchpad", night=night)], "worldW": 2400, **({"night": True} if night else {})}


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("datacenter")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.15}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1000, y=220, at=0.05, prefix="$", suffix="BN / MONTH", decimals=2, steps=[[0.05, 0], [1.6, 1.25]], text="RENT FOR COMPUTING POWER (PROSPECTUS)", scale=1.4),
              it("letters", x=1000, y=470, text="NOT FOR A ROCKET…", at=C("Not for a rocket launch"), until=C("For computer chips"), size=64, color="white"),
              it("letters", x=1000, y=470, text="FOR COMPUTER CHIPS", at=C("For computer chips"), size=72, color="gold")]},
    sources=["pros"])
stage("s02_twist", "h_twist", {
    **pad(), "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.05}, {"at": C("In its latest quarter"), "x": 1150, "y": 500, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("rocket", x=760, at=0.2, scale=0.62),
              it("letters", x=1100, y=120, text="SPACEX OPENS ITS BOOKS", at=0.3, until=C("In its latest quarter"), size=58, color="gold"),
              it("sign", x=1400, y=170, text="1 · ARTIFICIAL INTELLIGENCE", at=C("artificial intelligence came first"), color="#C8E6C9", size=32),
              it("sign", x=1400, y=270, text="2 · INTERNET SUBSCRIPTIONS", at=C("internet subscriptions second"), color="#BBDEFB", size=32),
              it("sign", x=1400, y=370, text="3 · ROCKETS", at=C("and rockets last"), color="#FFCDD2", size=32)]},
    sources=["q3"])
stage("s03_question", "h_question", {
    **pad(True), "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": 0.8, "x": 1000, "y": 380, "zoom": 0.95, "dur": 3}], "drift": 2,
    "items": [it("rocket", x=760, at=0.0, scale=0.62, launchAt=0.6),
              it("letters", x=1200, y=150, text="HOW DOES SPACEX MAKE MONEY?", at=0.3, size=56, color="gold"),
              it("sign", x=1300, y=300, text="WHY DO THE ROCKETS LOSE MONEY?", at=C("And why has"), color="#FFCDD2", size=34)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · WHERE THE MONEY COMES FROM", at=C("where SpaceX's money"), color="#BBDEFB", size=28),
              it("sign", x=960, y=520, text="2 · WHO RIDES THE ROCKETS", at=C("carry its own cargo"), color="#FFE0B2", size=30),
              it("sign", x=1560, y=380, text="3 · WHO CONTROLS IT", at=C("who really controls"), color="#C8E6C9", size=30),
              it("letters", x=960, y=760, text="FOLLOW THE MONEY TO ORBIT", at=0.4, size=60, color="gold")]})

# ====================================================================== PART 1: three businesses
card("s05_c1", "m1_card", "Three Businesses", "What the filings show")
stage("s06_ipo", "m1_ipo", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("At that price"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="JUNE 12, 2026 · TICKER SPCX", at=0.3, size=54, color="gold"),
              it("counter", x=760, y=280, at=C("The shares were sold"), prefix="$", suffix="", steps=[[0, 0], [{"cue": "each, and the company"}, 135]], text="IPO PRICE PER SHARE"),
              it("sign", x=1400, y=260, text="≈ $85.7BN RAISED, NET (SEC FILING)", at=C("raised about"), color="#C8E6C9", size=30),
              it("sign", x=1400, y=380, text="A TEXAS CORPORATION", at=C("a Texas corporation"), color="#BBDEFB", size=30),
              it("sign", x=1250, y=520, text="≈ $1.77 TRILLION AT $135 (OUR CALCULATION)", at=C("by our calculation"), color="#FFE0B2", size=32)]},
    sources=["ipo8k", "q2", "pros"])
stage("s07_recast", "m1_recast", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("On that basis"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("docs", x=700, y=560, at=0.3, text="PROSPECTUS · RECAST FIGURES", scale=0.7, stamp="+ xAI + X", stampAt=C("rewrite SpaceX's past")),
              it("sign", x=1350, y=220, text="xAI · ALSO OWNS X", at=C("bought xAI"), color="#BBDEFB", size=32),
              it("sign", x=1350, y=320, text="BOTH CONTROLLED BY ELON MUSK", at=C("Both were controlled"), color="#FFE0B2", size=30),
              it("counter", x=1350, y=470, at=C("On that basis"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "was eighteen"}, 18.7]], text="REVENUE 2025 (RECAST)")]},
    sources=["pros"])
stage("s08_split", "m1_split", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}, {"at": C("Connectivity"), "x": 1000, "y": 540, "zoom": 1.02, "dur": 2}], "drift": 1,
    "items": [chart([{"label": "SPACE", "value": 4.1, "color": "#90A4AE", "at": C("Space, meaning"), "display": "$4.1BN"},
                     {"label": "CONNECTIVITY", "value": 11.4, "color": "#1E88E5", "at": C("Connectivity"), "display": "$11.4BN"},
                     {"label": "AI (INCL. X ADS)", "value": 3.2, "color": "#43A047", "at": C("And artificial intelligence"), "display": "$3.2BN"}],
                    at=0.2, max=12, title="REVENUE BY SEGMENT, 2025 (PROSPECTUS)")]},
    sources=["pros"])
stage("s09_loss", "m1_loss", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Overall"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="OPERATING RESULT, 2025", at=0.3, size=54, color="gold"),
              it("sign", x=700, y=250, text="STARLINK: + $4.4BN", at=C("Starlink earned"), color="#C8E6C9", size=36),
              it("sign", x=1250, y=250, text="SPACE: − $657M", at=C("The space business lost"), color="#FFCDD2", size=36),
              it("sign", x=1800, y=250, text="AI: − $6.4BN", at=C("The artificial intelligence business lost"), color="#FFCDD2", size=36),
              it("counter", x=1250, y=470, at=C("Overall"), prefix="−$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "net loss"}, 4.9]], text="NET LOSS 2025 (PROSPECTUS)")]},
    sources=["pros"])
add("p10_engines", "m1_draw", "engine_draw", {
    "title": "Three engines (2025)", "board": BOARD, "draw_start": C("Here is the space business"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(640, 420, 230, 180), "color": "ink", "width": 6, "kind": "box", "start": C("Here is the space business"), "label": lbl("SPACE", 755, 518, 26, "ink")},
        {"d": rect(1000, 640, 260, 180), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is Starlink"), "label": lbl("STARLINK", 1130, 738, 26, "accent2")},
        {"d": rect(1380, 420, 230, 180), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is artificial intelligence"), "label": lbl("AI", 1495, 518, 26, "accent3")},
        {"d": arrow((1060, 635), (820, 605)), "color": "accent", "width": 5, "kind": "arrow", "start": C("Now the arrows")},
        {"d": arrow((1200, 635), (1430, 605)), "color": "accent", "width": 5, "kind": "arrow", "start": C("Now the arrows", 0.6), "label": lbl("ONLY PROFIT", 1130, 870, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("One engine was carrying", 0.1), "dur": 1.4, "target": [1130, 730]}],
    "scale": 0.86, "floor": 1040}, sources=["pros"])
kinetic("s11_t1", "m1_transition", [("Let's start with the engine…", 66, "So let's start", None, False),
                                    ("…that carries everything", 70, "carries everything", "gold", False)])

# ====================================================================== PART 2: Starlink
card("s12_c2", "m2_card", "Starlink", "Internet from orbit")
stage("s13_subs", "m2_subs", {
    "zones": [Z("orbit")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 420, "zoom": 1.05}, {"at": C("By the end of September"), "x": 1000, "y": 520, "zoom": 0.95, "dur": 2}], "drift": 3,
    "items": [it("constellation", x=1000, y=260, at=0.2, w=2000, n=12, rows=3, beamAt=C("A small dish"), ground=560),
              it("counter", x=1000, y=640, at=C("By the end of September"), prefix="", suffix="M", decimals=1, steps=[[0, 0], [{"cue": "consumer subscribers"}, 13.6]], text="STARLINK CONSUMER SUBSCRIBERS, SEP 2026"),
              it("sign", x=1000, y=780, text="174 COUNTRIES, TERRITORIES AND MARKETS", at=C("countries, territories"), color="#BBDEFB", size=30)]},
    sources=["q3", "tenq3"])
stage("s14_sats", "m2_sats", {
    "zones": [Z("orbit")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 400, "zoom": 1.15}, {"at": C("According to the prospectus"), "x": 1100, "y": 460, "zoom": 1.0, "dur": 2}], "drift": 3,
    "items": [it("constellation", x=1000, y=330, at=0.1, w=2200, n=16, rows=4),
              it("counter", x=700, y=120, at=0.3, prefix="", suffix="+", steps=[[0, 0], [{"cue": "Starlink satellites"}, 11100]], text="STARLINK SATELLITES IN ORBIT (10-Q)"),
              it("sign", x=1400, y=640, text="≈ 75% OF ACTIVE MANEUVERABLE SATELLITES (PROSPECTUS)", at=C("According to the prospectus"), color="#FFE0B2", size=28)]},
    sources=["pros", "tenq3"])
stage("s15_arpu", "m2_arpu", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The company says"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("home", x=500, at=0.2, scale=0.8), it("home", x=1500, at=0.4, scale=0.8, color="#E1F5FE"),
              it("counter", x=1000, y=230, at=C("Average revenue"), prefix="$", suffix=" / MONTH", steps=[[0, 99], [{"cue": "In early"}, 99], [{"cue": "sixty-six dollars"}, 66]], text="REVENUE PER SUBSCRIBER (PROSPECTUS)", scale=1.2),
              it("sign", x=1250, y=400, text="WHY: INTERNATIONAL EXPANSION + CHEAPER PLANS", at=C("The company says"), color="#FFE0B2", size=30)]},
    sources=["pros"])
stage("s16_margin", "m2_margin", {
    "zones": [Z("orbit")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.0}, {"at": C("By our calculation"), "x": 1000, "y": 520, "zoom": 1.06, "dur": 2}], "drift": 2,
    "items": [it("constellation", x=1000, y=200, at=0.1, w=2000, n=10, rows=2),
              it("coins", **{"from": [800, 260], "to": [1000, 700]}, at=0.5, rate=4, until=C("of every dollar")),
              it("counter", x=1300, y=430, at=C("the connectivity business earned"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "of operating profit"}, 2.4]], text="Q3 2026 OPERATING PROFIT (ON $5.2BN)"),
              it("letters", x=1000, y=720, text="≈ 45¢ OF EVERY $1 (OUR CALCULATION)", at=C("By our calculation"), size=48, color="gold")]},
    sources=["q3"])
add("p17_subs", "m2_draw", "engine_draw", {
    "title": "The subscriber climb", "board": BOARD, "draw_start": C("Twenty twenty-three, about"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 780 L 1500 780", "color": "ink", "width": 5, "start": C("Let me draw")},
        {"d": "M 640 780 L 640 735 L 800 735 L 800 780 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Twenty twenty-three, about"), "label": lbl("2023 · 2.3M", 720, 715, 20, "accent2")},
        {"d": "M 860 780 L 860 690 L 1020 690 L 1020 780 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Twenty twenty-four"), "label": lbl("2024 · 4.4M", 940, 670, 20, "accent2")},
        {"d": "M 1080 780 L 1080 600 L 1240 600 L 1240 780 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Twenty twenty-five"), "label": lbl("2025 · 8.9M", 1160, 580, 20, "accent2")},
        {"d": "M 1300 780 L 1300 505 L 1460 505 L 1460 780 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("And by September"), "label": lbl("SEP 2026 · 13.6M*", 1380, 485, 20, "accent3")},
        {"d": "M 1040 860 L 1040 860", "color": "muted", "width": 1, "start": C("consumers alone"), "label": lbl("* CONSUMERS ONLY (NEW DEFINITION)", 1050, 840, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Each bar is a city", 0.1), "dur": 1.4, "target": [1380, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["pros", "q3"])
kinetic("s18_t2", "m2_transition", [("Starlink pays the bills…", 70, "Starlink pays the bills", "gold", False),
                                    ("…so what about the rockets?", 66, "what about the rockets", None, False)])

# ====================================================================== PART 3: the rockets
card("s19_c3", "m3_card", "The Rockets", "A delivery truck to orbit")
stage("s20_count", "m3_count", {
    **pad(), "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("And according to"), "x": 1000, "y": 380, "zoom": 0.95, "dur": 2.5}], "drift": 2,
    "items": [it("rocket", x=760, at=0.1, scale=0.62, launchAt=C("Falcon rockets")),
              it("counter", x=1350, y=180, at=C("In twenty twenty-five"), prefix="", suffix="", steps=[[0, 0], [{"cue": "Falcon rockets"}, 165]], text="FALCON LAUNCHES IN 2025 (PROSPECTUS)"),
              it("sign", x=1350, y=380, text="> 80% OF THE WORLD'S MASS TO ORBIT, EACH YEAR", at=C("more than eighty percent"), color="#FFE0B2", size=28)]},
    sources=["pros"])
stage("s21_own", "m3_own", {
    "zones": [Z("orbit")], "worldW": 2400, "night": True, "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("By our calculation"), "x": 1200, "y": 500, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("constellation", x=700, y=300, at=C("The other one hundred"), w=1200, n=8, rows=2),
              it("letters", x=700, y=640, text="WHO RIDES THE ROCKETS?", at=0.2, until=C("The other one hundred"), size=50, color="white"),
              it("sign", x=1400, y=160, text="43 · PAYING CUSTOMERS", at=C("only forty-three"), color="#C8E6C9", size=32),
              it("sign", x=1400, y=260, text="122 · SPACEX'S OWN STARLINK", at=C("The other one hundred"), color="#BBDEFB", size=32),
              it("sign", x=1400, y=360, text="≈ 3 IN 4 (OUR CALCULATION)", at=C("three out of every four"), color="#FFE0B2", size=30),
              it("letters", x=1400, y=520, text="NO LAUNCH REVENUE BOOKED", at=C("books no revenue"), size=48, color="gold")]},
    sources=["pros"])
stage("s22_reuse", "m3_reuse", {
    **pad(), "cam": [{"at": 0, "x": 1300, "y": 300, "zoom": 0.9}, {"at": C("The prospectus counts"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 2.2}], "drift": 1,
    "items": [it("rocket", x=1728, at=0.0, scale=0.55, landAt=0.4),
              it("letters", x=900, y=140, text="FLY BACK. LAND. FLY AGAIN.", at=0.3, size=54, color="gold"),
              it("counter", x=900, y=330, at=C("The prospectus counts"), prefix="", suffix="+", steps=[[0, 0], [{"cue": "successful booster landings"}, 570]], text="SUCCESSFUL BOOSTER LANDINGS (PROSPECTUS)")]},
    sources=["pros"])
stage("s23_starship", "m3_starship", {
    "zones": [Z("site")], "worldW": 2400, "cam": [{"at": 0, "x": 900, "y": 420, "zoom": 1.0}, {"at": C("That year"), "x": 1250, "y": 500, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("rocket", x=950, at=0.1, scale=0.8),
              it("counter", x=1400, y=160, at=C("In twenty twenty-five alone"), prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "research and development"}, 3.0]], text="STARSHIP R&D IN 2025 (PROSPECTUS)"),
              it("sign", x=1400, y=320, text="> $15BN INVESTED SO FAR", at=C("more than fifteen billion"), color="#FFE0B2", size=32),
              it("sign", x=1400, y=420, text="SPACE SEGMENT 2025: − $657M", at=C("That year"), color="#FFCDD2", size=32),
              it("sign", x=1400, y=520, text="RISK: DELAY LIMITS GROWTH PLANS", at=C("The prospectus warns"), color="#BBDEFB", size=28)]},
    sources=["pros"])
stage("s24_gov", "m3_gov", {
    **pad(), "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("and every crew"), "x": 1250, "y": 500, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("rocket", x=760, at=0.1, scale=0.6, launchAt=C("and every crew", 0.5)),
              it("letters", x=1300, y=130, text="STEADY GOVERNMENT MONEY", at=0.3, size=52, color="gold"),
              it("sign", x=1350, y=270, text="11 OF 12 NATIONAL-SECURITY LAUNCHES (2025)", at=C("eleven of the twelve"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=370, text="ALL NASA CREW AND CARGO FLIGHTS TO THE STATION", at=C("and every crew"), color="#C8E6C9", size=28)]},
    sources=["pros"])
add("p25_launches", "m3_draw", "engine_draw", {
    "title": "One year of launches (2025)", "board": BOARD, "draw_start": C("Here are one hundred"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 380, 300, 150), "color": "ink", "width": 6, "kind": "box", "start": C("Here are one hundred"), "label": lbl("165 FALCON LAUNCHES", 1010, 462, 22, "ink")},
        {"d": rect(620, 660, 260, 140), "color": "accent3", "width": 6, "kind": "box", "start": C("forty-three carry"), "label": lbl("43 CUSTOMERS", 750, 737, 22, "accent3")},
        {"d": arrow((750, 655), (900, 540), 0.2), "color": "accent3", "width": 5, "kind": "arrow", "start": C("send money back in"), "label": lbl("$ IN", 790, 590, 20, "accent3")},
        {"d": rect(1140, 660, 280, 140), "color": "accent2", "width": 6, "kind": "box", "start": C("one hundred and twenty-two carry"), "label": lbl("122 STARLINK", 1280, 737, 22, "accent2")},
        {"d": arrow((1280, 655), (1280, 300)), "color": "accent2", "width": 5, "kind": "arrow", "start": C("send satellites up"), "label": lbl("SATELLITES UP, $0", 1280, 280, 20, "accent2")},
    ],
    "actions": [{"kind": "point", "at": C("delivery truck", 0.1), "dur": 1.4, "target": [1280, 730]}],
    "scale": 0.86, "floor": 1040}, sources=["pros"])
kinetic("s26_t3", "m3_transition", [("And then, in 2026…", 72, "And then", None, False),
                                    ("…a third business took over", 66, "a third business", "gold", False)])

# ====================================================================== PART 4: the landlord
card("s27_c4", "m4_card", "The Landlord", "Renting out computers")
stage("s28_xai", "m4_xai", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It also includes"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="FEB 2026: SPACEX + xAI", at=0.3, size=56, color="gold"),
              it("sign", x=1100, y=240, text="NEW NAME: 'SUPER INTELLIGENCE'", at=C("renamed Super Intelligence"), color="#C8E6C9", size=32),
              it("sign", x=1100, y=340, text="+ X (SOCIAL NETWORK)", at=C("the social network X"), color="#BBDEFB", size=30),
              it("sign", x=1100, y=440, text="+ CURSOR · IMPLIED VALUE $60BN", at=C("and Cursor"), color="#FFE0B2", size=30)]},
    sources=["q3"])
stage("s29_rent", "m4_rent", {
    "zones": [Z("datacenter")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("After three months"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="IT IS RENT", at=C("It is rent"), size=64, color="gold"),
              it("counter", x=800, y=300, at=0.3, prefix="≈ ", suffix="", steps=[[0, 0], [{"cue": "Nvidia graphics chips"}, 325000]], text="GRAPHICS CHIPS RENTED (PROSPECTUS)"),
              it("counter", x=1450, y=300, at=C("at one point two five"), prefix="$", suffix="BN / MO", decimals=2, steps=[[0, 0], [{"cue": "through May"}, 1.25]], text="TO MAY 2029 (PROSPECTUS)"),
              it("sign", x=1250, y=500, text="AFTER 3 MONTHS: EITHER SIDE CAN EXIT ON 90 DAYS' NOTICE", at=C("After three months"), color="#FFE0B2", size=26)]},
    sources=["pros"])
stage("s30_q3", "m4_q3", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And one single customer"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=800, y=200, at=0.3, prefix="$", suffix="BN", decimals=1, steps=[[0, 5.6], [{"cue": "a year earlier"}, 14.6]], text="Q3 2026 REVENUE (UP FROM $5.6BN)", scale=1.2),
              it("sign", x=1450, y=200, text="SUPER INTELLIGENCE $7.6BN > STARLINK $5.2BN", at=C("Super Intelligence brought in"), color="#C8E6C9", size=28),
              it("letters", x=1250, y=440, text="ONE UNNAMED CUSTOMER = 34.5% OF REVENUE", at=C("And one single customer"), size=44, color="gold")]},
    sources=["q3", "tenq3"])
stage("s31_profit", "m4_profit", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But that figure"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=200, at=0.3, prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "four point four billion"}, 4.4]], text="Q3 2026 NET INCOME"),
              it("docs", x=700, y=560, at=C("But that figure"), text="10-Q · Q3 2026", scale=0.7, stamp="READ THE DETAILS", stampAt=C("helped by a tax benefit")),
              it("sign", x=1400, y=380, text="+ TAX BENEFIT", at=C("helped by a tax benefit"), color="#FFE0B2", size=32),
              it("sign", x=1400, y=480, text="+ GAIN ON BORING CO. STAKE", at=C("by a gain"), color="#FFE0B2", size=32)]},
    sources=["tenq3"])
stage("s32_capex", "m4_capex", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By our calculation"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=200, at=0.3, prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "on capital expenditure"}, 48.1]], text="CAPITAL SPENDING, JAN–SEP 2026 (10-Q)", scale=1.3),
              it("letters", x=1250, y=440, text="≈ 83% FOR SUPER INTELLIGENCE (OUR CALCULATION)", at=C("By our calculation"), size=42, color="gold"),
              it("coins", **{"from": [600, 700], "to": [1500, 720]}, at=C("costs a fortune"), rate=5, until=C("By our calculation"))]},
    sources=["tenq3"])
add("p33_q3", "m4_draw", "engine_draw", {
    "title": "Q3 2026 revenue by segment", "board": BOARD, "draw_start": C("A bar for rockets"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 780 L 1480 780", "color": "ink", "width": 5, "start": C("Let me draw")},
        {"d": "M 680 780 L 680 700 L 880 700 L 880 780 Z", "color": "ink", "width": 3, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("A bar for rockets"), "label": lbl("ROCKETS $1.8BN", 780, 680, 20, "ink")},
        {"d": "M 950 780 L 950 545 L 1150 545 L 1150 780 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("A bar for Starlink"), "label": lbl("STARLINK $5.2BN", 1050, 525, 20, "accent2")},
        {"d": "M 1220 780 L 1220 440 L 1420 440 L 1420 780 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("And a bar for Super Intelligence"), "label": lbl("SUPER INTELLIGENCE $7.6BN", 1320, 420, 20, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("biggest share", 0.1), "dur": 1.4, "target": [1320, 500]}],
    "scale": 0.86, "floor": 1040}, sources=["q3"])
kinetic("s34_t4", "m4_transition", [("One question left…", 70, "Which leaves one question", None, False),
                                    ("…who is in charge?", 74, "Who is in charge", "gold", False)])

# ====================================================================== PART 5: who's in charge
card("s35_c5", "m5_card", "Who's In Charge", "Votes, risks and customers")
stage("s36_vote", "m5_vote", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("That makes SpaceX"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=1500, y=180, text="ELON MUSK: > 80% OF THE VOTES", at=0.3, color="#FFE082", size=36),
              it("shares", x=760, y=440, at=0.4, scale=0.9, groups=[{"n": 80, "color": "#FFC93C", "label": "MUSK (> 80%)", "at": C("he held")},
                                                                     {"n": 20, "color": "#90CAF9", "label": "EVERYONE ELSE", "at": C("of the voting power")}]),
              it("sign", x=1500, y=300, text="CLASS B = 10 VOTES PER SHARE", at=C("ten votes each"), color="#BBDEFB", size=30),
              it("sign", x=1500, y=420, text="A 'CONTROLLED COMPANY' (NASDAQ RULES)", at=C("That makes SpaceX"), color="#FFE0B2", size=28)]},
    sources=["pros"])
stage("s37_risk", "m5_risk", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("and that he does not"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("docs", x=700, y=560, at=0.3, text="RISK FACTORS · PROSPECTUS", scale=0.7, stamp="KEY PERSON", stampAt=C("highly dependent")),
              it("sign", x=1400, y=220, text="'HIGHLY DEPENDENT ON ... MR. MUSK'", at=C("highly dependent"), color="#FFCDD2", size=30),
              it("sign", x=1400, y=320, text="NO KEY-PERSON LIFE INSURANCE", at=C("key person life insurance"), color="#FFE0B2", size=30),
              it("sign", x=1400, y=420, text="NOT FULL TIME: ALSO RUNS TESLA", at=C("and that he does not"), color="#BBDEFB", size=30)]},
    sources=["pros"])
stage("s38_govdep", "m5_govdep", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Its government contracts"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("counter", x=1000, y=200, at=0.3, prefix="≈ ", suffix="%", steps=[[0, 0], [{"cue": "of SpaceX's revenue"}, 21]], text="ONE UNNAMED CUSTOMER'S SHARE OF 2025 REVENUE"),
              it("sign", x=1000, y=400, text="NASA · DEPARTMENT OF WAR · GSA · INTELLIGENCE AGENCIES", at=C("Its government contracts"), color="#BBDEFB", size=28)]},
    sources=["pros"])
add("p39_control", "m5_draw", "engine_draw", {
    "title": "The control panel", "board": BOARD, "draw_start": C("Here is SpaceX"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(940, 380, 320, 200), "color": "ink", "width": 6, "kind": "box", "start": C("Here is SpaceX"), "label": lbl("SPACEX · 3 BUSINESSES", 1100, 487, 20, "ink")},
        {"d": rect(620, 680, 260, 120), "color": "accent2", "width": 5, "kind": "box", "start": C("Here are the ordinary"), "label": lbl("SHAREHOLDERS", 750, 747, 20, "accent2")},
        {"d": rect(1320, 680, 260, 120), "color": "risk", "width": 6, "kind": "box", "start": C("And here is one person"), "label": lbl("ONE PERSON · > 80% VOTES", 1450, 747, 18, "risk")},
        {"d": arrow((1440, 675), (1200, 585)), "color": "risk", "width": 6, "kind": "arrow", "start": C("Every arrow of control"), "label": lbl("CONTROL", 1360, 610, 20, "risk")},
        {"d": arrow((760, 675), (980, 585)), "color": "accent2", "width": 3, "kind": "arrow", "start": C("with their shares"), "label": lbl("A SHARE OF VALUE", 830, 610, 18, "accent2")},
    ],
    "actions": [{"kind": "point", "at": C("runs through one box", 0.1), "dur": 1.4, "target": [1450, 740]}],
    "scale": 0.86, "floor": 1040}, sources=["pros"])

# ====================================================================== PAYOFF
stage("s40_payoff", "payoff", {
    **pad(True), "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("The lesson is"), "x": 1000, "y": 360, "zoom": 0.95, "dur": 3}], "drift": 3,
    "items": [it("rocket", x=760, at=0.1, scale=0.6, launchAt=C("The lesson is")),
              it("letters", x=1300, y=120, text="NOT MAINLY FROM ROCKETS", at=0.3, until=C("The lesson is"), size=54, color="gold"),
              it("sign", x=1400, y=230, text="ROCKET = DELIVERY TRUCK", at=C("the rocket is the delivery truck"), color="#FFE0B2", size=32),
              it("sign", x=1400, y=330, text="STARLINK = CASH REGISTER", at=C("Starlink is the cash register"), color="#C8E6C9", size=32),
              it("sign", x=1400, y=430, text="AI = LANDLORD WITH BIG BILLS", at=C("the newest business is a landlord"), color="#BBDEFB", size=32),
              it("letters", x=1300, y=120, text="STARSHIP · A FEW CUSTOMERS · ONE MAN", at=C("Whether that mix"), size=46, color="gold")]},
    sources=["pros", "q3"])
add("s41_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_spacex_storyboard.py; edit the generator, not this file.\n"
           "# Episode 51 storyboard (SpaceX): one visual language per part; tones from visual_direction.yaml.\n")
