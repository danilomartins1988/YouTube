"""Generates projects/who-actually-owns-americas-debt/deliverables/documentary/storyboard.yaml
(Episode 59: Who Actually Owns America's $40 Trillion in Debt?).

OWNER DIRECTION: as animated as possible, like a prime-time TV cartoon sitcom (genre level only; everything original).
NEUTRALITY (owner, "Sem viés político"): no party, president or administration named, blamed or credited; no politicians
drawn; no editorial adjectives; the film reports, it does not judge.
TV structure: cold open in the IOU vault -> channel intro (our "theme") -> show TITLE CARD with a typed joke subtitle -> five
acts, each opened by a BUMPER (rubber-stamped IOU card, rotating joke caption) -> payoff -> end card -> button joke.
Recurring cast: OWEN (a living IOU note, `owen` item in CartoonStage/debt.tsx: the running gag, he grows every act: $38T ->
$39T -> $40T -> $40.6T -> "+ INTEREST" and finally can't fit through the door), TED (taxpayer), RUTH (retiree), the
AUCTIONEER; dinner guests labelled by place cards only. Bespoke sets (debt.tsx): iouvault, auctionhouse, dinnerparty (+ feast),
mainstreet, fedwarehouse, trustcabinet, meterscale, debttitle, debtbumper.
Signature animations: the vault door + debt odometer (s01), the auction paddles and SOLD! (s09), the dinner plates
(s14), the Fed warehouse shelves thinning out (s27), the trust-fund drawer emptying through the tube (s31), the interest
meter outweighing the defense scale (s37). Presenter boards: p06 (boxes), p17 (bars + area), p25 (loop), p33 (round trip),
p40 (bars). No logos, no flags, no real people; jokes never change a number. Run: python tools/gen_debt_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/who-actually-owns-americas-debt/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
NAVY = "#2E4A66"


def toon(who, x, at=0.0, **kw):
    if "xk" in kw:
        x = kw.pop("xk")
    return it("toon", who=who, x=x, at=at, **kw)


def TED(x=None, at=0.0, **kw):
    """TED, an original worried taxpayer: glasses, green sweater."""
    kw.setdefault("scale", 1.35)
    return toon("shopper", x, at, v=3, glasses=True, color="#3E8E5E", hat="", scarf="", hair=0, hairStyle=1, **kw)


def RUTH(x=None, at=0.0, **kw):
    """RUTH, an original retiree: grey curls, purple cardigan."""
    kw.setdefault("scale", 1.3)
    return toon("shopper", x, at, v=6, color="#7E57C2", hat="", scarf="", hair=6, hairStyle=3, glasses=True, **kw)


def AUCT(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.3)
    return toon("shopper", x, at, v=8, color=NAVY, hat="", scarf="#F2B63A", hair=1, hairStyle=2, glasses=False, **kw)


def GUEST(v, x, **kw):
    kw.setdefault("scale", 1.15)
    return toon("shopper", x, kw.pop("at", 0.1), v=v, color=NAVY, hat="", scarf="#F2B63A", y=830, pose="sit", **kw)


def OWEN(x, at=0.0, **kw):
    return it("owen", x=x, at=at, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def chart(bars_, at=0.2, **kw):
    kw.setdefault("panel", True)
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


def bumper(id_, seg, num, title, caption, color, amount, owen_scale, face="sweat"):
    items = [OWEN([[0.7, -300], [3.7, 2300]], 0.7, y=1050, scale=owen_scale, amount=amount, face=face),
             TED(xk=[[1.2, -400], [4.0, 1900]], at=1.2, y=1060, scale=0.8, face="panic", pose="run")]
    stage(id_, seg, {**W1("debtbumper", num=num, act="ACT", title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "sitcom",
                     "min_seconds": 4.0, "items": items}, sfx=[{"kind": "hit", "at": 0.55, "gain": 0.35}, {"kind": "whoosh", "at": 0.05, "gain": 0.25}])


# ====================================================================== COLD OPEN (the IOU vault)
stage("s01_open", "co_open", {
    **W1("iouvault", openAt=C("It's so long"), odo=[[0, 40.5], [C("added at the bottom"), 40.6]], doorX=760, pressX=2050),
    "cam": cam((0, 1200, 300, 1.15), (C("It's signed"), 900, 480, 1.05, 1.6), (C("It's so long"), 800, 520, 0.95, 1.4),
               (C("And every single day"), 1550, 560, 1.05, 1.6), (C("added at the bottom"), 1700, 600, 1.3, WHIP)), "drift": 3,
    "items": [it("toonwords", text="THE BIGGEST IOU ON EARTH", x=1200, y=330, at=0.2, until=C("It's signed", 0.6), size=70),
              OWEN([[0, 1300], [C("It's so long"), 1300], [C("It's so long", 1.6), 760]], C("It's signed", -0.2), amount="$40.6T", face="happy",
                   faces=[[0, "happy"], [C("nobody has ever read"), "smug"], [C("added at the bottom"), "shock"]], label="OWEN · THE IOU",
                   labelUntil=C("And every single day"), scale=1.1),
              TED(380, 0.4, face="worry", label="TED · TAXPAYER", labelUntil=C("It's so long"), faces=[[0, "worry"], [C("nobody has ever read"), "shock"]],
                  takes=[C("nobody has ever read")], hold="clipboard"),
              it("ioustack", x=1500, at=C("And every single day"), rate=7, n=14, label="+ A FEW BILLION A DAY", scale=0.9),
              sign("ILLUSTRATION · FIGURES FOLLOW", 1200, 1000, C("And every single day"), color="#FFF8E1", size=24)]},
    sfx=[{"kind": "whoosh", "cue": "It's so long", "gain": 0.3}])
stage("s02_hook", "co_hook", {
    **W1("iouvault", open=1, odo=[[0, 38.2], [C("Debt to the Penny"), 38.2], [C("stood at"), 40.6]], odoLabel="DEBT TO THE PENNY · NOV 13, 2026", doorX=760, pressX=2050),
    "cam": cam((0, 1200, 260, 1.25), (C("So who actually holds"), 1000, 470, 0.95, 1.6), (C("Most people would guess"), 1250, 520, 1.1, 1.4), (C("Most people would be wrong"), 1250, 500, 1.35, WHIP)), "drift": 3,
    "items": [OWEN(1250, 0.2, amount="$40.6T", face="grin", faces=[[0, "grin"], [C("Most people would be wrong"), "smug"]], scale=1.1, hops=[C("stood at", 0.8)]),
              TED(600, 0.3, face="shock", faces=[[0, "shock"], [C("Most people would guess"), "worry"], [C("Most people would be wrong"), "shock"]], takes=[C("stood at", 0.4)]),
              it("bubble", text="CHINA?", x=800, y=320, at=C("Most people would guess", 0.3), until=C("Most people would be wrong", -0.1), tail=[640, 520], size=44),
              it("toonwords", text="WRONG!", x=1250, y=260, at=C("Most people would be wrong", 0.6), size=120, color="#D93A49")]},
    sources=["dtp"], sfx=[{"kind": "hit", "cue": "Most people would be wrong", "gain": 0.3}])
stage("s03_promise", "co_promise", {
    **W1("iouvault", open=1, odo=[[0, 40.6]], doorX=760, pressX=2050),
    "cam": cam((0, 900, 520, 1.0), (C("the dinner guests"), 1200, 520, 1.0, 1.2), (C("Then we'll check"), 1450, 520, 1.05, 1.2)), "drift": 6,
    "items": [it("toonwords", text="FOLLOW THE IOU", x=1200, y=330, at=0.2, size=70, until=C("We'll meet", -0.1)),
              sign("1 · THE BUYERS", 520, 420, C("the buyers"), color="#BBDEFB", size=30),
              sign("2 · THE DINNER GUESTS", 900, 300, C("the dinner guests"), color="#FFE0B2", size=30),
              sign("3 · THE WAREHOUSE", 1350, 420, C("the warehouse"), color="#C8E6C9", size=30),
              sign("4 · THE FILING CABINET", 1700, 300, C("the filing cabinet"), color="#E1BEE7", size=30),
              sign("5 · THE METER", 2000, 470, C("check the meter"), color="#FFCDD2", size=30),
              OWEN([[0, 300], [C("Then we'll check"), 1100]], 0.1, amount="$40.6T", face="happy", scale=0.9),
              TED(1900, 0.2, face="happy", pose="talk", talk=[[0.3, C("Social Security's IOUs")]])]})
stage("s04_title", "title_card", {
    **W1("debttitle", title="WHO OWNS THE DEBT?", sub="A HIDDEN ECONOMICS EPISODE", subs=[[2.2, "Tonight: “Some Assembly, and Interest, Required”"]]),
    "cam": STILL(), "drift": 0, "min_seconds": 6.0,
    "items": [TED(250, 2.4, scale=1.15, face="shock", hops=[2.8, 4.4], pose="armsup"),
              OWEN(1690, 2.6, scale=0.85, amount="$40.6T", face="grin", wave=True, hops=[3.2])]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}, {"kind": "hit", "at": 1.6, "gain": 0.25}])

# ====================================================================== ACT 1: the IOU
bumper("s05_b1", "a1_card", "1", "THE IOU", "Signed, sealed, rolled over", "#2E9E6B", "$38T", 0.7, face="happy")
stage("s06_split", "a1_split", {
    **W1("iouvault", open=1, odo=[[0, 40.6]], odoLabel="TOTAL · NOV 13, 2026", doorX=600, pressX=2150),
    "cam": cam((0, 1200, 420, 0.95), (C("It comes in two pieces"), 1200, 480, 0.9, 1.4), (C("The other"), 1350, 480, 0.95, 1.4)), "drift": 4,
    "items": [it("toonwords", text="WHAT IS THE DEBT?", x=1200, y=330, at=0.2, until=C("It comes in two pieces"), size=70),
              sign("EVERY TREASURY SECURITY NOT YET PAID BACK", 1200, 330, C("It's every Treasury security"), color="#FFF8E1", size=28, until=C("It comes in two pieces", 0.5)),
              it("pie", x=1200, y=560, r=200, at=C("It comes in two pieces"), total=40.6,
                 slices=[{"v": 32.8, "color": "#2E6BD1", "label": "PUBLIC\n$32.8T", "at": C("is debt held by the public", -1.5)},
                         {"v": 7.8, "color": "#F2B63A", "label": "GOV'T\n$7.8T", "at": C("The other")}], title="DEBT TO THE PENNY · NOV 13, 2026"),
              sign("BILLS · NOTES · BONDS", 520, 420, C("Bills, notes and bonds"), color="#BBDEFB", size=30),
              sign("OWED TO ITS OWN TRUST FUNDS", 1880, 420, C("to its own trust funds", -0.6), color="#FFE0B2", size=28),
              TED(300, 0.3, face="worry", faces=[[0, "worry"], [C("The other"), "shock"]], takes=[C("owes to itself")])]},
    sources=["dtp"])
add("p07_boxes", "a1_draw", "engine_draw", {
    "title": "The IOU in two boxes (Nov 13, 2026)", "board": BOARD, "draw_start": C("Here's the whole IOU"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 380, 920, 110), "color": "ink", "width": 6, "kind": "box", "start": C("Here's the whole IOU"), "label": lbl("TOTAL · $40.6T", 1020, 445, 34, "ink")},
        {"d": arrow((900, 500), (800, 580), 0.1), "color": "muted", "width": 5, "kind": "arrow", "start": C("Now split it")},
        {"d": arrow((1150, 500), (1290, 580), -0.1), "color": "muted", "width": 5, "kind": "arrow", "start": C("Now split it", 0.4)},
        {"d": rect(560, 590, 560, 220), "color": "accent2", "width": 7, "kind": "box", "start": C("The big box"), "label": lbl("HELD BY THE PUBLIC · $32.8T", 840, 660, 28, "accent2")},
        {"d": dot(840, 720), "color": "ink", "width": 1, "start": C("anyone outside"), "label": lbl("ANYONE OUTSIDE THE FEDERAL GOV'T", 840, 720, 20, "ink")},
        {"d": dot(840, 770), "color": "risk", "width": 1, "start": C("includes the Federal Reserve"), "label": lbl("(INCLUDING THE FED)", 840, 770, 22, "risk")},
        {"d": rect(1180, 590, 300, 220), "color": "accent", "width": 7, "kind": "box", "start": C("The smaller box"), "label": lbl("INTRAGOV'T · $7.8T", 1330, 660, 24, "accent")},
        {"d": dot(1330, 730), "color": "accent3", "width": 1, "start": C("Social Security's trust"), "label": lbl("≈ 1/3: SOCIAL SECURITY", 1330, 730, 20, "accent3")},
        {"d": dot(1330, 770), "color": "muted", "width": 1, "start": C("by our calculation"), "label": lbl("OUR CALC. (END-2025)", 1330, 770, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Hold on to that box", 0.1), "dur": 1.6, "target": [1330, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["dtp", "crs_ss"])
stage("s08_speed", "a1_speed", {
    **W1("iouvault", open=1, odo=[[0, 38.2], [C("That's about"), 38.2], [C("in twelve months"), 40.6]], odoLabel="ONE YEAR: NOV 2025 → NOV 2026", doorX=600, pressX=2150, pressRate=0.9),
    "cam": cam((0, 1200, 260, 1.2), (C("That's about"), 1200, 300, 1.1, 1.0), (C("or roughly"), 1700, 520, 1.0, 1.6), (C("The counter passed"), 1200, 500, 0.9, 1.4)), "drift": 4,
    "items": [it("counter", x=1700, y=400, at=C("or roughly"), prefix="$", suffix="BN / DAY", decimals=1, steps=[[0, 0], [C("or roughly"), 0], [C("a day"), 6.8]], text="AVERAGE, OUR CALCULATION", until=C("The counter passed")),
              it("calendar", x=450, y=360, at=C("The counter passed"), pages=[[C("The counter passed"), "$38T", "OCT 2025"], [C("thirty-nine trillion"), "$39T", "MAR 2026"], [C("and forty trillion"), "$40T", "AUG 18, 2026"]], scale=0.85),
              OWEN([[0, 900], [C("The counter passed"), 1000]], 0.2, amount="$38.2T", amounts=[[0, "$38.2T"], [C("in twelve months"), "$40.6T"]],
                   grow=[[0, 0.8], [C("That's about"), 0.8], [C("in twelve months"), 1.1]], face="shock", faces=[[0, "worry"], [C("That's about"), "shock"], [C("The counter passed"), "sweat"]]),
              TED(1950, 0.3, face="shock", hold="clipboard", takes=[C("in twelve months")])]},
    sources=["dtp"])
stage("s09_auction", "a1_auction", {
    **W1("auctionhouse", bidsAt=C("An auction"), soldAt=C("by our count", -0.3), board={"title": "FISCAL YEAR 2026 · ALL AUCTIONS", "rows": [[C("the Treasury held"), "436 AUCTIONS"], [C("and sold"), "≈ $32.9T SOLD (OUR SUM)"], [C("Most of that"), "MOSTLY SHORT-TERM BILLS"]]}),
    "cam": cam((0, 1200, 560, 0.9), (C("An auction"), 1200, 620, 1.0, WHIP), (C("In fiscal year"), 1200, 380, 1.1, 1.6), (C("Most of that"), 1200, 520, 0.95, 1.4)), "drift": 4,
    "items": [it("toonwords", text="WHERE DOES NEW DEBT COME FROM?", x=1200, y=40, at=0.2, until=C("An auction"), size=56),
              AUCT(880, 0.2, pose="talk", face="grin", label="THE AUCTIONEER", labelUntil=C("In fiscal year"), talk=[[C("An auction"), C("by our count")]], scale=1.25),
              it("gavel", x=1240, y=585, at=0.2, scale=0.8, hits=[C("An auction", 0.3), C("by our count", -0.3)]),
              it("feeflow", **{"from": [1200, 900], "to": [2000, 300]}, at=C("paid off and sold again"), n=8, sym="↻", color="#FFE27A")]},
    sources=["auct"], sfx=[{"kind": "hit", "cue": "An auction", "gain": 0.3}])
stage("s10_bidders", "a1_bidders", {
    **W1("auctionhouse", bidsAt=C("bids came in"), soldAt=C("Big dealer banks", 0.8), soldText="WON!", board={"title": "10-YEAR NOTE · AUG 12, 2026", "rows": [[C("the Treasury auctioned"), "OFFERED: $42BN"], [C("more than twice"), "BIDS: 2.53x (BID-TO-COVER)"], [C("indirect bidders"), "INDIRECT ≈ 77% (OUR CALC.)"], [C("Direct bidders"), "DIRECT ≈ 15% · DEALERS ≈ 9%"]]}),
    "cam": cam((0, 1200, 380, 1.1), (C("bids came in"), 1200, 650, 0.95, 1.4), (C("indirect bidders"), 1200, 380, 1.1, 1.4), (C("That group"), 900, 700, 1.15, 1.2), (C("Big dealer banks"), 1200, 520, 0.95, 1.2)), "drift": 4,
    "items": [sign("INDIRECT: BIDS VIA A DEALER (INCL. FOREIGN CENTRAL BANKS)", 800, 860, C("That group"), color="#BBDEFB", size=26, until=C("Big dealer banks", 0.5)),
              AUCT(880, 0.2, pose="point", face="happy", scale=1.25, faces=[[0, "happy"], [C("more than twice"), "grin"]]),
              it("gavel", x=1240, y=585, at=0.2, scale=0.8, hits=[C("Big dealer banks", 0.8)])]},
    sources=["auct"])
stage("s11_bills", "a1_bills", {
    **W1("auctionhouse", board={"title": "MARKETABLE DEBT HELD BY THE PUBLIC · OCT 31", "rows": [[C("Treasury bills"), "BILLS: $7.38T OF $32.13T"], [C("made up"), "≈ 23% (OUR CALC.)"], [C("Short paper"), "SHORT PAPER = QUICK REFI"]]}, bidsAt=C("Short paper")),
    "cam": cam((0, 1200, 380, 1.05), (C("Short paper"), 1200, 520, 0.9, 1.6)), "drift": 4,
    "items": [it("pie", x=500, y=560, r=170, at=C("Treasury bills"), total=32.13,
                 slices=[{"v": 7.38, "color": "#F2B63A", "label": "BILLS\n23%", "at": C("made up")}, {"v": 24.75, "color": "#2E6BD1", "label": "NOTES,\nBONDS…", "at": C("made up", 0.6)}], title="MSPD · OCT 31, 2026"),
              TED(1950, 0.3, face="worry", hold="clipboard", faces=[[0, "worry"], [C("Remember that"), "shock"]], takes=[C("Remember that")]),
              it("toonwords", text="REMEMBER THIS!", x=1950, y=380, at=C("Remember that"), size=48, color="#D93A49")]},
    sources=["mspd"])
stage("s12_turn", "a1_turn", {
    **W1("auctionhouse", bidsAt=0.1, soldAt=C("who ends up", -0.2), soldText="SOLD!"),
    "cam": cam((0, 1200, 540, 0.9), (C("who ends up"), 1600, 400, 1.2, WHIP)), "drift": 3,
    "items": [OWEN([[0, -200], [C("who ends up"), 1900]], 0.1, amount="$40.6T", face="worry", scale=0.9),
              it("toonwords", text="WHO HOLDS IT?", x=1200, y=200, at=C("who ends up"), size=90)]})

# ====================================================================== ACT 2: the dinner party (foreign holders)
bumper("s13_b2", "a2_card", "2", "THE DINNER PARTY", "Seating chart by custodian", "#2E6BD1", "$39T", 0.85)
GUESTS = [("JAPAN", 1068.3, "$1.07T"), ("UK", 1009.5, "$1.01T"), ("CHINA", 590.7, "$591BN"), ("BELGIUM", 490.5, "$491BN"), ("CANADA", 464.6, "$465BN"), ("CAYMAN IS.", 463.0, "$463BN")]
GX = [300 + k * 360 for k in range(6)]


def table(at_list, shrink=None, at=0.1):
    g = [{"x": GX[k], "label": l, "value": v, "display": d, "at": at_list[k]} for k, (l, v, d) in enumerate(GUESTS)]
    f = {"x0": 80, "x1": 2320, "at": at, "vmax": 1400, "guests": g, "candles": [120, 2280]}
    if shrink:
        f["shrink"] = shrink
    return it("feast", **f)


def diners(faces=None):
    faces = faces or {}
    return [GUEST(k * 2 + 1, GX[k], face=faces.get(k, "happy")) for k in range(6)]


stage("s14_table", "a2_table", {
    **W1("dinnerparty", chart="LATEST: AUGUST 2026\nTIC DATA · BY CUSTODY"),
    "cam": cam((0, 1200, 300, 0.85), (C("foreigners held"), 1200, 420, 0.85, 1.4), (C("The biggest plate"), 1200, 560, 0.95, 1.4), (C("It's Japan's"), 400, 600, 1.35, WHIP), (C("Second, the United Kingdom"), 700, 600, 1.25, 1.0)), "drift": 4,
    "items": [it("toonwords", text="THE HOLDERS' DINNER PARTY", x=1200, y=120, at=0.2, until=C("foreigners held"), size=64),
              it("counter", x=1200, y=140, at=C("foreigners held"), prefix="$", suffix="T", decimals=2, steps=[[0, 0], [C("foreigners held"), 0], [C("of Treasury securities"), 9.33]], text="FOREIGN HOLDINGS · AUG 2026 (TIC)", until=C("The biggest plate", 0.5)),
              *diners({0: "grin", 1: "happy", 2: "worry"}),
              table([C("It's Japan's"), C("Second, the United Kingdom"), C("The biggest plate", 0.3), 2.6, 3.0, 3.4]),
              it("bubble", text="NOT CHINA?!", x=1100, y=260, at=C("isn't China's"), until=C("It's Japan's", 0.3), tail=[1020, 420], size=40)]},
    sources=["tic"])
stage("s15_china", "a2_china", {
    **W1("dinnerparty", chart="CHINA, MAINLAND\nNOV 2013: $1,316.7BN"),
    "cam": cam((0, 1020, 560, 1.25), (C("its plate has been shrinking"), 1020, 540, 1.4, 1.4), (C("Back in"), 1500, 420, 0.9, 1.4), (C("Today"), 1020, 560, 1.3, 1.2)), "drift": 3,
    "items": [*diners({2: "worry"}),
              table([0.1, 0.1, 0.1, 0.1, 0.1, 0.1], shrink={"idx": 2, "at": C("its plate has been shrinking"), "to": 590.7}),
              it("counter", x=1500, y=150, at=C("Back in"), prefix="$", suffix="T", decimals=2, steps=[[0, 1.32], [C("Today"), 1.32], [C("less than half", 0.3), 0.59]], text="CHINA · NOV 2013 → AUG 2026 (TIC)"),
              it("toonwords", text="LESS THAN HALF", x=1020, y=260, at=C("less than half"), size=72, color="#D93A49")]},
    sources=["tichist", "tic"])
stage("s16_share", "a2_share", {
    **W1("dinnerparty", chart="SHARE OF TOTAL DEBT\nOUR CALC · AUG 31, 2026"),
    "cam": cam((0, 1200, 360, 0.85), (C("China's holdings are"), 1200, 360, 0.9, 1.4), (C("All foreign holders"), 1200, 400, 0.85, 1.2), (C("The idea that China"), 1200, 520, 1.0, 1.4)), "drift": 3,
    "items": [*diners(),
              table([0.1] * 6),
              it("counter", x=700, y=150, at=C("China's holdings are"), suffix="%", decimals=1, steps=[[0, 0], [C("China's holdings are"), 0], [C("of the total debt"), 1.5]], text="CHINA · OUR CALC."),
              sign("≈ 1.5¢ OF EVERY $1", 700, 330, C("About a penny"), color="#FFF59D", size=34),
              it("counter", x=1700, y=150, at=C("All foreign holders"), suffix="%", decimals=0, steps=[[0, 0], [C("All foreign holders"), 0], [C("about twenty-three percent"), 23]], text="ALL FOREIGN · OUR CALC."),
              it("toonwords", text="MYTH: “CHINA OWNS AMERICA”", x=1200, y=470, at=C("The idea that China"), size=56, color="#FFFFFF"),
              it("toonwords", text="NOT WHAT THE DATA SHOW", x=1200, y=560, at=C("isn't what the data show"), size=56, color="#D93A49")]},
    sources=["tic", "dtp"])
add("p17_scale", "a2_draw", "engine_draw", {
    "title": "Holdings to scale (TIC; total debt Aug 31, 2026)", "board": BOARD, "draw_start": C("Let me chart it"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 820 L 1000 820", "color": "ink", "width": 5, "start": C("Let me chart it")},
        {"d": "M 590 820 L 590 460 L 690 460 L 690 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("China in twenty thirteen"), "label": lbl("CHINA 2013 · $1.32T", 640, 440, 20, "risk")},
        {"d": "M 730 820 L 730 659 L 830 659 L 830 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.15, "kind": "bar", "start": C("China today"), "label": lbl("CHINA NOW · $591BN", 780, 640, 20, "risk")},
        {"d": "M 870 820 L 870 528 L 970 528 L 970 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Japan today"), "label": lbl("JAPAN · $1.07T", 920, 508, 20, "accent2")},
        {"d": rect(1080, 380, 440, 440), "color": "ink", "width": 6, "kind": "box", "start": C("the whole debt"), "label": lbl("TOTAL DEBT · $40.2T", 1300, 420, 28, "ink")},
        {"d": rect(1080, 740, 80, 80), "color": "risk", "width": 3, "kind": "box", "start": C("All three bars fit"), "label": lbl("", 1120, 780, 10, "risk")},
        {"d": rect(1160, 767, 53, 53), "color": "risk", "width": 3, "kind": "box", "start": C("All three bars fit", 0.3)},
        {"d": rect(1213, 748, 72, 72), "color": "accent2", "width": 3, "kind": "box", "start": C("All three bars fit", 0.6)},
        {"d": dot(1300, 600), "color": "muted", "width": 1, "start": C("in one corner"), "label": lbl("SAME SCALE, BY AREA", 1300, 600, 22, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("in one corner", 0.1), "dur": 1.4, "target": [1180, 780]}],
    "scale": 0.86, "floor": 1040}, sources=["tic", "tichist", "dtp"])
stage("s18_custody", "a2_custody", {
    **W1("dinnerparty", chart="TREASURY NOTE:\nCUSTODY ≠ OWNER"),
    "cam": cam((0, 2000, 480, 1.0), (C("Bonds kept in places"), 1500, 560, 1.0, 1.6), (C("So the guest list"), 1200, 420, 0.85, 1.4)), "drift": 3,
    "items": [*diners({3: "smug", 4: "smug", 5: "smug"}),
              table([0.1] * 6),
              it("docs", x=2150, y=860, at=C("One caveat"), text="TIC TABLE 5 · NOTES", scale=0.7, stamp="CUSTODY", stampAt=C("held in custody")),
              sign("BELGIUM · LUXEMBOURG · CAYMAN IS.: CUSTODY CENTERS", 1500, 140, C("Bonds kept in places"), color="#FFF8E1", size=26),
              it("toonwords", text="A GOOD MAP, NOT A PERFECT ONE", x=1200, y=260, at=C("So the guest list"), size=54)]},
    sources=["tic"])
stage("s19_official", "a2_official", {
    **W1("dinnerparty", chart="OFFICIAL HOLDERS\nAUG 2026: $3.76T"),
    "cam": cam((0, 1200, 400, 0.85), (C("When a country needs"), 1300, 560, 1.15, 1.6)), "drift": 4,
    "items": [*diners(),
              table([0.1] * 6),
              it("counter", x=1200, y=140, at=0.3, prefix="$", suffix="T", decimals=1, steps=[[0, 0], [0.3, 0], [C("of the foreign total"), 3.8]], text="FOREIGN OFFICIAL HOLDERS · AUG 2026 (TIC)"),
              sign("MOSTLY CENTRAL BANKS · RESERVES", 1200, 330, C("mostly central banks"), color="#BBDEFB", size=30),
              it("bondpop", x=1900, y=380, at=C("safe dollars"), text="SAFE DOLLARS", sub="THE PANTRY", scale=0.9)]},
    sources=["tic"])

# ====================================================================== ACT 3: made in America
bumper("s20_b3", "a3_card", "3", "MADE IN AMERICA", "Your retirement plan says hi", "#D93A49", "$40T", 1.0)
SHOPS = [["MONEY MARKET FUND", "#4FB3F6"], ["HOUSEHOLDS", "#FFB74D"], ["MUTUAL FUND / ETF", "#9575CD"], ["BANK", "#7BD389"], ["CITY HALL", "#E0E0E0"], ["PENSION FUND", "#F06292"], ["INSURANCE CO.", "#4DB6AC"]]
SX = [1200 - 3 * 420 + k * 420 for k in range(7)]
stage("s21_home", "a3_home", {
    **W1("mainstreet", shops=SHOPS, pops=[C("Mostly, Americans")] * 7),
    "cam": cam((0, 1200, 300, 0.7), (C("Mostly, Americans"), 1200, 480, 0.75, 1.4), (C("Here's the Federal Reserve's"), 1200, 520, 0.8, 1.6)), "drift": 4,
    "items": [it("toonwords", text="≈ 3/4 NOT FOREIGN", x=1200, y=120, at=0.3, until=C("Mostly, Americans"), size=72),
              it("toonwords", text="MOSTLY, AMERICANS", x=1200, y=120, at=C("Mostly, Americans"), size=80, color="#FFE27A"),
              sign("FED Z.1 · END OF JUNE 2026 · MARKET VALUE", 1200, 300, C("Here's the Federal Reserve's"), color="#FFF8E1", size=28),
              TED([[0, 200], [C("Here's the Federal Reserve's"), 900]], 0.2, face="happy", y=900, hops=[C("Mostly, Americans", 0.3)]),
              RUTH([[0, 2300], [C("Here's the Federal Reserve's"), 1600]], 0.4, face="happy", y=900)]},
    sources=["z1"])
stage("s22_mmf", "a3_mmf", {
    **W1("mainstreet", shops=SHOPS, pops=[0.1] * 7),
    "cam": cam((0, SX[0], 560, 1.1), (C("Households held"), SX[1], 560, 1.1, 1.2), (C("Mutual funds"), SX[2], 560, 1.1, 1.2)), "drift": 3,
    "items": [sign("$3.28T", SX[0], 230, C("Money market funds held"), color="#FFF59D", size=48, sub="MONEY MARKET FUNDS"),
              sign("$2.83T", SX[1], 230, C("Households held"), color="#FFF59D", size=48, sub="HOUSEHOLDS, DIRECTLY"),
              sign("$2.55T", SX[2], 230, C("Mutual funds"), color="#FFF59D", size=48, sub="MUTUAL FUNDS + ETFs"),
              TED([[0, SX[0] - 250], [C("Households held"), SX[1] - 230], [C("Mutual funds"), SX[2] - 230]], 0.1, face="happy", hold="phone", y=900)]},
    sources=["z1"])
stage("s23_banks", "a3_banks", {
    **W1("mainstreet", shops=SHOPS, pops=[0.1] * 7),
    "cam": cam((0, SX[3], 560, 1.1), (C("State and local"), SX[4], 560, 1.1, 1.2), (C("Pension funds"), SX[5], 560, 1.1, 1.2), (C("And insurance"), SX[6], 560, 1.1, 1.2)), "drift": 3,
    "items": [sign("$2.04T", SX[3], 230, C("Banks and credit unions"), color="#FFF59D", size=48, sub="BANKS + CREDIT UNIONS"),
              sign("$1.65T", SX[4], 200, C("State and local"), color="#FFF59D", size=48, sub="STATE & LOCAL GOV'TS"),
              sign("$1.18T", SX[5], 230, C("Pension funds"), color="#FFF59D", size=48, sub="PENSION FUNDS"),
              sign("$0.61T", SX[6], 230, C("And insurance"), color="#FFF59D", size=48, sub="INSURERS"),
              RUTH([[0, SX[3] - 250], [C("State and local"), SX[4] - 250], [C("Pension funds"), SX[5] - 230], [C("And insurance"), SX[6] - 230]], 0.1, face="happy", y=900)]},
    sources=["z1"])
stage("s24_you", "a3_you", {
    **W1("mainstreet", shops=SHOPS, pops=[0.1] * 7),
    "cam": cam((0, 1200, 480, 0.75), (C("there's a decent chance"), 1200, 600, 1.0, 1.6), (C("A lot of it lands"), 1200, 520, 0.85, 1.4)), "drift": 4,
    "items": [TED(1000, 0.2, face="worry", y=900, faces=[[0, "worry"], [C("there's a decent chance"), "shock"], [C("A lot of it lands"), "grin"]], takes=[C("there's a decent chance")], scale=1.5),
              RUTH(1400, 0.3, face="happy", y=900, scale=1.45, hops=[C("A lot of it lands", 0.4)]),
              it("feeflow", **{"from": [1200, -200], "to": [1200, 750]}, at=C("The interest the government pays"), n=8, lift=60),
              it("toonwords", text="INTEREST → AMERICAN ACCOUNTS", x=1200, y=250, at=C("A lot of it lands"), size=56),
              it("bubble", text="MY 401(k)?!", x=850, y=420, at=C("there's a decent chance", 0.5), until=C("The interest the government pays"), tail=[960, 560], size=36)]})
add("p25_loop", "a3_draw", "engine_draw", {
    "title": "The savings loop (simplified)", "board": BOARD, "draw_start": C("You put savings"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 560, 220, 110), "color": "ink", "width": 6, "kind": "box", "start": C("You put savings"), "label": lbl("YOU", 670, 625, 30, "ink")},
        {"d": arrow((790, 590), (930, 520), -0.1), "color": "accent3", "width": 6, "kind": "arrow", "start": C("into a fund"), "label": lbl("SAVINGS", 840, 500, 22, "accent3")},
        {"d": rect(940, 430, 240, 110), "color": "accent2", "width": 6, "kind": "box", "start": C("into a fund", 0.3), "label": lbl("FUND", 1060, 495, 30, "accent2")},
        {"d": arrow((1190, 470), (1320, 560), -0.1), "color": "accent2", "width": 6, "kind": "arrow", "start": C("by buying a bond"), "label": lbl("BUYS A BOND", 1300, 470, 22, "accent2")},
        {"d": rect(1310, 570, 230, 110), "color": "accent", "width": 6, "kind": "box", "start": C("lends to the Treasury"), "label": lbl("TREASURY", 1425, 635, 30, "accent")},
        {"d": arrow((1330, 690), (1110, 760), -0.15), "color": "risk", "width": 6, "kind": "arrow", "start": C("pays interest back"), "label": lbl("INTEREST", 1260, 780, 22, "risk")},
        {"d": arrow((1000, 760), (760, 680), -0.15), "color": "risk", "width": 6, "kind": "arrow", "start": C("And the fund pays you"), "label": lbl("RETURNS", 830, 780, 22, "risk")},
        {"d": dot(1050, 860), "color": "muted", "width": 1, "start": C("One person's debt"), "label": lbl("ONE PERSON'S DEBT = ANOTHER'S SAVINGS", 1050, 860, 24, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("pays interest back", 0.2), "dur": 1.4, "target": [1220, 740]}],
    "scale": 0.86, "floor": 1040})
stage("s26_fed", "a3_fed", {
    **W1("fedwarehouse", level=[[0, 0.62]], gauge=[[0, 0], [C("the Fed held"), 0], [C("in Treasury securities"), 4.59]], gaugeMax=6),
    "cam": cam((0, 1200, 300, 0.85), (C("The Federal Reserve"), 1200, 400, 0.8, 1.4), (C("the Fed held"), 2050, 300, 1.1, 1.4), (C("stacked in the warehouse"), 1300, 480, 0.85, 1.6)), "drift": 4,
    "items": [it("toonwords", text="THE BIGGEST SINGLE HOLDER", x=1200, y=880, at=0.3, until=C("the Fed held"), size=60),
              sign("H.4.1 · WED. NOV 11, 2026", 2050, 470, C("in Treasury securities"), color="#FFF8E1", size=26),
              it("forklift", x=[[0, -300], [C("stacked in the warehouse"), 700]], at=0.2, load=["T-NOTE", "T-BOND"], scale=0.9, face="happy"),
              TED(1750, 0.4, face="shock", takes=[C("in Treasury securities")], y=860)]},
    sources=["h41"])
stage("s27_qt", "a3_qt", {
    **W1("fedwarehouse", level=[[0, 1.0], [C("let bonds mature"), 1.0], [C("the shelves thinned out"), 0.62]], gauge=[[0, 5.77], [C("let bonds mature"), 5.77], [C("the shelves thinned out"), 4.59]], gaugeMax=6, billsAt=C("But over the past year")),
    "cam": cam((0, 2050, 300, 1.05), (C("After the pandemic"), 1200, 420, 0.8, 1.6), (C("But over the past year"), 1200, 620, 0.85, 1.4)), "drift": 4,
    "items": [it("calendar", x=2050, y=620, at=0.2, pages=[[0, "PEAK", "JUNE 2022"], [C("the shelves thinned out"), "NOW", "NOV 2026"]], scale=0.7),
              it("forklift", x=[[C("let bonds mature"), 900], [C("the shelves thinned out"), 2700]], at=C("After the pandemic"), load=["MATURED"], scale=0.85, face="happy"),
              sign("BILLS: +$382BN IN A YEAR (H.4.1)", 1200, 950, C("its holdings of short-term bills"), color="#FFF59D", size=30)]},
    sources=["h41", "treast"])
stage("s28_turn", "a3_turn", {
    **W1("mainstreet", shops=SHOPS, pops=[0.1] * 7),
    "cam": cam((0, 1200, 460, 0.8), (C("And the last big piece"), 1500, 460, 0.9, 1.4)), "drift": 3,
    "items": [it("pie", x=1200, y=430, r=230, at=0.1, total=100, title="ROUGH SPLIT OF $40.6T · OUR CALC., MIXED DATES",
                 slices=[{"v": 23, "color": "#2E6BD1", "label": "FOREIGN\n≈23%", "at": C("Foreign holders")},
                         {"v": 11, "color": "#7E57C2", "label": "FED\n≈11%", "at": C("The Fed")},
                         {"v": 47, "color": "#2E9E6B", "label": "OTHER, MOSTLY U.S.\n≈47%", "at": C("Other investors"), "size": 22},
                         {"v": 19, "color": "#F2B63A", "label": "GOV'T OWES\nITSELF ≈19%", "at": C("And the last big piece"), "size": 22}], popAt=[3, C("owes to itself")]),
              TED(400, 0.2, face="happy", y=900, faces=[[0, "happy"], [C("And the last big piece"), "shock"]]),
              RUTH(2000, 0.3, face="worry", y=900, takes=[C("owes to itself")])]},
    sources=["dtp", "tic", "h41"])

# ====================================================================== ACT 4: the IOU to yourself
bumper("s29_b4", "a4_card", "4", "THE IOU TO YOURSELF", "Dear Me, I owe you. Love, Me", "#7E57C2", "$40.6T", 1.15)
stage("s30_cabinet", "a4_cabinet", {
    **W1("trustcabinet", openAt=C("IOUs, filed in a drawer", -0.4), fill=[[0, 1]], cabX=1000),
    "cam": cam((0, 1000, 300, 0.85), (C("For years"), 800, 520, 0.95, 1.4), (C("The surplus was lent"), 1200, 480, 0.9, 1.4), (C("IOUs, filed"), 1000, 420, 1.1, WHIP)), "drift": 4,
    "items": [it("toonwords", text="MEET THE FILING CABINET", x=1000, y=60, at=0.2, until=C("For years"), size=60),
              RUTH(400, 0.2, face="happy", label="RUTH · RETIREE", labelUntil=C("The surplus was lent"), hold="clipboard"),
              it("feeflow", **{"from": [300, 300], "to": [1000, 200]}, at=C("collected more"), until=C("The surplus was lent"), n=6, lift=80),
              sign("PAYROLL TAXES > BENEFITS (SURPLUS YEARS)", 600, 130, C("collected more"), color="#C8E6C9", size=26, until=C("The surplus was lent", 0.5)),
              sign("SPECIAL TREASURY SECURITIES · HELD ONLY INSIDE THE GOV'T", 1200, 130, C("in exchange for"), color="#FFF8E1", size=26)]},
    sources=["dtp", "crs_ss"])
stage("s31_reserves", "a4_reserves", {
    **W1("trustcabinet", open=1, fill=[[0, 1], [C("costs beat revenue"), 1], [C("one hundred and sixty"), 0.94]], tubeAt=C("costs beat revenue"), cabX=1000),
    "cam": cam((0, 1000, 420, 1.0), (C("But in twenty twenty-five"), 1500, 420, 0.8, 1.6)), "drift": 4,
    "items": [it("counter", x=1000, y=-50, at=0.4, prefix="$", suffix="T", decimals=2, steps=[[0, 0], [0.4, 0], [C("those trust fund reserves held"), 2.56]], text="OASDI RESERVES · END OF 2025 (TRUSTEES, VIA CRS)", until=C("But in twenty twenty-five")),
              it("counter", x=1500, y=-50, at=C("But in twenty twenty-five"), prefix="−$", suffix="BN", decimals=0, steps=[[0, 0], [C("costs beat revenue"), 0], [C("one hundred and sixty"), 160]], text="CHANGE IN 2025: COSTS > REVENUE"),
              RUTH(450, 0.2, face="happy", faces=[[0, "happy"], [C("costs beat revenue"), "worry"]], takes=[C("shrank")])]},
    sources=["crs_ss"])
add("p32_trip", "a4_draw", "engine_draw", {
    "title": "The trust fund round trip (simplified)", "board": BOARD, "draw_start": C("Payroll taxes flow"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 440, 230, 100), "color": "accent3", "width": 6, "kind": "box", "start": C("Payroll taxes flow"), "label": lbl("PAYROLL TAXES", 675, 500, 24, "accent3")},
        {"d": arrow((800, 490), (920, 490)), "color": "accent3", "width": 6, "kind": "arrow", "start": C("into the trust fund")},
        {"d": rect(930, 430, 250, 120), "color": "accent", "width": 6, "kind": "box", "start": C("into the trust fund", 0.3), "label": lbl("TRUST FUND", 1055, 500, 26, "accent")},
        {"d": arrow((1190, 470), (1320, 470)), "color": "accent2", "width": 6, "kind": "arrow", "start": C("Any surplus goes"), "label": lbl("SURPLUS $", 1255, 445, 20, "accent2")},
        {"d": rect(1330, 430, 210, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("goes to the Treasury"), "label": lbl("TREASURY", 1435, 500, 26, "accent2")},
        {"d": arrow((1330, 530), (1190, 530)), "color": "ink", "width": 5, "kind": "arrow", "start": C("hands back an IOU"), "label": lbl("IOU", 1255, 565, 22, "ink")},
        {"d": arrow((1055, 560), (1055, 690), 0.1), "color": "risk", "width": 6, "kind": "arrow", "start": C("the fund hands the IOU back"), "label": lbl("CASH FOR BENEFITS", 1130, 720, 22, "risk")},
        {"d": rect(1330, 680, 210, 100), "color": "risk", "width": 6, "kind": "box", "start": C("it borrows from the public"), "label": lbl("THE PUBLIC", 1435, 735, 24, "risk")},
        {"d": arrow((1435, 670), (1435, 560)), "color": "risk", "width": 5, "kind": "arrow", "start": C("it borrows from the public", 0.4), "label": lbl("LENDS", 1490, 615, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("To find that cash", 0.2), "dur": 1.4, "target": [1435, 730]}],
    "scale": 0.86, "floor": 1040})
stage("s33_shift", "a4_shift", {
    **W1("iouvault", open=1, odo=[[0, 40.6]], odoLabel="TOTAL: UNCHANGED AT FIRST", doorX=600, pressX=2150),
    "cam": cam((0, 1200, 300, 1.1), (C("The IOU just moves"), 1200, 520, 0.85, 1.4), (C("Debt the government owed"), 1200, 500, 0.95, 1.4)), "drift": 4,
    "items": [it("pie", x=1200, y=560, r=200, at=0.2, total=40.6, title="SAME TOTAL",
                 slices=[{"v": 32.8, "color": "#2E6BD1", "label": "PUBLIC", "at": 0.3}, {"v": 7.8, "color": "#F2B63A", "label": "GOV'T", "at": 0.3}], popAt=[1, C("The IOU just moves")]),
              OWEN([[0, 1850], [C("The IOU just moves"), 1850], [C("to the big box"), 450]], 0.2, amount="TRUST FUND IOU", amounts=[[0, "TRUST FUND IOU"], [C("to the big box"), "OWED TO INVESTORS"]], face="happy", faces=[[0, "happy"], [C("to the big box"), "smug"]], scale=0.75),
              it("toonwords", text="NOTHING, AT FIRST", x=1200, y=200, at=C("Nothing, at first"), size=64, until=C("The IOU just moves", 1.0)),
              TED(2050, 0.3, face="worry", hold="clipboard")]},
    sources=["dtp"])
stage("s34_date", "a4_date", {
    **W1("trustcabinet", open=1, fill=[[0, 0.94], [C("run out in late"), 0.94], [C("into twenty thirty-four"), 0.05]], tubeAt=0.1, cabX=1000),
    "cam": cam((0, 1000, 420, 0.95), (C("The trustees project"), 1500, 380, 0.85, 1.4), (C("After that"), 1000, 480, 1.0, 1.4)), "drift": 4,
    "items": [it("calendar", x=1650, y=200, at=C("The trustees project"), pages=[[C("The trustees project"), "Q4 2032", "RETIREMENT FUND (OASI)"], [C("Counting the disability fund"), "2034", "COMBINED (OASI + DI)"]], scale=0.8, color="#7E57C2"),
              sign("THEN ≈ 83% OF SCHEDULED BENEFITS PAYABLE (PROJECTION)", 1000, -40, C("After that"), color="#FFF59D", size=28, sub="2026 TRUSTEES REPORT, VIA CRS"),
              RUTH(450, 0.2, face="worry", faces=[[0, "worry"], [C("After that"), "shock"]], takes=[C("eighty-three percent")])]},
    sources=["crs_ss"])

# ====================================================================== ACT 5: the meter is running
bumper("s35_b5", "a5_card", "5", "THE METER IS RUNNING", "Please do not tap the glass", "#F2B63A", "$40.6T + INTEREST", 1.35, face="shock")
stage("s36_meter", "a5_meter", {
    **W1("meterscale", meter=[[0, 0], [C("net interest"), 0], [C("one point zero five", 1.0), 1052]], meterLabel="NET INTEREST · FY2026", flagAt=C("Which brings us")),
    "cam": cam((0, 640, 320, 1.2), (C("In fiscal year"), 640, 320, 1.1, 1.4), (C("That's about"), 900, 440, 0.95, 1.4)), "drift": 4,
    "items": [sign("FISCAL YEAR 2026 · OCT 2025–SEP 2026 · MONTHLY TREASURY STATEMENT", 900, 950, C("which ended in September"), color="#FFF8E1", size=24),
              it("counter", x=1500, y=200, at=C("That's about"), prefix="$", suffix="BN / DAY", decimals=1, steps=[[0, 0], [C("That's about"), 0], [C("every day"), 2.9]], text="AVERAGE · OUR CALCULATION"),
              TED(1350, 0.3, face="shock", takes=[C("one point zero five")], hold="clipboard")]},
    sources=["mts"], sfx=[{"kind": "hit", "cue": "Which brings us", "gain": 0.3}])
stage("s37_defense", "a5_defense", {
    **W1("meterscale", meter=[[0, 1052]], meterLabel="NET INTEREST · FY2026", flagAt=0.1, tipAt=C("Interest outweighed it"), tip=0.32,
       left={"label": "DEFENSE", "sub": "$965BN", "at": C("Now put national defense")}, right={"label": "NET INTEREST", "sub": "$1,052BN", "at": C("Same year")}),
    "cam": cam((0, 1500, 380, 0.95), (C("Interest outweighed it"), 1700, 420, 1.05, WHIP), (C("In fiscal twenty twenty-five"), 1300, 440, 0.85, 1.4)), "drift": 4,
    "items": [it("toonwords", text="INTEREST > DEFENSE", x=1700, y=-60, at=C("Interest outweighed it", 0.3), size=70, color="#D93A49"),
              sign("FY2025: INTEREST $970BN · DEFENSE $917BN", 1300, 980, C("In fiscal twenty twenty-five"), color="#FFF59D", size=30, sub="MONTHLY TREASURY STATEMENT · BUDGET FUNCTIONS"),
              TED(2180, 0.2, face="worry", faces=[[0, "worry"], [C("Interest outweighed it"), "shock"]], takes=[C("Interest outweighed it")])]},
    sources=["mts"], sfx=[{"kind": "hit", "cue": "Interest outweighed it", "gain": 0.35}])
stage("s38_why", "a5_why", {
    **W1("meterscale", meter=[[0, 1052]], meterLabel="NET INTEREST · FY2026", flagAt=0.1, left={"label": "DEFENSE", "sub": "$965BN", "at": 0}, right={"label": "NET INTEREST", "sub": "$1,052BN", "at": 0}, tipAt=0, tip=0.32),
    "cam": cam((0, 1200, 420, 0.8), (C("In October twenty twenty-one"), 1200, 500, 0.9, 1.4), (C("Cheap old bonds"), 1200, 480, 0.85, 1.4)), "drift": 4,
    "items": [chart([{"label": "OCT 2021", "value": 1.455, "color": "#2E9E6B", "at": C("debt was"), "display": "1.46%"},
                     {"label": "OCT 2026", "value": 3.570, "color": "#D93A49", "at": C("By October twenty twenty-six", 0.6), "display": "3.57%"}],
                    at=C("In October twenty twenty-one", -0.3), max=4, title="AVG. RATE ON MARKETABLE TREASURY DEBT (TREASURY)", x=600, y=150, w=1200, h=560),
              it("toonwords", text="RATES!", x=1200, y=60, at=C("Rates"), size=110, color="#D93A49", until=C("In October twenty twenty-one", 0.3)),
              TED(2150, 0.2, face="worry", faces=[[0, "worry"], [C("By October twenty twenty-six"), "shock"]], hold="clipboard"),
              OWEN([[C("Cheap old bonds"), -300], [C("pricier new ones", 1.0), 2600]], C("Cheap old bonds", -0.2), y=980, amount="NEW, PRICIER IOU", face="sweat", scale=0.8)]},
    sources=["avgrate"])
add("p39_bars", "a5_draw", "engine_draw", {
    "title": "Federal outlays, fiscal year 2026 (Monthly Treasury Statement)", "board": BOARD, "draw_start": C("Let me put them"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 820 L 1500 820", "color": "ink", "width": 5, "start": C("Let me put them")},
        {"d": "M 650 820 L 650 577 L 820 577 L 820 820 Z", "color": "muted", "width": 3, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("Defense, fiscal"), "label": lbl("DEFENSE · $965BN", 735, 557, 20, "muted")},
        {"d": "M 860 820 L 860 555 L 1030 555 L 1030 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("Net interest, a bit taller"), "label": lbl("NET INTEREST · $1,052BN", 945, 535, 20, "risk")},
        {"d": "M 1070 820 L 1070 550 L 1240 550 L 1240 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Medicare"), "label": lbl("MEDICARE · $1,073BN", 1155, 530, 20, "accent2")},
        {"d": "M 1280 820 L 1280 400 L 1450 400 L 1450 820 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("Social Security, taller"), "label": lbl("SOCIAL SECURITY · $1,667BN", 1365, 380, 20, "accent3")},
        {"d": dot(1060, 870), "color": "ink", "width": 1, "start": C("Interest is now"), "label": lbl("INTEREST ≈ 14¢ OF EVERY $1 SPENT (OUR CALC.)", 1060, 870, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Net interest, a bit taller", 0.2), "dur": 1.4, "target": [945, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["mts"])
stage("s40_who", "a5_who", {
    **W1("mainstreet", shops=SHOPS, pops=[C("The holders we met")] * 7),
    "cam": cam((0, 1200, 380, 0.7), (C("Money funds"), 1200, 480, 0.75, 1.6), (C("Every tick"), 1200, 500, 0.8, 1.4)), "drift": 4,
    "items": [it("feeflow", **{"from": [1200, -300], "to": [SX[0], 650]}, at=C("Money funds"), n=5, lift=100),
              it("feeflow", **{"from": [1200, -300], "to": [SX[5], 650]}, at=C("pensions"), n=5, lift=100),
              it("feeflow", **{"from": [1200, -300], "to": [SX[3], 650]}, at=C("banks"), n=5, lift=100),
              it("feeflow", **{"from": [1200, -300], "to": [SX[1], 650]}, at=C("households"), n=5, lift=100),
              sign("+ THE FED · + INVESTORS ABROAD", 1200, 120, C("the Fed, and investors abroad"), color="#FFF8E1", size=30),
              it("toonwords", text="EVERY TICK = A PAYMENT", x=1200, y=260, at=C("Every tick"), size=64),
              TED(1000, 0.2, face="happy", y=900), RUTH(1400, 0.3, face="grin", y=900, hops=[C("Every tick", 0.5)])]},
    sources=["z1", "tic", "h41"])
stage("s41_cbo", "a5_cbo", {
    **W1("meterscale", meter=[[0, 1052], [C("climbs from"), 1052], [C("by twenty thirty-six"), 2146]], meterLabel="CBO PROJECTION (FEB 2026)", flagAt=0.1, flagText="PROJECTED"),
    "cam": cam((0, 640, 360, 1.0), (C("In its February baseline"), 1200, 420, 0.8, 1.4), (C("That's a projection"), 1300, 480, 0.9, 1.2)), "drift": 4,
    "items": [chart([{"label": "FY1991 HIGH", "value": 3.2, "color": "#677287", "at": C("The previous high"), "display": "3.2%"},
                     {"label": "FY2026", "value": 3.3, "color": "#F2B63A", "at": C("climbs from"), "display": "3.3%"},
                     {"label": "FY2036 (PROJ.)", "value": 4.6, "color": "#D93A49", "at": C("by twenty thirty-six", -0.5), "display": "4.6%"}],
                    at=C("In its February baseline"), max=5, title="NET INTEREST, % OF GDP · CBO BASELINE VIA CRS", x=1150, y=120, w=1000, h=520),
              TED(300, 0.2, face="worry", hold="clipboard", faces=[[0, "worry"], [C("by twenty thirty-six"), "shock"]]),
              it("docs", x=2350, y=900, at=C("That's a projection"), text="CBO BASELINE · FEB 2026", scale=0.65, stamp="PROJECTION", stampAt=C("not a result", -0.2))]},
    sources=["crs_deficit"])

# ====================================================================== PAYOFF + TEASER + BUTTON
stage("s42_payoff", "payoff", {
    **W1("mainstreet", shops=SHOPS, pops=[0.1] * 7),
    "cam": cam((0, 1200, 420, 0.75), (C("The biggest lender"), 1200, 480, 0.8, 1.6), (C("So every dollar"), 1200, 520, 0.85, 1.4)), "drift": 3,
    "items": [it("pie", x=1200, y=380, r=200, at=C("Foreign investors", -0.4), total=100, title="WHO HOLDS THE $40.6T (ROUGH, OUR CALC.)", until=C("The biggest lender"),
                 slices=[{"v": 23, "color": "#2E6BD1", "label": "FOREIGN", "at": C("Foreign investors")}, {"v": 11, "color": "#7E57C2", "label": "FED", "at": C("The Fed holds")},
                         {"v": 19, "color": "#F2B63A", "label": "GOV'T", "at": C("The government owes")}, {"v": 47, "color": "#2E9E6B", "label": "MOSTLY U.S.", "at": C("And most of the rest")}]),
              it("toonwords", text="THE BIGGEST LENDER TO THE U.S. IS THE U.S.", x=1200, y=250, at=C("The biggest lender"), size=52, until=C("So every dollar", 0.3)),
              sign("A COST FOR TAXPAYERS", 800, 250, C("A cost for taxpayers"), color="#FFCDD2", size=34),
              sign("INCOME FOR HOLDERS", 1600, 250, C("and income for"), color="#C8E6C9", size=34),
              OWEN([[0, 1200]], 0.2, y=900, amount="$40.6T", face="happy", faces=[[0, "happy"], [C("So every dollar"), "smug"]], scale=0.9, hops=[C("The biggest lender", 0.4)]),
              TED(700, 0.3, face="happy", y=900, faces=[[0, "worry"], [C("Not China"), "happy"], [C("A cost for taxpayers"), "worry"]]),
              RUTH(1700, 0.4, face="happy", y=900, faces=[[0, "happy"], [C("and income for"), "grin"]])]},
    sources=["dtp", "tic", "h41", "z1"])
add("s43_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s44_button", "button", {
    **W1("iouvault", open=1, odo=[[0, 40.6]], doorX=760, pressX=2050), "cam": cam((0, 900, 560, 1.15), (2.8, 800, 520, 1.3, WHIP)), "drift": 0, "min_seconds": 5.6,
    "items": [OWEN([[0, 1300], [1.4, 860]], 0.0, amount="$40.6T", grow=[[0, 1.0], [1.2, 1.0], [1.8, 2.3]], face="happy", faces=[[0, "happy"], [1.9, "shock"], [3.0, "sweat"]]),
              TED(1500, 0.1, face="deadpan", faces=[[0, "deadpan"], [2.0, "shock"], [3.6, "grin"]], takes=[2.0], hold="clipboard"),
              it("bubble", text="STUCK IN THE VAULT DOOR!", x=760, y=180, at=2.1, until=3.4, tail=[800, 380], size=34, shout=True),
              it("toonwords", text="SEE YOU NEXT TIME · INTEREST INCLUDED", x=1100, y=130, at=3.6, size=50)]},
    sfx=[{"kind": "hit", "at": 2.0, "gain": 0.3}])

write(OUT, "# GENERATED by tools/gen_debt_storyboard.py; edit the generator, not this file.\n"
           "# Episode 59 storyboard (US debt): sitcom-style episode; bespoke worlds in CartoonStage/debt.tsx; tones from visual_direction.yaml.\n")
