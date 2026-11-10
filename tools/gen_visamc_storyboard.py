"""Generates projects/how-visa-and-mastercard-became-financial-gatekeepers/deliverables/documentary/storyboard.yaml
(Episode 39, US batch #18: How Visa and Mastercard Became Financial Gatekeepers).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part, and distinct from Ep 30 (which lived
in the studio, the shop and the district):
- Hook: the network web at night with a giant counter; the bank hall (new `bankhall` set); a toll gate on the highway.
- Part 1 (the bank club): 1958 suburb, an office with a calendar, the bay at Sausalito, the member-owned bank hall.
- Part 2 (the club goes public): the stock exchange by day and by night; the courtroom.
- Part 3 (the moat): the growing two-sided network (new `netmesh` item); stores; numbers and a volume chart.
- Part 4 (the rules): the bank hall, the courtroom, Congress, a cap chart, a European canal street.
- Part 5 (the gate on trial): courtroom at night, the vault, stores, Congress at night.
No logos, no card designs, no real people drawn; names in text only. Lint: tools/lint_storyboard.py.
Run: python tools/gen_visamc_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-visa-and-mastercard-became-financial-gatekeepers/deliverables/documentary/storyboard.yaml"
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


def chart(bars, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars, at=at, **kw)


def card_(x=960, y=420, **kw):
    return it("creditcard", x=x, y=y, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("web", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.25}, {"at": 1.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("counter", x=960, y=300, at=0.05, prefix="", suffix="BN", steps=[[0.05, 0], [1.5, 355]], text="PAYMENTS CARRYING VISA'S NAME, FY2026 (VISA 10-K)", scale=1.5),
              it("letters", x=960, y=640, text="≈ 973 MILLION A DAY", at=C("Close to one billion"), size=64, color="gold")]},
    sources=["visak"])
stage("s02_twist", "h_twist", {
    "zones": [Z("bankhall", label="MEMBERS ONLY")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("They started as clubs"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=250, text="NOT A LENDER", at=0.3, size=50, color="gold"),
              it("letters", x=1000, y=420, text="NO LOANS", at=C("does not lend you money"), until=C("They started as clubs"), size=80, color="risk"),
              *crowd([1050, 1150, 1250, 1350, 1450], "stand", at=C("They started as clubs"), scale=0.7),
              it("sign", x=1250, y=420, text="OWNED BY THE BANKS", at=C("owned by the banks"), color="#FFE0B2", size=40)]},
    sources=["fedhist", "visas4"])
stage("s03_question", "h_question", {
    "zones": [Z("highway", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("tollbooth", x=1000, at=0.2, fee="THE GATE", rate=1.0, scale=0.9),
              it("letters", x=1000, y=150, text="HOW DID TWO BANK CLUBS BECOME THE GATE?", at=0.4, size=54, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · HOW IT WAS BUILT", at=C("how that gate was built"), color="#BBDEFB", size=40),
              it("sign", x=960, y=380, text="2 · WHY NOBODY GETS AROUND IT", at=C("why it is so hard"), color="#FFE0B2", size=30),
              it("sign", x=1600, y=380, text="3 · THE FIGHT", at=C("pry it open"), color="#C8E6C9", size=40),
              it("letters", x=960, y=700, text="THE GATEKEEPERS", at=0.4, size=72, color="gold")]})

# ====================================================================== PART 1: the bank club (1958-1976)
card("s05_c1", "m1_card", "The Bank Club", "From one bank's card to a members' network")
stage("s06_launch", "m1_launch", {
    "zones": [Z("suburb")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It signs up the shoppers"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="CALIFORNIA · 1958", at=0.3, size=64, color="gold"),
              card_(800, 420, at=C("a new kind of card"), scale=0.7, rot=-8, text="BANKAMERICARD (1958)"),
              it("sign", x=1050, y=300, text="SHOPPERS", at=C("It signs up the shoppers"), color="#BBDEFB", size=38),
              it("sign", x=1400, y=300, text="STORES", at=C("it signs up the stores"), color="#FFE0B2", size=38),
              it("sign", x=1720, y=300, text="RISK", at=C("it carries the risk"), color="#FFCDD2", size=38),
              it("letters", x=1350, y=470, text="ONE BANK · ONE CLOSED SYSTEM", at=C("It is one bank"), size=46, color="white")]},
    sources=["fedhist"])
stage("s07_license", "m1_license", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("That same year"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("calendar", x=550, y=560, at=0.3, pages=[[0, "1966", "LICENSING"], [{"cue": "In nineteen sixty-nine"}, "1969", "MASTER CHARGE"]], scale=0.8),
              it("sign", x=1100, y=230, text="LICENSED TO OTHER BANKS (FED HISTORY)", at=C("starts licensing"), color="#BBDEFB", size=32),
              it("sign", x=1350, y=360, text="RIVAL CO-OP: INTERBANK", at=C("a cooperative called Interbank"), color="#FFE0B2", size=36),
              it("letters", x=1450, y=500, text="→ MASTER CHARGE (1969)", at=C("it takes the name Master Charge"), size=46, color="gold")]},
    sources=["fedhist", "mas4"])
stage("s08_hock", "m1_hock", {
    "zones": [Z("beach")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("The answer was radical"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="SAUSALITO · 1969", at=0.3, size=60, color="gold"),
              it("letters", x=1000, y=250, text="'THE STRUGGLING BANKAMERICARD PROGRAM' (VISA)", at=C("was struggling"), size=34, color="white"),
              *crowd([800, 900, 1000, 1100, 1200], "stand", at=C("gathered a group"), scale=0.65),
              it("sign", x=1500, y=380, text="GIVE THE SYSTEM AWAY", at=C("give the system away"), color="#C8E6C9", size=40)]},
    sources=["hock"])
stage("s09_coop", "m1_coop", {
    "zones": [Z("bankhall", label="MEMBER-OWNED · 1970")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("In nineteen seventy-six"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [*crowd([700, 800, 900, 1000, 1100, 1200], "stand", at=0.3, scale=0.62),
              it("letters", x=1000, y=380, text="NO SHARES FOR SALE", at=C("no shares for sale"), size=56, color="risk"),
              it("letters", x=1450, y=480, text="1976 · THE NAME: VISA", at=C("sounds the same in almost every language"), size=56, color="gold")]},
    sources=["visas4", "fedhist", "hock"])
add("p10_club", "m1_draw", "engine_draw", {
    "title": "Why the club worked", "board": BOARD, "draw_start": C("Before, every bank"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 220, 90), "color": "accent2", "width": 6, "kind": "box", "start": C("Before, every bank"), "label": lbl("BANK A", 670, 413, 26, "accent2")},
        {"d": rect(560, 500, 220, 60), "color": "accent2", "width": 3, "kind": "box", "start": C("only in its own stores"), "label": lbl("ITS STORES", 670, 538, 20, "accent2")},
        {"d": rect(1220, 360, 220, 90), "color": "accent", "width": 6, "kind": "box", "start": C("Here is bank B"), "label": lbl("BANK B", 1330, 413, 26, "accent")},
        {"d": rect(1220, 500, 220, 60), "color": "accent", "width": 3, "kind": "box", "start": C("Here is bank B", 0.6), "label": lbl("ITS STORES", 1330, 538, 20, "accent")},
        {"d": rect(520, 320, 960, 480), "color": "accent3", "width": 6, "kind": "box", "start": C("Now put both inside one club"), "label": lbl("ONE CLUB · ONE NETWORK", 1000, 760, 30, "accent3")},
        {"d": arrow((680, 570), (1300, 570), 0.25) + " " + arrow((1320, 570), (700, 570), 0.25), "color": "ink", "width": 4, "kind": "arrow", "start": C("every card works in every store")},
    ],
    "actions": [{"kind": "point", "at": C("they all share one network", 0.1), "dur": 1.4, "target": [1000, 650]}],
    "scale": 0.86, "floor": 1040}, sources=["fedhist", "visas4"])
kinetic("s11_t1", "m1_transition", [("Clubs owned by thousands of banks…", 60, "Clubs owned by thousands", None, False),
                                    ("…then the club turned into a company", 60, "Then the club turned", "gold", False)])

# ====================================================================== PART 2: the club goes public (exchange + court)
card("s12_c2", "m2_card", "The Club Goes Public", "Mastercard 2006 · Visa 2008")
stage("s13_ma", "m2_ma", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And most of the money"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="MAY 2006 · MASTERCARD IPO", at=0.3, size=56, color="gold"),
              it("pricetag", x=700, y=380, at=C("at thirty-nine"), text="$39 / SHARE", scale=0.9),
              it("counter", x=1200, y=330, at=C("The offering raised"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "The offering raised", "offset": 1.2}, 2.4]], text="RAISED (424B4 PROSPECTUS)"),
              it("sign", x=1650, y=480, text="→ BUY BACK THE BANKS' SHARES", at=C("went straight back"), color="#FFE0B2", size=34)]},
    sources=["maipo"])
stage("s14_visa", "m2_visa", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By our calculation"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="≈ 14,000 MEMBER INSTITUTIONS (VISA U.S.A.)", at=0.3, until=C("In March two thousand eight"), size=44, color="white"),
              it("letters", x=1000, y=150, text="MARCH 2008 · VISA IPO", at=C("In March two thousand eight"), size=56, color="gold"),
              it("letters", x=900, y=300, text="406M SHARES × $44", at=C("four hundred and six million"), size=50, color="white"),
              it("counter", x=1300, y=420, at=C("By our calculation"), prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "By our calculation", "offset": 1.0}, 17.9]], text="GROSS, OUR CALCULATION"),
              it("letters", x=1650, y=600, text="'ONE OF THE LARGEST IPOS IN HISTORY' (VISA)", at=C("Visa itself calls it"), size=30, color="gold")]},
    sources=["visas4", "visaipo"])
stage("s15_why", "m2_why", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("As public companies"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="MERCHANT LAWSUITS", scale=0.7, stamp="FEES SET TOGETHER?", stampAt=C("setting fees together")),
              it("gavel", x=1650, y=F - 20, hits=[C("undo the listings")], at=0.2),
              it("letters", x=1300, y=220, text="CLUB OF BANKS → COMPANY", at=C("As public companies"), size=50, color="gold"),
              it("letters", x=1300, y=320, text="MERCHANTS ASKED: UNDO THE IPO", at=C("undo the listings"), size=40, color="risk")]},
    sources=["visak", "mak"])
add("p16_owners", "m2_draw", "engine_draw", {
    "title": "Who owns the network", "board": BOARD, "draw_start": C("Before, the banks owned"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 380, 220, 80), "color": "accent2", "width": 6, "kind": "box", "start": C("Before, the banks owned"), "label": lbl("BANKS", 650, 428, 26, "accent2")},
        {"d": rect(540, 600, 220, 80), "color": "ink", "width": 6, "kind": "box", "start": C("the network served"), "label": lbl("NETWORK", 650, 648, 26, "ink")},
        {"d": arrow((650, 470), (650, 590)), "color": "accent2", "width": 4, "kind": "arrow", "start": C("Before, the banks owned", 0.6), "label": lbl("OWN", 720, 540, 20, "accent2")},
        {"d": "M 860 300 L 860 820", "color": "muted", "width": 3, "start": C("After, the")},
        {"d": rect(1000, 330, 280, 80), "color": "accent3", "width": 6, "kind": "box", "start": C("owned by shareholders"), "label": lbl("SHAREHOLDERS", 1140, 378, 24, "accent3")},
        {"d": rect(1030, 500, 220, 80), "color": "ink", "width": 6, "kind": "box", "start": C("owned by shareholders", 0.5), "label": lbl("NETWORK", 1140, 548, 26, "ink")},
        {"d": rect(1030, 680, 220, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("The banks become customers"), "label": lbl("BANKS = CUSTOMERS", 1140, 728, 18, "accent2")},
        {"d": arrow((1140, 420), (1140, 495)) + " " + arrow((1140, 590), (1140, 675)), "color": "accent3", "width": 4, "kind": "arrow", "start": C("The banks become customers", 0.4)},
    ],
    "actions": [{"kind": "point", "at": C("its own share price", 0.1), "dur": 1.4, "target": [1140, 540]}],
    "scale": 0.86, "floor": 1040}, sources=["visas4", "maipo"])
kinetic("s17_t2", "m2_transition", [("A very, very large business…", 62, "very, very large", None, False),
                                    ("…and a force that is almost impossible to compete against", 52, "almost impossible", "gold", False)])

# ====================================================================== PART 3: the moat (network effects)
card("s18_c3", "m3_card", "The Moat", "Why nobody gets around the gate")
stage("s19_platform", "m3_platform", {
    "zones": [Z("web", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=110, text="'TWO-SIDED PLATFORM' (SUPREME COURT, 2018)", at=0.3, size=48, color="gold"),
              it("netmesh", x=960, y=520, at=C("serving two groups"), scale=0.95,
                 steps=[[0, 1, 1], [{"cue": "worth more to stores"}, 3, 2], [{"cue": "worth more to shoppers"}, 5, 4]])]},
    sources=["scotus"])
stage("s20_loop", "m3_loop", {
    "zones": [Z("shop", label="STORE")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The Court also noted"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [*crowd([600, 700, 800, 900], "walk", at=0.2, scale=0.6),
              it("letters", x=900, y=290, text="MORE CARDS → MORE STORES", at=C("More cards bring more stores"), size=52, color="gold"),
              it("letters", x=900, y=400, text="MORE STORES → MORE CARDS", at=C("More stores bring more cards"), size=52, color="white"),
              it("sign", x=1500, y=420, text="'BEGAN AS BANK COOPERATIVES' (SUPREME COURT)", at=C("began as bank cooperatives"), color="#FFE0B2", size=30)]},
    sources=["scotus"])
stage("s21_scale", "m3_scale", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=120, text="THE SIZE OF THE LOOP", at=0.3, size=56, color="gold"),
              it("counter", x=420, y=300, at=C("Visa reports"), prefix="", suffix="BN+", steps=[[0, 0], [{"cue": "payment credentials"}, 5]], text="VISA PAYMENT CREDENTIALS"),
              it("counter", x=960, y=300, at=C("more than four"), prefix="", suffix="M+", steps=[[0, 0], [{"cue": "places that accept them"}, 400]], text="ACCEPTANCE LOCATIONS (VISA)"),
              it("counter", x=1500, y=300, at=C("in total volume"), prefix="$", suffix="T", steps=[[0, 0], [{"cue": "in its latest year"}, 18]], text="VISA TOTAL VOLUME, FY2026"),
              it("letters", x=960, y=640, text="MASTERCARD: $10.6T GROSS VOLUME (2025)", at=C("Mastercard"), size=48, color="gold")]},
    sources=["visak", "mak"])
stage("s22_compare", "m3_compare", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "VISA", "value": 14.567, "color": "#1E88E5", "at": C("Visa handled"), "display": "$14.6T"},
                     {"label": "MASTERCARD", "value": 8.812, "color": "#FB8C00", "at": C("Mastercard, about"), "display": "$8.8T"},
                     {"label": "AMERICAN EXPRESS", "value": 1.888, "color": "#43A047", "at": C("American Express"), "display": "$1.9T"}],
                    at=0.2, max=16, title="PAYMENTS VOLUME 2025 (VISA 10-K, CITING THE NILSON REPORT)", x=360, w=1200)]},
    sources=["visak"])
add("p23_moat", "m3_draw", "engine_draw", {
    "title": "The moat (illustration)", "board": BOARD, "draw_start": C("Here is a new network"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1440 860", "color": "ink", "width": 4, "start": C("Let me draw the moat")},
        {"d": "M 600 860 L 600 820 L 700 820 L 700 860", "color": "muted", "width": 5, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is a new network"), "label": lbl("NEW NETWORK", 650, 790, 20, "muted")},
        {"d": rect(560, 400, 260, 110), "color": "risk", "width": 5, "kind": "box", "start": C("No store will accept it"), "label": lbl("NO STORES", 690, 445, 22, "risk")},
        {"d": rect(560, 560, 260, 110), "color": "risk", "width": 5, "kind": "box", "start": C("Nobody will carry the card"), "label": lbl("NO CARDS", 690, 605, 22, "risk")},
        {"d": arrow((830, 450), (830, 600), 0.4) + " " + arrow((550, 610), (550, 460), 0.4), "color": "risk", "width": 4, "kind": "arrow", "start": C("because no store accepts it")},
        {"d": "M 1040 860 L 1040 420 L 1160 420 L 1160 860", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("On the other side"), "label": lbl("VISA", 1100, 400, 22, "accent2")},
        {"d": "M 1220 860 L 1220 580 L 1340 580 L 1340 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("On the other side", 0.6), "label": lbl("MASTERCARD", 1280, 560, 20, "accent")},
        {"d": "M 900 300 L 900 860", "color": "accent3", "width": 6, "start": C("keeps others out"), "label": lbl("THE MOAT", 900, 280, 24, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("The loop that made them big", 0.1), "dur": 1.4, "target": [1100, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["scotus", "visak"])
kinetic("s24_t3", "m3_transition", [("A moat can be dug deeper on purpose…", 60, "dug deeper on purpose", None, False),
                                    ("…and the government stepped in", 60, "the government stepped in", "gold", False)])

# ====================================================================== PART 4: the rules (courts, Congress, Europe)
card("s25_c4", "m4_card", "The Rules", "Courts, Congress and Europe")
stage("s26_exclusive", "m4_exclusive", {
    "zones": [Z("bankhall", label="MEMBER RULES")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("The government sued"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=200, text="LATE 1990s", at=0.3, size=56, color="gold"),
              it("sign", x=1000, y=360, text="RULE: NO AMEX · NO DISCOVER CARDS", at=C("it could not issue"), color="#FFCDD2", size=38),
              it("counter", x=1000, y=560, at=C("accounted for"), prefix="", suffix="%", steps=[[0, 0], [{"cue": "of general purpose card transactions"}, 73]], text="SHARE OF CARD TRANSACTIONS (U.S. BRIEF)", until=C("of cards issued", 1.5)),
              it("counter", x=1500, y=560, at=C("of cards issued"), prefix="", suffix="%", steps=[[0, 0], [{"cue": "of cards issued", "offset": 1.0}, 85]], text="SHARE OF CARDS ISSUED (U.S. BRIEF)")]},
    sources=["osg"])
stage("s27_ruling", "m4_ruling", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("were ordered to repeal them"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=170, text="'NO BANK ... HAS AGREED TO ISSUE AMERICAN EXPRESS'", at=C("No bank in the continental"), size=36, color="white"),
              it("docs", x=800, y=560, at=0.3, text="EXCLUSIVITY RULES", scale=0.7, stamp="REPEALED", stampAt=C("were ordered to repeal them")),
              it("gavel", x=1650, y=F - 20, hits=[C("were ordered to repeal them"), C("upheld that order")], at=0.2),
              it("letters", x=1300, y=300, text="APPEALS COURT, 2003: UPHELD", at=C("upheld that order"), size=46, color="gold")]},
    sources=["osg"])
stage("s28_durbin", "m4_durbin", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Today the cap is"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=150, text="2010 · THE DURBIN AMENDMENT", at=0.3, size=56, color="gold"),
              it("pricetag", x=1000, y=360, at=C("Today the cap is"), text="21¢ + 0.05% + 1¢", scale=1.0),
              it("letters", x=1000, y=250, text="DEBIT CAP FOR LARGE BANKS (FED)", at=C("plus one cent for fraud"), size=34, color="white"),
              it("sign", x=1550, y=470, text="2 UNRELATED NETWORKS PER DEBIT CARD", at=C("at least two unrelated"), color="#C8E6C9", size=30)]},
    sources=["regii", "doj"])
stage("s29_proposal", "m4_proposal", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "TODAY'S CAP", "value": 24.5, "color": "#4FC3F7", "at": C("it would fall"), "display": "24.5¢"},
                     {"label": "2023 PROPOSAL", "value": 17.7, "color": "#FFB300", "at": C("it would fall", 1.0), "display": "17.7¢"}],
                    at=0.2, max=28, dark=True, title="DEBIT CAP ON A $50 PURCHASE (FEDERAL RESERVE)", x=300, w=900),
              it("letters", x=1550, y=380, text="NOT FINAL", at=C("has still not become final"), size=64, color="risk"),
              it("letters", x=1550, y=490, text="COURTS SPLIT · CAP STAYS", at=C("two federal"), size=36, color="white")]},
    sources=["regii", "mak", "visak"])
stage("s30_eu", "m4_eu", {
    "zones": [Z("dutch")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("at zero point two"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.4}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="EUROPEAN UNION · SINCE 2015", at=0.3, size=56, color="gold"),
              it("sign", x=900, y=370, text="DEBIT: 0.2%", at=C("at zero point two"), color="#BBDEFB", size=48),
              it("sign", x=1500, y=370, text="CREDIT: 0.3%", at=C("zero point three percent"), color="#FFE0B2", size=48),
              it("letters", x=1000, y=200, text="CONSUMER CARD FEE CAPS (REG. 2015/751)", at=C("capped the fee"), size=30, color="white")]},
    sources=["euifr"])
add("p31_walls", "m4_draw", "engine_draw", {
    "title": "Doors in the gate", "board": BOARD, "draw_start": C("First, the exclusivity rules"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(820, 330, 360, 480), "color": "ink", "width": 8, "kind": "box", "start": C("Let me draw the walls"), "label": lbl("THE GATE", 1000, 310, 28, "ink")},
        {"d": rect(860, 380, 120, 130), "color": "accent2", "width": 5, "kind": "box", "start": C("First, the exclusivity rules"), "label": lbl("COURTS", 920, 450, 18, "accent2")},
        {"d": rect(1020, 380, 120, 130), "color": "accent", "width": 5, "kind": "box", "start": C("Second, the debit cap"), "label": lbl("DEBIT CAP", 1080, 450, 18, "accent")},
        {"d": rect(940, 570, 120, 130), "color": "accent3", "width": 5, "kind": "box", "start": C("Third, Europe's caps"), "label": lbl("EUROPE", 1000, 640, 18, "accent3")},
        {"d": arrow((640, 450), (850, 450)) + " " + arrow((1360, 450), (1150, 450)) + " " + arrow((1000, 900), (1000, 710)), "color": "risk", "width": 4, "kind": "arrow", "start": C("Each one opened a small door")},
    ],
    "actions": [{"kind": "point", "at": C("None of them removed", 0.1), "dur": 1.4, "target": [1000, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["osg", "regii", "euifr"])
kinetic("s32_t4", "m4_transition", [("And now the gate itself…", 64, "And now the gate", None, False),
                                    ("…is on trial", 72, "is on trial", "risk", False)])

# ====================================================================== PART 5: the gate on trial
card("s33_c5", "m5_card", "The Gate on Trial", "Pending cases and bills")
stage("s34_doj", "m5_doj", {
    "zones": [Z("court", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("These are allegations"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="U.S. v. VISA (2024)", scale=0.7, stamp="ALLEGATIONS", stampAt=C("These are allegations")),
              it("counter", x=1150, y=280, at=C("According to the complaint"), prefix="> ", suffix="%", steps=[[0, 0], [{"cue": "of debit transactions"}, 60]], text="U.S. DEBIT ON VISA (DOJ ALLEGES)"),
              it("letters", x=1550, y=180, text="> $7BN IN FEES A YEAR (ALLEGED)", at=C("in fees a year"), size=40, color="gold"),
              it("letters", x=1550, y=520, text="2025: MOTION TO DISMISS DENIED · PENDING", at=C("a judge refused"), size=30, color="white")]},
    sources=["doj", "visak"])
stage("s35_moat", "m5_moat", {
    "zones": [Z("vault")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.1}, {"at": 1.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("letters", x=960, y=260, text="'AN ENORMOUS MOAT'", at=C("An enormous moat"), size=90, color="gold"),
              it("letters", x=960, y=380, text="VISA'S WORDS, QUOTED IN THE DOJ COMPLAINT", at=0.4, size=34, color="white")]},
    sources=["doj"])
stage("s36_merchants", "m5_merchants", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A second deal"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="MERCHANTS v. VISA & MASTERCARD (SINCE 2005)", at=0.3, size=44, color="gold"),
              it("counter", x=1000, y=330, at=C("a court approved"), prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "it came to"}, 5.5]], text="2019 SETTLEMENT, NET (OUR ARITHMETIC)"),
              it("sign", x=1550, y=480, text="2024 DEAL: REJECTED", at=C("was rejected by the judge"), color="#FFCDD2", size=42)]},
    sources=["visak"])
stage("s37_newdeal", "m5_newdeal", {
    "zones": [Z("shop", label="STORE")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And stores could choose"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=900, y=280, text="NOVEMBER 2025 · NEW DEAL", at=0.3, size=56, color="gold"),
              it("sign", x=750, y=400, text="−0.10 PT FOR 5 YEARS", at=C("a tenth of a"), color="#BBDEFB", size=40),
              it("sign", x=1500, y=400, text="STORES MAY REFUSE PREMIUM CARDS", at=C("refuse premium cards"), color="#FFE0B2", size=34),
              it("letters", x=1300, y=540, text="FINAL APPROVAL: PENDING", at=C("Final approval is still pending"), size=50, color="risk")]},
    sources=["visa8k", "visak"])
stage("s38_ccca", "m5_ccca", {
    "zones": [Z("parliament", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It has not passed"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="CREDIT CARD COMPETITION ACT (2026)", scale=0.7, stamp="NOT PASSED", stampAt=C("It has not passed")),
              it("letters", x=1250, y=200, text="BANKS > $100BN: A 2ND NETWORK", at=C("Banks with more than"), size=46, color="gold"),
              it("letters", x=1300, y=320, text="'UNCLEAR' IF IT GAINS TRACTION (VISA 10-K)", at=C("Visa itself says"), size=32, color="white")]},
    sources=["ccca", "visak"])
add("p39_pressure", "m5_draw", "engine_draw", {
    "title": "Three forces, one gate (status Nov 2026)", "board": BOARD, "draw_start": C("The Justice Department, on debit"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 380, 280, 420), "color": "ink", "width": 8, "kind": "box", "start": C("Let me draw where the pressure"), "label": lbl("THE GATE", 1000, 360, 28, "ink")},
        {"d": rect(520, 400, 220, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("The Justice Department, on debit"), "label": lbl("DOJ · DEBIT", 630, 448, 20, "accent2")},
        {"d": rect(520, 640, 220, 80), "color": "accent", "width": 5, "kind": "box", "start": C("The stores, through the courts"), "label": lbl("STORES · COURTS", 630, 688, 18, "accent")},
        {"d": rect(1260, 520, 240, 80), "color": "accent3", "width": 5, "kind": "box", "start": C("Congress, with a second network"), "label": lbl("CONGRESS · CREDIT", 1380, 568, 18, "accent3")},
        {"d": arrow((745, 440), (855, 480)) + " " + arrow((745, 680), (855, 640)) + " " + arrow((1255, 560), (1145, 560)), "color": "risk", "width": 5, "kind": "arrow", "start": C("Three forces pushing")},
        {"d": "M 900 860 L 900 820 L 960 820 L 960 860", "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("the gate is still standing"), "label": lbl("STILL STANDING", 1000, 900, 20, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("the gate is still standing", 0.1), "dur": 1.4, "target": [1000, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["doj", "visak", "ccca"])

# ====================================================================== PAYOFF
stage("s40_payoff", "payoff", {
    "zones": [Z("web", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.1}, {"at": C("Then as companies"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("netmesh", x=960, y=560, at=0.3, scale=0.85, steps=[[0, 2, 2], [{"cue": "thousands of banks"}, 4, 3], [{"cue": "gets stronger every time"}, 7, 6]], labels=["CARDS", "STORES"]),
              it("letters", x=960, y=110, text="THE MEETING POINT", at=C("They became"), size=64, color="gold")]},
    sources=["fedhist", "scotus"])
add("s41_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_visamc_storyboard.py; edit the generator, not this file.\n"
           "# Episode 39 storyboard (Visa and Mastercard): one visual language per part; tones from visual_direction.yaml.\n")
