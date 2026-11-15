"""Generates projects/how-black-friday-actually-makes-money/deliverables/documentary/storyboard.yaml
(Episode 56: How Black Friday Actually Makes Money).

OWNER DIRECTION: feel like an actual episode of a prime-time animated TV sitcom. Genre level only; everything original.
TV structure: cold open gag (5 a.m. at the mall) -> channel intro (our "theme") -> show TITLE CARD with a typed joke
subtitle -> five acts, each opened by a BUMPER with a rotating joke caption -> button joke after the end card.
Recurring cast (CartoonStage/sitcom.tsx `toon` rig and robots): GLORIA (store manager), DASH (deal-hunter), TAGBOT (price-
tag printer whose "WAS" tags grow absurdly every act: the running gag), BUZZ (delivery drone), LIFT (forklift).
Bespoke sets (new): megamall, storefloor, philly61, tvfactory, quarterhq, payrails, bnplride, adarena, returnsmtn, titlecard,
bumper. Signature animations: the 5 a.m. stampede (s01), the attach-sale cart that fills (s12), the spec-trimming doorbuster
factory (s15), the Q4 floor that balloons (s20), the payment-rails toll gantries (s28), the pay-in-4 carousel (s30), the
returns mountain (s36). Presenter boards: p14 (2 boxes + arrow), p22 (bars), p32 (money flow), p39 (price-history line).
No logos; no real people; jokes never change a number. Run: python tools/gen_blackfriday_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-black-friday-actually-makes-money/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35


def toon(who, x, at=0.0, **kw):
    if "xk" in kw:
        x = kw.pop("xk")
    return it("toon", who=who, x=x, at=at, **kw)


def G(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.35)
    return toon("gloria", x, at, **kw)


def D(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.35)
    return toon("dash", x, at, **kw)


def S(v, x, at=0.0, **kw):
    kw.setdefault("scale", 1.2)
    return toon("shopper", x, at, v=v, **kw)


def TB(x, at=0.0, **kw):
    kw.setdefault("scale", 1.15)
    return it("tagbot", x=x, at=at, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def chart(bars_, at=0.2, **kw):
    kw.setdefault("panel", True)
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


def bumper(id_, seg, num, act, title, caption, color="#E53950", gag=None):
    items = [TB(1650, 0.9, y=1010, scale=0.9, face="happy", prints=[[1.3, gag]] if gag else []),
             D(xk=[[0.8, -200], [3.6, 2300]], at=0.8, y=1075, scale=0.85, hold="tv", face="dollar", pose="run"),
             G(xk=[[1.4, -300], [3.9, 1900]], at=1.4, y=1075, scale=0.85, hold="clipboard", face="panic", pose="run")]
    stage(id_, seg, {**W1("bumper", num=num, act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "sitcom",
                     "min_seconds": 3.9, "items": items}, sfx=[{"kind": "hit", "at": 0.15, "gain": 0.3}, {"kind": "whoosh", "at": 0.05, "gain": 0.25}])


# ====================================================================== COLD OPEN (5 a.m. at the mall)
stage("s01_open", "co_open", {
    **W1("megamall", doorsAt=C("The doors open"), clockAt=C("The doors open", -0.6), dawn=0.55, mallX=0.47),
    "cam": cam((0, 1200, 300, 1.0), (C("A crowd has been waiting"), 700, 560, 1.05, 2.4), (C("priced so low"), 1150, 520, 1.25, 1.6),
               (C("The doors open"), 1050, 500, 1.0, WHIP), (C("starts losing money"), 1300, 560, 1.1, 1.4), (C("On purpose"), 1480, 600, 1.6, WHIP)),
    "drift": 3,
    "items": [it("toonwords", text="THE DAY AFTER THANKSGIVING", x=1200, y=150, at=0.2, until=C("A crowd has been waiting", 1.0), size=60),
              S(1, 300, 0.4, face="worry", scarf="#FFB300"), S(2, 430, 0.5, face="worry", hat="#2F6FD1"), S(4, 560, 0.6, face="dizzy"),
              S(6, 200, 0.7, face="grin"), S(7, 80, 0.8, face="worry"),
              D(740, 0.3, hold="coffee", pose="sip", face="dollar", label="DASH · DEAL HUNTER", labelUntil=C("priced so low"),
                poses=[[0, "sip"], [C("The doors open"), "stand"]], hops=[C("priced so low", 0.3)],
                xk=[[0, 740], [C("The doors open"), 740], [C("The doors open", 1.4), 1250]]),
              G(1180, C("A crowd has been waiting", 1.2), hold="clipboard", pose="key", face="worry", label="GLORIA · STORE MANAGER", labelUntil=C("The doors open", -1.8),
                faces=[[0, "worry"], [C("The doors open"), "panic"], [C("On purpose"), "deadpan"]],
                poses=[[0, "key"], [C("The doors open", 0.2), "armsup"], [C("On purpose", -0.3), "shrug"]],
                xk=[[0, 1180], [C("The doors open"), 1180], [C("The doors open", 0.6), 1480]], takes=[C("starts losing money")]),
              it("bigtag", x=1720, y=260, at=C("priced so low"), until=C("The doors open"), was="TV", now="DOORBUSTER!", scale=0.75),
              TB(1720, 0.6, faces=[[0, "deadpan"], [C("starts losing money"), "alarm"], [C("On purpose"), "deadpan"]],
                 prints=[[C("priced so low", 0.4), "DOORBUSTER!"], [C("On purpose"), "LOSS:\nON PURPOSE"]]),
              it("bubble", text="DOORS IN\n3... 2...", x=1250, y=330, at=C("The doors open", -1.6), until=C("The doors open", -0.1), tail=[1200, 520], size=32),
              it("stampede", at=C("The doors open", 0.3), x0=-300, x1=1500, n=14, dur=2.6, scale=1.0, until=C("On purpose", -0.2)),
              it("drone", x=[[0, 2100], [C("The doors open"), 1500], [C("On purpose"), 700]], y=200, at=0.2, carry="RUSH", scale=0.9)]},
    sfx=[{"kind": "hit", "at": C("The doors open"), "gain": 0.35}])
stage("s02_hook", "co_hook", {
    **W1("megamall", doorsAt=0.0, clockAt=0.0, dawn=0.85, mallX=0.47, banner="RECORD ONLINE BLACK FRIDAY"),
    "cam": cam((0, 1100, 420, 0.92), (C("Retailers plan"), 1200, 520, 1.05, 1.8), (C("So how does"), 1150, 540, 1.25, WHIP)), "drift": 4,
    "items": [it("drone", x=[[0, -300], [8, 2400]], y=180, at=0.1, carry="ORDER", scale=0.8),
              it("drone", x=[[0, 2300], [9, -300]], y=290, at=0.4, carry="ORDER", scale=0.7),
              it("drone", x=[[0, -500], [7, 2400]], y=110, at=0.8, carry="ORDER", scale=0.6),
              it("counter", x=1150, y=260, at=C("Americans spent"), prefix="$", suffix="BN", decimals=1,
                 steps=[[0, 0], [C("Americans spent"), 0], [C("online on Black Friday"), 11.8]], text="BLACK FRIDAY 2025, U.S. ONLINE (ADOBE)", until=C("So how does", -0.2)),
              sign("A RECORD", 1650, 420, C("a record"), color="#FFE0B2", size=34, until=C("So how does", -0.2)),
              G(500, 0.2, face="happy", pose="talk", talk=[[C("Retailers plan"), C("this weekend", 0.6)]], faces=[[0, "happy"], [C("So how does"), "worry"]],
                poses=[[0, "talk"], [C("So how does"), "shrug"]]),
              D(1700, 0.3, hold="tv", face="grin", faces=[[0, "grin"], [C("So how does"), "shock"]]),
              it("toonwords", text="HOW?!", x=1150, y=330, at=C("actually make money"), size=130, color="#FFC93C"),
              TB(1980, 0.5, face="deadpan", faces=[[0, "deadpan"], [C("So how does"), "alarm"]])]},
    sources=["adobe_jan"])
stage("s03_promise", "co_promise", {
    **W1("storefloor", padX=520, checkX=1700, tvX=-700),
    "cam": cam((0, 900, 500, 1.0), (C("the cable that wins"), 1100, 520, 1.05, 1.2), (C("everyone"), 1300, 500, 1.0, 1.2)), "drift": 6,
    "items": [it("toonwords", text="FOLLOW THE MONEY", x=1000, y=110, at=0.2, size=70, until=C("everyone", -0.2)),
              sign("1 · THE DEAL THAT LOSES", 520, 330, C("The deal that loses"), color="#FFCDD2", size=30),
              it("heapcart", x=1050, at=C("the cable that wins", -0.4), adds=[[C("the cable that wins"), "CABLE", "#7BD389"]], scale=1.0),
              sign("2 · THE CABLE THAT WINS", 1050, 450, C("the cable that wins"), color="#C8E6C9", size=30),
              sign("3 · THE QUARTER THAT PAYS", 1500, 300, C("the quarter that pays"), color="#FFF59D", size=30),
              sign("4 · WHO TAKES A CUT", 1450, 140, C("takes a cut", -0.4), color="#BBDEFB", size=30),
              it("feeflow", **{"from": [1700, 650], "to": [2300, 200]}, at=C("takes a cut", -0.3), n=6),
              D(1300, 0.2, face="dollar", pose="stand", xk=[[0, 1300], [C("the cable that wins"), 1300], [C("the cable that wins", 1.2), 900]]),
              G(1820, 0.3, face="grin", pose="talk", talk=[[C("the quarter"), C("takes a cut", 1.0)]])]},
    sfx=[{"kind": "whoosh", "at": C("the cable that wins"), "gain": 0.2}])
stage("s04_title", "title_card", {
    **W1("titlecard", subs=[[2.0, "Tonight: “Doors Open at Five, Wallets at Five-Oh-One”"]]), "cam": STILL(), "drift": 0, "min_seconds": 5.8,
    "items": [D(260, 2.4, scale=1.25, face="dollar", pose="cheer", hops=[2.8, 4.2]), G(1680, 2.6, scale=1.25, face="grin", pose="wave", hold="clipboard"),
              TB(1450, 3.0, scale=0.95, face="happy", prints=[[3.4, "SEASON\nPREMIERE"]])]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}, {"kind": "hit", "at": 1.6, "gain": 0.25}])

# ====================================================================== ACT 1: the name
bumper("s05_b1", "a1_card", "1", "ACT ONE", "WHY IT'S CALLED BLACK FRIDAY", "Not a horror movie. Mostly.", color="#2F6FD1", gag="WAS: A LOT")
stage("s06_police", "a1_police", {
    **W1("philly61", copX=0.47), "tone": "history",
    "cam": cam((0, 700, 560, 1.0), (C("In nineteen sixty-one"), 1100, 640, 1.0, 2.2), (C("police officers"), 1050, 600, 1.25, 1.4), (C("For them"), 1300, 620, 1.0, 1.8)), "drift": 8,
    "items": [it("toonwords", text="THE NAME", x=700, y=150, at=0.2, until=C("In nineteen sixty-one"), size=90),
              it("calendar", x=1650, y=260, at=C("In nineteen sixty-one", -0.3), pages=[[0, "1961"]], text="PHILADELPHIA", scale=0.8, until=C("For them")),
              it("docs", x=600, y=700, at=C("a public relations newsletter"), text="PUBLIC RELATIONS NEWS · 1961", scale=0.8, stamp="BLACK FRIDAY", stampAt=C("Black Friday and Black Saturday", -0.2), until=C("For them", 0.5)),
              sign("'BLACK FRIDAY AND BLACK SATURDAY'", 1100, 120, C("Black Friday and Black Saturday"), color="#FFF8E1", size=30, sub="PHILADELPHIA POLICE, PER 1961 NEWSLETTER (VIA INQUIRER)"),
              S(1, [[0, 1500], [9, 2100]], 0.3, hat="#5D4037", hold="bag", scale=1.1), S(3, [[0, 1700], [10, 2300]], 0.5, hold="bag", scale=1.1),
              S(5, [[C("jammed streets"), 2200], [C("long shifts", 2), 1500]], C("jammed streets"), hold="box", face="panic", scale=1.1),
              sign("JAMMED STREETS · PACKED SIDEWALKS · LONG SHIFTS", 1350, 330, C("jammed streets"), color="#FFE0B2", size=28)]},
    sources=["inq", "hist"])
stage("s07_big", "a1_big", {
    **W1("philly61", copX=0.3), "tone": "history",
    "cam": cam((0, 1300, 580, 1.05), (C("It didn't stick"), 1250, 560, 1.15, WHIP)), "drift": 5,
    "items": [S(8, 1000, 0.2, face="angry", pose="talk", glasses=True, scale=1.25, talk=[[0.3, C("hated the name", 0.8)]]),
              S(9, 1200, 0.4, face="angry", pose="armsup", scale=1.25),
              it("toonwords", text="BIG FRIDAY!", x=1300, y=240, at=C("rebrand it"), until=C("It didn't stick"), size=100, color="#FFC93C"),
              it("toonwords", text="BLACK FRIDAY", x=1300, y=240, at=C("It didn't stick", 0.3), size=100, color="#FFFFFF", rot=4),
              sign("PER HISTORY.COM", 1750, 420, C("According to History"), color="#FFF8E1", size=26),
              it("bubble", text="NOPE.", x=900, y=280, at=C("It didn't stick", 0.4), tail=[1000, 470], size=40, shout=True)]},
    sources=["hist"])
stage("s08_myth", "a1_myth", {
    **W1("storefloor", padX=-900, checkX=1250, tvX=200), "tone": "history",
    "cam": cam((0, 1000, 520, 1.0), (C("It's a great story"), 1100, 500, 1.1, 1.4), (C("The police came first"), 1000, 540, 1.0, WHIP)), "drift": 5,
    "items": [sign("LATE 1980s: THE 'IN THE BLACK' STORY", 1000, 110, C("retailers found"), color="#FFF8E1", size=32, sub="RETAILERS' REINVENTION (HISTORY.COM)"),
              it("bigtag", x=1000, y=420, at=C("from red ink"), was="RED INK (LOSS)", now="BLACK INK!", slashAt=C("to black"), nowAt=C("to black", 0.2), scale=1.2, until=C("But it's a reinvention")),
              G(1500, 0.3, face="grin", pose="talk", hold="clipboard", talk=[[C("This is the day"), C("from loss to profit", 1.0)]],
                faces=[[0, "grin"], [C("But it's a reinvention"), "worry"]]),
              it("docs", x=600, y=860, at=C("But it's a reinvention"), text="'IN THE BLACK' ORIGIN", scale=0.85, stamp="MYTH", stampAt=C("The police came first")),
              it("toonwords", text="POLICE FIRST!", x=1150, y=330, at=C("The police came first"), size=80, color="#FFFFFF")]},
    sources=["hist"])
stage("s09_turn", "a1_turn", {
    **W1("megamall", doorsAt=0.0, clockAt=0.0, dawn=0.9, mallX=0.5), "tone": "history", "toneShift": {"at": C("a real question"), "to": "sitcom", "dur": 0.6},
    "cam": cam((0, 1150, 520, 1.0), (C("How does a store"), 1000, 560, 1.45, WHIP)), "drift": 2,
    "items": [G(950, 0.2, face="worry", pose="shrug", faces=[[0, "worry"], [C("How does a store"), "panic"]], takes=[C("How does a store")]),
              D(1400, 0.3, face="dollar", hold="tv", pose="stand"),
              it("toonwords", text="SO... HOW?", x=1000, y=330, at=C("How does a store"), size=90)]})

# ====================================================================== ACT 2: the doorbuster trick
bumper("s10_b2", "a2_card", "2", "ACT TWO", "THE DOORBUSTER TRICK", "Prices may be closer than they appear", color="#E53950", gag="WAS: EVEN\nMORE")
stage("s11_door", "a2_door", {
    **W1("storefloor", padX=900, checkX=2300, tvX=-400),
    "cam": cam((0, 900, 480, 1.1), (C("Economists call it"), 1000, 500, 1.0, 1.4), (C("through the door"), 500, 540, 1.05, WHIP)), "drift": 4,
    "items": [it("toonwords", text="THE DOORBUSTER", x=900, y=100, at=0.3, until=C("Economists call it"), size=74),
              sign("SMALL BATCH · PRICED SO LOW", 1500, 230, C("priced so low"), color="#FFCDD2", size=30, until=C("Economists call it")),
              it("feeflow", **{"from": [900, 560], "to": [1600, 900]}, at=C("Sometimes less than nothing"), until=C("Economists call it", 1.0), n=5, color="#FF8A80", sym="-"),
              G(1450, 0.3, face="worry", hold="clipboard", pose="clipboard", faces=[[0, "worry"], [C("Sometimes less than nothing"), "panic"], [C("Its job isn't profit"), "smug"]]),
              it("toonwords", text="LOSS LEADER", x=1000, y=130, at=C("Economists call it"), size=90, color="#FFFFFF"),
              D([[0, -500], [C("get you through"), -500], [C("through the door", 0.6), 600]], C("get you through", -0.5), face="dollar", pose="run"),
              TB(1850, 0.5, face="deadpan", prints=[[C("Its job isn't profit"), "JOB:\nTRAFFIC"]])]})
stage("s12_basket", "a2_basket", {
    **W1("megamall", doorsAt=0.0, clockAt=0.0, dawn=0.95, mallX=0.47, banner="THANK YOU FOR SHOPPING!"),
    "cam": cam((0, 700, 560, 1.0), (C("You leave with"), 1200, 580, 1.0, 2.4)), "drift": 6,
    "items": [it("heapcart", x=[[0, 600], [C("You leave with"), 700], [C("never the headline deal"), 1350]], at=0.2, scale=1.25,
                 adds=[[C("You came for the television"), "TV", "#4FB3F6"], [C("a wall mount"), "WALL MOUNT"], [C("a cable"), "CABLE"], [C("a soundbar"), "SOUNDBAR"],
                       [C("a cart full"), "SNACKS"], [C("a cart full", 0.4), "BATTERIES"], [C("a cart full", 0.8), "GIFT WRAP"], [C("never the headline", -0.3), "SOCKS"]]),
              D([[0, 380], [C("You leave with"), 480], [C("never the headline deal"), 1130]], 0.2, face="grin", pose="hold", faces=[[0, "grin"], [C("a cart full"), "dollar"]]),
              sign("ONLY THE TV WAS THE HEADLINE DEAL", 1500, 140, C("never the headline deal", -0.4), color="#FFF59D", size=30),
              G(1900, 0.4, face="grin", pose="wave")]})
stage("s13_plan", "a2_plan", {
    **W1("storefloor", padX=-1200, checkX=1250, tvX=-300),
    "cam": cam((0, 1150, 540, 1.15), (C("Economists Jose Miguel"), 1050, 480, 1.0, 1.4), (C("Using failure rates"), 1050, 500, 1.0, 1.0)), "drift": 4,
    "items": [G(1230, 0.2, face="grin", pose="talk", talk=[[C("Would you like"), C("protection plan", 0.6)]], scale=1.3),
              it("bubble", text="WOULD YOU LIKE\nTHE PROTECTION PLAN?", x=1350, y=260, at=C("Would you like"), until=C("Economists Jose Miguel", 0.5), tail=[1260, 470], size=34),
              D(700, 0.2, hold="tv", face="happy", faces=[[0, "happy"], [C("Would you like", 0.5), "shock"]], takes=[C("Would you like", 0.5)]),
              sign("WARRANTIES AVERAGED ≈ 24% OF PRODUCT PRICE", 1050, 160, C("which averaged about"), color="#FFF8E1", size=30, sub="ABITO & SALANT, REVIEW OF ECONOMIC STUDIES (VIA KELLOGG INSIGHT)"),
              it("toonwords", text="UP TO 62–73% MARGIN", x=1050, y=360, at=C("profit margins as high as"), size=64, color="#FFC93C"),
              sign("TVs · ACADEMIC ESTIMATE FOR THE MARKET STUDIED", 1050, 470, C("profit margins as high as", 0.6), color="#FFE0B2", size=24),
              TB(1800, 0.3, face="dollar", prints=[[C("profit margins"), "PLAN:\nKA-CHING"]])]},
    sources=["kellogg"])
add("p14_trade", "a2_draw", "engine_draw", {
    "title": "The doorbuster trade (simplified)", "board": BOARD, "draw_start": C("Box one"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 470, 300, 220), "color": "risk", "width": 6, "kind": "box", "start": C("Box one"), "label": lbl("DOORBUSTER", 710, 560, 30, "risk")},
        {"d": dot(710, 630), "color": "risk", "width": 1, "start": C("a negative one"), "label": lbl("THIN OR NEGATIVE MARGIN", 710, 630, 20, "risk")},
        {"d": rect(1180, 400, 360, 360), "color": "accent3", "width": 7, "kind": "box", "start": C("Box two"), "label": lbl("THE REST OF THE CART", 1360, 470, 26, "accent3")},
        {"d": dot(1360, 540), "color": "ink", "width": 1, "start": C("The add-ons"), "label": lbl("ADD-ONS · CABLES", 1360, 540, 22, "ink")},
        {"d": dot(1360, 600), "color": "ink", "width": 1, "start": C("the plan"), "label": lbl("PROTECTION PLAN", 1360, 600, 22, "ink")},
        {"d": dot(1360, 660), "color": "ink", "width": 1, "start": C("the full-price items"), "label": lbl("FULL-PRICE ITEMS", 1360, 660, 22, "ink")},
        {"d": arrow((870, 580), (1170, 580), 0.12), "color": "accent", "width": 7, "kind": "arrow", "start": C("The arrow between them"), "label": lbl("FOOT TRAFFIC", 1020, 520, 26, "accent")},
        {"d": dot(1050, 840), "color": "accent2", "width": 1, "start": C("the price of a visitor"), "label": lbl("LOSS ON BOX ONE = PRICE OF A VISITOR", 1050, 840, 26, "accent2")},
    ],
    "actions": [{"kind": "point", "at": C("The arrow between them", 0.4), "dur": 1.4, "target": [1020, 580]}],
    "scale": 0.86, "floor": 1040})
stage("s15_factory", "a2_deriv", {
    **W1("tvfactory", machX=0.47, speed=170),
    "cam": cam((0, 1100, 470, 1.1), (C("Consumer Reports has described"), 1050, 450, 1.15, 1.6), (C("The industry calls them"), 1350, 470, 1.1, WHIP),
               (C("fewer HDMI inputs"), 1250, 500, 1.3, 1.2)), "drift": 6,
    "items": [it("toonwords", text="BUILT FOR THE DAY", x=1100, y=170, at=0.3, until=C("Consumer Reports has described"), size=74),
              sign("'MADE SPECIFICALLY FOR BLACK FRIDAY' · 'OFTEN … A SINGLE RETAILER'", 1050, 150, C("Consumer Reports has described"), color="#FFF8E1", size=26, sub="CONSUMER REPORTS (2018)", until=C("The industry calls them", -0.2)),
              it("toonwords", text="DERIVATIVES", x=1300, y=270, at=C("The industry calls them"), size=76, color="#FFFFFF"),
              sign("SIMILAR MODEL · NEW MODEL NUMBER · FEWER FEATURES", 1100, 390, C("different model numbers"), color="#FFE0B2", size=26),
              it("forklift", x=[[0, 2400], [C("The industry calls them"), 1700]], at=0.2, load=["SPECIAL EDITION", "SPECIAL EDITION"], lift=[[0, 0.1], [C("fewer HDMI"), 0.35]], scale=0.9, flip=True, face="happy"),
              TB(500, 0.4, face="deadpan", prints=[[C("fewer HDMI inputs"), "PORTS:\nFEWER"]])]},
    sources=["cr"])
stage("s16_compare", "a2_deriv2", {
    **W1("tvfactory", machX=0.2, speed=110),
    "cam": cam((0, 1050, 470, 1.1), (C("The catch is comparison"), 1350, 520, 1.3, WHIP)), "drift": 3,
    "items": [it("bigtag", x=700, y=330, at=C("cost about"), was="REGULAR MODEL", now="≈ $170 LESS", sub="ONE DERIVATIVE CR TESTED (2017)", slashAt=C("less than the model", 0.3), nowAt=C("less than the model", 0.5), scale=1.05),
              sign("PERFORMED JUST AS WELL (CR TEST)", 1100, 200, C("performed just as well"), color="#C8E6C9", size=30, until=C("The catch is comparison", -0.2)),
              D(1450, C("The catch is comparison", -0.3), hold="phone", face="dizzy", pose="stand", faces=[[0, "worry"], [C("you can't easily"), "dizzy"]]),
              it("bubble", text="SEARCH: ZERO\nOTHER STORES", x=1650, y=400, at=C("you can't easily"), tail=[1500, 560], size=30),
              sign("ONE STORE ONLY = HARD TO COMPARE", 1350, 220, C("If only one store"), color="#FFCDD2", size=30)]},
    sources=["cr"])
stage("s17_vendor", "a2_vendor", {
    **W1("storefloor", padX=1000, checkX=2500, tvX=-500),
    "cam": cam((0, 1000, 500, 1.0), (C("Target lists"), 1100, 480, 1.05, 1.6), (C("quietly paid by the brand"), 1000, 540, 1.15, WHIP)), "drift": 4,
    "items": [it("drone", x=[[0, 2400], [C("doesn't always pay"), 1000], [C("quietly paid"), 1000], [C("quietly paid", 2), -400]], y=[[0, 120], [C("doesn't always pay"), 230]], at=0.1, carry="FROM THE BRAND", scale=1.05),
              it("feeflow", **{"from": [1000, 380], "to": [1000, 640]}, at=C("reimbursement"), n=5, lift=40, per=0.9),
              it("docs", x=1600, y=860, at=C("Best Buy's annual report"), text="BEST BUY 10-K", scale=0.8, stamp="MARKDOWNS REIMBURSED", stampAt=C("cost of markdowns")),
              it("docs", x=400, y=860, at=C("Target lists"), text="TARGET 10-K", scale=0.8, stamp="MARKDOWN ALLOWANCES", stampAt=C("among the money")),
              G(1350, 0.3, face="smug", pose="talk", talk=[[C("Part of your price cut"), C("by the brand", 0.6)]], scale=1.25),
              TB(1950, 0.5, face="wink", prints=[[C("quietly paid"), "SPONSORED\nBY THE BRAND"]])]},
    sources=["bby10k", "tgt10k"])
stage("s18_clear", "a2_clear", {
    **W1("dccity", storeX=0.66),
    "cam": cam((0, 900, 520, 1.0), (C("Moving it"), 1300, 560, 1.05, 1.6)), "drift": 8,
    "items": [it("forklift", x=[[0, 300], [C("Moving it"), 1300]], at=0.2, load=["LAST SEASON", "LAST SEASON", "LAST SEASON"], lift=[[0, 0.2], [C("Moving it"), 0.05]], scale=0.95),
              sign("STOCK THAT SITS LOSES VALUE", 1000, 130, C("Stock that sits"), color="#FFE0B2", size=32),
              it("toonwords", text="BOXES → CASH", x=1300, y=280, at=C("back into cash"), size=80),
              it("feeflow", **{"from": [1300, 600], "to": [1900, 300]}, at=C("back into cash"), n=6)]})

# ====================================================================== ACT 3: the quarter that pays
bumper("s19_b3", "a3_card", "3", "ACT THREE", "THE QUARTER THAT PAYS FOR THE YEAR", "Brought to you by the fourth quarter", color="#2E9E5B", gag="WAS: $9,999\nAND CHANGE")
stage("s20_quarter", "a3_quarter", {
    **W1("quarterhq", towerX=0.403, growAt=C("it brought in")),
    "cam": cam((0, 1000, 640, 1.05), (C("it brought in"), 1000, 420, 0.82, 1.8), (C("That's about a third"), 1100, 460, 0.9, 1.4)), "drift": 3,
    "items": [it("calendar", x=1650, y=300, at=C("thirteen weeks"), pages=[[0, "13/52"]], text="WEEKS IN Q4", scale=0.85, until=C("it brought in", -0.2)),
              sign("BEST BUY · FISCAL 2026 (ENDED JAN 31, 2026)", 1000, -10, C("In fiscal"), color="#FFFFFF", size=28, until=C("That's about a third", -0.3)),
              it("counter", x=1700, y=430, at=C("it brought in"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [C("it brought in"), 0], [C("of revenue"), 13.8]], text="Q4 REVENUE"),
              sign("OF $41.7BN FOR THE YEAR", 1700, 640, C("for the whole year"), color="#FFF8E1", size=28),
              it("toonwords", text="≈ 1/3 OF THE MONEY", x=1000, y=60, at=C("That's about a third"), size=66),
              sign("OUR CALCULATION (8-K)", 1700, 760, C("by our calculation"), color="#FFE0B2", size=24),
              G(330, 0.3, face="panic", hold="clipboard", pose="clipboard", faces=[[0, "worry"], [C("it brought in"), "grin"]], scale=1.2)]},
    sources=["bbyq4", "bby10k"])
stage("s21_margin", "a3_margin", {
    **W1("storefloor", padX=-1000, checkX=2600, tvX=-600),
    "cam": cam((0, 960, 540, 1.0), (C("Operating income"), 1000, 520, 1.05, 1.4)), "drift": 3,
    "items": [chart([{"label": "HOLIDAY QUARTER", "value": 20.9, "color": "#E53950", "at": C("gross margin was"), "display": "20.9%"},
                     {"label": "FULL YEAR", "value": 22.5, "color": "#2F6FD1", "at": C("for the full year", -0.5), "display": "22.5%"}],
                    at=0.2, max=25, title="BEST BUY GROSS MARGIN, FISCAL 2026", x=330, y=220, w=760, h=470, until=C("Operating income", 1.2)),
              sign("DISCOUNTS SHAVE THE %", 1500, 230, C("Discounts shave"), color="#FFCDD2", size=30),
              sign("VOLUME BRINGS BACK THE $", 1500, 360, C("Volume brings back"), color="#C8E6C9", size=30),
              it("toonwords", text="Q4 ≈ HALF OF OPERATING INCOME", x=980, y=140, at=C("Operating income", 1.3), size=54),
              sign("$721M OF $1,389M (GAAP) · OUR CALCULATION", 980, 280, C("again our calculation", -0.6), color="#FFE0B2", size=26),
              D(1550, C("Volume brings back"), hold="tv", face="dollar", pose="run", xk=[[C("Volume brings back"), 2400], [C("Operating income"), 1600]]),
              TB(1850, 0.4, face="dollar")]},
    sources=["bbyq4"])
add("p22_bars", "a3_draw", "engine_draw", {
    "title": "Best Buy revenue per quarter, fiscal 2026", "board": BOARD, "draw_start": C("Let me chart it"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 800 L 1480 800", "color": "ink", "width": 5, "start": C("Let me chart it")},
        {"d": "M 700 800 L 700 545 L 940 545 L 940 800 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("The other three quarters"), "label": lbl("AVG. OF Q1-Q3 · ≈ $9.3BN", 820, 525, 22, "accent2")},
        {"d": "M 1160 800 L 1160 420 L 1400 420 L 1400 800 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("The holiday quarter brought"), "label": lbl("HOLIDAY Q4 · $13.8BN", 1280, 400, 22, "risk")},
        {"d": dot(1050, 860), "color": "muted", "width": 1, "start": C("stock up and staff up"), "label": lbl("8-K (MAR 2026) · AVERAGE IS OUR CALCULATION", 1050, 860, 18, "muted")},
        {"d": dot(1050, 330), "color": "accent3", "width": 1, "start": C("Target's annual report"), "label": lbl("TARGET 10-K: LARGER SHARE OF SALES IN Q4", 1050, 330, 22, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("That tall bar", 0.1), "dur": 1.4, "target": [1280, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["bbyq4", "tgt10k"])
stage("s23_crowd", "a3_crowd", {
    **W1("megamall", doorsAt=0.0, clockAt=0.0, dawn=0.8, mallX=0.47, banner="RECORD WEEKEND"),
    "cam": cam((0, 1100, 460, 0.9), (C("On Black Friday itself"), 1150, 520, 1.0, WHIP)), "drift": 5,
    "items": [it("stampede", at=0.3, x0=-400, x1=2600, n=21, dur=5.0, scale=0.95, seed=3),
              it("counter", x=1150, y=170, at=C("counted a record"), suffix="M", decimals=1, steps=[[0, 0], [C("counted a record"), 0], [C("shoppers in its survey"), 202.9]], text="SHOPPERS, THANKSGIVING–CYBER MONDAY 2025 (NRF SURVEY)", until=C("On Black Friday itself")),
              chart([{"label": "IN STORES", "value": 80.3, "color": "#E53950", "at": C("shopped in stores", -0.5), "display": "80.3M"},
                     {"label": "ONLINE", "value": 85.7, "color": "#2F6FD1", "at": C("shopped in stores", 0.6), "display": "85.7M"}],
                    at=C("On Black Friday itself"), max=100, title="BLACK FRIDAY 2025 SHOPPERS (NRF SURVEY)", x=650, y=160, w=800, h=380),
              G(1950, 0.3, face="panic", pose="armsup", scale=1.25)]},
    sources=["nrf_wk"])
stage("s24_online", "a3_online", {
    **W1("adarena", phoneX=0.48, slots=["CYBER WEEK", "DEAL", "DEAL"], winAt=C("The five days of Cyber Week"), query="cyber week deals", board="ONLINE SPENDING"),
    "cam": cam((0, 1150, 420, 0.86), (C("The five days"), 1150, 440, 0.88, 1.4)), "drift": 2,
    "items": [chart([{"label": "THANKSGIVING", "value": 6.4, "color": "#7E57C2", "at": C("Online, Adobe measured"), "display": "$6.4BN"},
                     {"label": "BLACK FRIDAY", "value": 11.8, "color": "#E53950", "at": C("on Black Friday", -0.3), "display": "$11.8BN"},
                     {"label": "CYBER MONDAY", "value": 14.25, "color": "#2F6FD1", "at": C("on Cyber Monday", -0.5), "display": "$14.25BN"}],
                    at=0.2, max=16, title="U.S. ONLINE SPENDING, 2025 (ADOBE)", x=200, y=170, w=640, h=480, dark=True),
              sign("BLACK FRIDAY +9.1% VS 2024", 440, 780, C("up nine percent"), color="#C8E6C9", size=28),
              sign("CYBER WEEK: $44.2BN", 1990, 260, C("reached"), color="#FFF59D", size=34),
              sign("56.4% OF ONLINE PURCHASES ON PHONES", 1376, 950, C("made on phones", -0.6), color="#BBDEFB", size=26),
              it("drone", x=[[0, 2600], [10, -400]], y=60, at=0.2, carry="ORDER", scale=0.8)]},
    sources=["adobe_jan", "adobe_cm"])
stage("s25_stores", "a3_stores", {
    **W1("storefloor", padX=-1300, checkX=1900, tvX=-700),
    "cam": cam((0, 1000, 520, 1.05), (C("More than four out of"), 1150, 520, 1.0, WHIP)), "drift": 5,
    "items": [chart([{"label": "E-COMMERCE", "value": 18.3, "color": "#2F6FD1", "at": C("e-commerce was only"), "display": "18.3%"},
                     {"label": "EVERYTHING ELSE", "value": 81.7, "color": "#E53950", "at": C("More than four out of"), "display": "81.7%"}],
                    at=0.3, max=100, title="SHARE OF U.S. RETAIL SALES, Q4 2025 (CENSUS)", x=300, y=200, w=760, h=470),
              sign("NOT SEASONALLY ADJUSTED · 81.7% = OUR SUBTRACTION", 700, 830, C("still spent offline"), color="#FFFFFF", size=22),
              S(2, [[0, 2500], [7, 1300]], 0.2, hold="bag", face="grin"), S(4, [[0, 2700], [8, 1550]], 0.4, hold="box", face="grin"),
              S(6, [[0, 2900], [9, 1800]], 0.6, hold="bag", face="happy"),
              it("toonwords", text="THE STAMPEDE SHARES THE STAGE", x=1300, y=110, at=C("The stampede is real"), size=50)]},
    sources=["census"])
stage("s26_next", "a3_next", {
    **W1("megamall", doorsAt=999, clockAt=999, dawn=0.5, mallX=0.47, banner="NEXT UP: NOV 27, 2026"),
    "cam": cam((0, 1150, 480, 1.0), (C("That's a forecast"), 1150, 520, 1.2, WHIP)), "drift": 3,
    "items": [it("counter", x=1150, y=180, at=C("Adobe forecasts"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [C("Adobe forecasts"), 0], [C("online on Black Friday"), 12.9]], text="BLACK FRIDAY 2026 ONLINE · FORECAST (ADOBE)"),
              it("docs", x=1650, y=860, at=C("That's a forecast"), text="ADOBE · SEP 2026", scale=0.75, stamp="FORECAST", stampAt=C("not a result")),
              TB(600, 0.3, face="happy", prints=[[C("That's a forecast"), "RESULT:\nTBD"]]),
              D(900, 0.4, face="dollar", hold="coffee", pose="sip")]},
    sources=["adobe_fc"])

# ====================================================================== ACT 4: everyone takes a cut
bumper("s27_b4", "a4_card", "4", "ACT FOUR", "EVERYONE TAKES A CUT", "Every swipe comes with a toll booth", color="#7E57C2", gag="WAS: $99,999\nPLUS FEES")
stage("s28_rails", "a4_cards", {
    **W1("payrails", gates=["INTERCHANGE", "INTERCHANGE"], gateX=620, gateGap=820, bank1X=1050, bank2X=2300),
    "cam": cam((0, 700, 480, 1.3), (C("The Federal Reserve counted"), 1050, 420, 1.1, 1.8), (C("For smaller"), 1450, 470, 1.25, WHIP)), "drift": 6,
    "items": [it("toonwords", text="EVERY SWIPE PAYS A TOLL", x=700, y=170, at=0.2, until=C("The Federal Reserve counted"), size=62),
              it("counter", x=1050, y=120, at=C("The Federal Reserve counted"), prefix="$", suffix="BN", decimals=2, steps=[[0, 0], [C("The Federal Reserve counted"), 0], [C("in twenty twenty-three"), 34.12]], text="DEBIT & PREPAID INTERCHANGE, 2023 (FEDERAL RESERVE)", until=C("For big banks", 1.5)),
              sign("BIG BANKS (CAPPED): ≈ 22–24¢ PER PURCHASE", 1000, 120, C("is capped"), color="#C8E6C9", size=30, until=C("For smaller", -0.2)),
              sign("SMALLER, EXEMPT BANKS: ≈ 52¢", 1500, 260, C("For smaller"), color="#FFE0B2", size=30)]},
    sources=["fed"])
stage("s29_net", "a4_net", {
    **W1("payrails", gates=["NETWORK FEE", "INTERCHANGE", "NETWORK FEE"], gateX=500, gateGap=700, bank1X=-300, bank2X=1250),
    "cam": cam((0, 1250, 450, 1.1), (C("And credit cards"), 900, 470, 1.25, WHIP), (C("On a record weekend"), 1150, 470, 1.05, 1.6)), "drift": 6,
    "items": [it("counter", x=1250, y=120, at=C("the card networks collected"), prefix="$", suffix="BN", decimals=2, steps=[[0, 0], [C("the card networks collected"), 0], [C("in network fees"), 12.95]], text="NETWORK FEES, DEBIT & PREPAID, 2023 (FED)", until=C("And credit cards")),
              sign("CREDIT CARDS: NOT UNDER THE DEBIT CAP", 900, 200, C("And credit cards"), color="#FFCDD2", size=32, until=C("On a record weekend", 0.3)),
              D([[0, -300], [C("On a record weekend"), -300], [C("toll booth", 1.0), 1700]], C("On a record weekend", -0.4), hold="card", face="dollar", pose="run", scale=1.1),
              it("toonwords", text="TOLL! TOLL! TOLL!", x=1150, y=200, at=C("every lane"), size=70)]},
    sources=["fed"])
stage("s30_bnpl", "a4_bnpl", {
    **W1("bnplride", rideX=0.5, x0=-800, x1=3400, spin=1.1),
    "cam": cam((0, 1300, 480, 1.1), (C("Adobe says"), 1550, 480, 1.1, 1.6)), "drift": 4,
    "items": [it("toonwords", text="BUY NOW, PAY LATER", x=1300, y=80, at=0.3, until=C("Adobe says"), size=70),
              sign("$20BN ONLINE · HOLIDAY 2025 (+9.8%)", 2050, 130, C("it drove"), color="#FFF59D", size=32, sub="ADOBE ANALYTICS"),
              sign("CYBER MONDAY: $1.03BN", 2050, 300, C("on Cyber Monday alone"), color="#BBDEFB", size=30),
              D(720, 0.3, face="love", pose="cheer", hops=[C("Split the price"), C("on Cyber Monday")], scale=1.2),
              S(3, 2450, 0.5, face="grin", hold="bag", scale=1.15)]},
    sources=["adobe_jan", "adobe_cm"])
stage("s31_fee", "a4_fee", {
    **W1("bnplride", rideX=0.35, x0=-800, x1=3400, boothDX=900, feeAt=C("Often, the merchant")),
    "cam": cam((0, 900, 470, 1.0), (C("Often, the merchant"), 1350, 600, 1.4, WHIP), (C("merchant fees averaged"), 1550, 500, 1.05, 1.4)), "drift": 3,
    "items": [G([[0, 1000], [C("Often, the merchant"), 1350]], 0.2, face="worry", faces=[[0, "happy"], [C("Often, the merchant"), "panic"]], takes=[C("Often, the merchant")], scale=1.2),
              it("feeflow", **{"from": [1350, 520], "to": [1850, 640]}, at=C("Often, the merchant", 0.5), n=6, lift=120),
              sign("MERCHANT FEES ≈ 2.49% OF VOLUME (2021)", 1500, 160, C("merchant fees averaged"), color="#FFF8E1", size=30, sub="CFPB STUDY OF FIVE BNPL LENDERS"),
              sign("THE PITCH: BIGGER BASKETS", 1500, 330, C("bigger baskets"), color="#C8E6C9", size=30)]},
    sources=["cfpb"])
add("p32_flow", "a4_draw", "engine_draw", {
    "title": "Who gets paid on one purchase (simplified)", "board": BOARD, "draw_start": C("The shopper pays"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 520, 200, 110), "color": "ink", "width": 6, "kind": "box", "start": C("The shopper pays"), "label": lbl("SHOPPER", 640, 585, 26, "ink")},
        {"d": arrow((750, 575), (880, 575)), "color": "accent", "width": 6, "kind": "arrow", "start": C("pays the store")},
        {"d": rect(890, 520, 200, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("pays the store", 0.3), "label": lbl("STORE", 990, 585, 26, "accent3")},
        {"d": arrow((1100, 545), (1250, 430), 0.1), "color": "risk", "width": 5, "kind": "arrow", "start": C("one slice goes")},
        {"d": rect(1260, 380, 240, 90), "color": "risk", "width": 5, "kind": "box", "start": C("issued the card"), "label": lbl("CARD ISSUER", 1380, 435, 22, "risk")},
        {"d": arrow((1100, 575), (1250, 575)), "color": "risk", "width": 5, "kind": "arrow", "start": C("one to the card network")},
        {"d": rect(1260, 530, 240, 90), "color": "risk", "width": 5, "kind": "box", "start": C("one to the card network", 0.4), "label": lbl("CARD NETWORK", 1380, 585, 22, "risk")},
        {"d": arrow((1100, 610), (1250, 720), -0.1), "color": "accent2", "width": 5, "kind": "arrow", "start": C("if you split")},
        {"d": rect(1260, 680, 240, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("one to the lender"), "label": lbl("BNPL LENDER", 1380, 735, 22, "accent2")},
        {"d": rect(890, 330, 200, 90), "color": "muted", "width": 5, "kind": "box", "start": C("before you ever clicked"), "label": lbl("AD SELLER", 990, 385, 22, "muted")},
        {"d": arrow((990, 510), (990, 430)), "color": "muted", "width": 5, "kind": "arrow", "start": C("paid to show you the ad")},
    ],
    "actions": [{"kind": "point", "at": C("one to the card network", 0.2), "dur": 1.4, "target": [1380, 575]}],
    "scale": 0.86, "floor": 1040}, sources=["fed", "cfpb"])
stage("s33_ads", "a4_ads", {
    **W1("adarena", phoneX=0.48, winAt=C("Amazon earned"), slots=["SPONSORED", "SPONSORED", "DEAL"]),
    "cam": cam((0, 1150, 450, 1.0), (C("Amazon earned"), 1050, 450, 1.05, 1.6)), "drift": 2,
    "items": [it("toonwords", text="ADS ON THE STORE'S OWN APP", x=480, y=140, at=C("Retailers now sell ads"), size=40, until=C("Amazon earned")),
              it("counter", x=450, y=330, at=C("Amazon earned"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [C("Amazon earned"), 0], [C("from advertising services"), 68.6]], text="AMAZON AD SERVICES, 2025 (10-K)"),
              sign("RETAIL MEDIA: BEST BUY ADS · TARGET'S ROUNDEL", 1376, 950, C("Best Buy and Target"), color="#FFF59D", size=26)]},
    sources=["amzn10k", "tgt10k", "bby10k"])
stage("s34_aff", "a4_aff", {
    **W1("adarena", phoneX=0.55, winAt=C("the first deal you see"), slots=["SPONSORED", "INFLUENCER PICK", "DEAL"], query="best black friday deal"),
    "cam": cam((0, 1250, 450, 1.0), (C("On Black Friday"), 1400, 430, 1.0, WHIP)), "drift": 2,
    "items": [it("counter", x=640, y=200, at=C("drove"), suffix="%", decimals=1, steps=[[0, 0], [C("drove"), 0], [C("of online holiday revenue"), 20.4]], text="AFFILIATES & PARTNERS · HOLIDAY 2025 (ADOBE)"),
              S(5, 640, 0.3, hold="phone", pose="talk", face="grin", talk=[[0.5, C("drove")]], label="AN INFLUENCER", scale=1.25),
              it("toonwords", text="PAID TO BE FIRST", x=1810, y=-75, at=C("may be the one"), size=70)]},
    sources=["adobe_jan"])

# ====================================================================== ACT 5: the hangover
bumper("s35_b5", "a5_card", "5", "ACT FIVE", "THE HANGOVER", "Receipt not included", color="#FF8A1F", gag="WAS: $9,999,999\n(REFERENCE)")
stage("s36_returns", "a5_returns", {
    **W1("returnsmtn", mtnX=0.5, growAt=C("expected")),
    "cam": cam((0, 1000, 640, 1.1), (C("expected"), 1000, 440, 0.85, 2.4), (C("And they believed"), 1150, 480, 0.95, 1.4)), "drift": 4,
    "items": [it("calendar", x=1700, y=200, at=0.2, pages=[[0, "JAN"]], text="THE MORNING AFTER", scale=0.8, until=C("expected")),
              it("toonwords", text="17% OF HOLIDAY SALES COME BACK", x=1000, y=-60, at=C("of holiday sales"), size=56),
              sign("RETAILER ESTIMATE (NRF / HAPPY RETURNS, 2025)", 1000, 50, C("to come back"), color="#FFF8E1", size=24),
              sign("2025: ≈ $849.9BN RETURNED · 15.8% OF SALES", 1550, 230, C("they estimated returns"), color="#FFE0B2", size=28),
              sign("≈ 9% OF RETURNS FRAUDULENT (RETAILERS' VIEW)", 1550, 380, C("were fraudulent", -0.5), color="#FFCDD2", size=28),
              it("forklift", x=[[0, 300], [C("And they believed"), 650]], at=0.4, load=["RETURN", "RETURN"], lift=[[0, 0.1], [C("expected"), 0.4]], scale=0.9, face="happy",
                 faces=[[0, "happy"], [C("were fraudulent"), "shock"]])]},
    sources=["nrf_ret"])
stage("s37_mountain", "a5_mountain", {
    **W1("returnsmtn", mtnX=0.62),
    "cam": cam((0, 1350, 500, 1.0), (C("Online orders"), 1500, 470, 0.95, 1.8), (C("Part of the holiday profit"), 1100, 600, 1.35, WHIP)), "drift": 4,
    "items": [sign("SHIP BACK", 760, 130, C("shipped back"), color="#BBDEFB", size=30), sign("CHECK", 1080, 130, C("checked"), color="#BBDEFB", size=30),
              sign("REPACK", 1360, 130, C("repacked"), color="#BBDEFB", size=30), sign("SELL OFF CHEAP", 1720, 130, C("sold off cheap"), color="#FFCDD2", size=30),
              it("drone", x=[[0, 2400], [C("Online orders"), 1500]], y=[[0, 200], [C("Online orders"), 330]], at=C("Online orders", -0.5), carry="RETURN", scale=1.0, face="squint"),
              sign("ONLINE: ≈ 19.3% RETURNED (2025 EST.)", 1500, 260, C("of online sales"), color="#FFF59D", size=30),
              G(1100, C("Part of the holiday profit", -0.5), face="panic", pose="armsup", scale=1.25),
              it("feeflow", **{"from": [1100, 560], "to": [300, 900]}, at=C("leaks out the back door"), n=6, color="#FF8A80", sym="-")]},
    sources=["nrf_ret"])
stage("s38_real", "a5_real", {
    **W1("storefloor", padX=-1200, checkX=2500, tvX=1700),
    "cam": cam((0, 900, 520, 1.05), (C("of them were"), 1000, 500, 1.0, 1.4), (C("That's one study"), 1150, 540, 1.1, WHIP)), "drift": 4,
    "items": [TB(700, 0.2, scale=1.3, faces=[[0, "deadpan"], [C("of them were"), "wink"]], prints=[[C("are the deals even real"), "WAS: $9,999,999\nNOW: SALE!"]]),
              it("toonwords", text="REAL DEALS?", x=1000, y=110, at=0.2, until=C("In Britain"), size=90),
              sign("UK STUDY · WHICH? · 227 BLACK FRIDAY 2023 DEALS", 1150, 120, C("In Britain"), color="#FFF8E1", size=28, sub="EIGHT UK RETAILERS · PUBLISHED NOV 2024"),
              it("counter", x=1300, y=360, at=C("of them were"), suffix="%", steps=[[0, 0], [C("of them were"), 0], [C("same price or cheaper"), 92]], text="SAME PRICE OR CHEAPER AT OTHER TIMES"),
              D(1800, C("That's one study"), face="worry", hold="phone", pose="stand", scale=1.25, faces=[[0, "worry"], [C("the lesson travels"), "smug"]])]},
    sources=["which"])
add("p39_price", "a5_draw", "engine_draw", {
    "title": "One price over a year (illustrative)", "board": BOARD, "draw_start": C("Here's one price"), "speed": 1300, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 800 L 1500 800 M 600 800 L 600 380", "color": "ink", "width": 5, "start": C("Here's one price")},
        {"d": "M 620 640 L 820 640 L 860 470 L 1080 470", "color": "accent2", "width": 6, "start": C("It sits high"), "label": lbl("'REFERENCE' PRICE", 960, 450, 22, "accent2")},
        {"d": "M 860 640 L 760 640", "color": "accent3", "width": 6, "start": C("this low in the summer"), "label": lbl("SUMMER: THIS LOW TOO", 720, 680, 20, "accent3")},
        {"d": "M 1080 470 L 1180 470 L 1220 650 L 1320 650", "color": "risk", "width": 6, "start": C("Then it drops"), "label": lbl("BLACK FRIDAY", 1270, 690, 22, "risk")},
        {"d": arrow((1150, 480), (1200, 630), 0.1), "color": "risk", "width": 5, "kind": "arrow", "start": C("a big percentage off"), "label": lbl("'BIG % OFF'", 1290, 560, 24, "risk")},
        {"d": "M 1320 650 L 1420 470 L 1480 470", "color": "accent2", "width": 6, "start": C("But look")},
        {"d": dot(1050, 860), "color": "muted", "width": 1, "start": C("Not always against the year"), "label": lbl("ILLUSTRATIVE · NO REAL PRODUCT", 1050, 860, 20, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("this low in the summer", 0.2), "dur": 1.4, "target": [760, 640]}],
    "scale": 0.86, "floor": 1040})
stage("s40_adobe", "a5_adobe", {
    **W1("storefloor", padX=1500, checkX=-900, tvX=300),
    "cam": cam((0, 1000, 500, 1.0), (C("The trick is"), 1080, 500, 1.05, 1.4)), "drift": 2,
    "items": [chart([{"label": "ELECTRONICS", "value": 30.9, "color": "#2F6FD1", "at": C("off listed prices"), "display": "30.9%"},
                     {"label": "TOYS", "value": 29.6, "color": "#E53950", "at": C("on toys", -0.4), "display": "29.6%"},
                     {"label": "TVs", "value": 24.3, "color": "#7E57C2", "at": C("on toys", 0.4), "display": "24.3%"}],
                    at=0.3, max=35, title="PEAK DISCOUNT OFF LISTED PRICE, HOLIDAY 2025 (ADOBE)", x=220, y=210, w=900, h=470),
              it("bigtag", x=1500, y=180, at=C("The trick is"), was="LISTED PRICE = ?", now="KNOW IT!", scale=0.85, nowAt=C("what the listed price", 0.3)),
              D(1850, 0.3, face="happy", hold="phone", faces=[[0, "happy"], [C("The trick is"), "smug"]], scale=1.25)]},
    sources=["adobe_jan"])

# ====================================================================== PAYOFF + TEASER + BUTTON
stage("s41_payoff", "payoff", {
    **W1("megamall", doorsAt=0.0, clockAt=0.0, dawn=1.0, mallX=0.47, banner="SEE YOU NEXT BLACK FRIDAY"),
    "cam": cam((0, 1150, 430, 0.82), (C("Not on the doorbuster"), 1150, 450, 0.9, 1.6), (C("And a whole crowd"), 1150, 440, 0.86, 1.8)), "drift": 2,
    "items": [it("toonwords", text="NOT THE DOORBUSTER. THE VISIT.", x=1150, y=40, at=C("Not on the doorbuster"), until=C("And a whole crowd"), size=48),
              sign("THE CART", 500, 180, C("The cart around"), color="#C8E6C9", size=30),
              sign("THE PLAN", 880, 120, C("the plan at the register"), color="#C8E6C9", size=30),
              sign("SUPPLIER MARKDOWN MONEY", 1300, 180, C("the supplier"), color="#C8E6C9", size=30),
              sign("THE QUARTER THAT CARRIES THE YEAR", 1800, 120, C("the one quarter"), color="#FFF59D", size=28),
              it("toonwords", text="+ CARDS · LENDERS · AD SELLERS", x=1150, y=40, at=C("And a whole crowd"), size=46, color="#FFFFFF"),
              G(600, 0.2, face="grin", pose="wave", hold="clipboard", scale=1.25), D(1700, 0.3, face="dollar", hold="tv", scale=1.25, hops=[C("whether your deal")]),
              TB(1100, 0.5, face="happy", scale=1.1), S(2, 300, 0.6, face="grin", hold="bag"), S(5, 2000, 0.7, face="grin", hold="bag"),
              it("drone", x=[[0, -300], [12, 2600]], y=-150, at=0.2, carry="PROFIT?", scale=0.8),
              it("forklift", x=[[0, 2700], [6, 2300]], at=0.3, load=["RETURNS"], scale=0.7, flip=True)]})
add("s42_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s43_button", "button", {
    **W1("storefloor", padX=-1200, checkX=1350, tvX=-500), "cam": cam((0, 1000, 520, 1.15), (2.6, 1000, 480, 1.3, WHIP)), "drift": 0, "min_seconds": 5.2,
    "items": [TB(1000, 0.0, scale=1.3, faces=[[0, "deadpan"], [2.6, "wink"]], prints=[[0.6, "THIS VIDEO\nWAS $0 · NOW $0"]]),
              G(600, 0.1, face="deadpan", hold="clipboard", faces=[[0, "deadpan"], [2.6, "grin"]], scale=1.3, hops=[2.7]),
              D(1450, 0.2, face="shock", faces=[[0, "shock"], [2.6, "love"]], scale=1.3, takes=[1.6], hops=[2.8]),
              it("bubble", text="0% OFF?!", x=1500, y=260, at=1.5, until=2.5, tail=[1450, 470], size=40, shout=True),
              it("toonwords", text="BEST DEAL ALL YEAR", x=1000, y=150, at=2.7, size=76)]},
    sfx=[{"kind": "hit", "at": 2.6, "gain": 0.3}])

write(OUT, "# GENERATED by tools/gen_blackfriday_storyboard.py; edit the generator, not this file.\n"
           "# Episode 56 storyboard (Black Friday): sitcom-style episode; bespoke worlds in CartoonStage/sitcom.tsx; tones from visual_direction.yaml.\n")
