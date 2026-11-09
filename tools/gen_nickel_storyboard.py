"""Generates projects/the-metal-trade-that-broke-a-billion-dollar-market/deliverables/documentary/storyboard.yaml (Episode 25, LME nickel 2022).

Bespoke worlds (tones from visual_direction.yaml: thriller -> crisis -> strategy -> reflective): a London exchange floor,
a night desk in Hong Kong, a clearing-house vault where margin calls pile up, a dawn boardroom, two courtrooms and a
regulator's office. The new `tradescreen` item (the 3M nickel screen: a line that climbs, a PRICE BANDS lamp that
turns OFF, then SUSPENDED and CANCELLED stamps) is the through-line.
Presenter: how a short works (boxes + arrows), the morning of March 8 (bars), the exchange's dilemma (boxes + arrows).
No LME logo, no real trading UI, no likeness of real people (names in text only).
Run: python tools/gen_nickel_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-metal-trade-that-broke-a-billion-dollar-market/deliverables/documentary/storyboard.yaml"
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


def screen(x=960, y=430, **kw):
    return it("tradescreen", x=x, y=y, **kw)


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("exchange", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 460, "zoom": 1.15}, {"at": 3.5, "x": 1000, "y": 480, "zoom": 1.0, "dur": 3.0}], "drift": 1,
    "items": [screen(1000, 430, at=0.2, scale=1.1, price=[[0, 28961], [3.0, 48075], [5.0, 101365]], bandsOffAt=2.5, haltAt=C("decides that none", 0.3), cancelAt=C("decides that none", 1.2), cancelFrom=3.0)],
    "callouts": [co("Doubled in one morning… then erased", 960, 960, C("What happens"), "gold", screen=True, size=40)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("exchange", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 460, "zoom": 1.0}, {"at": C("Then it cancelled"), "x": 1400, "y": 480, "zoom": 0.9, "dur": 2.4}], "drift": 2,
    "items": [screen(1000, 430, at=0.2, scale=0.95, price=[[0, 48075], [C("shot past", -2), 70000], [C("shot past", 1), 101365]], bandsOffAt=0.5, haltAt=C("suspended trading"), cancelAt=C("Then it cancelled"), cancelFrom=0.3),
              it("counter", x=1800, y=220, at=C("Then it cancelled"), prefix="$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "worth", "offset": 1}, 13.4]], text="TRADES CANCELLED"),
              *crowd([1750, 1880], "worry", at=C("Some traders lost"), scale=0.7), *crowd([2100, 2230], "cheer", at=C("Others were saved"), scale=0.7)],
    "callouts": [co("Nickel: $101,365 a tonne", 960, 960, C("shot past"), "risk", screen=True, size=42, sub="FCA Final Notice", until=C("Then it cancelled", -0.3)),
                 co("$13.4bn of trades cancelled", 960, 960, C("Then it cancelled"), "gold", screen=True, size=42)]},
    sources=["fca"])

# ====================================================================== PART 1: a market that never sleeps
card("s03_c1", "m1_card", "A Market That Never Sleeps", "London · Hong Kong")
stage("s04_q1", "m1_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("board", x=960, y=380, at=0.3, text="METALS · 3 MONTHS", rows=[{"name": "COPPER"}, {"name": "ALUMINIUM"}, {"name": "NICKEL", "color": "gold"}])],
    "callouts": [co("Who sets the price of metals?", 960, 150, C("Who sets"), "gold", screen=True, size=44)]})
stage("s05_lme", "m1_lme", {
    "zones": [Z("exchange", -1600, 1500), Z("city", 1500, 6000, night=True)], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("Miners, factories"), "x": 1400, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("And the market runs"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("device", type="phone", x=500, y=F, at=C("your phone"), scale=0.9), it("device", type="car", x=800, y=F, at=C("your car"), scale=0.6),
              it("board", x=1100, y=380, at=C("The London Metal Exchange trades"), text="DELIVER IN 3 MONTHS", rows=[{"name": "COPPER"}, {"name": "ALUMINIUM"}, {"name": "NICKEL", "color": "gold"}]),
              *crowd([1500, 1620, 1740], "stand", at=C("Miners, factories"), scale=0.7),
              it("clock", x=2200, y=330, at=C("And the market runs"), period=2.0),
              it("letters", x=2200, y=600, text="7 OF 19 HOURS: HONG KONG", at=C("handled overnight"), size=48, color="gold")],
    "callouts": [co("A key world price for metals, set in London", 960, 960, C("For most of the metals"), "white", screen=True, size=38, until=C("And the market runs", -0.3)),
                 co("7 of 19 trading hours run overnight from Hong Kong", 960, 960, C("And the market runs"), "gold", screen=True, size=34, sub="FCA Final Notice")]},
    sources=["fca"])
add("p06_short", "m1_draw", "engine_draw", {
    "title": "How a short works", "board": BOARD, "draw_start": C("A company that will sell"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 380, 240, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("A company that will sell"), "label": lbl("SHORT SELLER", 680, 448, 24, "accent2")},
        {"d": rect(1180, 380, 240, 120), "color": "accent", "width": 6, "kind": "box", "start": C("the exchange asks it"), "label": lbl("CLEARING HOUSE", 1300, 448, 22, "accent")},
        {"d": arrow((810, 420), (1170, 420), 0.1), "color": "ink", "width": 5, "start": C("to put up more cash"), "label": lbl("margin $$$", 990, 390, 22, "ink")},
        {"d": "M 600 760 L 760 700 L 920 620 L 1080 520", "color": "risk", "width": 6, "start": C("If the price rises"), "label": lbl("price ↑ = loss ↑", 840, 780, 24, "risk")},
        {"d": "M 1180 560 L 1420 560 L 1420 820 L 1180 820 Z", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.15, "kind": "box", "start": C("faster than anyone can pay"), "label": lbl("CAN'T PAY?", 1300, 700, 26, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("faster than anyone can pay", 0.2), "dur": 1.4, "target": [1300, 690]}],
    "scale": 0.86, "floor": 1040}, sources=["fca"])
stage("s07_short", "m1_short", {
    "zones": [Z("office", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("And much of it"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 2,
    "items": [it("stack", x=800, h=[[0, 60], [{"cue": "a very large short", "offset": 2}, 380]], at=C("a very large short"), text="SHORT NICKEL", sub="(claimants' account)", color="#C62828"),
              it("sign", x=800, y=200, text="TSINGSHAN (per the claimants)", sub="Chinese industrial user of nickel", at=C("Tsingshan"), color="#FFE082", size=28),
              it("contract", x=1600, y=430, at=C("private deals"), text="OTC DEALS", sub="off the exchange", scale=0.6),
              it("magnifier", x=[[0, 1400], [6, 1800]], y=[[0, 520], [6, 480]], at=C("The exchange could not see it"), scale=0.8),
              it("letters", x=1700, y=200, text="INVISIBLE", at=C("could not see it"), size=64, color="risk")],
    "callouts": [co("A huge short, mostly off-exchange (OTC)", 960, 960, C("In early"), "white", screen=True, size=38, sub="High Court judgment (claimants' case)", until=C("The exchange could not see it", -0.3)),
                 co("The exchange could not see it", 960, 960, C("The exchange could not see it"), "risk", screen=True, size=42, sub="FCA Final Notice")]},
    sources=["highcourt", "fca"])
kinetic("s08_t1", "m1_transition", [("Then Russia invaded Ukraine", 58, "Russia invaded Ukraine", None, True), ("…and Russia produces nickel", 56, "a large global producer", "risk", False)])

# ====================================================================== PART 2: the squeeze
card("s09_c2", "m2_card", "The Squeeze", "4-8 March 2022")
stage("s10_q2", "m2_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [*crowd([600 + 120 * k for k in range(7)], "worry", at=0.3, scale=0.65)],
    "callouts": [co("Everyone who bet on a fall buys at once", 960, 150, C("What happens"), "gold", screen=True, size=40)]})
stage("s11_friday", "m2_friday", {
    "zones": [Z("vault")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("By the end of Monday"), "x": 1800, "y": 480, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=0.2, pages=[[0, "MAR 4", "FRIDAY"], [{"cue": "On Monday morning"}, "MAR 7", "MONDAY"]], scale=0.8),
              it("stack", x=800, h=[[0, 40], [{"cue": "in extra margin", "offset": 1}, 175]], at=C("asked its members"), text="$3.5BN", sub="Fri margin (record)"),
              it("stack", x=1100, h=[[0, 40], [{"cue": "a new record", "offset": 0.5}, 255]], at=C("On Monday morning"), text="$5.1BN", sub="Mon morning (record)"),
              screen(1900, 430, at=C("By the end of Monday"), scale=0.8, price=[[0, 28961], [{"cue": "jumped by", "offset": 2}, 48075]])],
    "callouts": [co("Record margin calls: $3.5bn, then $5.1bn", 960, 960, C("On Friday"), "white", screen=True, size=38, sub="FCA Final Notice", until=C("By the end of Monday", -0.3)),
                 co("Monday close: +66% to $48,075", 960, 960, C("By the end of Monday"), "risk", screen=True, size=40)]},
    sources=["fca"])
stage("s12_monday", "m2_monday", {
    "zones": [Z("office")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("A board member wrote"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=800, y=220, at=C("By two in the afternoon"), prefix="$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "from its members that day", "offset": 0.5}, 7.4]], text="INTRADAY CALLS, MON 7 MARCH"),
              it("paper", x=900, y=520, at=C("one manager warned"), text="'adding to the market stress'", name="EMAIL 1.25PM", scale=0.6),
              it("paper", x=1600, y=380, at=C("A board member wrote"), text="'Nickel up 66%, aluminium down 3%?'", name="EMAIL 5.10PM", scale=0.65),
              it("letters", x=2100, y=220, text="'TOTAL DISARRAY'", at=C("Another described"), size=56, color="risk")],
    "callouts": [co("$7.4bn called by 2pm, then intraday calls halted", 960, 960, C("By two in the afternoon"), "white", screen=True, size=36, sub="FCA Final Notice", until=C("A board member wrote", -0.3)),
                 co("'Total disarray'", 960, 960, C("Another described"), "risk", screen=True, size=44)]},
    sources=["fca"])
stage("s13_night", "m2_night", {
    "zones": [Z("city", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.0}, {"at": C("But at four forty-nine"), "x": 1100, "y": 460, "zoom": 1.15, "dur": 2.4}], "drift": 2,
    "items": [it("clock", x=500, y=300, at=0.2, period=3.0),
              screen(1100, 430, at=C("Trading reopened"), scale=0.9, price=[[0, 50300], [{"cue": "But at four forty-nine"}, 60000], [{"cue": "For more than three hours", "offset": 3}, 64000]], bandsOffAt=C("they were switched off")),
              it("person", x=1800, pose="read", at=C("run from Hong Kong"), scale=0.75, hair=3, skin=2)],
    "callouts": [co("Overnight, run from Hong Kong", 960, 960, C("Then came the night"), "white", screen=True, size=40, until=C("But at four forty-nine", -0.3)),
                 co("4:49am: price bands switched OFF for 3+ hours", 960, 960, C("But at four forty-nine"), "risk", screen=True, size=38, sub="FCA Final Notice")]},
    sources=["fca"])
stage("s14_peak", "m2_peak", {
    "zones": [Z("city", night=True)], "worldW": 2400, "night": True, "min_seconds": 20,
    "cam": [{"at": 0, "x": 1100, "y": 460, "zoom": 1.15}, {"at": C("In London"), "x": 1300, "y": 480, "zoom": 1.0, "dur": 2.4}], "drift": 1,
    "items": [screen(1100, 430, at=0.2, scale=1.0, price=[[0, 60000], [{"cue": "in under an hour"}, 70000], [{"cue": "from seventy thousand to", "offset": 2.5}, 101365]], bandsOffAt=0.1),
              it("letters", x=1100, y=120, text="+44% IN 24 MINUTES", at=C("Then, in just"), size=56, color="risk"),
              it("device", type="phone", x=2000, y=F, at=C("In London"), scale=1.0),
              it("person", x=2150, pose="worry", at=C("woke up"), scale=0.75, hair=1, skin=1)],
    "callouts": [co("5:44 → 6:08am: $70,000 → $101,365", 960, 960, C("Then, in just"), "risk", screen=True, size=40, sub="FCA Final Notice", until=C("In London", -0.3)),
                 co("Doubled since Monday's close", 960, 960, C("In London"), "gold", screen=True, size=40)]},
    sources=["fca"])
add("p15_morning", "m2_draw", "engine_draw", {
    "title": "The morning of March 8", "board": BOARD, "draw_start": C("Here is the price on Friday"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 560 L 600 380 M 600 560 L 1460 560", "color": "ink", "width": 4, "start": C("Here is the price on Friday")},
        {"d": "M 640 520 L 900 470 L 1200 420 L 1420 330", "color": "risk", "width": 6, "start": C("Here is the price on Friday", 0.4), "label": lbl("PRICE: Mon $48k → Tue $101k", 1030, 360, 22, "risk")},
        {"d": "M 600 860 L 1460 860", "color": "ink", "width": 4, "start": C("Now look at the bars")},
        {"d": "M 700 860 L 700 832 L 820 832 L 820 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.4, "kind": "bar", "start": C("Three and a half billion"), "label": lbl("FRI $3.5bn", 760, 820, 20, "accent")},
        {"d": "M 960 860 L 960 819 L 1080 819 L 1080 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.4, "kind": "bar", "start": C("Five billion on Monday"), "label": lbl("MON $5.1bn", 1020, 805, 20, "accent")},
        {"d": "M 1240 860 L 1240 700 L 1360 700 L 1360 860", "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("almost twenty billion"), "label": lbl("TUE $19.7bn", 1300, 685, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("almost twenty billion", 0.2), "dur": 1.4, "target": [1300, 760]}],
    "scale": 0.86, "floor": 1040}, sources=["fca"])
kinetic("s16_t2", "m2_transition", [("7:30am. The managers meet.", 60, "At seven thirty", None, True), ("Less than an hour to decide", 58, "less than an hour", "risk", False)])

# ====================================================================== PART 3: tearing up the trades
card("s17_c3", "m3_card", "Tearing Up the Trades", "8 March 2022")
stage("s18_q3", "m3_question", {
    "zones": [Z("office")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("docs", x=960, y=580, at=0.3, text="TRADES · 8 MARCH", scale=0.8, stamp="VOID?", stampAt=3.0)],
    "callouts": [co("Can a market erase trades?", 960, 150, C("Can a market"), "gold", screen=True, size=44)]})
stage("s19_calls", "m3_calls", {
    "zones": [Z("vault")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("And when a member defaults"), "x": 1600, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=900, y=220, at=C("That morning's margin calls"), prefix="$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "totalled", "offset": 1}, 19.7]], text="MARGIN CALLS, TUE MORNING"),
              it("vaultdoor", x=900, at=0.3, openAt=C("That morning's margin calls"), scale=0.6),
              it("domino", x=1400, at=C("And when a member defaults"), labels=["A", "B", "C", "D", "E"], fallAt=C("the losses can spread"), step=0.5, gap=180, h=260)],
    "callouts": [co("$19.7bn of calls: defaults likely", 960, 960, C("That morning's margin calls"), "risk", screen=True, size=40, sub="FCA Final Notice", until=C("And when a member defaults", -0.3)),
                 co("One default can spread to everyone", 960, 960, C("And when a member defaults"), "white", screen=True, size=40)]},
    sources=["fca"])
stage("s20_suspend", "m3_suspend", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.0}, {"at": C("The market stayed shut"), "x": 1350, "y": 480, "zoom": 0.9, "dur": 2.4}], "drift": 3,
    "items": [screen(1000, 430, at=0.2, scale=0.9, price=[[0, 48075], [1.0, 101365], [3.0, 80010]], bandsOffAt=0.1, haltAt=C("suspended nickel trading"), cancelAt=C("It cancelled every"), cancelFrom=0.3),
              it("calendar", x=1700, y=300, at=C("The market stayed shut"), pages=[[0, "MAR 8", "SUSPENDED"], [{"cue": "reopened on"}, "MAR 16", "REOPENED"]], scale=0.8),
              it("letters", x=1900, y=620, text="NIGHT TRADING: BACK IN 2023", at=C("Night trading from Asia"), size=40, color="gold")],
    "callouts": [co("8:15am: nickel suspended", 960, 960, C("At eight fifteen"), "risk", screen=True, size=42, sub="FCA Final Notice", until=C("It cancelled every", -0.3)),
                 co("Every trade since midnight cancelled: $13.4bn", 960, 960, C("It cancelled every"), "gold", screen=True, size=38)]},
    sources=["fca"])
stage("s21_rewind", "m3_rewind", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1100, "y": 480, "zoom": 1.05}, {"at": C("And the billions"), "x": 1300, "y": 480, "zoom": 1.0, "dur": 2.4}], "drift": 1,
    "items": [it("clock", x=500, y=300, at=0.2, period=1.0),
              screen(1100, 430, at=0.3, scale=0.9, price=[[0, 48075], [2.0, 101365]], cancelAt=C("was wiped out"), cancelFrom=0.3, haltAt=C("was wiped out")),
              it("coins", **{"from": [1800, 300], "to": [2600, 200]}, at=C("And the billions"), rate=5)],
    "callouts": [co("Cut-off: midnight, not 4:49am", 960, 960, C("The exchange chose midnight"), "white", screen=True, size=40, sub="FCA Final Notice", until=C("Everything traded", -0.3)),
                 co("As if the morning never happened", 960, 960, C("Everything traded"), "gold", screen=True, size=40)]},
    sources=["fca"])
stage("s22_winners", "m3_winners", {
    "zones": [Z("office")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("And a company caught short"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [*crowd([700, 820], "worry", at=C("A trader who had sold"), scale=0.75),
              it("docs", x=800, y=560, at=C("suddenly had no trade"), text="PROFIT", scale=0.5, stamp="CANCELLED", stampAt=C("no trade at all")),
              *crowd([1600, 1720], "cheer", at=C("And a company caught short"), scale=0.75),
              it("letters", x=1700, y=220, text="SAVED · BUT AT WHOSE COST?", at=C("But it also took"), size=44, color="gold")],
    "callouts": [co("Some profits vanished…", 960, 960, C("A trader who had sold"), "risk", screen=True, size=40, until=C("And a company caught short", -0.3)),
                 co("…some losses were avoided", 960, 960, C("And a company caught short"), "white", screen=True, size=40)]},
    sources=["fca"])
kinetic("s23_t3", "m3_transition", [("Some of those people", 64, "Some of those people", None, False), ("went to court", 70, "went to court", "gold", False)])

# ====================================================================== PART 4: the court
card("s24_c4", "m4_card", "The Court", "2023-2024")
stage("s25_q4", "m4_question", {
    "zones": [Z("court")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("gavel", x=960, y=420, hits=[3.5])],
    "callouts": [co("Was it legal to erase the trades?", 960, 150, C("Was it legal"), "gold", screen=True, size=42)]})
stage("s26_claims", "m4_claims", {
    "zones": [Z("court")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("They argued"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("stack", x=800, h=[[0, 40], [{"cue": "in profits", "offset": 1}, 360]], at=C("The American hedge fund"), text="ELLIOTT ≈ $456M", sub="claimed lost profit", color="#C62828"),
              it("stack", x=1100, h=[[0, 40], [{"cue": "put its loss at", "offset": 1.5}, 60]], at=C("The trading firm"), text="JANE STREET ≈ $15M", sub="claimed"),
              it("docs", x=1700, y=560, at=C("They argued"), text="CLAIM: NOT DISORDERLY · UNLAWFUL", scale=0.6)],
    "callouts": [co("Claimed losses: ≈ $456M and ≈ $15M", 960, 960, C("The American hedge fund"), "white", screen=True, size=38, sub="High Court judgment", until=C("They argued", -0.3)),
                 co("Their case: a squeeze, not disorder", 960, 960, C("They argued"), "gold", screen=True, size=40)]},
    sources=["highcourt"])
stage("s27_rulings", "m4_rulings", {
    "zones": [Z("court")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("In October"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "NOV", "2023"], [{"cue": "In October"}, "OCT", "2024"]], scale=0.8),
              it("gavel", x=1000, y=420, hits=[C("dismissed the case", 0.2), C("upheld that decision", 0.2)]),
              it("docs", x=1700, y=560, at=C("The cancellation, the courts found"), text="CANCELLATION", scale=0.6, stamp="LAWFUL", stampAt=C("had been lawful"))],
    "callouts": [co("High Court: claim dismissed (Nov 2023)", 960, 960, C("In November"), "white", screen=True, size=40, sub="High Court judgment", until=C("In October", -0.3)),
                 co("Court of Appeal: upheld (Oct 2024)", 960, 960, C("In October"), "gold", screen=True, size=40, sub="Freshfields")]},
    sources=["highcourt", "freshfields"])
add("p28_dilemma", "m4_draw", "engine_draw", {
    "title": "The exchange's dilemma", "board": BOARD, "draw_start": C("Option one"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 280, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Option one"), "label": lbl("1 · TRADES STAND", 700, 428, 22, "accent2")},
        {"d": rect(1180, 360, 280, 120), "color": "accent", "width": 6, "kind": "box", "start": C("Option two"), "label": lbl("2 · CANCEL", 1320, 428, 24, "accent")},
        {"d": rect(560, 650, 280, 120), "color": "risk", "width": 6, "kind": "box", "start": C("several members might default"), "label": lbl("DEFAULTS SPREAD", 700, 718, 22, "risk")},
        {"d": rect(1180, 650, 280, 120), "color": "risk", "width": 6, "kind": "box", "start": C("some traders lose money"), "label": lbl("FAIR PROFITS LOST", 1320, 718, 20, "risk")},
        {"d": arrow((700, 490), (700, 640), 0.0), "color": "ink", "width": 5, "start": C("Then several members")},
        {"d": arrow((1320, 490), (1320, 640), 0.0), "color": "ink", "width": 5, "start": C("The system survives")},
        {"d": "M 1160 640 L 1480 640 L 1480 780 L 1160 780 Z", "color": "accent3", "width": 4, "kind": "box", "start": C("The exchange chose"), "label": lbl("CHOSEN", 1320, 810, 22, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("The exchange chose", 0.2), "dur": 1.4, "target": [1320, 710]}],
    "scale": 0.86, "floor": 1040}, sources=["fca", "highcourt"])
kinetic("s29_t4", "m4_transition", [("The decision was lawful", 60, "the decision was lawful", None, False), ("But how did it get that far?", 58, "How did it get that far", "gold", False)])

# ====================================================================== PART 5: the verdict
card("s30_c5", "m5_card", "The Verdict", "March 2025")
stage("s31_q5", "m5_question", {
    "zones": [Z("parliament")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("magnifier", x=[[0, 700], [8, 1250]], y=[[0, 500], [8, 460]], at=0.3, scale=0.9)],
    "callouts": [co("Who was responsible for the chaos?", 960, 150, C("Who was responsible"), "gold", screen=True, size=42)]})
stage("s32_fca", "m5_fca", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It found"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "MAR 19", "2025"]], scale=0.8),
              it("docs", x=1100, y=560, at=C("fined the London Metal Exchange"), text="FCA FINAL NOTICE", scale=0.6, stamp="≈ $12M FINE", stampAt=C("fined the London Metal Exchange", 1.5)),
              it("board", x=1800, y=380, at=C("It found"), text="NOT PREPARED", rows=[{"name": "POLICIES"}, {"name": "CONTROLS"}, {"name": "TRAINING", "color": "risk"}])],
    "callouts": [co("FCA fine ≈ $12M (H.10, Mar 2025)", 960, 960, C("In March"), "risk", screen=True, size=40, sub="FCA Final Notice", until=C("It found", -0.3)),
                 co("Not prepared for extreme volatility", 960, 960, C("It found"), "white", screen=True, size=40)]},
    sources=["fca", "fred_gbp"])
stage("s33_philosophy", "m5_philosophy", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.0}, {"at": C("Its price bands"), "x": 1300, "y": 480, "zoom": 1.05, "dur": 2.4}], "drift": 2,
    "items": [it("paper", x=900, y=380, at=C("The prevailing philosophy"), text="'should not be restricted even in times of extreme volatility'", name="FCA", scale=0.65),
              screen(1500, 430, at=C("Its price bands"), scale=0.75, price=[[0, 48075], [3, 50000], [{"cue": "Not a real squeeze", "offset": 2}, 101365]], bandsOffAt=C("Not a real squeeze"))],
    "callouts": [co("Philosophy: don't restrict trading", 960, 960, C("The prevailing philosophy"), "white", screen=True, size=40, sub="FCA Final Notice", until=C("Its price bands", -0.3)),
                 co("Bands built for fat fingers, not squeezes", 960, 960, C("Its price bands"), "gold", screen=True, size=38)]},
    sources=["fca"])
stage("s34_failures", "m5_failures", {
    "zones": [Z("city", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.0}, {"at": C("And it could not see"), "x": 1400, "y": 480, "zoom": 1.05, "dur": 2.4}], "drift": 2,
    "items": [it("person", x=900, pose="read", at=0.3, scale=0.8, hair=3, skin=2),
              it("docs", x=1300, y=560, at=C("switched off the price bands"), text="ESCALATION", scale=0.55, stamp="NEVER TRAINED", stampAt=C("never been trained")),
              it("contract", x=1900, y=430, at=C("And it could not see"), text="OTC POSITIONS", sub="'a material cause'", scale=0.6)],
    "callouts": [co("Night team: bands off, no escalation", 960, 960, C("Its overnight team"), "white", screen=True, size=40, sub="FCA Final Notice", until=C("And it could not see", -0.3)),
                 co("Blind to the positions that drove the rise", 960, 960, C("And it could not see"), "risk", screen=True, size=38)]},
    sources=["fca"])

# ====================================================================== PAYOFF
stage("s35_payoff", "payoff", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 460, "zoom": 1.05}, {"at": C("The exchange saved itself"), "x": 1200, "y": 480, "zoom": 1.0, "dur": 2.6}], "drift": 1,
    "items": [screen(1000, 430, at=0.2, scale=1.0, price=[[0, 28961], [6, 101365]], bandsOffAt=3.0, haltAt=C("The exchange saved itself"), cancelAt=C("by rewriting the morning"), cancelFrom=2.0),
              it("letters", x=1000, y=110, text="THE RULES CAN CHANGE MID-GAME", at=C("But it also showed"), size=44, color="gold")],
    "callouts": [co("A price is only as real as the system behind it", 960, 960, C("That a price is only"), "white", screen=True, size=36, until=C("The exchange saved itself", -0.3)),
                 co("Hidden bets + no brakes = a broken market", 960, 960, C("The exchange saved itself"), "risk", screen=True, size=38)]},
    sources=["fca"])
add("s36_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_nickel_storyboard.py; edit the generator, not this file.\n"
           "# Episode 25 storyboard (LME nickel 2022): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
