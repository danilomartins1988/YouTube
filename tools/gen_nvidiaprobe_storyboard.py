"""Generates projects/why-nvidia-lost-428-billion-in-two-days/deliverables/documentary/storyboard.yaml
(Episode 52, owner request R2: Why Nvidia Lost $428 Billion in Two Days).

OWNER DIRECTION: very animated cartoon, few charts, mostly drawn scenes; retro-future sci-fi comedy feel inspired at genre
level only (thick outlines, flat saturated colours, squash and stretch, joke signs, chrome + neon, tubes, flying cars).
All designs are original (new CartoonStage pieces: `chipcity`, `searoute`, `secretroom` sets; `chipbuddy`, `stockelevator`,
`detective`, `emptychair`, `freighter` items). Only ONE chart (the Singapore bar sketch).
One visual language per part:
- Hook: chip city with the falling stock elevator; the sea route at night.
- Part 1 (one man, one company): chip city by day, the empty CEO chair, the office with the annual report.
- Part 2 (the weekend): newsroom, the empty chair + memo, office + detective, chip city (rivals hop, Nvidia sinks), the elevator.
- Part 3 (chips at the border): the sea route with the EXPORT RULES checkpoint buoy and freighters, the data center.
- Part 4 (the Singapore question): tropical business district (billing), the data center, parliament + office.
- Part 5 (what happens next): office + detective, the closed-door briefing room, chip city.
Rules: Huang is never drawn (empty chair; name in text only); the woman is never named or shown; allegations labelled
REPORTED / ALLEGED; our market-value figures labelled OUR ESTIMATE. Lint: tools/lint_storyboard.py.
Run: python tools/gen_nvidiaprobe_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-nvidia-lost-428-billion-in-two-days/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
FLOORS = ["$4.50TN", "$4.31TN", "$4.07TN"]


def buddy(x, y=860, **kw):
    return it("chipbuddy", x=x, y=y, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("chipcity")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.15}, {"at": 1.2, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=640, y=200, at=0.05, prefix="≈ -$", suffix="BN", steps=[[0.05, 0], [{"cue": "two trading days"}, 428]], text="NVIDIA MARKET VALUE, 2 DAYS (OUR ESTIMATE)", scale=1.3),
              it("stockelevator", x=1560, y=110, at=0.3, scale=0.78, floors=FLOORS, stops=[C("lost in just"), C("two trading days")], text="NVIDIA SHARES × 24.1BN"),
              buddy(520, 860, at=0.5, mood="happy", moods=[[C("lost in just"), "shock"]], label="GPU", hop=30)]},
    sources=["px", "sec"])
stage("s02_twist", "h_twist", {
    "zones": [Z("chipcity")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("What changed"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=500, y=250, text="FACTORY: FINE ✓", at=C("No factory"), color="#C8E6C9", size=34),
              it("sign", x=1000, y=250, text="CHIPS: WORKING ✓", at=C("No chip"), color="#C8E6C9", size=34),
              it("sign", x=1500, y=250, text="ORDERS: STILL HERE ✓", at=C("No customer"), color="#C8E6C9", size=34),
              it("letters", x=1100, y=430, text="…ONE STORY, ONE WEEKEND", at=C("What changed"), size=58, color="gold"),
              buddy(700, 860, at=0.3, mood="cool", moods=[[C("What changed"), "worry"]], label="GPU", color="#FF9F1C"),
              buddy(1300, 860, at=0.5, mood="happy", moods=[[C("What changed"), "shock"]], label="GPU", color="#7B61FF", hop=20)]},
    sources=["px"])
stage("s03_question", "h_question", {
    "zones": [Z("searoute", night=True, buoyAt=0.5)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": 0.8, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("freighter", x=[[0, 200], [5.0, 1100]], y=650, at=0.2, scale=0.8, labels=["CHIPS", "SERVERS", "GPUS"], stopAt=C("why does")),
              it("letters", x=1000, y=150, text="HOW SO FAST? AND WHY SINGAPORE?", at=0.4, size=58, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("chipcity", signs=["FOUNDER = PRODUCT?", "REPORTED ≠ PROVEN", "EXPORT RULES AHEAD", "WHAT'S NEXT →"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("and what happens next"), "x": 1150, "y": 520, "zoom": 1.0, "dur": 2}], "drift": 3,
    "items": [it("sign", x=420, y=330, text="1 · FOUNDER AS PRODUCT", at=C("why investors"), color="#BBDEFB", size=30),
              it("sign", x=900, y=330, text="2 · CLAIMED VS ALLEGED", at=C("what the reports"), color="#FFE0B2", size=30),
              it("sign", x=1380, y=330, text="3 · EXPORT RULES", at=C("how American export"), color="#C8E6C9", size=30),
              it("sign", x=1820, y=330, text="4 · WHAT'S NEXT", at=C("and what happens next"), color="#F8BBD0", size=30),
              buddy(1000, 860, at=0.3, mood="happy", label="YOU?", hop=24)]})

# ====================================================================== PART 1: one man, one company
card("s05_c1", "m1_card", "One Man, One Company", "Key-person risk")
stage("s06_size", "m1_size", {
    "zones": [Z("chipcity")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Before"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=760, y=230, at=C("it reported about"), prefix="≈ $", suffix="BN", steps=[[0, 0], [{"cue": "of revenue"}, 216]], text="REVENUE, FISCAL 2026 (10-K)"),
              it("letters", x=1450, y=200, text="≈ $4.5 TRILLION", at=C("Before"), size=72, color="gold"),
              it("sign", x=1450, y=320, text="MARKET VALUE, NOV 6 (OUR ESTIMATE)", at=C("by our estimate"), color="#FFE0B2", size=28),
              *[buddy(500 + k * 260, 860, at=0.3 + k * 0.15, mood="happy", label="AI", color=c, hop=22 + 6 * k)
                for k, c in enumerate(["#2EC4B6", "#FF9F1C", "#7B61FF", "#E71D73", "#3A86FF"])]]},
    sources=["sec", "px"])
stage("s07_founder", "m1_founder", {
    "zones": [Z("chipcity", night=True, signs=["CEO PARKING ONLY", "KEYNOTE TONIGHT", "VISION SOLD HERE", "NOW HIRING: MORE CORES"])], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 540, "zoom": 1.1}, {"at": C("One well known"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("emptychair", x=1000, y=860, at=0.2, scale=0.9, text="FOUNDER AND CEO: JENSEN HUANG"),
              it("letters", x=1000, y=130, text="'JENSEN IS NVIDIA. NVIDIA IS JENSEN.'", at=C("Jensen is Nvidia"), size=50, color="gold"),
              it("sign", x=1000, y=230, text="STACY RASGON, ANALYST (CNBC)", at=C("Jensen is Nvidia"), color="#BBDEFB", size=28),
              buddy(420, 860, at=0.5, mood="happy", label="GPU", hop=18), buddy(1600, 860, at=0.7, mood="happy", label="GPU", color="#FF9F1C", hop=18)]},
    sources=["press"])
stage("s08_risk", "m1_risk", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And the latest proxy"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="KEY-PERSON RISK", at=0.3, size=70, color="gold"),
              it("docs", x=700, y=860, at=C("annual report"), stampAt=C("highly dependent"), text="ANNUAL REPORT", stamp="RISK"),
              it("sign", x=760, y=300, text="'HIGHLY DEPENDENT ON … OUR LONGSTANDING EXECUTIVE TEAM'", at=C("highly dependent"), color="#FFE0B2", size=24),
              it("sign", x=1450, y=420, text="'SUCCESSION' IN THE PROXY: 0 TIMES", at=C("use the word succession"), color="#FFCDD2", size=30),
              it("magnifier", x=1450, y=600, at=C("And the latest proxy"), scale=0.9),
              buddy(1150, 860, at=0.4, mood="worry", label="GPU", hop=10)]},
    sources=["sec"])
stage("s09_stake", "m1_stake", {
    "zones": [Z("chipcity")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By our estimate"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("sign", x=700, y=250, text="HUANG: ≈ 3.6% · ≈ 871M SHARES (PROXY)", at=0.4, color="#BBDEFB", size=30),
              it("counter", x=1350, y=260, at=C("By our estimate"), prefix="≈ -$", suffix="BN", steps=[[0, 0], [{"cue": "fifteen billion"}, 15]], text="HIS STAKE, PAPER VALUE, 2 DAYS (OUR ESTIMATE)"),
              it("coins", x=1350, y=520, at=C("fifteen billion"), n=10),
              buddy(700, 860, at=0.4, mood="happy", moods=[[C("By our estimate"), "sad"]], label="GPU", hop=16)]},
    sources=["sec", "px"])
add("p10_keyperson", "m1_draw", "engine_draw", {
    "title": "Key-person risk", "board": BOARD, "draw_start": C("Here is the company"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(700, 420, 300, 260), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the company"), "label": lbl("THE COMPANY", 850, 558, 24, "accent2")},
        {"d": rect(1240, 440, 220, 220), "color": "accent", "width": 6, "kind": "box", "start": C("Here is the founder"), "label": lbl("THE FOUNDER", 1350, 558, 22, "accent")},
        {"d": arrow((1235, 550), (1005, 550), 0.12), "color": "risk", "width": 10, "kind": "arrow", "start": C("Now draw an arrow"), "label": lbl("REPUTATION → PRICE", 1120, 640, 20, "risk")},
        {"d": "M 820 720 L 1380 720", "color": "ink", "width": 4, "start": C("Dan Ives"), "label": lbl("ANALYST OPINION: -25% TO -30% WITHOUT HIM", 1100, 760, 18, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("how thick that arrow is", 0.1), "dur": 1.4, "target": [1120, 540]}],
    "scale": 0.86, "floor": 1040}, sources=["sec", "press"])
kinetic("s11_t1", "m1_transition", [("Then, one weekend in November…", 70, "Then", None, False),
                                    ("…the arrow came under strain", 62, "came under strain", "gold", False)])

# ====================================================================== PART 2: the weekend
card("s12_c2", "m2_card", "The Weekend", "November 6 to 10, 2026")
stage("s13_reports", "m2_reports", {
    "zones": [Z("newsroom")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Then, on Friday"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("calendar", x=620, y=330, at=0.2, pages=[[0, "OCT 29", "2026"], [C("Then, on Friday"), "NOV 6", "2026"]]),
              it("paper", x=900, y=430, at=C("reported on a relationship"), until=C("Then, on Friday"), text="CEO AND A CHIP CUSTOMER", sub="REPORTED BY THE NEW YORK TIMES", size=36),
              it("paper", x=1300, y=430, at=C("the Times reported"), text="'WORKING FOR CHINA'S MSS'", sub="REPORTED · RELAYED BY BLOOMBERG", size=34),
              it("sign", x=1300, y=760, text="ALLEGATION · NOT PROVEN", at=C("Ministry of State Security"), color="#FFCDD2", size=30)]},
    sources=["press"])
stage("s14_memo", "m2_memo", {
    "zones": [Z("chipcity", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 540, "zoom": 1.1}, {"at": C("That is all"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 1,
    "items": [it("emptychair", x=1000, y=860, at=0.2, scale=0.9, memoAt=C("Huang wrote"), memo="MEMO, NOV 8"),
              it("sign", x=1000, y=170, text="HUANG'S EMAIL TO EMPLOYEES (NOV 8)", at=C("Huang wrote"), color="#FFF8E1", size=30),
              it("sign", x=1520, y=330, text="PRIVATE LIFE: THAT'S ALL", at=C("That is all"), color="#E1BEE7", size=28),
              it("letters", x=1000, y=290, text="WHAT MATTERS: THE MONEY", at=C("What matters"), size=54, color="gold")]},
    sources=["nvidia"])
stage("s15_board", "m2_board", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("China's foreign"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("detective", x=[[0, -200], [C("independent investigation"), 600]], y=860, at=0.2, scale=0.85, text="INDEPENDENT INVESTIGATION"),
              it("sign", x=1150, y=230, text="BOARD: 'NO REASON TO BELIEVE … SECRETS WERE COMPROMISED'", at=C("no reason to believe"), color="#C8E6C9", size=24),
              it("sign", x=1450, y=360, text="CHINA: 'UNSUBSTANTIATED'", at=C("China's foreign"), color="#FFE0B2", size=30),
              it("sign", x=1450, y=480, text="CHARGES FILED: NONE", at=C("no one has"), color="#BBDEFB", size=32)]},
    sources=["nvidia", "press"])
stage("s16_monday", "m2_monday", {
    "zones": [Z("chipcity")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Nvidia fell"), "x": 1080, "y": 530, "zoom": 1.02, "dur": 1.6}], "drift": 1,
    "items": [buddy(480, 860, at=C("The S and P"), mood="happy", label="S&P 500", color="#3A86FF", hop=30, text="+2.35%"),
              buddy(820, 860, at=C("A M D"), mood="happy", label="AMD", color="#E71D73", hop=70, hopRate=4.5, text="≈ +13%"),
              buddy(1160, 860, at=C("Broadcom"), mood="happy", label="AVGO", color="#FF9F1C", hop=55, hopRate=4, text="≈ +9%"),
              it("stockelevator", x=1720, y=120, at=0.3, scale=0.7, floors=FLOORS, stops=[C("Nvidia fell", 0.5)], text="NVIDIA: -4.27%"),
              it("letters", x=1000, y=130, text="MONDAY, NOV 9", at=0.2, size=60, color="gold")]},
    sources=["px"])
stage("s17_tuesday", "m2_tuesday", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The stock fell again"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("detective", x=[[0, 300], [C("named their investigator"), 700]], y=860, at=0.2, scale=0.85, searchAt=C("Wachtell"), text="INVESTIGATOR: JOON KIM"),
              it("sign", x=1000, y=200, text="FORMER ACTING U.S. ATTORNEY (SDNY) + WACHTELL, LIPTON", at=C("former acting"), color="#BBDEFB", size=26),
              it("stockelevator", x=1720, y=120, at=0.3, scale=0.7, floors=FLOORS, stops=[0.0, C("The stock fell again", 0.6)], text="TUESDAY: -5.47% → $168.89")]},
    sources=["nvidia", "px"])
stage("s18_sum", "m2_sum", {
    "zones": [Z("chipcity", night=True, dimAt=0.6)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": C("With roughly"), "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.2}], "drift": 2,
    "items": [it("counter", x=700, y=230, at=0.3, prefix="-", suffix="%", decimals=1, steps=[[0.3, 0], [{"cue": "nine and a half"}, 9.5]], text="SHARE PRICE, NOV 6 → NOV 10"),
              it("counter", x=700, y=480, at=C("With roughly"), prefix="≈ -$", suffix="BN", steps=[[0, 0], [{"cue": "of market value"}, 428]], text="× ≈ 24.1BN SHARES (OUR ESTIMATE)", scale=1.2),
              it("stockelevator", x=1600, y=120, at=0.2, scale=0.72, floors=FLOORS, stops=[0.0, 0.0], text="FRI → TUE"),
              buddy(1150, 860, at=0.4, mood="sad", label="GPU", hop=0)]},
    sources=["px", "sec"])
kinetic("s19_t2", "m2_transition", [("Why so scared?", 76, "So why", None, False),
                                    ("China, and the rules on chips", 64, "The answer is China", "gold", False)])

# ====================================================================== PART 3: chips at the border
card("s20_c3", "m3_card", "Chips at the Border", "U.S. export rules")
stage("s21_rules", "m3_rules", {
    "zones": [Z("searoute", buoyAt=0.5)], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("In April"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("calendar", x=820, y=260, at=0.2, pages=[[0, "2022", "LICENCES"], [C("the rules got tighter"), "2023", "TIGHTER"], [C("In April"), "2025", "H20 TOO"]]),
              it("freighter", x=[[0, 200], [C("In April"), 1100]], y=650, at=0.3, scale=0.75, labels=["H100", "A100", "H20"], stopAt=C("needed a licence")),
              it("letters", x=1400, y=140, text="≈ $4.5BN CHARGE (H20, 10-Q)", at=C("took a charge"), size=50, color="gold")]},
    sources=["sec"])
stage("s22_foreclosed", "m3_foreclosed", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Customers headquartered"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="'EFFECTIVELY FORECLOSED' (NVIDIA)", at=C("effectively foreclosed"), size=54, color="gold"),
              it("sign", x=700, y=260, text="HOPPER CHIPS TO CHINA: < 1% OF DATA CENTER REVENUE", at=C("shipments of its Hopper"), color="#BBDEFB", size=26),
              it("sign", x=1350, y=380, text="CHINA-BASED CUSTOMERS ≈ 8% OF REVENUE (OUR CALC)", at=C("Customers headquartered"), color="#FFE0B2", size=26),
              buddy(1000, 860, at=0.3, mood="sad", label="H20", color="#7B61FF", hop=8)]},
    sources=["sec"])
stage("s23_smuggle", "m3_smuggle", {
    "zones": [Z("searoute", night=True, buoyAt=0.53, sign="EXPORT RULES CHECKPOINT", sub="NO LICENCE? NO PASSAGE")], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("pleaded guilty"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 3,
    "items": [it("freighter", x=[[0, -200], [C("And in October"), 900]], y=660, at=0.3, scale=0.75, labels=["RELABELED", "SERVERS", "?"], stopAt=C("And in October")),
              it("sign", x=1000, y=170, text="GUILTY PLEA: ≥ $160M OF CHIPS, RELABELED (DOJ)", at=C("pleaded guilty"), color="#FFE0B2", size=26),
              it("sign", x=1000, y=360, text="OCT 2026: SERVERS VIA MALAYSIA AND SINGAPORE (ALLEGED)", at=C("And in October"), color="#FFCDD2", size=24),
              it("sign", x=1300, y=840, text="NVIDIA: NOT ACCUSED", at=C("Nvidia is not accused"), color="#C8E6C9", size=32)]},
    sources=["doj"])
add("p24_route", "m3_draw", "engine_draw", {
    "title": "The route the cases describe", "board": BOARD, "draw_start": C("Here is the chip"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(640, 470, 220, 160), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the chip"), "label": lbl("BUYER ABROAD", 750, 558, 20, "accent2")},
        {"d": rect(980, 470, 220, 160), "color": "accent", "width": 6, "kind": "box", "start": C("Here is a middleman"), "label": lbl("MIDDLEMAN", 1090, 558, 20, "accent")},
        {"d": rect(1320, 470, 200, 160), "color": "risk", "width": 6, "kind": "box", "start": C("into China"), "label": lbl("CHINA", 1420, 558, 22, "risk")},
        {"d": arrow((865, 550), (975, 550)), "color": "ink", "width": 5, "kind": "arrow", "start": C("Here is a middleman"), "label": lbl("RESOLD", 920, 520, 16, "ink")},
        {"d": arrow((1205, 550), (1315, 550)), "color": "risk", "width": 7, "kind": "arrow", "start": C("the arrow the rules forbid"), "label": lbl("FORBIDDEN", 1240, 450, 16, "risk")},
        {"d": "M 1292 480 L 1292 700", "color": "accent3", "width": 6, "start": C("like a checkpoint"), "label": lbl("CHECKPOINT", 1292, 730, 20, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("new labels", 0.1), "dur": 1.4, "target": [1260, 550]}],
    "scale": 0.86, "floor": 1040}, sources=["doj"])
kinetic("s25_t3", "m3_transition", [("Next stop:", 70, "Which brings us", None, False),
                                    ("Singapore", 92, "Singapore", "gold", False)])

# ====================================================================== PART 4: the Singapore question
card("s26_c4", "m4_card", "The Singapore Question", "Billed there, shipped elsewhere")
stage("s27_billing", "m4_billing", {
    "zones": [Z("tropic")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But in the same"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="SINGAPORE ON PAPER", at=0.3, size=60, color="gold"),
              it("counter", x=950, y=230, at=C("Singapore accounted"), prefix="", suffix="%", steps=[[0, 0], [{"cue": "based on where"}, 18]], text="NVIDIA REVENUE BILLED TO SINGAPORE (FY2025)", scale=1.2),
              it("sign", x=950, y=430, text="≈ $23.7BN OF INVOICES", at=C("more than twenty-three"), color="#FFE0B2", size=30),
              it("docs", x=1400, y=860, at=C("centralize invoicing"), stampAt=C("almost always shipped"), text="INVOICES", stamp="BILLED"),
              it("sign", x=1450, y=300, text="SHIPPED TO SINGAPORE: < 2%", at=C("Actual shipments"), color="#C8E6C9", size=32)]},
    sources=["sec"])
add("p28_gap", "m4_draw", "engine_draw", {
    "title": "Billed vs shipped (FY2025)", "board": BOARD, "draw_start": C("Here is the bar for billing"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 780 700 L 1460 700", "color": "ink", "width": 4, "start": C("Here is the bar for billing"), "label": lbl("SHARE OF FY2025 REVENUE (10-K)", 1120, 750, 18, "ink")},
        {"d": "M 860 700 L 860 340 L 1020 340 L 1020 700 Z", "color": "accent", "width": 4, "fill": "accent", "fillOpacity": 0.35, "kind": "bar", "start": C("Here is the bar for billing"), "label": lbl("BILLED 18%", 940, 320, 24, "accent")},
        {"d": "M 1200 700 L 1200 660 L 1360 660 L 1360 700 Z", "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.5, "kind": "bar", "start": C("actually shipped there"), "label": lbl("SHIPPED < 2%", 1280, 640, 24, "accent3")},
        {"d": arrow((1030, 420), (1190, 640), 0.15), "color": "risk", "width": 5, "kind": "arrow", "start": C("the difference is invoicing"), "label": lbl("INVOICING", 1170, 470, 18, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("companies based in the United States", 0.1), "dur": 1.4, "target": [940, 500]}],
    "scale": 0.86, "floor": 1040}, sources=["sec"])
stage("s29_megaspeed", "m4_megaspeed", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("New York Times reported"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="MEGASPEED (SINGAPORE CLOUD)", at=0.3, size=60, color="gold"),
              it("sign", x=950, y=260, text="ASSETS: $33M → $3BN IN ONE YEAR (REUTERS)", at=C("its assets grew"), color="#BBDEFB", size=28),
              it("sign", x=1400, y=380, text="≈ $2BN OF NVIDIA PRODUCTS (NYT, 2025 · REPORTED)", at=C("New York Times reported"), color="#FFE0B2", size=26),
              it("chipbuddy", x=[[0, 200], [6, 900]], y=860, at=0.3, mood="happy", label="GPU", hop=28),
              it("chipbuddy", x=[[0, 0], [6, 700]], y=860, at=0.5, mood="happy", label="GPU", color="#FF9F1C", hop=24),
              it("chipbuddy", x=[[0, -200], [6, 500]], y=860, at=0.7, mood="happy", label="GPU", color="#7B61FF", hop=20)]},
    sources=["reuters", "press"])
stage("s30_alleged", "m4_alleged", {
    "zones": [Z("parliament", x1=1500), Z("office", x0=1500)], "worldW": 3200,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.0}, {"at": C("According to the New York Times"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 1,
    "items": [it("letters", x=700, y=110, text="WASHINGTON STEPS IN", at=0.3, size=58, color="gold"),
              it("sign", x=700, y=230, text="SEN. COTTON: 'INVESTIGATE MEGASPEED' (2025)", at=C("Senator Tom Cotton"), color="#FFE0B2", size=28),
              it("sign", x=700, y=350, text="ALLEGED: DIVERSION VIA SHELL COMPANIES", at=C("alleging"), color="#FFCDD2", size=26),
              it("sign", x=2200, y=230, text="COMMERCE INQUIRY PAUSED; CASE MOVED TO DOJ (NYT · REPORTED)", at=C("According to the New York Times"), color="#BBDEFB", size=24),
              it("sign", x=2200, y=360, text="COMMERCE: 'BY THE BOOK'", at=C("by the book"), color="#C8E6C9", size=32),
              it("detective", x=[[0, 1800], [C("the case moved"), 2500]], y=860, at=C("According to the New York Times"), scale=0.8, searchAt=C("by the book"))]},
    sources=["cotton", "press"])
stage("s31_denial", "m4_denial", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Nvidia has described"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=650, y=220, text="MEGASPEED: 'MISLEADING'", at=C("calls the reporting"), color="#FFE0B2", size=32),
              it("sign", x=650, y=340, text="NOT CHARGED · NOT ON THE ENTITY LIST", at=C("It has not been charged"), color="#C8E6C9", size=28),
              it("sign", x=1450, y=460, text="NVIDIA: 'INVESTIGATED AND DEBUNKED'", at=C("debunked"), color="#BBDEFB", size=28),
              buddy(1000, 860, at=0.3, mood="cool", moods=[[C("Nvidia has described"), "happy"]], label="GPU", hop=14)]},
    sources=["reuters", "press"])
kinetic("s32_t4", "m4_transition", [("All unresolved.", 76, "So, with all", None, False),
                                    ("So what happens now?", 64, "what happens now", "gold", False)])

# ====================================================================== PART 5: what happens next
card("s33_c5", "m5_card", "What Happens Next", "Three things to watch")
stage("s34_detective", "m5_detective", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Until it reports"), "x": 1150, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="1 · THE INVESTIGATION", at=0.2, size=60, color="gold"),
              it("detective", x=[[0, 400], [3, 900], [6, 1300], [9, 800]], y=860, at=0.2, scale=0.9, searchAt=C("examine all available"), text="INDEPENDENT DIRECTORS + OUTSIDE LAWYERS"),
              it("docs", x=1500, y=860, at=0.6, text="EVIDENCE", stampAt=C("further updates"), stamp="PENDING"),
              it("letters", x=1450, y=330, text="?", at=C("question mark"), size=160, color="gold")]},
    sources=["nvidia"])
stage("s35_calendar", "m5_calendar", {
    "zones": [Z("secretroom", spinAt=0.5)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And three House"), "x": 1000, "y": 470, "zoom": 1.1, "dur": 2.0}], "drift": 1,
    "items": [it("letters", x=760, y=90, text="2 · THE CALENDAR", at=0.2, size=56, color="gold"),
              it("calendar", x=420, y=330, at=C("scheduled to report"), pages=[[0, "NOV 17", "RESULTS"], [C("And three House"), "NOV 18", "BRIEFING?"]]),
              it("sign", x=1000, y=300, text="REQUESTED, NOT CONFIRMED", at=C("not yet confirmed"), color="#FFCDD2", size=30),
              buddy(1600, 860, at=0.4, mood="worry", label="GPU", hop=10)]},
    sources=["press", "nvidia"])
stage("s36_politics", "m5_politics", {
    "zones": [Z("chipcity", signs=["NO POLITICS IN THE TUBE", "GPU PARKING ONLY", "STAY CHILL", "MORE CORES"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("He said Huang"), "x": 1150, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="3 · POLITICS", at=0.2, size=60, color="gold"),
              it("sign", x=800, y=300, text="PRESIDENT TRUMP: 'I REALLY BELIEVE HIM'", at=C("really believes him"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=430, text="HIS ACCOUNT OF THE CALL", at=C("That is his account"), color="#E1BEE7", size=28),
              it("emptychair", x=1600, y=860, at=0.3, scale=0.6)]},
    sources=["press"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("chipcity", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("But markets"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=110, text="≈ -$428BN: NOT THE CHIPS", at=0.3, size=58, color="gold"),
              it("sign", x=650, y=260, text="RISK 1 · ONE PERSON", at=C("The first is"), color="#FFE0B2", size=32),
              it("sign", x=1350, y=260, text="RISK 2 · THE RULES", at=C("The second is"), color="#BBDEFB", size=32),
              it("sign", x=1000, y=400, text="HARM PROVEN: NONE · CHARGES: NONE", at=C("Neither risk"), color="#C8E6C9", size=28),
              it("letters", x=1000, y=540, text="MARKETS PRICE STORIES, AND PEOPLE", at=C("They price stories"), size=50, color="gold"),
              buddy(500, 860, at=0.4, mood="worry", moods=[[C("Even a company"), "cool"]], label="GPU", hop=22),
              buddy(1500, 860, at=0.6, mood="worry", moods=[[C("Even a company"), "happy"]], label="GPU", color="#FF9F1C", hop=22)]},
    sources=["px", "nvidia"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_nvidiaprobe_storyboard.py; edit the generator, not this file.\n"
           "# Episode 52 storyboard (Nvidia): retro-future cartoon, one visual language per part; tones from visual_direction.yaml.\n")
