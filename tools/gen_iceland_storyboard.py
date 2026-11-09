"""Generates projects/how-three-banks-nearly-destroyed-an-entire-country/deliverables/documentary/storyboard.yaml (Episode 22, Iceland 2008).

Bespoke worlds (tones from visual_direction.yaml: spectacle -> thriller -> crisis -> strategy -> reflective): a fjord with
fishing boats, the new `bankisle` item (a small island carrying three bank towers that grow far above it, sway and
topple into the sea) as the through-line, a British high street of savers, a television address at night, a London
order stamped "anti-terrorism", the krona chart, a ballot box, and the EFTA courtroom.
Presenter: the giant on a small island (bars), the savers' chain (boxes + arrows), why the rescue arrow cannot reach (boxes + arrow).
No bank logos, no flags, no likeness of real people (names in text only).
Run: python tools/gen_iceland_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-three-banks-nearly-destroyed-an-entire-country/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
NAMES = ["KAUPTHING", "LANDSBANKI", "GLITNIR"]


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def isle(x=960, y=760, **kw):
    return it("bankisle", x=x, y=y, names=["K", "L", "G"], **kw)


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("fjord", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.0}, {"at": 3.0, "x": 1000, "y": 520, "zoom": 0.9, "dur": 3.0}], "drift": 2,
    "items": [isle(1000, 800, at=0.2, scale=1.0, grow=[[0, 0.2], [3.5, 1.0]], wobbleAt=4.0)],
    "callouts": [co("Banks too big for their own country", 960, 960, C("What happens"), "gold", screen=True, size=40)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("fjord", night=True)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 480, "zoom": 0.95}, {"at": C("The prime minister"), "x": 1800, "y": 500, "zoom": 1.0, "dur": 2.4},
            {"at": C("And the British government"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [isle(900, 800, at=0.2, scale=1.0, grow=1.0, wobbleAt=0.5, fallAt=C("collapsed in", 0.3)),
              it("calendar", x=350, y=280, at=0.3, pages=[[0, "OCT", "2008"]], scale=0.8),
              it("device", type="tv", x=1800, y=F, at=C("The prime minister"), scale=1.2),
              it("docs", x=2400, y=560, at=C("And the British government"), text="UK FREEZING ORDER", scale=0.6, stamp="ANTI-TERRORISM LAW", stampAt=C("anti-terrorism law"))],
    "callouts": [co("Three banks collapse in < 1 week", 960, 960, C("Its three biggest banks"), "risk", screen=True, size=40, sub="IMF", until=C("According to the International", -0.3)),
                 co("Banking system ≈ 9× the whole economy", 960, 960, C("According to the International"), "gold", screen=True, size=40, sub="IMF", until=C("The prime minister", -0.3)),
                 co("'National bankruptcy'", 960, 960, C("The prime minister"), "white", screen=True, size=42, until=C("And the British government", -0.3)),
                 co("Britain uses an anti-terrorism law", 960, 960, C("And the British government"), "risk", screen=True, size=40)]},
    sources=["imf_pr", "haarde", "freeze"])

# ====================================================================== PART 1: from fish to finance
card("s03_c1", "m1_card", "From Fish to Finance", "Iceland, 1990s-2007")
stage("s04_q1", "m1_question", {
    "zones": [Z("fjord")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("ship", type="dhow", x=700, at=0.2, scale=0.6, color="#455A64"), isle(1300, 820, at=0.8, scale=0.6, grow=[[0, 0.0], [5, 0.6]])],
    "callouts": [co("Fishermen → global bankers?", 960, 150, C("How does a country"), "gold", screen=True, size=44)]})
stage("s05_fish", "m1_fish", {
    "zones": [Z("fjord", -1600, 1500), Z("parliament", 1500, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("Then, around the turn"), "x": 2100, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("ship", type="dhow", x=[[0, 400], [12, 900]], at=0.2, scale=0.6, color="#455A64"),
              it("sign", x=700, y=300, text="FISH · ALUMINIUM", sub="the old economy", at=C("Fishing"), color="#BBDEFB", size=34),
              it("building", x=1200, at=C("Its banks were small"), text="STATE BANK", scale=0.6),
              it("pricetag", x=2000, y=300, at=C("the government sold them off"), pages=[[0, "SOLD"]], sub="privatised"),
              it("docs", x=2400, y=560, at=C("arbitrary and opaque"), text="THE SALE", scale=0.6, stamp="'ARBITRARY AND OPAQUE'", stampAt=C("arbitrary and opaque", 0.5))],
    "callouts": [co("Iceland lived on fish and aluminium", 960, 960, C("Iceland lived mainly"), "white", screen=True, size=40, sub="Cambridge", until=C("Then, around the turn", -0.3)),
                 co("Bank sale: 'arbitrary and opaque procedures'", 960, 960, C("A study from the University"), "gold", screen=True, size=36, sub="McCombie & Spreafico, Cambridge")]},
    sources=["cambridge"])
stage("s06_boom", "m1_boom", {
    "zones": [Z("fjord")], "worldW": 2800,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 0.95}, {"at": C("In fact, the owners"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [isle(1000, 820, at=0.2, scale=0.9, grow=[[0, 0.15], [{"cue": "extraordinary speed", "offset": 4}, 0.8]]),
              it("coins", **{"from": [-200, 300], "to": [1000, 400]}, at=C("The banks borrowed abroad"), rate=7, until=C("In fact, the owners", 2)),
              *crowd([1700, 1830], "cheer", at=C("lent to Iceland's own businessmen"), scale=0.7),
              it("arrow", **{"from": [1150, 450], "to": [1650, 500]}, at=C("In fact, the owners")),
              it("letters", x=1800, y=200, text="OWNERS = BORROWERS", at=C("biggest borrowers"), size=54, color="risk")],
    "callouts": [co("From 2003: 'extraordinary fast' growth", 960, 960, C("From about"), "gold", screen=True, size=40, sub="Cambridge", until=C("In fact, the owners", -0.3)),
                 co("The banks' owners became top borrowers", 960, 960, C("In fact, the owners"), "risk", screen=True, size=38)]},
    sources=["cambridge"])
add("p07_giant", "m1_draw", "engine_draw", {
    "title": "A small country holding up a giant", "board": BOARD, "draw_start": C("Here is the size"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 820 L 1400 820 M 560 820 L 560 330", "color": "ink", "width": 4, "start": C("Here is the size")},
        {"d": "M 640 820 L 640 772 L 780 772 L 780 820", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.4, "kind": "bar", "start": C("One bar"), "label": lbl("ECONOMY (GDP) = 1", 710, 860, 22, "accent2")},
        {"d": "M 900 820 L 900 388 L 1040 388 L 1040 820", "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("Now here are the assets"), "label": lbl("BANK ASSETS ≈ 9 (end-2007, IMF)", 970, 360, 22, "risk")},
        {"d": "M 1100 760 Q 1200 700 1280 760 Q 1200 820 1100 760 Z", "color": "accent3", "width": 4, "start": C("A small country"), "label": lbl("small island", 1190, 860, 20, "accent3")},
        {"d": "M 1190 700 L 1190 420", "color": "ink", "width": 5, "start": C("holding up a giant")},
        {"d": "M 1260 420 Q 1340 520 1290 640", "color": "risk", "width": 4, "start": C("who could possibly catch it"), "label": lbl("?", 1340, 500, 60, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Almost nine bars", 0.2), "dur": 1.4, "target": [970, 400]}],
    "scale": 0.86, "floor": 1040}, sources=["imf_pr"])
kinetic("s08_t1", "m1_transition", [("The banks needed more money", 56, "needed more money", None, True), ("So they looked for savers. In Britain.", 52, "In Britain", "gold", True)])

# ====================================================================== PART 2: Icesave
card("s09_c2", "m2_card", "Icesave", "Britain and the Netherlands, 2006-2008")
stage("s10_q2", "m2_question", {
    "zones": [Z("city")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("piggy", x=800, at=0.3, scale=0.8), it("arrow", **{"from": [950, 450], "to": [1350, 400]}, at=1.5), isle(1500, 820, at=1.0, scale=0.5, grow=0.6)],
    "callouts": [co("Why bank with an Icelandic bank?", 960, 150, C("Why would a British"), "gold", screen=True, size=42)]})
stage("s11_icesave", "m2_icesave", {
    "zones": [Z("city")], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("It also took savers"), "x": 1900, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("browser", x=900, y=420, w=520, h=300, at=C("launched an internet savings account"), url="icesave · online savings", pages=[[0, "TOP INTEREST RATE"]]),
              it("pricetag", x=1350, y=300, at=C("best interest rates"), pages=[[0, "BEST RATE"]], sub="2006"),
              it("coins", **{"from": [2400, 300], "to": [900, 450]}, at=C("the deposits flooded in"), rate=9),
              *crowd([1700 + 110 * k for k in range(7)], "phone", at=C("It also took savers"), scale=0.6),
              it("counter", x=2050, y=200, at=C("In the end"), steps=[[0, 0], [{"cue": "In the end", "offset": 1.5}, 340000]], prefix="≈ ", text="BRITISH + DUTCH SAVERS")],
    "callouts": [co("Oct 2006: Icesave, the best rates in Britain", 960, 960, C("In October"), "gold", screen=True, size=38, sub="Cambridge", until=C("It also took savers", -0.3)),
                 co("≈ 340,000 British and Dutch savers", 960, 960, C("It also took savers"), "white", screen=True, size=40, sub="The Irish Times")]},
    sources=["cambridge", "irish_2010"])
add("p12_catch", "m2_risk", "engine_draw", {
    "title": "The catch", "board": BOARD, "draw_start": C("Here is a British saver"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 400, 220, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is a British saver"), "label": lbl("UK SAVER", 670, 468, 26, "accent2")},
        {"d": rect(900, 400, 240, 120), "color": "accent", "width": 6, "kind": "box", "start": C("Here is Icesave"), "label": lbl("ICESAVE (BRANCH)", 1020, 468, 22, "accent")},
        {"d": arrow((790, 460), (890, 460), 0.1), "color": "ink", "width": 5, "start": C("Here is Icesave", 0.6)},
        {"d": rect(900, 660, 240, 120), "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.15, "kind": "box", "start": C("comes from here"), "label": lbl("ICELAND'S FUND", 1020, 728, 22, "risk")},
        {"d": arrow((1020, 530), (1020, 650), 0.0), "color": "ink", "width": 5, "start": C("If the bank fails")},
        {"d": "M 1200 760 L 1240 760 M 1300 600 L 1460 600 L 1460 840 L 1300 840 Z", "color": "muted", "width": 4, "start": C("two much bigger ones"), "label": lbl("UK + NETHERLANDS", 1380, 880, 20, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("A fund in a small country", 0.2), "dur": 1.4, "target": [1020, 720]}],
    "scale": 0.86, "floor": 1040}, sources=["cambridge", "efta"])
stage("s13_warning", "m2_warning", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("The Cambridge study"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("chart", x=800, y=420, w=500, h=300, at=C("huge deficits"), dur=2.5, text="CURRENT ACCOUNT (% GDP)", pts=[0.6, 0.5, 0.35, 0.2, 0.05], color="risk"),
              it("docs", x=1600, y=560, at=C("toxic mortgage-linked securities"), text="TOXIC MORTGAGE BONDS", scale=0.6, stamp="NONE", stampAt=C("that sank others")),
              it("letters", x=1700, y=220, text="TOO BIG · BORROWED MONEY", at=C("They were too big"), size=48, color="risk")],
    "callouts": [co("Deficit near 21% of GDP by 2006", 960, 960, C("Iceland was running"), "risk", screen=True, size=38, sub="Cambridge (Table 2)", until=C("The Cambridge study", -0.3)),
                 co("No toxic bonds, just too big and too indebted", 960, 960, C("The Cambridge study"), "white", screen=True, size=36)]},
    sources=["cambridge"])
stage("s14_praise", "m2_praise", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("When the people paid"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("paper", x=900, y=380, at=C("a report by respected"), text="'very well run banks'", name="REPORT · 2007", scale=0.75),
              *crowd([1500, 1640], "cheer", at=C("Iceland's regulators"), scale=0.7),
              it("letters", x=1600, y=200, text="WHAT IF THE MONEY STOPS?", at=C("What if the money stops"), size=50, color="gold")],
    "callouts": [co("2007 report: 'very well run banks'", 960, 960, C("a report by respected"), "white", screen=True, size=40, sub="quoted by Cambridge", until=C("When the people paid", -0.3)),
                 co("Nobody asked: what if the money stops?", 960, 960, C("When the people paid"), "gold", screen=True, size=38)]},
    sources=["cambridge"])
kinetic("s15_t2", "m2_transition", [("September 2008", 70, "September", None, False), ("The borrowed money stopped", 58, "money stopped", "risk", False)])

# ====================================================================== PART 3: seven days in October
card("s16_c3", "m3_card", "Seven Days in October", "October 2008")
stage("s17_q3", "m3_question", {
    "zones": [Z("fjord", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.2}, {"at": 3.0, "x": 960, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [isle(960, 820, at=0.2, scale=0.9, grow=0.9, wobbleAt=1.0)],
    "callouts": [co("When the money stops…", 960, 150, C("What happens when"), "gold", screen=True, size=44)]})
stage("s18_fall", "m3_fall", {
    "zones": [Z("fjord", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.0}, {"at": C("One after another"), "x": 1100, "y": 520, "zoom": 0.9, "dur": 2.4}], "drift": 2,
    "items": [it("sign", x=500, y=260, text="LEHMAN BROTHERS", sub="Sep 2008", at=C("After the collapse"), color="#FFCDD2", size=30),
              isle(1100, 820, at=0.2, scale=1.0, grow=1.0, wobbleAt=C("that was fatal"), fallAt=C("One after another", 0.5)),
              it("letters", x=1650, y=220, text="NO FOREIGN MONEY TO PRINT", at=C("could not print the foreign money"), size=46, color="risk")],
    "callouts": [co("No one rolls over the debts", 960, 960, C("They could not roll over"), "risk", screen=True, size=40, until=C("One after another", -0.3)),
                 co("Glitnir, Landsbanki, Kaupthing: ≈ 85% of the system", 960, 960, C("One after another"), "gold", screen=True, size=36, sub="IMF")]},
    sources=["imf_pr"])
stage("s19_speech", "m3_speech", {
    "zones": [Z("den", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And he ended"), "x": 1200, "y": 500, "zoom": 1.15, "dur": 2.4}], "drift": 2,
    "items": [it("device", type="tv", x=1100, y=F, at=0.2, scale=1.6),
              it("calendar", x=400, y=300, at=0.3, pages=[[0, "OCT 6", "2008"]], scale=0.8),
              *crowd([1700, 1820, 1940], "worry", at=C("a very real danger"), scale=0.7),
              it("letters", x=1100, y=200, text="'GOD BLESS ICELAND'", at=C("God bless Iceland"), size=60, color="gold")],
    "callouts": [co("'Sucked with the banks into the whirlpool'", 960, 960, C("There was, he said"), "white", screen=True, size=38, sub="Address to the Nation", until=C("He announced", -0.3)),
                 co("Emergency bill, passed the same day", 960, 960, C("He announced"), "gold", screen=True, size=40)]},
    sources=["haarde"])
stage("s20_scale", "m3_scale", {
    "zones": [Z("parliament")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Measured together"), "x": 1600, "y": 520, "zoom": 0.9, "dur": 2.4}], "drift": 3,
    "items": [it("docs", x=800, y=560, at=0.3, text="BANKS NATIONALISED · OCT 7", scale=0.6, stamp="STATE CONTROL", stampAt=C("took control")),
              it("tower", x=1400, text="LEHMAN", color="#455A64", h=600, at=C("after Lehman Brothers"), scale=0.7),
              it("tower", x=1750, text="WASHINGTON MUTUAL", color="#546E7A", h=420, at=C("Washington Mutual"), scale=0.7),
              it("tower", x=2100, text="ICELAND'S 3", color="#C62828", h=[[0, 20], [{"cue": "Measured together", "offset": 1.5}, 380]], at=C("Measured together"), scale=0.7)],
    "callouts": [co("The third largest bankruptcy in the world", 960, 960, C("Measured together"), "risk", screen=True, size=40, sub="Cambridge (heights illustrative)")]},
    sources=["cambridge"])
stage("s21_terror", "m3_terror", {
    "zones": [Z("parliament")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("The power it used"), "x": 1600, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("clock", x=500, y=300, at=0.3, period=4.0),
              it("calendar", x=800, y=300, at=0.3, pages=[[0, "OCT 8", "10:00"]], scale=0.8),
              it("docs", x=1400, y=560, at=C("made an order"), text="LANDSBANKI FREEZING ORDER", scale=0.65, stamp="FROZEN", stampAt=C("freezing Landsbanki's assets")),
              it("sign", x=1900, y=300, text="ANTI-TERRORISM, CRIME AND SECURITY ACT 2001", sub="the legal power used", at=C("The power it used"), color="#FFCDD2", size=24),
              isle(2300, 820, at=C("used against the bank"), scale=0.5, grow=0.3)],
    "callouts": [co("8 Oct, 10:00: UK freezes Landsbanki's assets", 960, 960, C("At ten in the morning"), "white", screen=True, size=38, sub="legislation.gov.uk", until=C("The power it used", -0.3)),
                 co("…under an anti-terrorism law", 960, 960, C("The power it used"), "risk", screen=True, size=42)]},
    sources=["freeze"])
add("p22_reach", "m3_draw", "engine_draw", {
    "title": "Why the rescue cannot reach", "board": BOARD, "draw_start": C("Here is the government"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 240, 160), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the government"), "label": lbl("GOVERNMENT", 680, 450, 24, "accent2")},
        {"d": rect(1100, 330, 380, 430), "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.15, "kind": "box", "start": C("Here are the banks"), "label": lbl("BANKS' DEBTS", 1290, 550, 28, "risk")},
        {"d": arrow((810, 440), (1000, 520), -0.15), "color": "ink", "width": 5, "start": C("An arrow from the government")},
        {"d": "M 1010 520 L 1050 600 M 1050 520 L 1010 600", "color": "risk", "width": 6, "start": C("The arrow simply cannot reach"), "label": lbl("TOO SHORT", 1030, 640, 22, "risk")},
        {"d": "M 920 300 L 920 860", "color": "accent", "width": 7, "start": C("drew a line"), "label": lbl("THE LINE", 920, 290, 24, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("cannot reach", 0.2), "dur": 1.4, "target": [1030, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["imf_pr", "haarde"])
kinetic("s23_t3", "m3_transition", [("The banks were gone", 62, "The banks were gone", None, False), ("Now the bill arrived", 62, "the bill arrived", "risk", False)])

# ====================================================================== PART 4: the bill
card("s24_c4", "m4_card", "The Bill", "2008-2011")
stage("s25_q4", "m4_question", {
    "zones": [Z("vault")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vaultdoor", x=960, at=0.2, openAt=1.0, scale=0.8), it("letters", x=960, y=200, text="EMPTY", at=2.5, size=80, color="risk")],
    "callouts": [co("Who pays when the banks vanish?", 960, 150, C("Who pays"), "gold", screen=True, size=42)]})
stage("s26_krona", "m4_krona", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Even at official rates"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("chart", x=800, y=420, w=520, h=320, at=C("the currency fell"), dur=3, text="CURRENCY OFFSHORE · STOCKS", pts=[0.9, 0.85, 0.5, 0.25, 0.15], color="risk"),
              it("counter", x=1700, y=220, at=C("Even at official rates"), decimals=1, steps=[[0, 60.7], [{"cue": "lost", "offset": 1.5}, 135.3]], text="KRÓNUR PER US DOLLAR (OECD)"),
              it("pricetag", x=1700, y=520, at=C("Imports became"), pages=[[0, "IMPORTS ↑"], [{"cue": "inflation rose"}, "INFLATION 18%+"]], sub="2009")],
    "callouts": [co("Currency −70%+ offshore · stocks −80%", 960, 960, C("According to the IMF"), "risk", screen=True, size=38, sub="IMF", until=C("Even at official rates", -0.3)),
                 co("60.7 → 135.3 krónur per dollar (Oct 2007 → Nov 2008)", 960, 960, C("Even at official rates"), "white", screen=True, size=32, sub="OECD via FRED")]},
    sources=["imf_pr", "fred_isk", "cambridge"])
stage("s27_recession", "m4_recession", {
    "zones": [Z("fjord")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("According to the Cambridge"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=900, y=220, at=C("The economy shrank"), suffix="%", decimals=1, steps=[[0, 1.1], [{"cue": "in twenty oh nine", "offset": 0.5}, -6.6], [{"cue": "the year after", "offset": 0.5}, -4.1]], text="GDP GROWTH 2008 → 2009 → 2010"),
              *crowd([1500, 1620, 1740, 1860], "worry", at=C("Unemployment soared"), scale=0.7),
              it("letters", x=1700, y=220, text="WORST IN THE OECD", at=C("the worst recession"), size=56, color="risk")],
    "callouts": [co("2009: −6.6% · 2010: −4.1%", 960, 960, C("The economy shrank"), "risk", screen=True, size=40, sub="Cambridge", until=C("According to the Cambridge", -0.3)),
                 co("The worst recession of any OECD country", 960, 960, C("According to the Cambridge"), "white", screen=True, size=38)]},
    sources=["cambridge"])
stage("s28_imf", "m4_imf", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In return"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("contract", x=900, y=430, at=C("the IMF approved"), text="IMF LOAN", sub="≈ $2.1bn · 2 years", scale=0.65),
              it("stack", x=1500, h=[[0, 40], [{"cue": "about", "offset": 1.5}, 260]], at=C("the IMF approved"), text="$2.1BN", sub="IMF"),
              it("sign", x=1500, y=260, text="STABILIZE THE CURRENCY", sub="and the public finances", at=C("In return"), color="#BBDEFB", size=30)],
    "callouts": [co("Nov 2008: IMF loan ≈ {{imf.display}}", 960, 960, C("In November"), "gold", screen=True, size=40, sub="IMF")]},
    sources=["imf_pr"])
add("p29_bill", "m4_icesave", "engine_draw", {
    "title": "Who pays the savers?", "board": BOARD, "draw_start": C("Britain and the Netherlands paid"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 260, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Britain and the Netherlands paid"), "label": lbl("UK + NL GOVERNMENTS", 690, 428, 20, "accent2")},
        {"d": rect(1200, 360, 240, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("paid back their own savers"), "label": lbl("SAVERS REPAID", 1320, 428, 22, "accent3")},
        {"d": arrow((830, 420), (1190, 420), 0.1), "color": "ink", "width": 5, "start": C("paid back their own savers", 0.5), "label": lbl("UK alone ≈ $7.8bn", 1010, 380, 20, "ink")},
        {"d": rect(880, 640, 260, 120), "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.15, "kind": "box", "start": C("sent the bill to Iceland"), "label": lbl("ICELAND'S TAXPAYERS?", 1010, 708, 20, "risk")},
        {"d": arrow((690, 490), (900, 640), 0.15), "color": "risk", "width": 5, "start": C("sent the bill to Iceland", 0.4), "label": lbl("the bill", 720, 600, 22, "risk")},
        {"d": "M 1160 700 L 1300 700", "color": "accent", "width": 5, "start": C("with interest"), "label": lbl("+ interest", 1320, 690, 22, "accent", "start")},
    ],
    "actions": [{"kind": "point", "at": C("The governments negotiated", 0.2), "dur": 1.4, "target": [1010, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["irish_2010", "ukgov_2016", "fred_gbp"])
stage("s30_vote", "m4_vote", {
    "zones": [Z("parliament")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("A new, softer deal"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=900, y=220, at=C("In a referendum"), suffix="% NO", steps=[[0, 0], [{"cue": "voted against", "offset": 0.5}, 93]], text="MARCH 2010"),
              it("counter", x=1700, y=220, at=C("A new, softer deal"), suffix="% NO", decimals=1, steps=[[0, 0], [{"cue": "rejected again", "offset": 0.5}, 58.9]], text="APRIL 2011"),
              *crowd([800 + 120 * k for k in range(8)], "cheer", at=C("Icelanders said no"), scale=0.6)],
    "callouts": [co("2010: just over 93% vote No", 960, 960, C("In a referendum"), "risk", screen=True, size=40, sub="The Irish Times", until=C("A new, softer deal", -0.3)),
                 co("2011: rejected again, 58.9% No", 960, 960, C("A new, softer deal"), "risk", screen=True, size=40, sub="Fondation Robert Schuman")]},
    sources=["irish_2010", "schuman_2011"])
kinetic("s31_t4", "m4_transition", [("Britain and the Netherlands", 56, "Britain and the Netherlands", None, True), ("took the fight to court", 60, "to court", "gold", False)])

# ====================================================================== PART 5: the verdicts
card("s32_c5", "m5_card", "The Verdicts", "2012-2016")
stage("s33_q5", "m5_question", {
    "zones": [Z("court")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("gavel", x=960, y=420, hits=[3.5]), it("letters", x=960, y=200, text="?", at=1.0, size=120, color="gold")],
    "callouts": [co("Did Iceland have to pay?", 960, 150, C("Did Iceland"), "gold", screen=True, size=44)]})
stage("s34_efta", "m5_efta", {
    "zones": [Z("court")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Iceland had not broken"), "x": 1500, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=C("On January"), pages=[[0, "JAN 28", "2013"]], scale=0.8),
              it("gavel", x=1000, y=420, hits=[C("it ruled", 0.3)]),
              it("docs", x=1600, y=560, at=C("The claim against Iceland"), text="CASE E-16/11", scale=0.65, stamp="DISMISSED", stampAt=C("The claim against Iceland", 1.5))],
    "callouts": [co("EFTA Court: application dismissed", 960, 960, C("it ruled"), "green", screen=True, size=42, sub="EFTA Court, 28 Jan 2013")]},
    sources=["efta"])
stage("s35_estate", "m5_estate", {
    "zones": [Z("vault")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("In January"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("vaultdoor", x=800, at=0.2, openAt=0.6, scale=0.7),
              it("coins", **{"from": [800, 450], "to": [2200, 400]}, at=C("Landsbanki's remaining assets"), rate=6),
              it("calendar", x=1700, y=300, at=C("In January"), pages=[[0, "JAN 15", "2016"]], scale=0.8),
              it("letters", x=2200, y=200, text="PAID IN FULL", at=C("recovered all"), size=60, color="green")],
    "callouts": [co("Landsbanki's estate pays the priority claims", 960, 960, C("The savers' money came back"), "white", screen=True, size=38, sub="Government of Iceland", until=C("In January", -0.3)),
                 co("UK Treasury: all taxpayer money recovered", 960, 960, C("In January"), "green", screen=True, size=40, sub="HM Treasury, 15 Jan 2016")]},
    sources=["ukgov_2016"])
stage("s36_people", "m5_people", {
    "zones": [Z("court")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("In twenty fifteen"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("gavel", x=900, y=420, hits=[C("was convicted on one charge", 0.3), C("sent the former head", 0.3)]),
              it("docs", x=800, y=600, at=C("In twenty twelve"), text="FORMER PM: 1 CHARGE", scale=0.55, stamp="NO PUNISHMENT", stampAt=C("with no punishment")),
              it("docs", x=1700, y=600, at=C("In twenty fifteen"), text="FORMER KAUPTHING CEO", scale=0.55, stamp="5½ YEARS", stampAt=C("to prison for"))],
    "callouts": [co("2012: ex-PM convicted on one count, no punishment", 960, 960, C("In twenty twelve"), "white", screen=True, size=34, sub="CBC / AP", until=C("In twenty fifteen", -0.3)),
                 co("2015: Kaupthing's ex-CEO gets 5½ years", 960, 960, C("In twenty fifteen"), "risk", screen=True, size=38, sub="AP via Fox News")]},
    sources=["cbc_2012", "fox_2015"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("fjord")], "worldW": 2800,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.0}, {"at": C("In the end"), "x": 1400, "y": 520, "zoom": 0.9, "dur": 2.6}], "drift": 2,
    "items": [isle(1000, 820, at=0.2, scale=1.0, grow=[[0, 0.3], [{"cue": "bigger than the country", "offset": 1}, 1.0]], wobbleAt=C("the bank starts controlling"), fallAt=C("Iceland let its banks fail")),
              it("ship", type="dhow", x=[[0, 1700], [30, 2300]], at=C("In the end"), scale=0.6, color="#455A64"),
              it("letters", x=1900, y=200, text="TOO BIG FOR ITS COUNTRY", at=C("That a bank can grow"), size=48, color="risk")],
    "callouts": [co("A bank can outgrow its own country", 960, 150, C("That a bank can grow"), "white", screen=True, size=40, until=C("In the end", -0.3)),
                 co("Iceland let its banks fail", 960, 150, C("In the end"), "gold", screen=True, size=42)]},
    sources=["imf_pr", "efta"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_iceland_storyboard.py; edit the generator, not this file.\n"
           "# Episode 22 storyboard (Iceland 2008): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
