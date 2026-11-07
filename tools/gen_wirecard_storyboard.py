"""Generates projects/the-2-billion-that-never-existed/deliverables/documentary/storyboard.yaml (Episode 12, Wirecard).

Cartoon-first with tools/cartoon_kit.py: a company tower on the German coast, an island with two banks where the
money was "supposed" to be, a piggy-bank trust account, coin streams that stop, a storm, a plane flying away with a
question mark. No real person is drawn; names appear in text only. Legal care: "accused", "rejects all charges".
Run: python tools/gen_wirecard_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-2-billion-that-never-existed/deliverables/documentary/storyboard.yaml"


def tower(x=200, text="WIRECARD", **kw):
    return office(x, text, "purple", **kw)


def bank(x, text="BANK", y=None, **kw):
    o = office(x, text, "gold", **kw)
    if y is not None:
        o["y"] = y
    return o


def piggy(x, y=230, at=0.0, scale=0.8):
    return {"kind": "piggy", "x": x, "y": y, "at": at, "scale": scale}


GER = {"plain": True, "left": True, "leftLabel": "GERMANY"}
PH = lambda x=2000, **kw: island(x=x, text="PHILIPPINES", **kw)

# ====================================================================== HOOK
cart("s01_hook", "h_question", {
    "worldW": 2800, "coasts": GER,
    "cam": [{"at": 0, "x": 700, "y": 400, "zoom": 1.1}, {"at": C("admitted"), "x": 1300, "y": 400, "zoom": 0.85, "dur": 2.6}], "drift": 0,
    "actors": [tower(200), PH(), piggy(2050, at=0.3), coins(2700, -100, [2050, 200], 0.3, rate=6, until=C("admitted"))],
    "callouts": [co("Billions in the bank?", 1300, 160, C("billions in the bank"), "gold", size=44),
                 co("…probably never existed", 1300, 270, C("never existed"), "risk", size=44)]})
cart("s02_stakes", "h_stakes", {
    "worldW": 2800, "night": True, "coasts": {**GER, "darkAt": C("bankrupt")},
    "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 0.9}], "drift": 8,
    "actors": [tower(200), PH(), piggy(2050, at=0.0), {"kind": "storm", "x": [[0, 1200], [20, 400]], "y": 130, "at": C("most likely")}],
    "callouts": [co("June 2020", 960, 140, C("June twenty twenty"), "white", screen=True, size=40),
                 co("{{missing.display}} of cash: not there", 960, 240, C("most likely"), "risk", screen=True, size=44, sub="converted at the 2020 average rate (ECB)"),
                 co("Days later: bankrupt", 960, 960, C("bankrupt"), "risk", screen=True, size=44)]},
    sources=["aljazeera_2020", "reuters_insolvency", "bbk_rates"], sfx=[{"kind": "hit", "cue": "bankrupt", "gain": 0.35}])

# ====================================================================== PART 1: the rocket
card("s03_c1", "m1_card", "The Rocket", "From Aschheim to the DAX")
cart("s04_q1", "m1_question", {
    "worldW": 2400, "min_seconds": 9.0, "coasts": GER,
    "cam": [{"at": 0, "x": 600, "y": 380, "zoom": 1.2}], "drift": 10,
    "actors": [tower(180, "SMALL FIRM", scale=0.6), tower(330, "STOCK STAR", at=C("star of the stock market"), scale=1.1), coins(2300, -80, [300, 160], C("star of the stock market"), rate=5)],
    "callouts": [co("Small firm → stock-market star?", 1000, 160, C("small payments firm"), "gold", size=42)]})
cart("s05_origin", "m1_origin", {
    "worldW": 2800, "coasts": {"plain": True, "left": True, "leftLabel": "ASCHHEIM, NEAR MUNICH"},
    "cam": [{"at": 0, "x": 700, "y": 400, "zoom": 1.1}, {"at": C("early customers"), "x": 1300, "y": 400, "zoom": 0.85, "dur": 2.4}], "drift": 0,
    "actors": [tower(200, at=C("Wirecard was founded")), island(x=2100, text="HIGH-RISK WEBSITES"), office(2050, "ONLINE GAMES", "green", scale=0.6) | {"y": 314},
               coins(2100, 200, [250, 160], C("process card payments"), rate=4)],
    "callouts": [co("{{founded.display}}: founded", 700, 150, C("Wirecard was founded"), "gold", size=44),
                 co("Card payments for websites", 1300, 170, C("process card payments"), "white"),
                 co("Early clients: gambling, adult sites", 1300, 280, C("early customers"), "risk", sub="'high-risk verticals' (Quartr)"),
                 co("2005: onto the stock market by merging into a listed company", 960, 960, C("merging into"), "white", screen=True)]},
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
cart("s07_asia", "m1_asia", {
    "worldW": 3000, "coasts": GER,
    "cam": [{"at": 0, "x": 900, "y": 400, "zoom": 0.9}, {"at": C("Southeast Asia"), "x": 2000, "y": 400, "zoom": 0.85, "dur": 2.6}], "drift": 0,
    "actors": [tower(200), island(x=2300, text="SOUTHEAST ASIA"), office(2250, "PARTNER", "green", scale=0.6) | {"y": 314},
               coins(2300, 200, [250, 160], C("far from home"), rate=6)],
    "callouts": [co("≈ {{asia.display}} of revenue", 2000, 160, C("Southeast Asia"), "gold", size=44, sub="Southeast Asia + Middle East, early 2016"),
                 co("2017: revenue {{asia.rev_display}}", 960, 960, C("twenty seventeen"), "green", screen=True, sub="converted at the 2017 average rate")]},
    sources=["quartr", "bbk_rates"])
cart("s08_dax", "m1_dax", {
    "worldW": 2400, "coasts": {"plain": True, "left": True, "right": True, "leftLabel": "WIRECARD", "rightLabel": "COMMERZBANK"},
    "cam": [{"at": 0, "x": 1200, "y": 380, "zoom": 0.85}], "drift": 0,
    "actors": [tower(200, scale=0.8), office(2200, "COMMERZBANK", "blue", scale=1.3),
               {"kind": "letters", "text": "DAX", "y": 130, "at": 0.3, "size": 110, "color": "blue",
                "x": [[0, 2150], [{"cue": "pushed out"}, 2150], [{"cue": "pushed out", "offset": 2.0}, 260]]}],
    "callouts": [co("{{dax.display}}: Wirecard enters the DAX", 1200, 170, C("entered the DAX"), "gold", size=40),
                 co("Staff {{dax.staff_display}}: a tenth of the bank's", 1200, 280, C("employees"), "white"),
                 co("…but worth twice as much", 1200, 380, C("twice as much"), "green"),
                 co("Peak value ≈ {{peak.display}}", 960, 960, C("At its peak"), "gold", screen=True, size=44, sub="Reuters")]},
    sources=["reuters_dax", "reuters_insolvency", "quartr"], sfx=[{"kind": "hit", "cue": "pushed out", "gain": 0.3}])
kinetic("s09_t1", "m1_transition", [("A German fintech champion", 58, "A German fintech", None, True), ("Where does the money come from?", 72, "where does all", "accent", False)])

# ====================================================================== PART 2: the warnings
card("s10_c2", "m2_card", "The Warnings", "The critics, and who went after them")
cart("s11_q2", "m2_question", {
    "worldW": 2600, "min_seconds": 9.0, "coasts": {"plain": True, "left": True, "right": True, "leftLabel": "COMPANY", "rightLabel": "CRITICS"},
    "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 0.8}], "drift": 0,
    "actors": [tower(200), office(2400, "NEWSPAPER", "blue")],
    "callouts": [co("Who saw it first?", 1300, 160, C("Who saw"), "gold", size=46), co("Why did nobody listen?", 1300, 270, C("nobody listen"), "risk")]})
cart("s12_ft", "m2_ft", {
    "worldW": 2600, "coasts": {"plain": True, "left": True, "right": True, "leftLabel": "WIRECARD", "rightLabel": "FINANCIAL TIMES"},
    "cam": [{"at": 0, "x": 1700, "y": 400, "zoom": 1.0}, {"at": C("January twenty nineteen"), "x": 1300, "y": 400, "zoom": 0.8, "dur": 2.4}], "drift": 0,
    "actors": [tower(200), office(2400, "NEWSPAPER", "blue"), island(x=1300, text="SINGAPORE"),
               {"kind": "letters", "text": "?", "x": 2380, "y": 120, "at": C("began asking"), "size": 120, "color": "blue"}],
    "callouts": [co("{{ft_2015.display}}: questions about the accounts", 1800, 170, C("began asking"), "white", sub="FT journalist Dan McCrum"),
                 co("Jan 2019: a whistleblower in Singapore", 1300, 200, C("whistleblower"), "gold", sub="former head of legal, Wirecard Asia (Quartr)")]},
    sources=["quartr"])
cart("s13_bafin", "m2_bafin", {
    "worldW": 2600, "coasts": {"plain": True, "left": True, "right": True, "leftLabel": "REGULATOR", "rightLabel": "FINANCIAL TIMES"},
    "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 0.8}], "drift": 0,
    "actors": [office(200, "REGULATOR", "gold"), office(2400, "NEWSPAPER", "blue"),
               {"kind": "letters", "text": "→", "x": [[0, 700], [{"cue": "prosecutors"}, 700], [{"cue": "prosecutors", "offset": 2.0}, 2000]], "y": 200, "at": C("prosecutors"), "size": 140, "color": "grey"}],
    "callouts": [co("Betting against the shares: banned", 960, 150, C("banned investors"), "risk", screen=True, size=40, sub="{{short_ban.display}}, for two months: a first for a single stock"),
                 co("Prosecutors investigate an FT journalist", 960, 260, C("prosecutors"), "risk", screen=True, sub="after a criminal complaint"),
                 co("FT: “baseless and false”", 1900, 380, C("baseless"), "white")]},
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
cart("s17_q3", "m3_question", {
    "worldW": 2600, "min_seconds": 9.0, "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.1}], "drift": 0,
    "actors": [PH(x=1300), piggy(1350, at=0.3), {"kind": "letters", "text": "?", "x": 1300, "y": 120, "at": C("couldn't anyone"), "size": 130, "color": "grey"}],
    "callouts": [co("Where was the money?", 1300, 140, C("Where was"), "gold", size=46)]})
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
cart("s19_kpmg", "m3_kpmg", {
    "worldW": 2600, "coasts": GER,
    "cam": [{"at": 0, "x": 900, "y": 400, "zoom": 0.95}], "drift": 10,
    "actors": [tower(200), office(520, "AUDITORS", "blue", at=C("special investigation"), scale=0.8), PH(x=2000), piggy(2050, at=0.0)],
    "callouts": [co("April 2020: special investigation", 1100, 150, C("special investigation"), "white", sub="KPMG"),
                 co("Data in the partners' hands", 1100, 260, C("in the hands"), "risk", sub="Wirecard's own statement"),
                 co("Company: “no incriminating evidence”", 1100, 370, C("for its part"), "gold")]},
    sources=["wirecard_kpmg"])
cart("s20_ey", "m3_ey", {
    "worldW": 2600, "coasts": GER,
    "cam": [{"at": 0, "x": 900, "y": 400, "zoom": 1.0}], "drift": 0,
    "actors": [tower(200), office(520, "EY", "blue", scale=0.8), {"kind": "storm", "x": [[0, 1400], [20, 500]], "y": 120, "at": C("refused to sign")}],
    "callouts": [co("June 18, 2020: auditor refuses to sign", 1100, 150, C("refused to sign"), "risk", size=40),
                 co("{{missing.display}} of cash unconfirmed", 1100, 260, C("could not be confirmed"), "risk", size=40),
                 co("Shares {{missing.drop_display}} in one day", 960, 960, C("shares fell"), "risk", screen=True, size=44)]},
    sources=["irish_2020", "bbk_rates"], sfx=[{"kind": "hit", "cue": "refused to sign", "gain": 0.35}])
cart("s21_banks", "m3_banks", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 380, "zoom": 1.1}], "drift": 0,
    "actors": [PH(x=1300, w=520), bank(1170, "BANK 1", y=314, scale=0.6), bank(1430, "BANK 2", y=314, scale=0.6), piggy(1750, y=230, at=0.0, scale=0.7)],
    "callouts": [co("Documents: false", 700, 160, C("documents were false"), "risk"), co("“Not a client”", 700, 260, C("not even a client"), "risk"),
                 co("Central bank: the money never came in", 1900, 160, C("central bank"), "white"),
                 co("Most likely did not exist", 1300, 960, C("most likely did not exist"), "risk", screen=True, size=46, sub="≈ a quarter of all its assets")]},
    sources=["aljazeera_2020"])
kinetic("s22_t3", "m3_transition", [("Built, at least in part,", 52, "A company worth", None, True), ("on cash that wasn't there", 74, "wasn't there", "risk", False),
                                    ("What happened next took one week", 40, "one week", "muted", True)])

# ====================================================================== PART 4: the collapse
card("s23_c4", "m4_card", "The Collapse", "One week")
cart("s24_q4", "m4_question", {
    "worldW": 2400, "min_seconds": 9.0, "night": True, "coasts": GER,
    "cam": [{"at": 0, "x": 500, "y": 380, "zoom": 1.2}], "drift": 0,
    "actors": [tower(200), {"kind": "storm", "x": [[0, 900], [12, 300]], "y": 120, "at": 0.3}],
    "callouts": [co("How fast can a star fall?", 1000, 160, C("How fast"), "risk", size=46)]})
cart("s25_week", "m4_week", {
    "worldW": 2600, "night": True, "coasts": {**GER, "darkAt": C("filed for insolvency")},
    "cam": [{"at": 0, "x": 700, "y": 380, "zoom": 1.0}], "drift": 8,
    "actors": [tower(200), {"kind": "storm", "x": [[0, 1300], [22, 400]], "y": 120, "at": 0.3}],
    "callouts": [co("June 19: the CEO resigns", 1300, 150, C("resigned"), "white"), co("June 25: insolvency", 1300, 250, C("filed for insolvency"), "risk", size=44),
                 co("First DAX company ever to go bust", 1300, 350, C("first company in the DAX"), "risk"),
                 co("Creditors owed {{insolvency.display}}", 960, 960, C("creditors owed"), "gold", screen=True, size=44, sub="Reuters")]},
    sources=["aljazeera_2020", "reuters_insolvency"], sfx=[{"kind": "hit", "cue": "filed for insolvency", "gain": 0.35}])
cart("s26_marsalek", "m4_marsalek", {
    "worldW": 3000, "night": True, "coasts": GER,
    "cam": [{"at": 0, "x": 700, "y": 380, "zoom": 1.0}, {"at": C("whereabouts"), "x": 1700, "y": 380, "zoom": 0.85, "dur": 3.0}], "drift": 0,
    "actors": [tower(200), {"kind": "plane", "x": [[0, 300], [{"cue": "vanished"}, 300], [{"cue": "vanished", "offset": 8}, 3200]], "y": 150, "text": "?", "scale": 0.7}],
    "callouts": [co("The COO: wanted in Germany", 1100, 160, C("is wanted"), "risk", size=40, sub="Jan Marsalek (not tried)"),
                 co("Believed to be in Russia", 1900, 160, C("believed to be"), "white", sub="whereabouts unknown (Reuters)"),
                 co("London 2025: Russian spy ring convicted", 960, 960, C("a court in London"), "gold", screen=True, sub="its leader reported to Marsalek (CPS)")]},
    sources=["reuters_spies", "cps_spies"])
kinetic("s27_trial", "m4_trial", [
    ("Munich: trial since {{trial.display}}", 44, "went on trial", None, True),
    ("Accused: commercial gang fraud · false accounting · breach of trust", 34, "accused of", "accent", True),
    ("“I reject all the charges”", 60, "rejects all the charges", "accent2", False),
    ("Hearings scheduled to the end of 2026 · presumed innocent until a verdict", 32, "presumed innocent", "muted", True)], chapter="The collapse")
kinetic("s28_t4", "m4_transition", [("A fraud this size needs people looking away", 48, "But a fraud", None, True), ("So who failed?", 88, "who failed", "risk", False)])

# ====================================================================== PART 5: who failed
card("s29_c5", "m5_card", "Who Failed", "The checks that came too late")
cart("s30_q5", "m5_question", {
    "worldW": 2600, "min_seconds": 9.0, "coasts": {"plain": True, "left": True, "right": True, "leftLabel": "AUDITOR", "rightLabel": "REGULATOR"},
    "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 0.8}], "drift": 0,
    "actors": [office(200, "AUDITOR", "blue"), office(2400, "REGULATOR", "gold"), island(x=1300, text="INVESTORS")],
    "callouts": [co("Who was supposed to catch it?", 1300, 160, C("supposed to catch"), "gold", size=44)]})
add("s31_auditor", "m5_auditor", "compare", {"chapter": "Who failed", "title": "The auditor", "sides": [
    {"kicker": "Clean audit opinions", "value": "10+ years", "label": "more than a decade (FT)", "cue": "without objections"},
    {"kicker": "2023 sanction in Germany", "value": "{{ey_ban.display}}", "label": "no new listed audit clients", "cue": "banned it"},
    {"kicker": "Fines", "value": "Firm + staff", "label": "current and former employees", "cue": "fined the firm"}]},
    sources=["irish_2023"])
cart("s32_regulator", "m5_regulator", {
    "worldW": 2400, "coasts": {"plain": True, "left": True, "leftLabel": "REGULATOR", "darkAt": C("left his post")},
    "cam": [{"at": 0, "x": 700, "y": 400, "zoom": 1.0}], "drift": 10,
    "actors": [office(200, "REGULATOR", "gold")],
    "callouts": [co("{{hufeld.display}}: the regulator's chief leaves", 1200, 160, C("left his post"), "white", size=40),
                 co("“…overlooked Germany's greatest postwar accounting fraud”", 960, 960, C("overlooked"), "risk", screen=True, sub="finance minister Olaf Scholz")]},
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
cart("s35_payoff", "payoff", {
    "worldW": 2800, "night": True, "coasts": {**GER, "darkAt": 0.0},
    "cam": [{"at": 0, "x": 1300, "y": 380, "zoom": 1.2}, {"at": C("They lived"), "x": 1300, "y": 400, "zoom": 0.85, "dur": 3.0}], "drift": 0,
    "actors": [tower(200), PH(x=1900), piggy(1950, at=0.0), coins(2700, -100, [1950, 200], 0.2, rate=5, until=C("asked to see")),
               {"kind": "letters", "text": "?", "x": 1950, "y": 100, "at": C("nothing there"), "size": 140, "color": "grey"}],
    "callouts": [co("Not stolen from a vault: never in one", 960, 160, C("never in one"), "white", screen=True, size=40),
                 co("…and there was nothing there", 960, 960, C("nothing there"), "risk", screen=True, size=46)]},
    sources=["aljazeera_2020"])
add("s36_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})

write(OUT, "# GENERATED by tools/gen_wirecard_storyboard.py; edit the generator, not this file.\n"
           "# Episode 12 storyboard: cartoon-first. The channel intro is inserted automatically after the hook.\n")
