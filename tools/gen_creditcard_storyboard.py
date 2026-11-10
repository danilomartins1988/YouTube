"""Generates projects/the-hidden-business-behind-your-credit-card/deliverables/documentary/storyboard.yaml (Episode 30,
US batch #02: The Hidden Business Behind Your Credit Card).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: typography + a generic card tapping (new `creditcard` item).
- Part 1 (the swipe): a store checkout where the $100 splits into slices.
- Part 2 (the toll road): a highway toll booth that takes a cut of every coin (new `tollbooth` item) + full-screen charts.
- Part 3 (interest): the night financial district with data charts.
- Part 4 (rewards): a night airport (travel points) and an evidence board of who pays.
- Part 5 (fees): an office and a courtroom (the late-fee rule).
No real card designs or logos (names in text only); no likeness of real people. Lint: tools/lint_storyboard.py.
Run: python tools/gen_creditcard_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-hidden-business-behind-your-credit-card/deliverables/documentary/storyboard.yaml"
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
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.25}, {"at": 1.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("counter", x=960, y=250, at=0.05, prefix="$", suffix="BN", steps=[[0.05, 0], [1.5, 160]], text="CARD INTEREST CHARGED, 2024 (CFPB)", scale=1.6),
              card_(960, 680, at=0.6, scale=0.9, rot=-6)]},
    sources=["cfpb_2025"])
stage("s02_twist", "h_twist", {
    "zones": [Z("shop", label="STORE")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("the store you are buying from"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.4}], "drift": 1,
    "items": [card_(800, 480, at=0.2, scale=0.75, tapAt=C("Every time you tap")),
              it("terminal", x=1150, y=F, at=0.2, text="$100.00", scale=0.9),
              it("letters", x=1400, y=230, text="STORE PAYS A FEE", at=C("pays a fee too"), size=70, color="risk"),
              it("letters", x=1400, y=340, text="(YOU NEVER SEE IT)", at=C("You just never see it"), size=44, color="white")]},
    sources=["crs"])
stage("s03_question", "h_question", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.2}, {"at": 0.8, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [card_(960, 430, at=0.1, scale=1.2, rot=4),
              it("letters", x=960, y=820, text="WHO MAKES MONEY ON THIS?", at=0.4, size=80, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=480, y=360, text="1 · THE SWIPE", at=0.3, color="#BBDEFB", size=50),
              it("sign", x=960, y=360, text="2 · INTEREST", at=0.7, color="#FFCDD2", size=50),
              it("sign", x=1440, y=360, text="3 · FEES", at=1.1, color="#FFE0B2", size=50),
              it("letters", x=960, y=650, text="+ WHO PAYS FOR YOUR REWARDS", at=C("who quietly pays"), size=56, color="gold")]},
    sources=["cfpb_rewards"])

# ====================================================================== PART 1: the two-second swipe (store checkout)
card("s05_c1", "m1_card", "The Two-Second Swipe", "Where $100 goes")
stage("s06_swipe", "m1_swipe", {
    "zones": [Z("shop", label="STORE")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("But in that time"), "x": 1300, "y": 520, "zoom": 0.95, "dur": 1.5}], "drift": 2,
    "items": [it("person", x=600, pose="stand", at=0.2, scale=0.8, hair=2, skin=1),
              card_(820, 470, at=0.2, scale=0.55, tapAt=C("and tap your card")),
              it("terminal", x=1050, y=F, at=0.2, text="$100.00", scale=0.8),
              it("clock", x=1750, y=330, at=C("It takes a couple"), period=1.0, text="≈ 2 SECONDS"),
              it("coins", **{"from": [1050, 450], "to": [1900, 300]}, at=C("the money passes through"), rate=6)]},
    sources=["crs"])
stage("s07_split", "m1_split", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "STORE RECEIVES", "value": 97, "color": "#23995A", "at": C("the store receives"), "display": "$97"},
                     {"label": "FEES (1–3%)", "value": 3, "color": "#E53935", "at": C("If it is three percent"), "display": "$3"}],
                    at=0.2, max=100, title="A $100 PURCHASE WITH A 3% FEE (CRS EXAMPLE)", x=520, w=880),
              it("letters", x=960, y=990, text="FEE SET BY THE NETWORK", at=C("but by the card network"), size=52, color="gold")]},
    sources=["crs"])
add("p08_flow", "m1_draw", "engine_draw", {
    "title": "Where your $100 goes", "board": BOARD, "draw_start": C("Here is you"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 380, 200, 110), "color": "ink", "width": 6, "kind": "box", "start": C("Here is you"), "label": lbl("YOU $100", 640, 443, 24, "ink")},
        {"d": rect(1260, 380, 200, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("and here is the store"), "label": lbl("STORE $97", 1360, 443, 24, "accent3")},
        {"d": rect(560, 640, 220, 100), "color": "accent2", "width": 6, "kind": "box", "start": C("Your bank, which issued"), "label": lbl("YOUR BANK", 670, 698, 22, "accent2")},
        {"d": rect(900, 640, 220, 100), "color": "accent", "width": 6, "kind": "box", "start": C("The network"), "label": lbl("NETWORK", 1010, 698, 22, "accent")},
        {"d": rect(1240, 640, 220, 100), "color": "risk", "width": 6, "kind": "box", "start": C("And the store's own bank"), "label": lbl("STORE'S BANK", 1350, 698, 20, "risk")},
        {"d": arrow((750, 435), (1250, 435), 0.0), "color": "ink", "width": 5, "start": C("The store gets ninety-seven")},
        {"d": arrow((1000, 450), (680, 630), 0.15), "color": "accent2", "width": 7, "start": C("the biggest piece goes to your bank"), "label": lbl("biggest slice", 780, 560, 22, "accent2")},
    ],
    "actions": [{"kind": "point", "at": C("the biggest piece goes to your bank", 0.4), "dur": 1.4, "target": [670, 690]}],
    "scale": 0.86, "floor": 1040}, sources=["crs"])
stage("s09_total", "m1_total", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.15}, {"at": 1.5, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("counter", x=960, y=330, at=0.3, prefix="≈ $", suffix="BN", steps=[[0, 0], [{"cue": "came to", "offset": 1}, 160]], text="SWIPE FEES, CREDIT + DEBIT, 2022 (ESTIMATE CITED BY CRS)", scale=1.5),
              it("letters", x=960, y=700, text="MOSTLY FROM CREDIT CARDS", at=C("And most of that"), size=56, color="gold")]},
    sources=["crs"])
kinetic("s10_t1", "m1_transition", [("Way 1: a toll on every payment", 56, "the first way", None, True), ("…and the toll road is very profitable", 50, "extraordinarily profitable", "gold", False)])

# ====================================================================== PART 2: the toll road (toll booth + charts)
card("s11_c2", "m2_card", "The Toll Road", "Visa and Mastercard")
stage("s12_networks", "m2_networks", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In its latest financial year"), "x": 1200, "y": 500, "zoom": 1.05, "dur": 1.5}], "drift": 1,
    "items": [it("tollbooth", x=1000, at=0.2, fee="NETWORK TOLL", rate=1.2, scale=0.9),
              it("letters", x=1000, y=150, text="NO LOANS · NO INTEREST · JUST THE NETWORK", at=C("It runs the network"), size=40, color="gold"),
              it("counter", x=1650, y=300, at=C("In its latest financial year"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "net revenue of", "offset": 1}, 45.9]], text="VISA NET REVENUE")]},
    sources=["visa"])
stage("s13_margin", "m2_margin", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "VISA", "value": 61.2, "color": "#2F6FD1", "at": C("By our calculation"), "display": "≈61%", "sub": "our calculation"},
                     {"label": "MASTERCARD", "value": 57.6, "color": "#E89A00", "at": C("Mastercard, the second network"), "display": "57.6%", "sub": "FY2025, reported"}],
                    at=0.2, max=70, dark=True, title="OPERATING MARGIN", x=520, w=880)]},
    sources=["visa", "mastercard"])
stage("s14_incentives", "m2_incentives", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Those incentives"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("tollbooth", x=700, at=0.2, fee="NETWORK", rate=1.0, scale=0.7),
              it("coins", **{"from": [800, 400], "to": [1700, 350]}, at=C("client incentives"), rate=6),
              it("tower", x=1750, at=0.3, text="BANKS", scale=0.8, color="#1565C0"),
              it("counter", x=1250, y=180, at=C("it reported about"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in client incentives", "offset": 0}, 18.3]], text="VISA CLIENT INCENTIVES")]},
    sources=["visa"])
add("p15_network", "m2_draw", "engine_draw", {
    "title": "Why a network wins", "board": BOARD, "draw_start": C("Here is one card user"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 180, 90), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is one card user"), "label": lbl("USER", 650, 413, 24, "accent2")},
        {"d": rect(1260, 360, 180, 90), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is one store"), "label": lbl("STORE", 1350, 413, 24, "accent3")},
        {"d": arrow((750, 405), (1250, 405), 0.0), "color": "ink", "width": 4, "start": C("Connect them")},
        {"d": "M 560 520 L 740 520 M 560 580 L 740 580 M 560 640 L 740 640 M 1260 520 L 1440 520 M 1260 580 L 1440 580 M 1260 640 L 1440 640", "color": "ink", "width": 5, "start": C("Add more users")},
        {"d": rect(880, 520, 240, 140), "color": "accent", "width": 7, "kind": "box", "start": C("The network becomes a toll road"), "label": lbl("NETWORK", 1000, 598, 30, "accent")},
        {"d": "M 740 580 L 880 590 M 1260 580 L 1120 590", "color": "accent", "width": 5, "start": C("nearly every payment has to use")},
        {"d": "M 1000 680 L 1000 780", "color": "risk", "width": 6, "start": C("And the toll is a small percentage"), "label": lbl("% OF EVERY SALE", 1000, 820, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("And the toll is a small percentage", 0.3), "dur": 1.4, "target": [1000, 590]}],
    "scale": 0.86, "floor": 1040}, sources=["crs", "visa"])
kinetic("s16_t2", "m2_transition", [("Way 2: the banks", 66, "the second business", None, False), ("Interest.", 90, "Interest", "risk", False)])

# ====================================================================== PART 3: the interest machine (night district + charts)
card("s17_c3", "m3_card", "The Interest Machine", "Balances, rates, margins")
stage("s18_balances", "m3_balances", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And more than eight in ten"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("counter", x=900, y=250, at=0.3, prefix="$", suffix=" TRILLION", decimals=2, steps=[[0, 0], [{"cue": "in the middle of", "offset": 0}, 1.26]], text="US CARD BALANCES, Q2 2026 (NY FED)", scale=1.2),
              *crowd([1300 + 70 * k for k in range(10)], "walk", at=C("And more than eight in ten"), scale=0.5),
              it("letters", x=1600, y=460, text="82% OF ADULTS HAVE A CARD", at=C("And more than eight in ten", 0.5), size=48, color="gold")]},
    sources=["nyfed", "shed"])
stage("s19_apr", "m3_apr", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2021 AVERAGE", "value": 16.45, "color": "#90A4AE", "at": 0.5, "display": "16.45%"},
                     {"label": "LATEST (Q3 2026)", "value": 22.36, "color": "#E53935", "at": C("Its latest reading"), "display": "22.36%"}],
                    at=0.2, max=26, dark=True, title="AVERAGE CARD APR, ACCOUNTS PAYING INTEREST (FED G.19)", x=520, w=880)]},
    sources=["g19"])
stage("s20_margin", "m3_margin", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By its estimate"), "x": 1300, "y": 520, "zoom": 1.05, "dur": 1.5}], "drift": 2,
    "items": [it("docs", x=800, y=560, at=0.3, text="CFPB · APR MARGIN", scale=0.7, stamp="RECORD HIGH", stampAt=C("to the highest level")),
              it("letters", x=1450, y=230, text="+4.3 POINTS IN A DECADE", at=C("had grown by"), size=56, color="risk"),
              it("counter", x=1500, y=420, at=C("By its estimate"), prefix="+$", suffix="BN", steps=[[0, 0], [{"cue": "in extra interest", "offset": 0}, 25]], text="EXTRA INTEREST, ONE YEAR (CFPB EST.)")]},
    sources=["cfpb_margin"])
stage("s21_bill", "m3_bill", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2022", "value": 105, "color": "#90A4AE", "at": 0.5, "display": "$105bn"},
                     {"label": "2024", "value": 160, "color": "#E53935", "at": C("Two years later"), "display": "$160bn"}],
                    at=0.2, max=180, title="CARD INTEREST CHARGED (CFPB)", x=520, w=880),
              it("letters", x=1500, y=170, text="+$55BN", at=C("more than fifty billion"), size=90, color="risk")]},
    sources=["cfpb_2025"])
stage("s22_who", "m3_who", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 0.95}], "drift": 1,
    "items": [*crowd([500 + 80 * k for k in range(5)], "worry", at=0.3, scale=0.6),
              it("sign", x=660, y=300, text="CARRIED A BALANCE", sub="45% of card owners (Fed)", at=C("of card owners said"), color="#FFCDD2", size=36),
              *crowd([1300 + 80 * k for k in range(6)], "cheer", at=0.3, scale=0.6),
              it("sign", x=1500, y=300, text="PAY IN FULL", sub="no interest at all", at=C("The rest pay in full"), color="#C8E6C9", size=36)]},
    sources=["shed"])
add("p23_twousers", "m3_draw", "engine_draw", {
    "title": "Same card, two deals", "board": BOARD, "draw_start": C("On one side"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 400, 300, 130), "color": "accent3", "width": 6, "kind": "box", "start": C("On one side"), "label": lbl("PAY IN FULL", 710, 473, 26, "accent3")},
        {"d": "M 600 600 L 820 600", "color": "accent3", "width": 5, "start": C("a free short-term loan"), "label": lbl("free loan + rewards", 710, 640, 22, "accent3")},
        {"d": rect(1140, 400, 300, 130), "color": "risk", "width": 6, "kind": "box", "start": C("On the other side"), "label": lbl("CARRY A BALANCE", 1290, 473, 24, "risk")},
        {"d": "M 1180 600 L 1400 600", "color": "risk", "width": 6, "start": C("They pay over twenty percent"), "label": lbl("20%+ a year", 1290, 640, 24, "risk")},
        {"d": "M 1000 360 L 1000 760", "color": "ink", "width": 3, "start": C("The same plastic")},
    ],
    "actions": [{"kind": "point", "at": C("Two completely different deals", 0.2), "dur": 1.4, "target": [1290, 470]}],
    "scale": 0.86, "floor": 1040}, sources=["shed", "g19"])
kinetic("s24_t3", "m3_transition", [("If rewards are free…", 64, "If the people who pay in full", None, True), ("who pays for them?", 72, "who is paying for those rewards", "gold", False)])

# ====================================================================== PART 4: who pays for your rewards (airport + evidence board)
card("s25_c4", "m4_card", "Who Pays for Your Rewards", "Points, cash back, miles")
stage("s26_rewards", "m4_rewards", {
    "zones": [Z("airport", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Almost all card spending"), "x": 1300, "y": 500, "zoom": 1.0, "dur": 1.5}], "drift": 3,
    "items": [it("plane", x=[[0, 400], [10, 1600]], y=[[0, 600], [10, 300]], at=0.2, text="POINTS", tilt=-10),
              it("counter", x=1000, y=200, at=C("consumers earned more than"), prefix="> $", suffix="BN", steps=[[0, 0], [{"cue": "in rewards", "offset": 0}, 40]], text="REWARDS EARNED, 2022 (CFPB)"),
              it("letters", x=1500, y=480, text="92% OF CARD SPENDING ON REWARDS CARDS", at=C("Almost all card spending"), size=40, color="gold")]},
    sources=["cfpb_rewards", "cfpb_2025"])
stage("s27_funded", "m4_funded", {
    "zones": [Z("shop", label="STORE")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In other words"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("terminal", x=800, y=F, at=0.2, text="FEE 1.8%", scale=0.9),
              it("coins", **{"from": [850, 450], "to": [1700, 350]}, at=C("issuers typically fund rewards"), rate=6),
              card_(1700, 420, at=0.3, scale=0.55, text="REWARDS"),
              it("letters", x=1250, y=160, text="REWARDS ≈ 9/10 OF INTERCHANGE", at=C("rewards made up almost"), size=48, color="gold")]},
    sources=["cfpb_2023"])
stage("s28_amex", "m4_amex", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "FEES FROM MERCHANTS", "value": 37.4, "color": "#23995A", "at": C("it collected about"), "display": "$37.4bn"},
                     {"label": "REWARDS PAID", "value": 18.4, "color": "#E89A00", "at": C("American Express spent about"), "display": "$18.4bn"}],
                    at=0.2, max=42, title="AMERICAN EXPRESS, 2025 (WORLDWIDE, 10-K)", x=520, w=880)]},
    sources=["amex"])
stage("s29_prices", "m4_prices", {
    "zones": [Z("shop", label="STORE")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So a customer paying with cash"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("pricetag", x=800, y=320, at=0.3, text="PRICE", pages=[[{"cue": "costs end up in prices"}, "PRICE + FEE", True]], scale=1.0),
              it("person", x=1400, pose="shrug", at=C("So a customer paying with cash"), scale=0.8, hair=4, skin=3),
              it("letters", x=1650, y=260, text="CASH PAYER → HELPS FUND POINTS?", at=C("may be helping"), size=42, color="gold")]},
    sources=["crs"])
stage("s30_revolvers", "m4_revolvers", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.1}, {"at": C("Not everyone agrees"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 650, "y": 380, "text": "PAY 94%", "sub": "of interest and fees (balance carriers)", "at": 0.3, "w": 420, "color": "#FFCDD2", "size": 52},
                {"x": 1550, "y": 380, "text": "GET < 30%", "sub": "of rewards", "at": C("but receive less than"), "w": 360, "color": "#C8E6C9", "size": 52},
                {"x": 1100, "y": 680, "text": "DEBATED", "sub": "a Fed staff paper challenges the framing", "at": C("Not everyone agrees"), "w": 520, "size": 40}],
              links=[[0, 1, C("but receive less than", 0.4)], [1, 2, C("Not everyone agrees", 0.4)]])]},
    sources=["cfpb_rewards"])
add("p31_loop", "m4_draw", "engine_draw", {
    "title": "The rewards loop", "board": BOARD, "draw_start": C("Money comes in from two places"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 340, 260, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("Swipe fees"), "label": lbl("SWIPE FEES", 670, 403, 24, "accent3")},
        {"d": rect(540, 620, 260, 110), "color": "risk", "width": 6, "kind": "box", "start": C("And interest and fees"), "label": lbl("INTEREST + FEES", 670, 683, 22, "risk")},
        {"d": rect(880, 480, 240, 120), "color": "ink", "width": 6, "kind": "box", "start": C("Money comes in from two places"), "label": lbl("BANK", 1000, 548, 28, "ink")},
        {"d": arrow((810, 400), (880, 500), 0.0), "color": "accent3", "width": 5, "start": C("paid by every store")},
        {"d": arrow((810, 680), (880, 590), 0.0), "color": "risk", "width": 5, "start": C("paid mostly by people")},
        {"d": rect(1200, 480, 260, 120), "color": "accent", "width": 6, "kind": "box", "start": C("Money goes out as rewards"), "label": lbl("REWARDS", 1330, 548, 26, "accent")},
        {"d": arrow((1130, 540), (1190, 540), 0.0), "color": "accent", "width": 6, "start": C("Money goes out as rewards", 0.4)},
    ],
    "actions": [{"kind": "point", "at": C("keeps what is left", 0.2), "dur": 1.4, "target": [1000, 540]}],
    "scale": 0.86, "floor": 1040}, sources=["cfpb_rewards", "cfpb_2023"])
kinetic("s32_t4", "m4_transition", [("One more source of money", 60, "one more source", None, False), ("Missing a payment", 64, "when you miss a payment", "risk", False)])

# ====================================================================== PART 5: the fees (office + courtroom)
card("s33_c5", "m5_card", "The Fees", "Late fees and bad debt")
stage("s34_late", "m5_late", {
    "zones": [Z("office")], "worldW": 2000,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": 2.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 1,
    "items": [it("calendar", x=700, y=320, at=0.2, pages=[[0, "DUE", "TODAY"], [1.5, "LATE", "+FEE"]], scale=0.9),
              it("counter", x=1300, y=300, at=0.4, prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in late fees", "offset": 0}, 17.0]], text="LATE FEES, BIG ISSUERS, 2024 (CFPB)"),
              it("letters", x=1300, y=520, text="+17% IN TWO YEARS", at=C("up seventeen percent"), size=56, color="risk")]},
    sources=["cfpb_2025"])
stage("s35_rule", "m5_rule", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Business and banking groups"), "x": 1400, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("pricetag", x=800, y=330, at=0.3, pages=[[0, "$32"], [{"cue": "to eight"}, "$8"]], scale=1.0),
              it("gavel", x=1500, y=420, hits=[C("it was vacated", 0.3)]),
              it("docs", x=1800, y=560, at=C("Business and banking groups"), text="LATE-FEE RULE", scale=0.6, stamp="VACATED", stampAt=C("it was vacated", 0.5)),
              it("calendar", x=1150, y=280, at=C("on April fifteenth"), pages=[[0, "APR 15", "2025"]], scale=0.7)]},
    sources=["cfpb_late", "cfpb_vacated"])
stage("s36_risk", "m5_risk", {
    "zones": [Z("district", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("When that happens"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.5}], "drift": 1,
    "items": [it("counter", x=1000, y=260, at=0.3, suffix="%", decimals=2, steps=[[0, 0], [{"cue": "into serious delinquency", "offset": 0}, 6.97]], text="CARD BALANCES ENTERING 90+ DAYS LATE (ANNUALIZED, NY FED)"),
              it("stack", x=1500, h=[[0, 80], [{"cue": "keep piling up", "offset": 1}, 380]], at=C("When that happens"), text="INTEREST + FEES", color="#C62828")]},
    sources=["nyfed"])
stage("s37_distress", "m5_distress", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "LATE 2022", "value": 7.6, "color": "#90A4AE", "at": 0.5, "display": "7.6%"},
                     {"label": "EARLY 2026", "value": 12.8, "color": "#E53935", "at": C("to twelve point eight"), "display": "12.8%"}],
                    at=0.2, max=15, dark=True, title="SHARE OF CARD BALANCES 90+ DAYS LATE (NY FED)", x=420, w=760),
              it("letters", x=1550, y=420, text="23M+ AMERICANS", at=C("still carry card debts"), size=56, color="gold"),
              it("letters", x=1550, y=500, text="WITH WRITTEN-OFF CARD DEBT", at=C("already written off"), size=32, color="white")]},
    sources=["libst"])
add("p38_three", "m5_draw", "engine_draw", {
    "title": "Three streams, one card", "board": BOARD, "draw_start": C("The toll on every swipe"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("The toll on every swipe")},
        {"d": "M 640 860 L 640 560 L 800 560 L 800 860", "color": "accent3", "width": 6, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("collected by the networks"), "label": lbl("SWIPE ≈$160bn*", 720, 540, 22, "accent3")},
        {"d": "M 920 860 L 920 560 L 1080 560 L 1080 860", "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("The interest, paid by"), "label": lbl("INTEREST $160bn", 1000, 540, 22, "risk")},
        {"d": "M 1200 860 L 1200 800 L 1360 800 L 1360 860", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("And the fees, paid by"), "label": lbl("LATE FEES $17bn", 1280, 780, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("all flowing through the same small card", 0.2), "dur": 1.4, "target": [1000, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["crs", "cfpb_2025"])

# ====================================================================== PAYOFF
stage("s39_payoff", "payoff", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.1}, {"at": C("If you pay in full"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [card_(960, 420, at=0.2, scale=1.1, rot=-4),
              it("letters", x=960, y=150, text="IT'S NOT THE PLASTIC. IT'S THE POSITION.", at=C("It is not the plastic"), size=54, color="gold"),
              it("letters", x=520, y=820, text="PAY IN FULL: CAN WORK FOR YOU", at=C("If you pay in full"), size=40, color="green"),
              it("letters", x=1400, y=820, text="CARRY A BALANCE: YOU PAY", at=C("If you carry a balance"), size=40, color="risk")]},
    sources=["crs", "cfpb_2025", "cfpb_rewards"])
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_creditcard_storyboard.py; edit the generator, not this file.\n"
           "# Episode 30 storyboard (the credit card business): one visual language per part; tones from visual_direction.yaml.\n")
