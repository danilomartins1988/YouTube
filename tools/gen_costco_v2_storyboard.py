"""Generates projects/how-costco-makes-billions-selling-almost-nothing/deliverables/documentary/storyboard.yaml
(Episode 57: How Costco Makes Billions Selling Almost Nothing; supersedes Ep 32).

OWNER DIRECTION: as animated as possible, in the style of a prime-time animated TV sitcom. Genre level only; everything original.
TV structure: cold open (10 a.m. rush to the food court) -> channel intro (our "theme") -> show TITLE CARD ("THE CLUB") with a
typed joke subtitle -> five acts, each opened by a BUMPER with a joke caption -> payoff -> end card -> BUTTON joke.
RUNNING GAG: the food-court board says $1.50; every bumper someone tries to change it (ladder, crane, drone, sticker, robot arm)
and fails ("NOPE."); in the button it finally "changes"... to $1.50.
Recurring cast (CartoonStage/sitcom.tsx `toon` rig + costco.tsx): BEV (membership clerk), HANK (bulk-buying dad), PEARL
(sample lady), SKIP (food-court teen), CARDIE (walking membership card), LIFT (forklift), BUZZ (drone).
Real people (respectful caricatures, CARI presets 'vachris' and 'sinegal', name labels): Ron Vachris holding his shareholder
letter (a3_kirk), Jim Sinegal at the food court (a4_sinegal). Nothing else is attributed to them.
Bespoke sets (new, costco.tsx): clubfloor, memberdesk, foodcourt, housebrand, treasureaisle, loadingdock, gasbar, seattle83,
cashvault, clubtitle, clubbumper. Signature animations: the cold-open food-court stampede (s01), the $100 receipt (s07), the
membership desk card printer + renewal screen (s12-s13), the treasure-hunt turntable (s22), the house-brand labeller (s23),
the loading-dock day clock (s32), the dividend vault chute (s37). Presenter boards: p08 ($100 split, bars), p14 (fee history,
bars), p25 (the squeeze: boxes + arrows), p33 (cash clock timeline), p39 (the machine loop).
No logos; jokes never change a number. Run: python tools/gen_costco_v2_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

ROOT = Path(__file__).resolve().parents[1]
PROJ = ROOT / "projects/how-costco-makes-billions-selling-almost-nothing"
OUT = PROJ / "deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35


def toon(who, x, at=0.0, **kw):
    if "xk" in kw:
        x = kw.pop("xk")
    kw.setdefault("scale", 1.3)
    return it("toon", who=who, x=x, at=at, **kw)


BEV = lambda x=None, at=0.0, **kw: toon("bev", x, at, **kw)
HANK = lambda x=None, at=0.0, **kw: toon("hank", x, at, **kw)
PEARL = lambda x=None, at=0.0, **kw: toon("pearl", x, at, **kw)
SKIP = lambda x=None, at=0.0, **kw: toon("skip", x, at, **kw)
S = lambda v, x, at=0.0, **kw: toon("shopper", x, at, v=v, **{"scale": 1.15, **kw})


def CARD(x, at=0.0, **kw):
    kw.setdefault("scale", 1.0)
    return it("cardie", x=x, at=at, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def chart(bars_, at=0.2, **kw):
    kw.setdefault("panel", True)
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


def bumper(id_, seg, num, act, title, caption, gag, color="#2F6FD1", cast=None):
    items = cast or []
    stage(id_, seg, {**W1("clubbumper", num=num, act=act, title=title, caption=caption, color=color, gag=gag), "cam": STILL(), "drift": 0,
                     "tone": "sitcom", "min_seconds": 4.2, "items": items},
          sfx=[{"kind": "whoosh", "at": 0.05, "gain": 0.25}, {"kind": "hit", "at": 0.25, "gain": 0.3}, {"kind": "hit", "at": 2.3, "gain": 0.35}])


# ====================================================================== COLD OPEN (10 a.m., the food-court rush)
stage("s01_open", "co_open", {
    **W1("clubfloor", regX=-900, sampleX=2700, signs=["AISLE 1", "TVs", "BULK", "FOOD COURT →", "PALLETS"]),
    "cam": cam((0, 1100, 380, 1.0), (C("A giant box"), 1000, 420, 0.9, 2.4), (C("The doors open"), 900, 520, 1.05, WHIP),
               (C("right past the televisions"), 1300, 540, 1.05, 1.6), (C("Price?"), 1500, 520, 1.35, WHIP), (C("Reportedly"), 1450, 500, 1.15, 1.4)),
    "drift": 3,
    "items": [it("toonwords", text="10:00 A.M.", x=1100, y=150, at=0.2, until=C("A giant box", 0.8), size=90),
              sign("NO WINDOWS · CONCRETE FLOORS · STEEL RACKS", 1000, 110, C("A giant box"), color="#FFF8E1", size=28, until=C("The doors open", -0.2)),
              it("stampede", at=C("The doors open", 0.2), x0=-300, x1=2300, n=16, dur=3.4, scale=0.95, until=C("Price?", -0.3)),
              HANK([[0, 300], [C("The doors open"), 300], [C("for a hot dog"), 1250]], 0.3, hold="bigpack", packText="TV 75\"",
                   face="grin", faces=[[0, "grin"], [C("right past the televisions"), "dollar"]], label="HANK · BULK BUYER", labelUntil=C("The doors open", 1.2)),
              PEARL(2050, C("A giant box", 0.5), hold="tray", face="happy", faces=[[0, "happy"], [C("The doors open", 0.4), "shock"]], takes=[C("The doors open", 0.4)],
                    label="PEARL · SAMPLES", labelUntil=C("half the crowd")),
              it("combo", x=1500, y=330, at=C("for a hot dog"), price="$1.50", scale=0.8, boing=[C("Price?", 0.3)], face="happy"),
              sign("REPORTEDLY SINCE 1985 (CNN)", 1500, 640, C("Reportedly"), color="#FFE0B2", size=30),
              CARD(700, 0.4, face="deadpan", faces=[[0, "deadpan"], [C("Price?"), "dollar"]], label="CARDIE", labelUntil=C("The doors open"), hops=[C("Price?", 0.4)])]},
    sources=["cnn_hotdog"], sfx=[{"kind": "hit", "cue": "The doors open", "gain": 0.3}, {"kind": "hit", "cue": "Price?", "gain": 0.3}])
stage("s02_hook", "co_hook", {
    **W1("foodcourt", boardX=1100, tablesX=[150, 2050]),
    "cam": cam((0, 1100, 470, 0.95), (C("But on the goods"), 1050, 500, 1.05, 1.4), (C("So where do"), 1100, 520, 1.3, WHIP)), "drift": 4,
    "items": [it("counter", x=650, y=560, at=C("Costco sold"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [C("Costco sold"), 0], [C("worth of goods"), 297.2]],
                 text="NET SALES · FISCAL 2026", until=C("So where do", -0.2)),
              it("counter", x=1550, y=560, at=C("and earned"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [C("and earned"), 0], [C("But on the goods", -0.3), 9.2]],
                 text="NET INCOME · FISCAL 2026", until=C("So where do", -0.2)),
              HANK(250, 0.2, face="grin", hold="bigpack", packText="x30", faces=[[0, "grin"], [C("So where do"), "worry"]]),
              SKIP(1950, 0.3, hold="hotdog", face="happy", faces=[[0, "happy"], [C("it makes almost nothing"), "shock"]], takes=[C("it makes almost nothing")]),
              it("toonwords", text="ALMOST NOTHING?!", x=1100, y=420, at=C("it makes almost nothing"), until=C("So where do", -0.1), size=80, color="#FFFFFF"),
              it("toonwords", text="WHERE'S THE MONEY?", x=1100, y=330, at=C("So where do"), size=90)]},
    sources=["results", "tenk"])
stage("s03_promise", "co_promise", {
    **W1("clubfloor", regX=1700, sampleX=500, signs=["THE TOUR", "AISLE 1", "AISLE 2"]),
    "cam": cam((0, 1000, 480, 1.0), (C("a very short shopping list"), 1150, 480, 1.0, 1.4), (C("the money Costco holds"), 1300, 470, 1.0, 1.2)), "drift": 6,
    "items": [it("toonwords", text="FOLLOW THE MONEY", x=1000, y=110, at=0.2, size=70, until=C("the money Costco holds", -0.2)),
              sign("1 · THE THINNEST MARGIN", 600, 330, C("The thinnest margin"), color="#FFCDD2", size=30),
              sign("2 · A PLASTIC CARD", 1000, 230, C("a plastic card"), color="#BBDEFB", size=30),
              sign("3 · A SHORT LIST", 1400, 330, C("a very short shopping list"), color="#C8E6C9", size=30),
              sign("4 · A CHEAP HOT DOG", 1000, 430, C("a very cheap hot dog"), color="#FFF59D", size=30),
              sign("5 · MONEY BEFORE PAYING", 1500, 140, C("the money Costco holds"), color="#E1BEE7", size=30),
              it("feeflow", **{"from": [1700, 650], "to": [2300, 200]}, at=C("the money Costco holds"), n=6),
              CARD([[0, -300], [C("a plastic card"), 900]], C("a plastic card", -0.6), face="happy", scale=0.8),
              PEARL(500, 0.3, hold="tray", face="grin", pose="talk", talk=[[0.2, C("a plastic card")]])]},
    sfx=[{"kind": "whoosh", "cue": "a plastic card", "gain": 0.2}])
stage("s04_title", "title_card", {
    **W1("clubtitle", title="THE CLUB", sub="HOW COSTCO MAKES BILLIONS SELLING ALMOST NOTHING",
         subs=[[2.4, "Tonight: “Membership Has Its Pallets”"]]), "cam": STILL(), "drift": 0, "min_seconds": 6.2,
    "items": [it("toonwords", text="★ ★ ★", x=960, y=980, at=0.0, size=60, until=1.6),
              HANK(250, 2.6, scale=1.15, face="dollar", pose="cheer", hops=[3.0, 4.4]), BEV(1690, 2.8, scale=1.15, face="grin", pose="wave"),
              CARD(1480, 3.2, scale=0.8, face="happy", hops=[3.8, 5.0])]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}, {"kind": "hit", "at": 1.4, "gain": 0.3}])

# ====================================================================== ACT 1: the thinnest margin
bumper("s05_b1", "a1_card", "1", "ACT ONE", "THE THINNEST MARGIN", "Some assembly required. Mostly by you.", "ladder", "#E53950",
       cast=[HANK(xk=[[0.8, -200], [3.8, 2300]], at=0.8, y=1060, scale=0.8, hold="bigpack", face="grin", pose="run")])
stage("s06_size", "a1_size", {
    **W1("seattle83", whX=0.42), "tone": "history", "toneShift": {"at": C("Net sales grew"), "to": "sitcom", "dur": 0.6},
    "cam": cam((0, 1000, 520, 1.0), (C("By the end of fiscal"), 1150, 470, 0.92, 1.8), (C("Net sales grew"), 1100, 460, 1.0, WHIP)), "drift": 6,
    "items": [it("calendar", x=1750, y=260, at=0.3, pages=[[0, "1983"]], text="SEATTLE", scale=0.8, until=C("By the end of fiscal")),
              it("counter", x=1100, y=120, at=C("it ran"), steps=[[0, 0], [C("it ran"), 0], [C("warehouses, and today"), 939], [C("today it has"), 939], [C("from Iceland"), 945]],
                 text="WAREHOUSES · FY-END 939 → NOV 2026 945", scale=0.9),
              sign("ICELAND → NEW ZEALAND", 1650, 330, C("from Iceland"), color="#FFF8E1", size=30),
              it("toonwords", text="NET SALES ≈ +10%", x=1100, y=320, at=C("Net sales grew"), size=80),
              S(2, [[0, 300], [C("Net sales grew"), 900]], 0.4, hold="bag", face="happy"),
              S(5, [[0, 1900], [C("Net sales grew"), 1400]], 0.5, hold="box", face="grin")]},
    sources=["tenk", "div8k", "results"])
stage("s07_margin", "a1_margin", {
    **W1("clubfloor", regX=1150, sampleX=-900),
    "cam": cam((0, 1000, 480, 1.0), (C("By our calculation"), 1050, 470, 1.0, 1.4), (C("Costco's own annual report"), 1100, 500, 1.1, WHIP)), "drift": 3,
    "items": [it("receipt", x=500, y=80, at=0.3, title="ONE $100 BASKET", lines=[[C("Gross margin"), "GOODS (SUPPLIER)", "$88.91"], [C("of sales"), "GROSS MARGIN", "$11.09"]],
                 totalAt=C("of sales", 0.6), total="$100.00", scale=0.9),
              it("toonwords", text="GROSS MARGIN 11.1%", x=1250, y=150, at=C("of sales", -0.3), size=70, until=C("By our calculation", -0.2)),
              it("toonwords", text="MARKUP ≈ 12.5%", x=1300, y=150, at=C("By our calculation"), size=74, color="#FFFFFF", until=C("Costco's own annual report", -0.1)),
              sign("OUR CALCULATION · FISCAL 2026 10-K", 1300, 280, C("By our calculation", 0.4), color="#FFE0B2", size=26, until=C("Costco's own annual report", -0.1)),
              sign("'SIGNIFICANTLY LOWER GROSS MARGINS ... THAN MOST OTHER RETAILERS'", 1150, 150, C("Costco's own annual report"), color="#FFF8E1", size=26, sub="COSTCO 10-K, FISCAL 2026"),
              CARD(1850, 0.4, face="deadpan", faces=[[0, "deadpan"], [C("Costco's own annual report"), "wink"]]),
              HANK(1600, 0.2, hold="bigpack", packText="x30", face="happy", pose="stand")]},
    sources=["tenk", "results"])
add("p08_hundred", "a1_draw", "engine_draw", {
    "title": "Where $100 at the register goes (fiscal 2026, our calculation)", "board": BOARD, "draw_start": C("Let me draw"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 800 L 1500 800", "color": "ink", "width": 5, "start": C("Let me draw")},
        {"d": "M 660 800 L 660 430 L 860 430 L 860 800 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("About eighty-nine dollars"), "label": lbl("GOODS · ≈ $89", 760, 410, 24, "accent2")},
        {"d": "M 920 800 L 920 756 L 1120 756 L 1120 800 Z", "color": "accent", "width": 3, "fill": "accent", "fillOpacity": 0.35, "kind": "bar", "start": C("That leaves about eleven"), "label": lbl("GROSS MARGIN · ≈ $11", 1020, 736, 22, "accent")},
        {"d": "M 1180 800 L 1180 764 L 1380 764 L 1380 800 Z", "color": "muted", "width": 3, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("Around nine of those"), "label": lbl("STORES · STAFF · TRUCKS ≈ $9", 1280, 700, 20, "muted")},
        {"d": "M 1420 800 L 1420 792 L 1490 792 L 1490 800 Z", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.5, "kind": "bar", "start": C("is about two dollars"), "label": lbl("≈ $2", 1455, 770, 26, "risk")},
        {"d": dot(1050, 330), "color": "risk", "width": 1, "start": C("Two dollars, out of a hundred"), "label": lbl("$2 OF $100 FROM THE GOODS (BEFORE FEES)", 1050, 330, 26, "risk")},
        {"d": dot(1050, 860), "color": "muted", "width": 1, "start": C("by our calculation"), "label": lbl("10-K FISCAL 2026 · NET SALES SPLIT · OUR CALCULATION", 1050, 860, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("is about two dollars", 0.3), "dur": 1.6, "target": [1455, 790]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])
stage("s09_fees", "a1_fees", {
    **W1("memberdesk", deskX=1150, feeText="$65 / YEAR", screen="$5.9BN", screenTop="FEES · FISCAL 2026"),
    "cam": cam((0, 1150, 470, 0.95), (C("That's equal to"), 1100, 470, 1.0, 1.4), (C("But they arrive"), 1150, 500, 1.15, WHIP)), "drift": 3,
    "items": [it("counter", x=1100, y=170, at=C("Membership fees"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [C("Membership fees"), 0], [C("in a single year"), 5.9]],
                 text="MEMBERSHIP FEES · FISCAL 2026", until=C("That's equal to", -0.1)),
              it("toonwords", text="≈ HALF OF OPERATING INCOME", x=1100, y=330, at=C("That's equal to"), size=60, until=C("Fees have their own costs", -0.1)),
              sign("$5.9BN VS $11.7BN · 'EQUAL TO', OUR CALCULATION", 1100, 450, C("That's equal to", 0.5), color="#FFE0B2", size=26, until=C("Fees have their own costs", -0.1)),
              sign("FEES HAVE THEIR OWN COSTS", 1100, 380, C("Fees have their own costs"), color="#FFF8E1", size=32, until=C("But they arrive", -0.1)),
              it("feeflow", **{"from": [400, 700], "to": [1150, 500]}, at=C("But they arrive"), n=8, per=1.0),
              BEV(1150, 0.3, face="happy", pose="talk", talk=[[C("Membership fees"), C("in a single year", 0.6)]], label="BEV · MEMBERSHIP DESK", labelUntil=C("That's equal to")),
              HANK(500, C("But they arrive", -0.4), hold="membercard", face="grin", pose="stand", xk=[[C("But they arrive", -0.4), 300], [C("But they arrive", 1.2), 700]])]},
    sources=["tenk"])
stage("s10_turn", "a1_turn", {
    **W1("clubfloor", regX=-900, sampleX=-900),
    "cam": cam((0, 1100, 500, 1.0), (C("The real business"), 600, 500, 1.4, WHIP)), "drift": 3,
    "items": [it("toonwords", text="BREAK-EVEN MACHINE", x=1150, y=200, at=C("almost a break-even"), until=C("The real business"), size=70),
              CARD([[0, 1400], [C("The real business"), 1400], [C("by the front door"), 600]], 0.3, face="wink", faces=[[0, "deadpan"], [C("The real business"), "wink"]]),
              sign("→ THE MEMBERSHIP DESK", 600, 260, C("a little desk"), color="#BBDEFB", size=34),
              PEARL(1900, 0.3, hold="tray", face="smug")]})

# ====================================================================== ACT 2: the membership desk
bumper("s11_b2", "a2_card", "2", "ACT TWO", "THE MEMBERSHIP DESK", "Please have your card ready. And your other card.", "crane", "#2F6FD1",
       cast=[CARD([[0.8, -200], [3.8, 2300]], at=0.8, y=1060, scale=0.6, face="happy")])
stage("s12_members", "a2_members", {
    **W1("memberdesk", deskX=1150, printAt=C("paid members", -1.5), flashAt=[C("you need a card", 0.2)], screen="84.1M", screenTop="PAID MEMBERS"),
    "cam": cam((0, 1150, 480, 1.0), (C("cardholders"), 1300, 470, 1.0, 1.4), (C("In the United States"), 1100, 470, 0.95, 1.6)), "drift": 3,
    "items": [BEV(1150, 0.2, face="grin", pose="talk", talk=[[0.3, C("you need a card", 0.8)]]),
              S(4, [[0, -200], [C("you need a card"), 450]], 0.2, face="happy", hold="membercard"),
              it("counter", x=1150, y=360, at=C("Costco had"), suffix="M", decimals=1, steps=[[0, 0], [C("Costco had"), 0], [C("paid members"), 84.1], [C("cardholders", -1.2), 84.1], [C("cardholders"), 150.4]],
                 text="PAID MEMBERS → CARDHOLDERS (10-K)", until=C("In the United States", -0.1)),
              it("membercard", x=1150, y=330, at=C("In the United States"), back="$65 A YEAR", backSub="+ A FREE HOUSEHOLD CARD", flipAt=C("sixty-five dollars"), scale=0.62)]},
    sources=["tenk"])
stage("s13_renew", "a2_renew", {
    **W1("memberdesk", deskX=1150, screen="92.3%", screenTop="RENEWALS · U.S. & CANADA"),
    "cam": cam((0, 1500, 450, 1.05), (C("That's a fee"), 1150, 480, 0.95, 1.6), (C("more than nine out of ten"), 1150, 470, 1.1, WHIP)), "drift": 3,
    "items": [sign("WORLDWIDE: 89.8%", 1770, 330, C("worldwide"), color="#FFF8E1", size=32),
              *[S(v, [[0, -300 - k * 160], [C("That's a fee", k * 0.15), 300 + k * 150]], 0.2, hold="membercard", face="happy" if k != 4 else "worry", scale=0.95) for k, v in enumerate([1, 2, 3, 6, 7, 8, 9, 10, 11, 12])],
              it("toonwords", text="9 OUT OF 10 COME BACK", x=1150, y=140, at=C("more than nine out of ten"), size=72),
              BEV(1150, 0.2, face="happy", pose="wave", faces=[[0, "happy"], [C("more than nine out of ten"), "grin"]], hops=[C("pay it again")])]},
    sources=["tenk"])
add("p14_fees", "a2_hist", "engine_draw", {
    "title": "U.S. basic membership fee (Gold Star)", "board": BOARD, "draw_start": C("Let me chart"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 800 L 1500 800", "color": "ink", "width": 5, "start": C("Let me chart")},
        {"d": "M 640 800 L 640 500 L 800 500 L 800 800 Z", "color": "muted", "width": 3, "fill": "muted", "fillOpacity": 0.25, "kind": "bar", "start": C("Fifty dollars"), "label": lbl("$50 · TO 2011", 720, 480, 22, "muted")},
        {"d": "M 860 800 L 860 470 L 1020 470 L 1020 800 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.25, "kind": "bar", "start": C("Then fifty-five"), "label": lbl("$55 · NOV 2011", 940, 450, 22, "accent2")},
        {"d": "M 1080 800 L 1080 440 L 1240 440 L 1240 800 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.35, "kind": "bar", "start": C("In twenty seventeen"), "label": lbl("$60 · JUN 2017", 1160, 420, 22, "accent2")},
        {"d": "M 1300 800 L 1300 410 L 1460 410 L 1460 800 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.35, "kind": "bar", "start": C("And in September"), "label": lbl("$65 · SEP 2024", 1380, 390, 22, "risk")},
        {"d": "M 720 330 L 1380 330", "color": "accent", "width": 5, "start": C("A small step"), "label": lbl("+$5 EVERY 6-7 YEARS", 1050, 310, 26, "accent")},
        {"d": dot(1050, 870), "color": "accent3", "width": 1, "start": C("renewal rates stayed"), "label": lbl("RENEWALS (U.S. & CANADA): 89.7% · 90% · 92.3%", 1050, 870, 22, "accent3")},
        {"d": dot(1050, 910), "color": "muted", "width": 1, "start": C("Let me chart", 1.0), "label": lbl("10-Ks FY2012, FY2017, FY2026 · 8-K JUL 2024 · BARS NOT TO SCALE FROM ZERO", 1050, 910, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("And in September", 0.5), "dur": 1.4, "target": [1380, 500]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk2012", "tenk2017", "fee2024", "tenk"])
stage("s15_raise", "a2_raise", {
    **W1("memberdesk", deskX=1150, feeText="$65 / YEAR", posterTop="SINCE SEP 2024", screen="≈ 52M", screenTop="MEMBERSHIPS AFFECTED"),
    "cam": cam((0, 1500, 460, 1.0), (C("The Executive card"), 1150, 470, 1.0, 1.4), (C("And Costco says"), 1100, 470, 1.0, 1.6)), "drift": 3,
    "items": [it("bigtag", x=1150, y=200, at=C("The Executive card"), was="$120 EXECUTIVE", now="$130", slashAt=C("to one hundred and thirty", -0.6), nowAt=C("to one hundred and thirty"), scale=0.85,
                 until=C("And Costco says", -0.1)),
              chart([{"label": "FEE INCREASE", "value": 30, "color": "#E53950", "at": C("only about thirty percent"), "display": "≈ 30%"},
                     {"label": "NEW MEMBERS + UPGRADES", "value": 70, "color": "#2E9E5B", "at": C("The rest came from"), "display": "≈ 70%"}],
                    at=C("And Costco says"), max=80, title="WHAT DROVE FEE-INCOME GROWTH, FISCAL 2026 (10-K)", x=360, y=230, w=900, h=420),
              BEV(1800, 0.2, face="smug", pose="talk", talk=[[C("That last increase"), C("memberships", 0.6)]], scale=1.25)]},
    sources=["fee2024", "tenk"])
stage("s16_deferred", "a2_deferred", {
    **W1("cashvault", vaultX=0.35, openAt=C("members had already handed over", -0.6), screen="≈ $3.0BN", screenTop="FEES PAID, NOT YET COUNTED"),
    "cam": cam((0, 700, 480, 1.05), (C("It spreads it"), 900, 470, 1.0, 1.4), (C("members had already"), 1250, 470, 0.95, 1.6)), "drift": 3,
    "items": [it("calendar", x=1150, y=280, at=C("It spreads it"), pages=[[C("It spreads it"), "JAN"], [C("It spreads it", 0.5), "MAR"], [C("It spreads it", 1.0), "JUN"], [C("It spreads it", 1.5), "SEP"], [C("It spreads it", 2.0), "DEC"]],
                 text="1/12 OF YOUR FEE A MONTH", scale=0.75, until=C("members had already", -0.2)),
              it("feeflow", **{"from": [300, 700], "to": [700, 430]}, at=C("members had already"), n=6, per=1.0),
              CARD(1950, 0.3, face="sleepy", faces=[[0, "sleepy"], [C("Next year's income"), "dollar"]], hops=[C("Next year's income")], say=[[C("And here's a quiet detail"), C("doesn't count", 0.4), "PSST."]]),
              sign("DEFERRED MEMBERSHIP FEES · AUG 30, 2026 (10-K)", 1500, 860, C("hadn't even counted"), color="#FFF8E1", size=24)]},
    sources=["tenk"])
stage("s17_exec", "a2_exec", {
    **W1("memberdesk", deskX=1150, feeText="$130 / YEAR", posterTop="EXECUTIVE", posterSub="≈ 2% BACK, CAPPED", screen="≈ 75%", screenTop="SHARE OF SALES"),
    "cam": cam((0, 1150, 470, 1.0), (C("There are about"), 1150, 470, 0.95, 1.4), (C("And they account"), 1700, 470, 1.15, WHIP)), "drift": 3,
    "items": [it("membercard", x=1150, y=320, at=0.2, title="EXECUTIVE", color="#1B2433", name="2% BACK · YEARLY CAP", scale=0.55, until=C("There are about", -0.1)),
              it("counter", x=1150, y=330, at=C("There are about"), suffix="M", decimals=1, steps=[[0, 0], [C("There are about"), 0], [C("of them"), 42.3]], text="EXECUTIVE MEMBERS · FISCAL 2026"),
              sign("≈ HALF OF PAID MEMBERS (OUR CALCULATION)", 1150, 500, C("By our calculation"), color="#FFE0B2", size=28),
              HANK(450, 0.3, hold="membercard", face="dollar", pose="cheer", hops=[C("earn about two percent")])]},
    sources=["tenk"])
stage("s18_loop", "a2_loop", {
    **W1("clubfloor", regX=1150, sampleX=-900),
    "cam": cam((0, 1100, 470, 1.0), (C("In fiscal twenty seventeen"), 1100, 450, 0.95, 1.6), (C("More than double"), 1100, 480, 1.25, WHIP)), "drift": 3,
    "items": [it("toonwords", text="FEE → COME BACK", x=700, y=150, at=C("The fee makes you"), size=60, until=C("In fiscal twenty seventeen", -0.1)),
              it("toonwords", text="REWARD → SPEND MORE", x=1500, y=260, at=C("The reward makes you"), size=60, color="#FFFFFF", until=C("In fiscal twenty seventeen", -0.1)),
              chart([{"label": "FISCAL 2017", "value": 2.85, "color": "#2F6FD1", "at": C("membership fees were"), "display": "$2.9BN"},
                     {"label": "FISCAL 2026", "value": 5.91, "color": "#E53950", "at": C("Last fiscal year"), "display": "$5.9BN"}],
                    at=C("In fiscal twenty seventeen"), max=6.5, title="MEMBERSHIP FEES (10-Ks)", x=420, y=220, w=760, h=470),
              sign("× 2.07 (OUR CALCULATION)", 1600, 300, C("More than double"), color="#FFE0B2", size=34),
              HANK([[0, 1700], [C("The fee makes you"), 1500]], 0.2, face="grin", hold="bigpack", pose="stand", faces=[[0, "grin"], [C("More than double"), "dollar"]])]},
    sources=["tenk", "tenk2017"])

# ====================================================================== ACT 3: the treasure hunt
bumper("s19_b3", "a3_card", "3", "ACT THREE", "THE TREASURE HUNT", "Objects in cart are larger than they appear", "drone", "#2E9E5B",
       cast=[PEARL(xk=[[0.8, -200], [3.8, 2300]], at=0.8, y=1060, scale=0.8, hold="tray", face="grin", pose="run")])
stage("s20_skus", "a3_skus", {
    **W1("clubfloor", regX=-900, sampleX=-900, palletLabels=["KETCHUP x3", "KETCHUP x3", "TOWELS x30", "NUTS 2.5 LB"]),
    "cam": cam((0, 1100, 470, 1.0), (C("Not twenty kinds"), 1000, 470, 1.0, 1.4), (C("One or two"), 1150, 560, 1.2, WHIP)), "drift": 3,
    "items": [it("counter", x=1100, y=130, at=C("fewer than"), prefix="< ", steps=[[0, 0], [C("fewer than"), 0], [C("active items"), 4000]], text="ACTIVE ITEMS PER WAREHOUSE (10-K)",
                 until=C("Not twenty kinds", -0.1)),
              sign("ILLUSTRATION · NOT A FIGURE", 1100, 130, C("Not twenty kinds"), color="#FFF8E1", size=26, until=C("One or two", -0.1)),
              *[it("toonwords", text="KETCHUP", x=300 + (k % 5) * 360, y=240 + (k // 5) * 120, at=C("Not twenty kinds", k * 0.06), until=C("One or two", -0.2), size=36, color=["#E53950", "#FF8A65", "#FFC93C", "#F06292"][k % 4], rot=(k % 3 - 1) * 6) for k in range(10)],
              it("palletstack", x=1150, at=C("One or two"), n=2, labels=["KETCHUP x3", "KETCHUP x3"], scale=1.1),
              HANK(1800, 0.3, face="happy", faces=[[0, "happy"], [C("Not twenty kinds"), "dizzy"], [C("One or two"), "grin"]], hold="bigpack", packText="x3")]},
    sources=["tenk"])
stage("s21_volume", "a3_volume", {
    **W1("loadingdock", dockX=1100, truckAt=C("And the goods arrive", -1.2), truckText="SUPPLIER"),
    "cam": cam((0, 1100, 470, 1.0), (C("Enormous volume means"), 1000, 470, 1.0, 1.4), (C("And the goods arrive"), 1300, 480, 0.95, 1.6)), "drift": 3,
    "items": [it("toonwords", text="ENORMOUS VOLUME", x=1100, y=150, at=C("sells in enormous volume"), size=76, until=C("Enormous volume means", -0.1)),
              it("toonwords", text="= BARGAINING POWER", x=1100, y=150, at=C("Enormous volume means"), size=76, color="#FFFFFF", until=C("And the goods arrive", -0.1)),
              it("forklift", x=[[0, 300], [C("And the goods arrive"), 800]], at=0.3, load=["PALLET", "PALLET"], lift=[[0, 0.1], [C("stored on racks"), 0.5]], scale=0.9, face="happy"),
              sign("'REDUCING LABOR REQUIRED' (10-K)", 1100, 280, C("reduces the labor"), color="#FFF8E1", size=30)]},
    sources=["tenk"])
stage("s22_treasure", "a3_treasure", {
    **W1("treasureaisle", spotX=1150, goods=[[0, "KAYAK", "#4FB3F6"], [C("Shoppers call it"), "GOLD BARS?", "#FFC93C"], [C("If you see it"), "GIANT TEDDY", "#F06292"], [C("next week"), "HOT TUB", "#7BD389"]]),
    "cam": cam((0, 1150, 470, 1.0), (C("Shoppers call it"), 1150, 480, 1.1, WHIP), (C("If you see it"), 1200, 480, 1.0, 1.2)), "drift": 2,
    "items": [sign("'DYNAMICALLY ADJUST THE ITEMS WE SELL' (2025 LETTER)", 1150, 120, C("Costco says"), color="#FFF8E1", size=26, until=C("Shoppers call it", -0.1)),
              it("toonwords", text="THE TREASURE HUNT", x=1150, y=140, at=C("Shoppers call it"), size=78, color="#FFD23F"),
              HANK([[0, 300], [C("If you see it"), 650]], 0.2, face="shock", faces=[[0, "happy"], [C("Shoppers call it"), "shock"], [C("If you see it"), "dollar"]], takes=[C("Shoppers call it")]),
              S(9, [[0, 2300], [C("you'd better buy it"), 1700]], 0.4, face="panic", pose="run"),
              PEARL(2000, 0.3, hold="tray", face="smug")]},
    sources=["ars"], sfx=[{"kind": "hit", "cue": "Shoppers call it", "gain": 0.25}])
stage("s23_kirk", "a3_kirk", {
    **W1("housebrand", machX=0.5, ticker="HOUSE BRAND · TYPICALLY 15-20% CHEAPER (COMPANY)"),
    "cam": cam((0, 1100, 470, 1.0), (C("In his latest letter"), 700, 480, 1.1, 1.4), (C("now brings in"), 1150, 450, 0.95, 1.6)), "drift": 3,
    "items": [it("caricature", who="vachris", x=500, at=C("In his latest letter", -0.4), pose="stand", poses=[[0, "stand"], [C("wrote that"), "talk"]], hold="letter",
                 label="RON VACHRIS · CEO", labelUntil=C("now brings in", 0.6), scale=1.2),
              PEARL(1900, 0.1, hold="tray", face="happy", faces=[[0, "happy"], [C("now brings in"), "dollar"]]),
              sign("KIRKLAND SIGNATURE = COSTCO'S HOUSE BRAND", 1250, 230, C("Kirkland"), color="#FFFFFF", size=30, until=C("now brings in", 1.6)),
              it("counter", x=1500, y=200, at=C("now brings in"), prefix="≈ $", suffix="BN", steps=[[0, 0], [C("now brings in"), 0], [C("a year worldwide"), 90]], text="KIRKLAND SIGNATURE · ANNUAL REVENUE (2025 LETTER)"),
              sign("15-20% SAVINGS VS NATIONAL BRAND (COMPANY STATEMENT)", 1300, 420, C("fifteen to twenty percent"), color="#C8E6C9", size=26)]},
    sources=["ars"])
stage("s24_kirk2", "a3_kirk2", {
    **W1("housebrand", machX=0.62, speed=190),
    "cam": cam((0, 1150, 470, 1.0), (C("And according to"), 1300, 470, 1.05, 1.4), (C("The cheaper box"), 1100, 480, 1.0, WHIP)), "drift": 3,
    "items": [it("toonwords", text="≈ 1/3 OF SALES", x=1100, y=130, at=C("about a third"), size=80, until=C("And according to", -0.1)),
              sign("$90BN VS $269.9BN FISCAL 2025 SALES · OUR ROUGH CALCULATION", 1100, 260, C("about a third", 0.3), color="#FFE0B2", size=24, until=C("And according to", -0.1)),
              sign("'GENERALLY EARN HIGHER MARGINS' (10-K)", 1250, 160, C("generally earn Costco"), color="#FFF8E1", size=32, until=C("The cheaper box", -0.1)),
              it("toonwords", text="CHEAPER FOR YOU · BETTER FOR COSTCO", x=1100, y=150, at=C("The cheaper box"), size=50, until=C("And Costco says", -0.1)),
              sign("'CONTINUE TO INCREASE THE SALES PENETRATION OF OUR PRIVATE-LABEL ITEMS'", 1100, 160, C("And Costco says"), color="#FFF8E1", size=24, sub="COSTCO 10-K, FISCAL 2026"),
              HANK(400, 0.3, face="happy", hold="bigpack", packText="HOUSE", faces=[[0, "happy"], [C("The cheaper box"), "dollar"]])]},
    sources=["ars", "tenk"])
add("p25_squeeze", "a3_draw", "engine_draw", {
    "title": "The squeeze (schematic, not to scale)", "board": BOARD, "draw_start": C("Let me draw"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 400, 300, 380), "color": "muted", "width": 5, "kind": "box", "start": C("Here's a typical supermarket"), "label": lbl("SUPERMARKET", 710, 440, 26, "muted")},
        {"d": "M 590 480 L 830 480 M 590 510 L 830 510 M 590 540 L 830 540 M 590 570 L 830 570 M 590 600 L 830 600 M 590 630 L 830 630 M 590 660 L 830 660 M 590 690 L 830 690 M 590 720 L 830 720",
         "color": "muted", "width": 3, "start": C("A long list"), "label": lbl("MANY ITEMS · SMALL VOLUME EACH", 710, 760, 18, "muted")},
        {"d": rect(1180, 400, 300, 380), "color": "accent3", "width": 6, "kind": "box", "start": C("Here's Costco"), "label": lbl("COSTCO", 1330, 440, 28, "accent3")},
        {"d": "M 1210 500 L 1450 500 M 1210 580 L 1450 580 M 1210 660 L 1450 660", "color": "accent3", "width": 14, "start": C("A short list"), "label": lbl("FEW ITEMS · HUGE VOLUME EACH", 1330, 760, 18, "accent3")},
        {"d": rect(1180, 230, 300, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("a strong hand with the supplier"), "label": lbl("SUPPLIER", 1330, 285, 26, "accent2")},
        {"d": arrow((1330, 395), (1330, 330)), "color": "accent2", "width": 6, "kind": "arrow", "start": C("Big volume per item"), "label": lbl("BARGAINING POWER", 1520, 365, 20, "accent2")},
        {"d": rect(900, 600, 220, 90), "color": "accent", "width": 5, "kind": "box", "start": C("The house brand"), "label": lbl("HOUSE BRAND", 1010, 655, 22, "accent")},
        {"d": arrow((1120, 645), (1175, 645)), "color": "accent", "width": 6, "kind": "arrow", "start": C("a second lever")},
        {"d": arrow((1330, 800), (1330, 870), 0), "color": "risk", "width": 7, "kind": "arrow", "start": C("Both push the price down"), "label": lbl("LOWER PRICES", 1500, 860, 26, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Big volume per item", 0.3), "dur": 1.4, "target": [1330, 360]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])

# ====================================================================== ACT 4: the dollar-fifty hot dog
bumper("s26_b4", "a4_card", "4", "ACT FOUR", "THE DOLLAR-FIFTY HOT DOG", "Do not tap on the glass. Or the price.", "sticker", "#FF9F1C",
       cast=[SKIP(xk=[[0.8, -200], [3.8, 2300]], at=0.8, y=1060, scale=0.8, hold="hotdog", face="panic", pose="run")])
stage("s27_dog", "a4_dog", {
    **W1("foodcourt", boardX=1150, shakeAt=C("might finally go up", -0.2), tablesX=[200, 2100]),
    "cam": cam((0, 1150, 360, 1.0), (C("When speculation spread"), 1150, 380, 1.1, 1.6), (C("Costco's finance chief"), 1150, 470, 0.95, 1.4), (C("is safe"), 1150, 330, 1.25, WHIP)), "drift": 2,
    "items": [it("bubble", text="IT'S GOING UP?!", x=600, y=330, at=C("might finally go up", -0.6), until=C("Costco's finance chief", -0.1), tail=[520, 520], size=36, shout=True),
              S(3, 520, 0.2, face="panic", hold="hotdog", faces=[[0, "happy"], [C("might finally go up", -0.6), "panic"], [C("is safe"), "grin"]], takes=[C("might finally go up", -0.5)]),
              SKIP(1150, 0.3, face="worry", faces=[[0, "happy"], [C("might finally go up"), "worry"], [C("is safe"), "grin"]], hops=[C("is safe", 0.3)]),
              sign("CFO ON THE MAY 2024 EARNINGS CALL (VIA CNN)", 1150, 700, C("Costco's finance chief"), color="#FFF8E1", size=26),
              it("bubble", text="\"THE $1.50 HOT DOG\nPRICE IS SAFE\"", x=1750, y=360, at=C("quote"), tail=[1700, 560], size=34),
              it("toonwords", text="SAFE!", x=1150, y=120, at=C("is safe"), size=110, color="#7CFF8A")]},
    sources=["cnn_hotdog"], sfx=[{"kind": "hit", "cue": "is safe", "gain": 0.3}])
stage("s28_sinegal", "a4_sinegal", {
    **W1("foodcourt", boardX=900, tablesX=[-400, 1900]),
    "cam": cam((0, 1100, 470, 1.0), (C("We're known for that hot dog"), 1300, 470, 1.15, 1.4), (C("That's something"), 1350, 480, 1.25, WHIP)), "drift": 2,
    "items": [it("caricature", who="sinegal", x=1350, at=0.2, pose="stand", poses=[[0, "stand"], [C("We're known"), "talk"]], hold="hotdog", label="JIM SINEGAL · CO-FOUNDER", labelUntil=C("We're known"), scale=1.25),
              sign("CEO UNTIL JAN 1, 2012 (10-K)", 1900, 380, C("who was chief executive"), color="#FFF8E1", size=28, until=C("put it simply", 0.4)),
              sign("2009 NEWSPAPER INTERVIEW, AS QUOTED BY CNN", 1850, 380, C("put it simply", 0.5), color="#FFE0B2", size=26, until=C("We're known", -0.1)),
              it("bubble", text="\"WE'RE KNOWN FOR\nTHAT HOT DOG.\"", x=1700, y=250, at=C("We're known"), until=C("That's something", -0.1), tail=[1450, 430], size=32),
              it("bubble", text="\"THAT'S SOMETHING\nYOU DON'T MESS WITH.\"", x=1700, y=250, at=C("That's something"), tail=[1450, 430], size=32),
              SKIP(700, 0.3, face="happy", faces=[[0, "happy"], [C("That's something"), "grin"]], hold="hotdog")]},
    sources=["cnn_hotdog", "proxy2012", "tenk2012"])
stage("s29_why", "a4_why", {
    **W1("gasbar", gasX=1150, carsAt=C("A cheap lunch", -1.0), canopy="MEMBER FUEL", signText="GAS", signSub="MEMBERS ONLY"),
    "cam": cam((0, 1150, 470, 1.0), (C("groups it with gas"), 600, 400, 1.0, 1.6), (C("A cheap lunch"), 1100, 480, 0.95, 1.4), (C("And every visit"), 1150, 500, 1.1, WHIP)), "drift": 3,
    "items": [it("combo", x=1150, y=280, at=0.2, price="$1.50", scale=0.6, until=C("groups it with gas", -0.1), face="smug"),
              it("toonwords", text="NOT A RESTAURANT", x=1150, y=120, at=C("isn't really a restaurant"), size=70, until=C("groups it with gas", -0.1)),
              sign("10-K: 'WAREHOUSE ANCILLARY' · 'ENCOURAGING MORE FREQUENT SHOPPING'", 1150, 110, C("groups it with gas"), color="#FFF8E1", size=24, until=C("A cheap lunch", -0.1)),
              it("toonwords", text="A REASON TO VISIT", x=1150, y=140, at=C("A cheap lunch"), size=70, until=C("And every visit", -0.1)),
              it("toonwords", text="...PAST THE PALLETS", x=1150, y=140, at=C("And every visit"), size=70, color="#FFFFFF"),
              HANK([[0, -300], [C("A cheap lunch"), 300], [C("And every visit"), 800]], C("A cheap lunch", -0.8), face="happy", hold="hotdog")]},
    sources=["tenk"])
stage("s30_gas", "a4_gas", {
    **W1("gasbar", gasX=1150, carsAt=0.0, cars=6),
    "cam": cam((0, 1150, 470, 0.95), (C("and gasoline was"), 1100, 470, 1.0, 1.4), (C("Fill up the tank"), 1400, 520, 1.2, WHIP)), "drift": 3,
    "items": [it("counter", x=600, y=330, at=C("Costco ran"), steps=[[0, 0], [C("Costco ran"), 0], [C("gas stations"), 774]], text="GAS STATIONS · END OF FISCAL 2026", until=C("Fill up the tank", -0.1)),
              it("counter", x=1700, y=330, at=C("and gasoline was"), suffix="%", steps=[[0, 0], [C("and gasoline was"), 0], [C("of its net sales"), 11]], text="GASOLINE · SHARE OF NET SALES", until=C("Fill up the tank", -0.1)),
              it("bubble", text="...AND WHILE\nYOU'RE HERE", x=1500, y=300, at=C("while you're here"), tail=[1450, 560], size=36),
              CARD(1900, 0.3, face="happy", faces=[[0, "happy"], [C("while you're here"), "wink"]])]},
    sources=["tenk"])
stage("s31_float", "a4_float", {
    **W1("loadingdock", dockX=1100, truckAt=0.0, sellAt=C("before it is required"), sellDur=2.5),
    "cam": cam((0, 1150, 470, 1.0), (C("In Costco's own words"), 900, 470, 1.05, 1.6), (C("even while"), 1100, 480, 1.0, 1.4)), "drift": 3,
    "items": [it("toonwords", text="THE CASH", x=1100, y=150, at=0.2, size=90, until=C("In Costco's own words", -0.1)),
              sign("'WE OFTEN SELL INVENTORY BEFORE WE ARE REQUIRED TO PAY FOR IT'", 1100, 140, C("In Costco's own words"), color="#FFF8E1", size=26, sub="COSTCO 10-K, FISCAL 2026"),
              sign("'... EVEN WHILE TAKING ADVANTAGE OF EARLY PAYMENT DISCOUNTS'", 1100, 300, C("even while"), color="#FFF8E1", size=26),
              CARD(1900, 0.3, face="dollar")]},
    sources=["tenk"])
stage("s32_balance", "a4_balance", {
    **W1("loadingdock", dockX=1100, truckAt=-5),
    "cam": cam((0, 1100, 470, 1.0), (C("It owed more"), 1100, 470, 1.05, 1.4), (C("That's the quiet superpower"), 1150, 470, 1.0, 1.2)), "drift": 3,
    "items": [chart([{"label": "MERCHANDISE HELD", "value": 19.3, "color": "#2F6FD1", "at": C("it held"), "display": "$19.3BN"},
                     {"label": "OWED TO SUPPLIERS", "value": 22.6, "color": "#E53950", "at": C("And it owed"), "display": "$22.6BN"}],
                    at=0.2, max=25, title="BALANCE SHEET · AUG 30, 2026 (10-K)", x=360, y=300, w=900, h=470, until=C("That's the quiet superpower", -0.1)),
              it("toonwords", text="OWES MORE THAN IT HOLDS", x=1100, y=90, at=C("It owed more"), size=60, until=C("That's the quiet superpower", -0.1)),
              it("toonwords", text="NOTHING SITS STILL", x=1100, y=150, at=C("That's the quiet superpower"), size=80),
              it("forklift", x=[[0, 2300], [C("That's the quiet superpower"), 1500]], at=0.3, load=["SOLD", "SOLD"], scale=0.85, flip=True, face="happy"),
              CARD(1900, 0.3, face="wink")]},
    sources=["tenk"])
add("p33_clock", "a4_draw", "engine_draw", {
    "title": "The cash clock (illustrative)", "board": BOARD, "draw_start": C("Let me draw"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 620 L 1500 620", "color": "ink", "width": 5, "start": C("Let me draw"), "label": lbl("DAYS →", 1500, 660, 20, "ink")},
        {"d": rect(570, 460, 120, 120), "color": "accent2", "width": 5, "kind": "box", "start": C("a pallet arrives"), "label": lbl("DAY 0 · PALLET IN", 630, 440, 20, "accent2")},
        {"d": dot(1050, 360), "color": "accent", "width": 1, "start": C("turns over about fourteen"), "label": lbl("≈ 14 TURNS A YEAR · ≈ 26 DAYS (OUR CALCULATION)", 1050, 360, 22, "accent")},
        {"d": rect(1110, 460, 160, 120), "color": "accent3", "width": 5, "kind": "box", "start": C("The member pays"), "label": lbl("MEMBER PAYS", 1190, 440, 20, "accent3")},
        {"d": arrow((700, 520), (1100, 520), -0.08), "color": "accent3", "width": 5, "kind": "arrow", "start": C("gone in less than a month")},
        {"d": rect(1350, 460, 150, 120), "color": "risk", "width": 5, "kind": "box", "start": C("Only later"), "label": lbl("BILL DUE", 1425, 440, 20, "risk")},
        {"d": "M 1270 700 L 1350 700", "color": "accent", "width": 14, "start": C("In between"), "label": lbl("CASH IN HAND", 1310, 750, 22, "accent")},
        {"d": dot(1050, 860), "color": "muted", "width": 1, "start": C("works for Costco"), "label": lbl("TIMELINE ILLUSTRATIVE · TERMS VARY BY SUPPLIER", 1050, 860, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("In between", 0.3), "dur": 1.6, "target": [1310, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])

# ====================================================================== ACT 5: who pays the bill
bumper("s34_b5", "a5_card", "5", "ACT FIVE", "WHO PAYS THE BILL", "Membership has its responsibilities", "robot", "#7E57C2",
       cast=[BEV(xk=[[0.8, -200], [3.8, 2300]], at=0.8, y=1060, scale=0.8, face="panic", pose="run")])
stage("s35_people", "a5_people", {
    **W1("clubfloor", regX=1150, sampleX=-900),
    "cam": cam((0, 1100, 470, 1.0), (C("Its letter put"), 1100, 470, 1.0, 1.4), (C("It employed about"), 1150, 470, 0.95, 1.4)), "drift": 3,
    "items": [it("toonwords", text="WHO PAYS?", x=1100, y=150, at=0.2, size=90, until=C("Its letter put", -0.1)),
              it("counter", x=1100, y=150, at=C("Its letter put"), prefix="≈ $", steps=[[0, 0], [C("Its letter put"), 0], [C("in twenty twenty-five"), 32]], text="AVERAGE U.S. HOURLY WAGE, 2025 (COMPANY LETTER)",
                 until=C("It employed about", -0.1)),
              sign("'OUR LARGEST EXPENSE AFTER THE COST OF MERCHANDISE' (10-K)", 1100, 330, C("its annual report calls"), color="#FFF8E1", size=24, until=C("It employed about", -0.1)),
              it("counter", x=1100, y=150, at=C("It employed about"), steps=[[0, 0], [C("It employed about"), 0], [C("people worldwide"), 355000]], text="EMPLOYEES · END OF FISCAL 2026"),
              BEV(500, 0.2, face="happy", pose="wave"), PEARL(1750, 0.3, hold="tray", face="grin"), SKIP(2050, 0.4, hold="hotdog", face="happy")]},
    sources=["ars", "tenk"])
stage("s36_div", "a5_div", {
    **W1("cashvault", vaultX=0.35, openAt=C("Costco declared", -0.4), pourAt=C("a special dividend"), screen="$30 / SHARE", screenTop="SPECIAL DIVIDEND · NOV 10, 2026"),
    "cam": cam((0, 900, 470, 1.0), (C("a special dividend"), 1250, 450, 0.95, 1.6), (C("By our calculation"), 1150, 450, 0.95, 1.2)), "drift": 3,
    "items": [it("toonwords", text="AND THE SHAREHOLDERS?", x=1000, y=130, at=0.2, size=60, until=C("Costco declared", -0.1)),
              it("counter", x=900, y=830, at=C("in total", -1.4), prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [C("in total", -1.4), 0], [C("in total"), 13.3]], text="TOTAL PAYOUT (8-K)", scale=0.85),
              it("toonwords", text="> 2 YEARS OF FEES", x=1150, y=120, at=C("By our calculation"), size=70),
              sign("$13.3BN ÷ $5.9BN · OUR CALCULATION", 1150, 250, C("By our calculation", 0.4), color="#FFE0B2", size=26)]},
    sources=["div8k", "tenk"], sfx=[{"kind": "hit", "cue": "a special dividend", "gain": 0.3}])
stage("s37_risk", "a5_risk", {
    **W1("memberdesk", deskX=1150, screen="RENEWING?", screenTop="THE PROMISE"),
    "cam": cam((0, 1150, 470, 1.0), (C("Costco's own annual report"), 1150, 450, 1.0, 1.4), (C("If the savings"), 1150, 480, 1.15, WHIP)), "drift": 2,
    "items": [it("toonwords", text="ONE PROMISE", x=1150, y=330, at=0.2, size=90, until=C("Costco's own annual report", -0.1)),
              sign("'MEMBERSHIP LOYALTY AND GROWTH ARE ESSENTIAL TO OUR BUSINESS'", 1150, 330, C("Costco's own annual report"), color="#FFF8E1", size=26, sub="COSTCO 10-K RISK FACTORS"),
              sign("REPUTATION DAMAGE → LOWER RENEWALS", 1150, 470, C("damage to its reputation"), color="#FFCDD2", size=30, until=C("If the savings", -0.1)),
              it("bigtag", x=1150, y=280, at=C("If the savings"), was="SAVINGS > FEE ?", now="OR GOODBYE", slashAt=C("the card stops", -0.3), nowAt=C("the card stops"), scale=0.85),
              BEV(1700, 0.2, face="worry", pose="clipboard", faces=[[0, "happy"], [C("If the savings"), "worry"]]),
              CARD(600, 0.3, face="alarm", faces=[[0, "deadpan"], [C("If the savings"), "alarm"]])]},
    sources=["tenk"])
add("p38_machine", "a5_draw", "engine_draw", {
    "title": "The Costco machine (summary)", "board": BOARD, "draw_start": C("Let me put"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(940, 300, 260, 90), "color": "accent3", "width": 5, "kind": "box", "start": C("Low prices bring"), "label": lbl("LOW PRICES", 1070, 355, 24, "accent3")},
        {"d": rect(1280, 470, 260, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("Members pay fees"), "label": lbl("FEES ≈ ½ OP. PROFIT", 1410, 525, 20, "accent2")},
        {"d": arrow((1200, 360), (1330, 465), 0.15), "color": "accent2", "width": 5, "kind": "arrow", "start": C("Members pay fees", -0.3)},
        {"d": rect(940, 650, 260, 90), "color": "accent", "width": 5, "kind": "box", "start": C("A short list"), "label": lbl("SHORT LIST · VOLUME", 1070, 705, 20, "accent")},
        {"d": arrow((1330, 565), (1200, 680), 0.15), "color": "accent", "width": 5, "kind": "arrow", "start": C("sells in huge volume")},
        {"d": rect(650, 470, 260, 90), "color": "risk", "width": 5, "kind": "box", "start": C("Fast sales"), "label": lbl("SUPPLIERS' MONEY", 780, 525, 20, "risk")},
        {"d": arrow((940, 700), (800, 565), 0.15), "color": "risk", "width": 5, "kind": "arrow", "start": C("Fast sales", 0.2)},
        {"d": arrow((800, 465), (940, 360), 0.15), "color": "accent3", "width": 5, "kind": "arrow", "start": C("keeps prices low")},
        {"d": dot(1070, 525), "color": "ink", "width": 1, "start": C("And the hot dog"), "label": lbl("$1.50 HOT DOG: COME BACK", 1070, 525, 22, "ink")},
        {"d": dot(1070, 860), "color": "muted", "width": 1, "start": C("Every part feeds the next"), "label": lbl("EVERY PART FEEDS THE NEXT", 1070, 860, 24, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Members pay fees", 0.4), "dur": 1.4, "target": [1410, 520]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])

# ====================================================================== PAYOFF + TEASER + BUTTON
stage("s39_payoff", "payoff", {
    **W1("foodcourt", boardX=1150, tablesX=[300, 2000]),
    "cam": cam((0, 1150, 430, 0.85), (C("It sells access"), 1150, 450, 0.92, 1.6), (C("The store is the bait"), 1150, 470, 1.0, 1.2), (C("And the dollar-fifty"), 1150, 330, 1.2, WHIP)), "drift": 2,
    "items": [it("toonwords", text="IT SELLS ACCESS", x=1150, y=470, at=C("It sells access"), until=C("The store is the bait", -0.1), size=64),
              it("toonwords", text="THE STORE = BAIT", x=1150, y=470, at=C("The store is the bait"), until=C("The fee is the catch", -0.1), size=64, color="#FFFFFF"),
              it("toonwords", text="THE FEE = THE CATCH", x=1150, y=470, at=C("The fee is the catch"), until=C("And the dollar-fifty", -0.1), size=64),
              it("membercard", x=600, y=330, at=C("the card is the business"), scale=0.32, until=C("And the dollar-fifty", -0.1)),
              BEV(500, 0.2, face="grin", pose="wave"), HANK(1800, 0.3, face="dollar", hold="bigpack", hops=[C("the deal is still on")]),
              PEARL(800, 0.4, hold="tray", face="happy"), SKIP(1500, 0.5, hold="hotdog", face="grin"),
              CARD(2100, 0.6, face="happy", hops=[C("still on")])]})
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s41_button", "button", {
    **W1("foodcourt", boardX=1000, price="$1.50", shakeAt=1.0, tablesX=[-400, 2300]),
    "cam": cam((0, 1000, 380, 1.1), (2.8, 1000, 330, 1.3, WHIP)), "drift": 0, "min_seconds": 5.6,
    "items": [it("toonwords", text="NEW PRICE, FINALLY!", x=1000, y=500, at=0.4, until=2.6, size=64),
              SKIP(700, 0.1, face="shock", takes=[1.0], faces=[[0, "shock"], [2.8, "grin"]], hops=[3.0]),
              HANK(1350, 0.2, face="worry", hold="hotdog", faces=[[0, "worry"], [2.8, "love"]], hops=[3.2]),
              it("toonwords", text="... STILL $1.50", x=1000, y=500, at=2.8, size=84, color="#7CFF8A"),
              CARD(1700, 0.3, face="deadpan", faces=[[0, "deadpan"], [2.8, "wink"]])]},
    sfx=[{"kind": "hit", "at": 1.0, "gain": 0.3}, {"kind": "hit", "at": 2.8, "gain": 0.3}])


# ---------------------------------------------------------------------------------------------- cue check + write
def _cues(o, acc):
    if isinstance(o, dict):
        if "cue" in o and isinstance(o["cue"], str):
            acc.append(o["cue"])
        for v in o.values():
            _cues(v, acc)
    elif isinstance(o, list):
        for v in o:
            _cues(v, acc)
    return acc


script = yaml.safe_load((PROJ / "deliverables/documentary/script.yaml").read_text())
narr = {s["id"]: s["narration"] for s in script["segments"]}
bad = [(s["id"], c) for s in scenes for c in _cues(s["params"], []) if c not in narr.get(s["segment"], "")]
missing = [k for k in narr if k not in {s["segment"] for s in scenes}]
if bad or missing:
    raise SystemExit(f"cue problems: {bad}\nsegments without scenes: {missing}")
write(OUT, "# GENERATED by tools/gen_costco_v2_storyboard.py; edit the generator, not this file.\n"
           "# Episode 57 storyboard (Costco v2): sitcom-style episode; bespoke worlds in CartoonStage/costco.tsx; tones from visual_direction.yaml.\n")
