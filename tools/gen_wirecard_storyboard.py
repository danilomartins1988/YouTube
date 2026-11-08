"""Generates projects/the-2-billion-that-never-existed/deliverables/documentary/storyboard.yaml (Episode 12, Wirecard).

Bespoke CartoonStage worlds for this story (no ocean): a Bavarian city street with Alps and a tram, the stock-exchange
floor with a split-flap DAX board, a newsroom with a printing press, the regulator as a watchdog, an auditor's office
with a contract nobody signs, a bank vault that opens on nothing, a tropical business district with two banks and a
stamp that says FALSE, a night airport, a courtroom with a gavel. No real person is drawn (generic cartoon people);
names appear in text only. Legal care: "accused", "rejects all charges", "presumed innocent".
Run: python tools/gen_wirecard_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-2-billion-that-never-existed/deliverables/documentary/storyboard.yaml"

F = 860                       # floor line of every stage
TOWER = lambda x=960, **kw: it("tower", x=x, text="WIRECARD", color="purple", **kw)
CITY = lambda x0=-1600, x1=4600, **kw: {"set": "city", "x0": x0, "x1": x1, **kw}
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 1, "skin": k, "color": None, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **{k2: v for k2, v in d.items() if v is not None}))
    return out


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [CITY()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.25}, {"at": C("billions in the bank"), "x": 1100, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [TOWER(760, growAt=0.2, scale=1.1),
              it("piggy", x=1420, at=C("billions in the bank"), crackAt=C("never existed"), text="BANK", scale=0.9),
              it("coins", **{"from": [760, 300], "to": [1420, 660]}, at=C("billions in the bank"), until=C("never existed"), rate=5),
              *crowd([380, 500, 1050], "cheer", at=0.6, until=C("one day")),
              *crowd([380, 500, 1050], "worry", at=C("one day", 0.3)),
              it("burst", x=760, y=260, at=1.4)],
    "callouts": [co("Billions in the bank?", 960, 150, C("billions in the bank"), "gold", screen=True, size=46),
                 co("…probably never existed", 960, 260, C("never existed"), "risk", screen=True, size=46)]})
stage("s02_stakes", "h_stakes", {
    "zones": [CITY(night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}, {"at": C("bankrupt"), "x": 1000, "y": 520, "zoom": 1.12, "dur": 2.0}], "drift": 0,
    "shake": [{"at": C("bankrupt"), "dur": 2.0, "amp": 16}],
    "items": [TOWER(1000, scale=1.1, darkAt=C("most likely"), crumbleAt=C("bankrupt")),
              it("calendar", x=330, y=330, at=0.2, pages=[[0, "JUNE", "2020"]], scale=0.9),
              it("storm", x=[[0, 1700], [16, 1100]], y=140, at=C("most likely")),
              *crowd([1450, 1580], "worry", at=C("bankrupt", 0.6))],
    "callouts": [co("{{missing.display}} of cash: not there", 960, 160, C("most likely"), "risk", screen=True, size=44, sub="converted at the 2020 average rate (ECB)"),
                 co("Days later: bankrupt", 960, 960, C("bankrupt"), "risk", screen=True, size=44, until=C("greatest postwar", -0.4)),
                 co("“Greatest postwar accounting fraud”", 960, 960, C("greatest postwar"), "gold", screen=True, size=40, sub="Germany's finance minister (2021)")]},
    sources=["aljazeera_2020", "reuters_insolvency", "bbk_rates", "irish_2021"], sfx=[{"kind": "hit", "cue": "bankrupt", "gain": 0.35}])

# ====================================================================== PART 1: the rocket
card("s03_c1", "m1_card", "The Rocket", "From Aschheim to the DAX")
stage("s04_q1", "m1_question", {
    "zones": [CITY()], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 760, "y": 600, "zoom": 1.25}, {"at": C("star of the stock market"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 4,
    "items": [TOWER(620, at=0.2, h=[[0, 220], [{"cue": "star of the stock market"}, 220], [{"cue": "star of the stock market", "offset": 2.0}, 600]]),
              it("chart", x=1360, y=380, w=620, h=360, at=C("star of the stock market"), dur=3.5, text="SHARE PRICE", pts=[0.05, 0.08, 0.12, 0.2, 0.32, 0.5, 0.72, 0.95]),
              *crowd([980, 1100], "cheer", at=C("star of the stock market", 1.0))],
    "callouts": [co("Small firm → stock-market star?", 960, 150, C("small payments firm"), "gold", screen=True, size=42)]})
stage("s05_origin", "m1_origin", {
    "zones": [CITY(x1=2300), Z("exchange", 2300, 5000)], "worldW": 3600,
    "cam": [{"at": 0, "x": 760, "y": 560, "zoom": 1.1}, {"at": C("process card payments"), "x": 1150, "y": 560, "zoom": 1.0, "dur": 2.0},
            {"at": C("early customers"), "x": 1750, "y": 540, "zoom": 1.0, "dur": 2.2}, {"at": C("merging into"), "x": 2650, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("building", x=560, style="office", color="purple", text="WIRECARD", at=C("Wirecard was founded"), scale=0.8),
              it("sign", x=250, y=640, text="ASCHHEIM", sub="near Munich", post=True, at=C("Aschheim"), color="#C8E6C9", size=30),
              it("terminal", x=1150, y=620, at=C("process card payments", -0.5), taps=[C("process card payments", 0.4), C("process card payments", 2.4), C("tiny", 0) if False else C("high risk", 0)]),
              it("sign", x=1650, y=520, text="ONLINE GAMBLING", color="#FFCDD2", at=C("online gambling"), swing=True, hang=True),
              it("sign", x=1900, y=680, text="ADULT SITES 18+", color="#FFCDD2", at=C("adult sites"), swing=True, hang=True),
              it("building", x=2900, style="bank", color="#B0BEC5", text="LISTED COMPANY", at=C("without a classic"), scale=0.8),
              it("arrow", **{"from": [2380, 520], "to": [2700, 520]}, at=C("merging into"), color="gold", text="MERGER"),
              *crowd([2550], "point", at=C("merging into", 0.5), tie=True)],
    "callouts": [co("{{founded.display}}: founded", 960, 150, C("Wirecard was founded"), "gold", screen=True, size=44, until=C("process card payments", -0.3)),
                 co("Card payments for websites", 960, 150, C("process card payments"), "white", screen=True, until=C("early customers", -0.3)),
                 co("Early clients: high-risk websites", 960, 150, C("early customers"), "risk", screen=True, sub="'high-risk verticals' (Quartr)", until=C("merging into", -0.3)),
                 co("2005: onto the stock market by merging into a listed company", 960, 960, C("merging into"), "white", screen=True, sub="in Frankfurt")]},
    sources=["quartr"])
# ---- PRESENTER A: what a payment processor does
add("p06_processor", "m1_draw", "engine_draw", {
    "title": "What a payment processor does", "board": BOARD, "draw_start": C("You buy something"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(520, 380, 220, 100), "color": "accent2", "width": 5, "start": C("tap your card"), "label": lbl("YOU + CARD", 630, 440, 26, "accent2")},
        {"d": arrow((750, 430), (830, 430)), "color": "ink", "width": 4, "start": C("The shop sends")},
        {"d": rect(840, 380, 200, 100), "color": "accent3", "width": 5, "start": C("The shop sends", 0.3), "label": lbl("SHOP", 940, 440, 28, "accent3")},
        {"d": arrow((1050, 430), (1130, 430)), "color": "ink", "width": 4, "start": C("to a processor")},
        {"d": rect(1140, 380, 260, 100), "color": "accent", "width": 6, "start": C("to a processor", 0.3), "label": lbl("PROCESSOR", 1270, 440, 28, "accent")},
        {"d": arrow((1270, 490), (1270, 590)), "color": "ink", "width": 4, "start": C("card network")},
        {"d": rect(1110, 600, 320, 100), "color": "accent2", "width": 5, "start": C("and the banks"), "label": lbl("CARD NETWORK + BANKS", 1270, 660, 22, "accent2")},
        {"d": arrow((1100, 650), (950, 500), 0.1), "color": "accent3", "width": 5, "start": C("gets paid")},
        {"d": "M 1460 520 m -40 0 a 40 40 0 1 0 80 0 a 40 40 0 1 0 -80 0", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.4, "start": C("tiny fee"), "label": lbl("FEE", 1460, 530, 24, "ink")},
        {"d": "M 1560 900 L 1560 800 L 1620 800 L 1620 900 M 1650 900 L 1650 720 L 1710 720 L 1710 900", "color": "accent", "width": 4, "fill": "accent", "fillOpacity": 0.3, "kind": "bar",
         "start": C("Millions of tiny"), "label": lbl("× millions", 1635, 950, 24, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("tiny fee", 0.3), "dur": 1.3, "target": [1460, 520]}, {"kind": "smile", "at": C("very big business"), "dur": 1.5}],
    "scale": 0.86, "floor": 1040})
stage("s07_asia", "m1_asia", {
    "zones": [CITY(x1=1800), Z("tropic", 1800, 6000)], "worldW": 4000,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("Southeast Asia", -1.0), "x": 2700, "y": 540, "zoom": 1.0, "dur": 3.0},
            {"at": C("twenty seventeen"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [TOWER(700, h=[[0, 420], [{"cue": "twenty seventeen"}, 420], [{"cue": "twenty seventeen", "offset": 3}, 620]]),
              it("plane", x=[[0, 900], [{"cue": "far from home"}, 900], [{"cue": "far from home", "offset": 4}, 2900]], y=[[0, 380], [{"cue": "far from home", "offset": 4}, 260]], text="", scale=0.7, at=C("far from home")),
              it("building", x=2500, style="office", color="green", text="PARTNERS", at=C("Southeast Asia", 0.5), scale=0.75),
              it("building", x=3050, style="office", color="cyan", text="CUSTOMERS", at=C("Middle East"), scale=0.65),
              it("coins", **{"from": [2500, 520], "to": [800, 360]}, at=C("Middle East", 0.8), rate=5, arc=260),
              it("chart", x=1400, y=420, w=560, h=340, at=C("eight hundred percent", -1.0), dur=3, text="SHARES SINCE 2005", pts=[0.03, 0.06, 0.1, 0.18, 0.3, 0.45, 0.65, 0.9])],
    "callouts": [co("≈ {{asia.display}} of revenue", 960, 150, C("Southeast Asia"), "gold", screen=True, size=44, sub="Southeast Asia + Middle East, early 2016", until=C("twenty seventeen", -0.3)),
                 co("2017: revenue {{asia.rev_display}}", 960, 150, C("twenty seventeen"), "green", screen=True, sub="converted at the 2017 average rate"),
                 co("Shares: about +800% since 2005", 960, 960, C("eight hundred percent"), "gold", screen=True)]},
    sources=["quartr", "bbk_rates"])
stage("s08_dax", "m1_dax", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 420, "zoom": 1.1}, {"at": C("employees"), "x": 960, "y": 560, "zoom": 1.0, "dur": 2.2}], "drift": 0,
    "items": [it("board", x=960, y=60, w=1100, at=0.2, text="DAX · GERMANY'S TOP COMPANIES",
                 rows=[{"name": "· · ·", "value": ""}, {"name": "COMMERZBANK", "value": "BANK"}, {"name": "· · ·", "value": ""}],
                 swap={"at": C("pushed out"), "out": 1, "in": {"name": "WIRECARD", "value": "NEW", "color": "gold"}}),
              it("sign", x=330, y=560, text="WIRECARD STAFF", at=C("employees"), size=28, color="#E1BEE7"),
              *crowd([330], "cheer", at=C("employees", 0.2), scale=0.85),
              it("sign", x=1230, y=560, text="BANK STAFF: 10×", at=C("a tenth"), size=28, color="#BBDEFB"),
              *crowd([820, 910, 1000, 1090, 1180, 1270, 1360, 1450, 1540, 1630], "stand", at=C("a tenth", 0.2), scale=0.7, tie=True),
              it("letters", x=330, y=380, text="×2 VALUE", at=C("twice as much"), size=70, color="green")],
    "callouts": [co("{{dax.display}}: Wirecard enters the DAX", 960, 960, C("entered the DAX"), "gold", screen=True, size=40, until=C("employees", -0.3)),
                 co("Staff {{dax.staff_display}}: a tenth of the bank's", 960, 960, C("employees"), "white", screen=True, until=C("At its peak", -0.3)),
                 co("Peak value ≈ {{peak.display}}", 960, 960, C("At its peak"), "gold", screen=True, size=44, sub="Reuters")]},
    sources=["reuters_dax", "reuters_insolvency", "quartr"], sfx=[{"kind": "hit", "cue": "pushed out", "gain": 0.3}])
kinetic("s09_t1", "m1_transition", [("A German fintech champion", 58, "A German fintech", None, True), ("Where does the money come from?", 72, "where does all", "accent", False)])
# ====================================================================== PART 2: the warnings
card("s10_c2", "m2_card", "The Warnings", "The critics, and who went after them")
stage("s11_q2", "m2_question", {
    "zones": [Z("newsroom")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 600, "zoom": 1.2}, {"at": C("nobody listen"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("desk", x=560, glow="green", pile=True), it("desk", x=1360, glow="cyan"),
              *crowd([490], "type", glasses=True, scale=0.95), *crowd([1290], "read", scale=0.95),
              it("magnifier", x=[[0, 300], [8, 1600]], y=380, at=0.4, text="?", scale=0.9)],
    "callouts": [co("Who saw it first?", 960, 150, C("Who saw"), "gold", screen=True, size=46),
                 co("Why did nobody listen?", 960, 260, C("nobody listen"), "risk", screen=True)]})
stage("s12_ft", "m2_ft", {
    "zones": [Z("newsroom")], "worldW": 2600,
    "cam": [{"at": 0, "x": 760, "y": 560, "zoom": 1.05}, {"at": C("January twenty nineteen"), "x": 1700, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("desk", x=560, glow="green", pile=True), *crowd([490], "type", glasses=True, hair=3),
              it("paper", x=1000, y=420, at=C("began asking", 0.4), text="WHERE DOES THE", sub="money come from? Questions about the accounts", size=40, scale=0.85, until=C("January twenty nineteen")),
              it("press", x=1550, at=C("went further", -0.5), runAt=C("went further"), text="PRINTING"),
              *crowd([2250], "phone", at=C("whistleblower"), hair=4),
              it("sign", x=2250, y=420, text="WHISTLEBLOWER", sub="ex-head of legal, Asia", at=C("whistleblower", 0.3), size=28, color="#FFF59D"),
              it("paper", x=1750, y=360, at=C("suspicions"), text="SUSPICIONS", sub="about the business in Singapore", size=46, scale=0.8, tilt=3)],
    "callouts": [co("{{ft_2015.display}}: questions about the accounts", 960, 960, C("began asking"), "white", screen=True, sub="Financial Times journalist Dan McCrum", until=C("January twenty nineteen", -0.3)),
                 co("Jan 2019: a whistleblower", 960, 960, C("whistleblower"), "gold", screen=True, sub="former head of legal for Wirecard in Asia (Quartr)")]},
    sources=["quartr"])
stage("s13_bafin", "m2_bafin", {
    "zones": [CITY(label="nochurch")], "worldW": 2400,
    "cam": [{"at": 0, "x": 700, "y": 540, "zoom": 1.05}, {"at": C("banned investors"), "x": 1200, "y": 540, "zoom": 0.92, "dur": 2.4},
            {"at": C("prosecutors"), "x": 1500, "y": 560, "zoom": 1.05, "dur": 2.4}], "drift": 0,
    "items": [TOWER(250, scale=0.9), it("building", x=720, style="gov", color="#FFE082", text="REGULATOR", scale=0.75),
              it("dog", x=980, at=0.4, barks=[C("did not turn on", 0.4), C("banned investors", 0.3), C("prosecutors", 0.3)], scale=0.9),
              it("building", x=1850, style="news", color="#BBDEFB", text="NEWSPAPER", scale=0.8),
              *crowd([1450, 1560], "worry", at=C("betting against"), tie=True),
              it("sign", x=1500, y=470, text="NO BETTING AGAINST THESE SHARES", color="#FFCDD2", at=C("banned investors"), size=28, hang=True, swing=True),
              *crowd([2000], "read", at=C("Financial Times journalist", -0.5), glasses=True, hair=3),
              it("magnifier", x=[[0, 1700], [{"cue": "Financial Times journalist"}, 1700], [{"cue": "Financial Times journalist", "offset": 3}, 2000]], y=520,
                 at=C("Financial Times journalist", -0.2), scale=0.8, until=C("baseless")),
              it("paper", x=1450, y=420, at=C("baseless"), text="“BASELESS AND FALSE”", sub="the newspaper's reply", size=40, scale=0.8)],
    "callouts": [co("Betting against the shares: banned", 960, 150, C("banned investors"), "risk", screen=True, size=40, sub="{{short_ban.display}}: a first for a single stock", until=C("prosecutors", -0.3)),
                 co("Prosecutors investigate an FT journalist", 960, 150, C("prosecutors"), "risk", screen=True, sub="after a criminal complaint")]},
    sources=["reuters_short", "irish_2021"])
# ---- PRESENTER B: who the watchdog pointed at
add("p14_finger", "m2_draw", "engine_draw", {
    "title": "The watchdog pointed the wrong way", "board": BOARD, "draw_start": C("On one side"), "speed": 1300, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(520, 380, 300, 120), "color": "accent2", "width": 5, "start": C("On one side"), "label": lbl("CRITICS", 670, 450, 30, "accent2")},
        {"d": dot(670, 540), "color": "muted", "width": 1, "start": C("look at these"), "label": lbl("“look at these numbers”", 670, 540, 24, "muted")},
        {"d": rect(1180, 380, 300, 120), "color": "risk", "width": 5, "start": C("On the other"), "label": lbl("COMPANY", 1330, 450, 30, "risk")},
        {"d": dot(1330, 540), "color": "muted", "width": 1, "start": C("being attacked"), "label": lbl("“we are being attacked”", 1330, 540, 24, "muted")},
        {"d": rect(850, 680, 300, 120), "color": "accent", "width": 6, "start": C("in the middle"), "label": lbl("WATCHDOG", 1000, 750, 30, "accent")},
        {"d": arrow((900, 680), (700, 510), -0.1), "color": "risk", "width": 7, "start": C("pointed its finger")},
        {"d": "M 1180 900 L 1180 830 L 1240 830 L 1240 900", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("at the critics")},
    ],
    "actions": [{"kind": "point", "at": C("pointed its finger", 0.3), "dur": 1.4, "target": [700, 510]}, {"kind": "react", "at": C("at the critics", 0.5)}],
    "scale": 0.86, "floor": 1040}, sources=["reuters_short", "irish_2021"])
kinetic("s15_t2", "m2_transition", [("So the critics were wrong?", 60, "So the critics", None, True), ("Someone had to find the money", 72, "find the money", "accent", False)])
# ====================================================================== PART 3: the money that wasn't there
card("s16_c3", "m3_card", "The Money That Wasn't There", "Trust accounts, partners and a trustee")
stage("s17_q3", "m3_question", {
    "zones": [Z("vault")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.25}, {"at": C("see it"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("vaultdoor", x=960, r=270, label="TRUST ACCOUNT"),
              it("magnifier", x=[[0, 500], [5, 1400], [10, 600]], y=[[0, 400], [5, 600], [10, 380]], at=0.6, scale=0.8),
              *crowd([1500], "shrug", at=C("see it"), glasses=True),
              it("letters", x=1500, y=360, text="?", at=C("see it", 0.3), size=130, color="grey")],
    "callouts": [co("Where was the money?", 960, 140, C("Where was"), "gold", screen=True, size=46)]})
# ---- PRESENTER C: third-party partners and trust accounts
add("p18_tpa", "m3_tpa", "engine_draw", {
    "title": "Where the money was supposed to be", "board": BOARD, "draw_start": C("third-party partners"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": C("An important part", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 560 360 Q 640 320 720 360 Q 760 430 700 480 Q 620 500 580 450 Z", "color": "border", "width": 4, "kind": "map", "start": C("Asia and"), "label": lbl("ASIA · MIDDLE EAST", 650, 530, 22, "muted")},
        {"d": rect(830, 360, 260, 110), "color": "accent2", "width": 5, "start": C("third-party partners"), "label": lbl("PARTNERS", 960, 425, 28, "accent2")},
        {"d": arrow((1100, 415), (1210, 415)), "color": "ink", "width": 4, "start": C("booked the revenue", -0.4)},
        {"d": rect(1220, 360, 280, 110), "color": "accent", "width": 5, "start": C("booked the revenue"), "label": lbl("WIRECARD BOOKS IT", 1360, 425, 24, "accent")},
        {"d": arrow((1360, 480), (1360, 600)), "color": "ink", "width": 4, "start": C("trust accounts", -0.4)},
        {"d": rect(1180, 610, 360, 130), "color": "risk", "width": 6, "dash": "14 10", "start": C("trust accounts"), "label": lbl("TRUST ACCOUNT  ?", 1360, 685, 28, "risk")},
        {"d": dot(1360, 780), "color": "muted", "width": 1, "start": C("held for it"), "label": lbl("held by a trustee", 1360, 790, 24, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("held for it", 0.4), "dur": 1.4, "target": [1360, 680]}],
    "scale": 0.86, "floor": 1040}, sources=["wirecard_kpmg", "irish_2020", "aljazeera_2020"])
stage("s19_kpmg", "m3_kpmg", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 560, "zoom": 1.05}, {"at": C("for its part"), "x": 1400, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("calendar", x=340, y=330, at=0.2, pages=[[0, "APR", "2020"]], color="blue", scale=0.8),
              *crowd([700, 830], "read", at=C("special investigation"), glasses=True, color="#90CAF9"),
              it("docs", x=1150, y=F, at=C("special investigation", 0.5), text="PARTNER DATA", stampAt=C("could be obtained"), stamp="INCOMPLETE", color="orange"),
              it("magnifier", x=[[0, 1000], [6, 1250]], y=480, at=C("not all the data"), scale=0.7, until=C("for its part")),
              TOWER(1900, scale=0.8),
              it("sign", x=1900, y=330, text="“NO INCRIMINATING EVIDENCE”", at=C("for its part"), color="#FFF59D", size=28)],
    "callouts": [co("April 2020: special investigation by KPMG", 960, 150, C("special investigation"), "white", screen=True, until=C("not all the data", -0.3)),
                 co("Not all the data could be obtained", 960, 150, C("not all the data"), "risk", screen=True, sub="it was with the partners (Wirecard's own statement)", until=C("for its part", -0.3)),
                 co("Wirecard: no evidence of balance sheet forgery", 960, 150, C("for its part"), "gold", screen=True)]},
    sources=["wirecard_kpmg"])
stage("s20_ey", "m3_ey", {
    "zones": [Z("office")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("That day"), "x": 1750, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("calendar", x=330, y=330, at=0.2, pages=[[0, "18", "JUNE 2020"]], scale=0.8),
              it("contract", x=880, y=480, at=0.3, refuseAt=C("refused to sign"), text="ANNUAL ACCOUNTS", sub="Auditor signature", scale=0.85),
              *crowd([1260], "shrug", at=C("refused to sign"), glasses=True, tie=True, color="#90CAF9"),
              it("sign", x=1260, y=420, text="CASH: NOT CONFIRMED", at=C("could not be confirmed"), color="#FFCDD2", size=26),
              it("chart", x=1850, y=420, w=640, h=380, at=0.5, dur=4, text="WIRECARD SHARES", pts=[0.5, 0.6, 0.55, 0.7, 0.72, 0.8], crashAt=C("shares fell"))],
    "callouts": [co("June 18, 2020: the auditor, EY, refuses to sign", 960, 150, C("refused to sign"), "risk", screen=True, size=38, until=C("could not be confirmed", -0.3)),
                 co("{{missing.display}} of cash unconfirmed", 960, 150, C("could not be confirmed"), "risk", screen=True, size=40, until=C("shares fell", -0.3)),
                 co("“A trustee tried to deceive the auditor”", 960, 960, C("indications"), "white", screen=True, sub="indications, according to the company", until=C("shares fell", -0.3)),
                 co("Shares {{missing.drop_display}} in one day", 960, 960, C("shares fell"), "risk", screen=True, size=44)]},
    sources=["irish_2020", "bbk_rates"], sfx=[{"kind": "hit", "cue": "refused to sign", "gain": 0.35}])
stage("s21_banks", "m3_banks", {
    "zones": [Z("tropic")], "worldW": 3200,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}, {"at": C("central bank"), "x": 2100, "y": 540, "zoom": 1.0, "dur": 2.4},
            {"at": C("Four days later"), "x": 2400, "y": 560, "zoom": 1.05, "dur": 2.2}], "drift": 0,
    "items": [it("sign", x=260, y=560, text="THE PHILIPPINES", post=True, color="#FFF59D", size=30),
              it("building", x=620, style="bank", color="#FFB74D", text="BANK 1", scale=0.7, at=0.3),
              it("building", x=1300, style="bank", color="#81C784", text="BANK 2", scale=0.7, at=0.6),
              it("docs", x=960, y=F, at=C("two banks"), text="BANK CONFIRMATION", stampAt=C("documents were false"), stamp="FALSE"),
              *crowd([520, 1400], "shrug", at=C("not even a client"), tie=True),
              it("sign", x=960, y=300, text="“NOT A CLIENT”", at=C("not even a client"), color="#FFCDD2", size=36),
              it("building", x=2000, style="gov", color="#CE93D8", text="CENTRAL BANK", scale=0.7, at=C("central bank", -0.5)),
              it("coins", **{"from": [1500, 300], "to": [2000, 560]}, at=C("central bank"), until=C("entered the country"), rate=3, ghost=True),
              it("letters", x=1780, y=360, text="✗", at=C("entered the country"), size=120, color="risk"),
              it("piggy", x=2600, at=C("Four days later", -0.6), crackAt=C("most likely did not exist"), text="TRUST", scale=0.9)],
    "callouts": [co("Documents: false", 960, 150, C("documents were false"), "risk", screen=True, until=C("central bank", -0.3)),
                 co("Central bank: the money never came in", 960, 150, C("central bank"), "white", screen=True, until=C("Four days later", -0.3)),
                 co("Most likely did not exist", 960, 150, C("most likely did not exist"), "risk", screen=True, size=46),
                 co("≈ a quarter of everything it said it owned", 960, 960, C("of everything"), "gold", screen=True)]},
    sources=["aljazeera_2020"], sfx=[{"kind": "hit", "cue": "documents were false", "gain": 0.3}])
kinetic("s22_t3", "m3_transition", [("Built, at least in part,", 52, "A company worth", None, True), ("on cash that wasn't there", 74, "wasn't there", "risk", False),
                                    ("What happened next took one week", 40, "one week", "muted", True)])
# ====================================================================== PART 4: the collapse
card("s23_c4", "m4_card", "The Collapse", "One week")
stage("s24_q4", "m4_question", {
    "zones": [CITY(night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 420, "zoom": 1.25}, {"at": 3.5, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "shake": [{"at": 1.0, "dur": 1.0, "amp": 6}, {"at": 4.5, "dur": 1.0, "amp": 8}],
    "items": [TOWER(960, scale=1.1), it("storm", x=[[0, 1600], [10, 1000]], y=130, at=0.3),
              it("letters", x=1450, y=380, text="?", at=C("How fast", 0.6), size=140, color="gold")],
    "callouts": [co("How fast can a star fall?", 960, 960, C("How fast"), "risk", screen=True, size=46)]})
stage("s25_week", "m4_week", {
    "zones": [Z("office", -1600, 1500), CITY(1500, 6000, night=True)], "worldW": 3600, "night": True,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.05}, {"at": C("filed for insolvency", -1.0), "x": 2500, "y": 540, "zoom": 1.0, "dur": 2.6},
            {"at": C("Two years earlier"), "x": 2500, "y": 500, "zoom": 1.15, "dur": 3}], "drift": 0,
    "shake": [{"at": C("filed for insolvency", 0.4), "dur": 2.0, "amp": 16}],
    "items": [it("calendar", x=[[0, 330], [{"cue": "filed for insolvency", "offset": -1.0}, 330], [{"cue": "filed for insolvency", "offset": 1.6}, 1880]], y=330, at=0.2,
                 pages=[[0, "19", "JUNE 2020"], [C("June twenty"), "25", "JUNE 2020"]] if False else [[0, "19", "JUNE 2020"], [C("filed for insolvency"), "25", "JUNE 2020"]], scale=0.8),
              it("chair", x=900, at=0.2, spinAt=C("resigned"), text="CEO"),
              TOWER(2500, scale=1.1, darkAt=C("filed for insolvency"), crumbleAt=C("filed for insolvency", 0.4)),
              *crowd([2950, 3080, 3210], "worry", at=C("creditors owed"), tie=True),
              it("sign", x=3080, y=560, text="CREDITORS", at=C("creditors owed", 0.2), color="#FFF59D", size=28)],
    "callouts": [co("June 19: the CEO resigns", 960, 150, C("resigned"), "white", screen=True, until=C("filed for insolvency", -0.3)),
                 co("June 25: insolvency", 960, 150, C("filed for insolvency"), "risk", screen=True, size=44, until=C("first company in the DAX", -0.3)),
                 co("First DAX company ever to go out of business", 960, 150, C("first company in the DAX"), "risk", screen=True, until=C("creditors owed", -0.3)),
                 co("Creditors owed {{insolvency.display}}", 960, 150, C("creditors owed"), "gold", screen=True, size=44, sub="Reuters", until=C("Two years earlier", -0.3)),
                 co("Once worth ≈ {{peak.display}}. Gone.", 960, 960, C("once valued"), "risk", screen=True, size=42)]},
    sources=["aljazeera_2020", "reuters_insolvency"], sfx=[{"kind": "hit", "cue": "filed for insolvency", "gain": 0.35}])
stage("s26_marsalek", "m4_marsalek", {
    "zones": [Z("airport", -1600, 2300, night=True), Z("court", 2300, 6000, cx=3250)], "worldW": 4200, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("a court in London", -0.6), "x": 3250, "y": 540, "zoom": 1.0, "dur": 2.8}], "drift": 0,
    "items": [it("plane", x=[[0, 700], [{"cue": "vanished"}, 700], [{"cue": "vanished", "offset": 7}, 2600]], y=[[0, 760], [{"cue": "vanished", "offset": 2}, 700], [{"cue": "vanished", "offset": 7}, 200]],
                 tilt=-14, text="?", scale=0.75),
              it("sign", x=1500, y=470, text="WANTED", sub="by German authorities · not tried", at=C("is wanted"), color="#FFE082", size=48, post=True),
              it("letters", x=1500, y=280, text="?", at=C("whereabouts"), size=120, color="white"),
              it("gavel", x=3250, y=F - 414, hits=[C("convicted"), C("convicted", 0.9)], scale=1.0),
              *crowd([2750, 2860, 2970], "stand", at=C("spy ring"), color="#B0BEC5", scale=0.75)],
    "callouts": [co("The COO: wanted in Germany", 960, 150, C("is wanted"), "risk", screen=True, size=40, sub="Jan Marsalek (not tried)", until=C("believed to be", -0.3)),
                 co("Believed to be in Russia", 960, 150, C("believed to be"), "white", screen=True, sub="whereabouts unknown (Reuters)", until=C("a court in London", -0.3)),
                 co("London 2025: Russian spy ring convicted", 960, 150, C("a court in London"), "gold", screen=True, until=C("Between", -0.3)),
                 co("Its leader reported to Marsalek", 960, 960, C("reported to"), "white", screen=True, sub="according to British prosecutors (CPS)"),
                 co("2020–2023: information gathered for the Russian state", 960, 150, C("Between"), "white", screen=True, sub="prosecutors said")]},
    sources=["reuters_spies", "cps_spies"])
stage("s27_trial", "m4_trial", {
    "zones": [Z("court", cx=960)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.15}, {"at": C("If convicted"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("gavel", x=960, y=F - 414, hits=[C("went on trial", 0.3), C("presumed innocent", 0.4)], scale=1.0),
              it("calendar", x=330, y=330, at=0.3, pages=[[0, "2022", "TRIAL OPENS"], [C("gone on for years"), "2026", "STILL GOING"]], scale=0.8, color="navy"),
              it("sign", x=1330, y=330, text="CHARGES", sub="commercial gang fraud · false accounting · breach of trust", at=C("accused of"), color="#FFF59D", size=34),
              it("sign", x=960, y=200, text="PRESUMED INNOCENT", sub="until a verdict", at=C("presumed innocent"), color="#C8E6C9", size=40)],
    "callouts": [co("Munich: trial since {{trial.display}}", 960, 960, C("went on trial"), "white", screen=True, size=40, until=C("If convicted", -0.3)),
                 co("If convicted: up to 15 years in prison", 960, 960, C("If convicted"), "risk", screen=True, until=C("rejects all", -0.3)),
                 co("Markus Braun: “I reject all the charges”", 960, 960, C("rejects all"), "gold", screen=True, sub="he has blamed Marsalek", until=C("presumed innocent", -0.3))]},
    sources=["lto_2025", "enca_2023", "bavaria_2026"])
kinetic("s28_t4", "m4_transition", [("A fraud this size needs people looking away", 48, "But a fraud", None, True), ("So who failed?", 88, "who failed", "risk", False)])
# ====================================================================== PART 5: who failed
card("s29_c5", "m5_card", "Who Failed", "The checks that came too late")
stage("s30_q5", "m5_question", {
    "zones": [CITY(label="nochurch")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 600, "zoom": 1.2}, {"at": C("who was supposed"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [*crowd([480], "read", at=C("Auditors"), glasses=True, color="#90CAF9"),
              it("sign", x=480, y=470, text="AUDITOR", at=C("Auditors", 0.2), size=28),
              it("dog", x=880, at=C("regulators"), barks=[C("regulators", 0.5)], scale=0.75),
              it("sign", x=960, y=470, text="REGULATOR", at=C("regulators", 0.2), size=28),
              *crowd([1440], "phone", at=C("investors"), tie=True),
              it("sign", x=1440, y=470, text="INVESTORS", at=C("investors", 0.2), size=28),
              it("piggy", x=[[0, 2300], [{"cue": "who was supposed"}, 2300], [{"cue": "who was supposed", "offset": 5}, -400]], y=F - 10, at=0.2, text="?", scale=0.5)],
    "callouts": [co("Who was supposed to catch it?", 960, 150, C("who was supposed"), "gold", screen=True, size=44)]})
stage("s31_auditor", "m5_auditor", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 860, "y": 540, "zoom": 1.05}, {"at": C("banned it"), "x": 1250, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("docs", x=700, y=F, at=0.2, text="WIRECARD ACCOUNTS", stampAt=C("without objections"), stamp="APPROVED", color="green"),
              *crowd([1050], "stand", at=0.3, glasses=True, tie=True, color="#90CAF9"),
              it("letters", x=700, y=180, text="10+ YEARS", at=C("for", 0) if False else C("without objections", 0.8), size=70, color="green"),
              it("sign", x=1450, y=380, text="BANNED", sub="no new listed audit clients in Germany", at=C("banned it"), color="#FFCDD2", size=56),
              it("coins", **{"from": [1050, 640], "to": [2300, 400]}, at=C("fined the firm"), rate=5)],
    "callouts": [co("Clean audits for more than a decade", 960, 150, C("without objections"), "white", screen=True, sub="EY (Financial Times)", until=C("banned it", -0.3)),
                 co("2023: {{ey_ban.display}} in Germany", 960, 150, C("banned it"), "risk", screen=True, sub="as reported by the FT", until=C("fined the firm", -0.3)),
                 co("Fines: the firm + current and former staff", 960, 150, C("fined the firm"), "gold", screen=True)]},
    sources=["irish_2023"])
stage("s32_regulator", "m5_regulator", {
    "zones": [CITY(label="nochurch")], "worldW": 2400,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.05}, {"at": C("overlooked"), "x": 1100, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("building", x=600, style="gov", color="#FFE082", text="REGULATOR", scale=0.8),
              it("person", x=[[0, 760], [{"cue": "left his post"}, 760], [{"cue": "left his post", "offset": 6}, 2300]], pose="walk", at=0.3, scale=0.85, tie=True, hair=2),
              it("person", x=[[0, 640], [{"cue": "left too"}, 640], [{"cue": "left too", "offset": 5}, 2300]], pose="walk", at=0.3, scale=0.8, tie=True, hair=4, color="#B39DDB"),
              it("dog", x=330, at=0.2, scale=0.7, barks=[C("fresh start", 0.3)], text="?!"),
              it("sign", x=1500, y=420, text="FRESH START", at=C("fresh start"), color="#C8E6C9", size=40, hang=True, swing=True)],
    "callouts": [co("{{hufeld.display}}: the regulator's chief leaves", 960, 150, C("left his post"), "white", screen=True, size=40, until=C("overlooked", -0.3)),
                 co("“…overlooked Germany's greatest postwar accounting fraud”", 960, 960, C("overlooked"), "risk", screen=True, sub="finance minister Olaf Scholz"),
                 co("His deputy for securities supervision left too", 960, 150, C("left too"), "white", screen=True)]},
    sources=["irish_2021"])
# ---- PRESENTER D: the safety net
add("p33_net", "m5_draw", "engine_draw", {
    "title": "The safety net", "board": BOARD, "draw_start": C("The company reports"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1640, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(560, 330, 700, 90), "color": "ink", "width": 4, "start": C("The company reports"), "label": lbl("1 · COMPANY REPORTS", 910, 388, 26)},
        {"d": rect(560, 450, 700, 90), "color": "accent2", "width": 4, "start": C("The auditor checks"), "label": lbl("2 · AUDITOR CHECKS", 910, 508, 26, "accent2")},
        {"d": rect(560, 570, 700, 90), "color": "accent2", "width": 4, "start": C("The regulator watches"), "label": lbl("3 · REGULATOR WATCHES", 910, 628, 26, "accent2")},
        {"d": rect(560, 690, 700, 90), "color": "accent3", "width": 6, "start": C("ask hard questions"), "label": lbl("4 · JOURNALISTS + INVESTORS ASK", 910, 748, 24, "accent3")},
        {"d": "M 1290 495 L 1340 495 M 1290 615 L 1340 615", "color": "risk", "width": 8, "start": C("came too late")},
        {"d": dot(1420, 505), "color": "risk", "width": 1, "start": C("came too late", 0.3), "label": lbl("too late", 1420, 512, 26, "risk")},
        {"d": "M 1300 790 L 1300 720 L 1360 720 L 1360 790", "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("the one that worked"),
         "label": lbl("worked", 1450, 760, 26, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("the one that worked", 0.3), "dur": 1.3, "target": [910, 735]}],
    "scale": 0.86, "floor": 1040}, sources=["irish_2023", "irish_2021", "quartr"])
kinetic("s34_lesson", "m5_lesson", [("A national champion · a tech success · a rising share price", 40, "a national champion", None, True),
                                    ("people want to believe", 76, "want to believe", "accent", False),
                                    ("the critics were treated as the problem", 40, "treated as the problem", "risk", True)])
# ====================================================================== PAYOFF
stage("s35_payoff", "payoff", {
    "zones": [Z("vault")], "worldW": 2200,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}, {"at": C("asked to see"), "x": 1150, "y": 520, "zoom": 1.08, "dur": 2.4}], "drift": 0,
    "items": [it("vaultdoor", x=1150, r=270, label="TRUST ACCOUNT", openAt=C("when they"), text="NOTHING THERE"),
              it("docs", x=420, y=F, at=C("lived in documents"), text="BALANCE: BILLIONS", scale=0.8),
              it("person", x=[[0, -200], [{"cue": "asked to see"}, -200], [{"cue": "asked to see", "offset": 3}, 700]], pose="walk", at=0.2, glasses=True, color="#90CAF9", scale=0.9),
              it("letters", x=1150, y=180, text="?", at=C("can I"), size=130, color="gold")],
    "callouts": [co("Not stolen from a vault: never in one", 960, 150, C("never in one"), "white", screen=True, size=40, until=C("when they", -0.3)),
                 co("…and there was nothing there", 960, 150, C("nothing there"), "risk", screen=True, size=44, until=C("can I", -0.4)),
                 co("“Can I see the money?”", 960, 960, C("can I"), "gold", screen=True, size=52)]},
    sources=["aljazeera_2020"])
add("s36_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_wirecard_storyboard.py; edit the generator, not this file.\n"
           "# Episode 12 storyboard: bespoke CartoonStage worlds. The channel intro is inserted automatically after the hook.\n")
