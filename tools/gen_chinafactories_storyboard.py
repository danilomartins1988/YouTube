"""Generates projects/why-the-world-still-depends-on-chinese-factories/deliverables/documentary/storyboard.yaml
(Episode 60: Why the World Still Depends on Chinese Factories).

OWNER DIRECTION (as Ep 56): feel like an actual episode of a prime-time animated TV sitcom; genre level only, everything original.
TV structure: cold open gag (Mel's toaster dies; every appliance gets an origin tag) -> channel intro (our "theme") -> show TITLE
CARD with a typed joke subtitle -> four acts, each opened by a BUMPER where a drone delivers the next part of Mel's new toaster
(the GIZMO: the running gag, every parcel "FROM: DOWN THE STREET") -> payoff -> end card -> button joke (the plug's tag).
Cast (toon rig, fictional): MEL (shopper), WEI (line engineer: a competent professional), KIP (relocation consultant).
Bespoke sets (CartoonStage/factory.tsx): kitchen, megafloor, partsstreet, megaport, refinery, solarline, tariffwall, movingday,
fctitle, fcbumper. Signature animations: the everything floor (s06), the parts street lighting up (s13), the rare-earth cascade
(s18), the tariff wall growing and toppling (s22-s24), the boxes that walk back home (s27/s32).
Presenter boards: p08 (stacked bars), p14 (cluster diagram), p25 (who pays: boxes + arrows), p30 (import shares bars).
Respectful and neutral toward China and its people. No logos; no real people; jokes never change a number.
Run: python tools/gen_chinafactories_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-the-world-still-depends-on-chinese-factories/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
TEAL, ORANGE, RED, GREEN, PURPLE, NAVY = "#1F7A8C", "#FF9F1C", "#E5484D", "#2E9E5B", "#7E57C2", "#16232E"


def toon(x, at=0.0, **kw):
    if "xk" in kw:
        x = kw.pop("xk")
    return it("toon", x=x, at=at, **kw)


def MEL(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.35)
    return toon(x, at, who="shopper", v=2, skin=2, hair=0, hairStyle=3, color="#FF8A65", glasses=False, scarf="#FFD23F", **kw)


def WEI(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.35)
    return toon(x, at, who="shopper", v=1, skin=0, hair=1, hairStyle=4, color=TEAL, glasses=True, scarf="#FFFFFF", **kw)


def KIP(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.35)
    return toon(x, at, who="shopper", v=3, skin=4, hair=3, hairStyle=2, color="#5C6BC0", glasses=False, scarf=RED, **kw)


def WK(v, x, at=0.0, **kw):
    """a generic factory worker (teal/orange work shirts)"""
    kw.setdefault("scale", 1.15)
    return toon(x, at, who="shopper", v=v, color=[TEAL, ORANGE, "#26A69A", "#5C6BC0"][v % 4], **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def chart(bars_, at=0.2, **kw):
    kw.setdefault("panel", True)
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


PARTS_ALL = [[0, "BODY"], [0, "SLOTS"], [0, "COIL"], [0, "LEVER"], [0, "KNOB"], [0, "PLUG"], [0, "FEET"]]


def gz(n_have, new=(), x=1600, y=1000, at=0.0, **kw):
    """the GIZMO with n_have parts already in, plus new [[t, label], ...] arriving"""
    parts = [[0, p[1]] for p in PARTS_ALL[:n_have]] + [list(p) for p in new]
    kw.setdefault("scale", 0.75)
    return it("gizmo", x=x, y=y, at=at, parts=parts, **kw)


def bumper(id_, seg, num, act, title, caption, color, have, new_parts, drone_txt="FROM: DOWN THE STREET"):
    items = [gz(have, [[1.6 + k * 0.5, p] for k, p in enumerate(new_parts)], x=1620, y=1010, at=0.5, scale=0.55, face="happy",
                faces=[[0, "worry"], [1.6, "happy"]]),
             it("drone", x=[[0, 2300], [1.4, 1620], [3.2, 1620], [4.2, -300]], y=[[0, 120], [1.4, 760], [3.2, 760], [4.2, 120]], at=0.3,
                carry=drone_txt, scale=0.9)]
    stage(id_, seg, {**W1("fcbumper", num=num, act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "sitcom",
                     "min_seconds": 4.2, "items": items}, sfx=[{"kind": "hit", "at": 0.15, "gain": 0.3}, {"kind": "whoosh", "at": 0.05, "gain": 0.25}])


# ====================================================================== COLD OPEN (the toaster dies)
stage("s01_open", "co_open", {
    **W1("kitchen", counterX=300, windowX=1250, tags=[[C("The kettle"), 0], [C("The lamp"), 1], [C("The charger"), 3], [C("again and again"), 2]]),
    "cam": cam((0, 950, 520, 1.2), (C("flips it over"), 760, 560, 1.45, 1.2), (C("Made in China"), 760, 520, 1.7, WHIP),
               (C("The kettle"), 600, 520, 1.15, 1.0), (C("The lamp"), 800, 500, 1.1, 0.9), (C("The charger"), 1000, 520, 1.05, 0.9),
               (C("again and again"), 900, 520, 0.95, 1.2)), "drift": 3,
    "items": [gz(7, x=[[0, 760], [C("flips it over"), 760]], y=610, at=0.1, scale=0.55, face="dead", smokeAt=0.3, stamp="MADE IN CHINA",
                 stampAt=C("Made in China", -0.2), stampY=-110),
              it("toonwords", text="A TOASTER DIES", x=950, y=170, at=0.3, until=C("Its owner"), size=70),
              MEL([[0, 1500], [C("Its owner"), 1100], [C("buy a new one"), 1100], [C("The kettle"), 550], [C("The lamp"), 800], [C("The charger"), 1150]], 0.2,
                  label="MEL · JUST WANTS TOAST", labelUntil=C("flips it over", 1.0),
                  faces=[[0, "worry"], [C("Made in China"), "shock"], [C("buy a new one"), "smug"], [C("The kettle"), "shock"], [C("again and again"), "dizzy"]],
                  takes=[C("Made in China"), C("The kettle"), C("The lamp")], hops=[C("The charger")], hold="phone"),
              it("bubble", text="FINE. I'LL BUY ONE\nTHAT ISN'T.", x=1250, y=260, at=C("buy a new one", -1.0), until=C("The kettle", -0.2), tail=[1120, 470], size=30)]},
    sfx=[{"kind": "hit", "cue": "Made in China", "gain": 0.3}])
stage("s02_hook", "co_hook", {
    **W1("tariffwall", wallX=1100, rows=[{"at": C("Since twenty eighteen"), "label": "2018", "h": 50}, {"at": C("again and again", -0.8), "label": "2019", "h": 45, "color": "#B5563A"},
                                          {"at": C("again and again", -0.2), "label": "2024", "h": 55, "color": "#8E3B2A"}, {"at": C("again and again", 0.4), "label": "2025", "h": 90, "color": RED},
                                          {"at": C("again and again", 0.9), "label": "2026", "h": 45, "color": "#C76B4A"}]),
    "cam": cam((0, 1100, 520, 1.05), (C("Last year"), 1100, 480, 0.95, 1.6), (C("And yet"), 1150, 500, 1.15, WHIP), (C("So why is it"), 1100, 560, 1.35, 1.2)), "drift": 4,
    "items": [it("counter", x=1100, y=150, at=C("Last year"), prefix="$", suffix="B", decimals=1, until=C("And yet", -0.2),
                 steps=[[0, 440.3], [C("fell to"), 440.3], [C("the year before", -0.3), 308.7]], text="U.S. GOODS IMPORTS FROM CHINA · 2024 → 2025 (CENSUS)"),
              it("toonwords", text="≈ 27% OF WORLD MANUFACTURING", x=1150, y=150, at=C("China still makes"), size=58, until=C("So why is it", 0.5)),
              sign("2025 · WORLD BANK DATA · OUR CALCULATION", 1150, 270, C("of everything the world"), color="#FFF8E1", size=24, until=C("So why is it", 0.5)),
              it("toonwords", text="WHY SO HARD TO LEAVE?", x=1100, y=250, at=C("So why is it"), size=66, color="#FFFFFF"),
              it("homebox", x=[[0, 300], [C("Last year"), 900], [C("And yet"), 900], [C("So why is it"), 300]], at=0.3, label="MADE IN CHINA", scale=1.0,
                 faces=[[0, "happy"], [C("And yet"), "grin"]], hops=[C("China still makes")])]},
    sources=["census_cn", "wdi_mva"])
stage("s03_promise", "co_promise", {
    **W1("megafloor", board="TODAY'S TOUR"),
    "cam": cam((0, 700, 520, 1.0), (C("the street of suppliers"), 1100, 500, 1.0, 1.6), (C("one factory that tried"), 1500, 540, 1.1, 1.4)), "drift": 6,
    "items": [it("toonwords", text="NOT JUST CHEAP LABOR", x=900, y=120, at=0.2, until=C("Let's walk"), size=64),
              sign("1 · THE FACTORY FLOOR", 520, 300, C("the factory floor"), color="#FFE0B2", size=28),
              sign("2 · THE STREET OF SUPPLIERS", 900, 180, C("the street of suppliers"), color="#C8E6C9", size=28),
              sign("3 · THE PORT", 1250, 300, C("the port"), color="#BBDEFB", size=28),
              sign("4 · THE REFINERY", 1550, 180, C("the refinery"), color="#E1BEE7", size=28),
              sign("5 · THE FACTORY THAT TRIED TO MOVE", 1650, 420, C("one factory that tried"), color="#FFCDD2", size=28),
              WEI(1200, 0.3, pose="wave", face="happy", label="WEI · LINE ENGINEER", labelUntil=C("the refinery"), poses=[[0, "wave"], [C("the street"), "point"]]),
              it("homebox", x=[[C("one factory that tried"), 1300], [C("move away", 0.8), 2100]], at=C("one factory that tried"), label="MOVING!", face="grin")]})
stage("s04_title", "title_card", {
    **W1("fctitle", lines=["STILL MADE", "IN CHINA"], sub="WHY THE WORLD STILL DEPENDS ON CHINESE FACTORIES",
         subs=[[2.0, "Tonight: “The Toaster That Wouldn't Leave Home”"]]), "cam": STILL(), "drift": 0, "min_seconds": 5.8,
    "items": [MEL(260, 2.4, scale=1.2, face="shock", pose="armsup", hops=[2.8, 4.2], y=1080), WEI(1680, 2.6, scale=1.2, face="happy", pose="wave", y=1080)]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}, {"kind": "hit", "at": 1.6, "gain": 0.25}])

# ====================================================================== ACT 1: the everything factory
bumper("s05_b1", "a1_card", "1", "ACT ONE", "THE EVERYTHING FACTORY", "Some assembly required. All of it, actually.", TEAL, 0, ["BODY"])
stage("s06_floor", "a1_floor", {
    **W1("megafloor", hi=0, board="TODAY: EVERYTHING"), "zonesKey": None,
    "cam": cam((0, 900, 560, 1.25), (C("phone chargers"), 1050, 520, 1.1, 1.0), (C("sneakers"), 1150, 500, 1.0, 1.0), (C("solar panels"), 1100, 500, 0.9, 1.2),
               (C("That floor is a cartoon"), 1000, 540, 1.15, WHIP), (C("The numbers behind it"), 1100, 480, 0.95, 1.4)), "drift": 5,
    "items": [it("toonwords", text="THE EVERYTHING FACTORY", x=1100, y=40, at=0.3, until=C("That floor is a cartoon"), size=64),
              WEI(1350, 0.3, pose="talk", face="happy", label="WEI · LINE ENGINEER", labelUntil=C("sneakers"), talk=[[0.4, C("solar panels", 0.6)]],
                  poses=[[0, "talk"], [C("phone chargers"), "point"], [C("That floor is a cartoon"), "shrug"]], faces=[[0, "happy"], [C("That floor is a cartoon"), "smug"]]),
              WK(0, 500, 0.4), WK(5, 1800, 0.5), WK(6, 2200, 0.6),
              sign("ILLUSTRATIVE SET", 700, 760, C("That floor is a cartoon"), color="#FFFFFF", size=24),
              it("toonwords", text="THE NUMBERS ARE REAL", x=1100, y=60, at=C("The numbers behind it"), size=64, color="#FFFFFF")]})
# per-cue line highlight: re-emit as separate zone keyframes is not supported, so highlight follows a timeline param
scenes[-1]["params"].pop("zonesKey")
scenes[-1]["params"]["zones"][0]["hiAt"] = [[0, 0], [C("phone chargers"), 1], [C("sneakers"), 2], [C("batteries"), 3], [C("solar panels"), 4]]
stage("s07_scale", "a1_scale", {
    **W1("megafloor", board="VALUE ADDED, 2025", boardX=-1400),
    "cam": cam((0, 1000, 480, 1.0), (C("By World Bank data"), 1100, 470, 1.05, 1.4), (C("Back in twenty oh-four"), 1100, 500, 1.15, WHIP)), "drift": 4,
    "items": [it("toonwords", text="VALUE ADDED = WHAT THE FACTORY ADDS", x=1050, y=120, at=C("Manufacturing value added"), until=C("By World Bank data"), size=46),
              it("counter", x=1100, y=160, at=C("By World Bank data"), prefix="$", suffix="T", decimals=2,
                 steps=[[0, 0], [C("China's factories added"), 0], [C("in twenty twenty-five"), 4.82]], text="CHINA, MANUFACTURING VALUE ADDED, 2025 (WORLD BANK)"),
              sign("≈ 27.4% OF THE WORLD TOTAL · OUR CALCULATION", 1100, 330, C("of the world total"), color="#FFF59D", size=30),
              sign("2004: ≈ 8.5%", 1700, 470, C("Back in twenty oh-four"), color="#FFE0B2", size=34),
              it("stackbox", x=500, y=860, at=0.4, cols=3, rows=5, fill=[[0, 0.1], [C("in twenty twenty-five"), 1.0]], text="CHINA"),
              WEI(1750, 0.3, face="happy", pose="clipboard", hold="clipboard")]},
    sources=["wdi_mva"])
add("p08_bars", "a1_draw", "engine_draw", {
    "title": "World manufacturing value added, China's slice (current US$)", "board": BOARD, "draw_start": C("Let me draw that"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 820 L 1480 820", "color": "ink", "width": 5, "start": C("Let me draw that")},
        {"d": "M 720 820 L 720 664 L 920 664 L 920 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.25, "kind": "bar", "start": C("in twenty oh-four"), "label": lbl("WORLD 2004 · $7.3T", 820, 644, 22, "accent2")},
        {"d": "M 720 820 L 720 807 L 920 807 L 920 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.7, "kind": "bar", "start": C("one dollar in twelve"), "label": lbl("CHINA ≈ 8.5%", 820, 860, 22, "risk")},
        {"d": "M 1180 820 L 1180 446 L 1380 446 L 1380 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.25, "kind": "bar", "start": C("Now twenty twenty-five"), "label": lbl("WORLD 2025 · $17.6T", 1280, 426, 22, "accent2")},
        {"d": "M 1180 820 L 1180 718 L 1380 718 L 1380 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.7, "kind": "bar", "start": C("China's slice is more"), "label": lbl("CHINA $4.8T ≈ 27%", 1280, 860, 22, "risk")},
        {"d": dot(1050, 360), "color": "muted", "width": 1, "start": C("more than one dollar in four"), "label": lbl("WORLD BANK WDI · SHARES ARE OUR CALCULATION", 1050, 360, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("more than one dollar in four", 0.1), "dur": 1.4, "target": [1280, 760]}],
    "scale": 0.86, "floor": 1040}, sources=["wdi_mva"])
stage("s09_exports", "a1_exports", {
    **W1("megaport", quayX=1500, fill=[[0, 0.15], [C("more than any other country"), 0.75], [C("its goods surplus"), 1.0]]),
    "cam": cam((0, 900, 480, 0.95), (C("The World Trade Organization"), 1200, 470, 0.9, 1.6), (C("It sold so much more"), 1500, 520, 1.0, 1.4)), "drift": 5,
    "items": [it("counter", x=800, y=150, at=C("China exported"), prefix="$", suffix="T", decimals=2, steps=[[0, 0], [C("China exported"), 0], [C("of goods in twenty"), 3.77]], text="CHINA GOODS EXPORTS, 2025 (WTO)"),
              sign("#1 IN THE WORLD · 14.4% OF WORLD EXPORTS", 800, 330, C("more than any other country"), color="#FFF59D", size=30),
              sign("TRADE SURPLUS 2025: $1.19T (WTO)", 1500, 200, C("its goods surplus"), color="#C8E6C9", size=32),
              it("drone", x=[[0, -300], [12, 2600]], y=60, at=0.2, carry="EXPORT", scale=0.8)]},
    sources=["wto_gtos"])
stage("s10_workers", "a1_workers", {
    **W1("megafloor", hi=3, board="SHIFT CHANGE", boardX=-1400),
    "cam": cam((0, 1100, 520, 0.95), (C("That count includes builders"), 1100, 520, 1.15, WHIP)), "drift": 5,
    "items": [*[WK(k, [[0, -300 - k * 160], [6, 2700 - k * 160]], 0.1 + k * 0.12, pose="stand", face="happy", scale=1.0) for k in range(9)],
              it("counter", x=1100, y=150, at=C("counted"), suffix="M", decimals=0, steps=[[0, 0], [C("counted"), 0], [C("working in industry"), 213]],
                 text="EMPLOYED IN INDUSTRY & CONSTRUCTION, END-2024 (NBS)"),
              sign("INCLUDES CONSTRUCTION AND MINING", 1100, 330, C("That count includes builders"), color="#FFE0B2", size=30)]},
    sources=["nbs_emp"])
stage("s11_wage", "a1_wage", {
    **W1("megafloor", board="PAYDAY", boardX=-1400),
    "cam": cam((0, 960, 540, 1.0), (C("Cheaper, clearly"), 1000, 520, 1.05, 1.2), (C("If wages were the whole"), 1200, 560, 1.15, WHIP)), "drift": 3,
    "items": [chart([{"label": "CHINA · PRODUCTION WORKER", "value": 11.2, "color": RED, "at": C("A production worker"), "display": "≈ $11.2K / YR"},
                     {"label": "U.S. · PRODUCTION WORKER", "value": 60.4, "color": TEAL, "at": C("An American factory"), "display": "≈ $29 / HR (≈ $60K)"}],
                    at=0.2, max=65, title="ROUGH PAY COMPARISON, 2025", x=300, y=220, w=860, h=470, until=C("If wages were the whole", 0.5)),
              sign("NBS ¥80,739 AT FED 2025 RATE · BLS · OUR CALCULATION", 730, 830, C("at the Federal Reserve"), color="#FFFFFF", size=20, until=C("If wages were the whole", 0.5)),
              sign("CHINESE PAY STILL RISING: +6.4% (PRIVATE, 2025)", 1600, 200, C("keeps rising"), color="#FFCDD2", size=26),
              it("toonwords", text="WAGES AREN'T THE WHOLE STORY", x=1200, y=200, at=C("If wages were the whole"), size=54),
              MEL(1650, 0.3, face="worry", pose="shrug", faces=[[0, "worry"], [C("Cheaper, clearly"), "smug"], [C("Many of them didn't"), "shock"]], takes=[C("Many of them didn't")])]},
    sources=["nbs_wage", "fed_g5a", "bls_ces"])

# ====================================================================== ACT 2: everything is down the street
bumper("s12_b2", "a2_card", "2", "ACT TWO", "EVERYTHING IS DOWN THE STREET", "Parts may arrive before you finish this sentence", ORANGE, 1, ["SLOTS", "COIL"])
stage("s13_street", "a2_street", {
    **W1("partsstreet", asmX=2700, shopX=-200, gap=330,
         lit=[[C("Screws"), 0], [C("Cables"), 1], [C("Molds"), 2], [C("motors"), 3], [C("glass"), 4], [C("batteries"), 5], [C("circuit boards"), 6]], rushAt=C("An engineer changes")),
    "cam": cam((0, 300, 520, 1.1), (C("Screws"), 100, 500, 1.1, 1.0), (C("Molds"), 600, 500, 1.0, 1.4), (C("circuit boards"), 1500, 500, 0.95, 1.6),
               (C("An engineer changes"), 2300, 520, 1.0, 1.6), (C("Economists call this"), 1200, 480, 0.85, 1.4)), "drift": 4,
    "items": [it("toonwords", text="EVERY PART: DOWN THE STREET", x=600, y=60, at=C("Picture a street"), until=C("Screws"), size=56),
              WEI([[0, 200], [C("circuit boards"), 1500], [C("An engineer changes"), 2350]], 0.3, hold="clipboard", face="happy", pose="stand"),
              it("bubble", text="NEW DESIGN!\n(MORNING)", x=2350, y=280, at=C("An engineer changes"), until=C("holds a new sample"), tail=[2350, 470], size=28),
              it("bubble", text="SAMPLE'S HERE!\n(AFTERNOON)", x=2350, y=280, at=C("holds a new sample"), until=C("Economists call this", 0.3), tail=[2350, 470], size=28),
              it("toonwords", text="SUPPLIER CLUSTER", x=1200, y=90, at=C("Economists call this"), size=72),
              sign("SPEED YOU CAN'T PUT IN A CONTAINER", 1200, 250, C("It's speed"), color="#FFF59D", size=32)]})
add("p14_cluster", "a2_draw", "engine_draw", {
    "title": "A supplier cluster (simplified)", "board": BOARD, "draw_start": C("Let me draw why"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(820, 520, 220, 110), "color": "accent2", "width": 7, "kind": "box", "start": C("Box one"), "label": lbl("FINAL ASSEMBLER", 930, 585, 24, "accent2")},
        *[{"d": rect(x, y, 120, 56), "color": "ink", "width": 4, "kind": "box", "start": C("dozens of suppliers", k * 0.25), "label": lbl(t_, x + 60, y + 36, 16, "ink")}
          for k, (x, y, t_) in enumerate([(640, 400, "SCREWS"), (870, 380, "CABLES"), (1100, 400, "MOLDS"), (620, 680, "GLASS"), (870, 700, "MOTORS"), (1110, 680, "BOARDS")])],
        {"d": arrow((760, 456), (840, 520)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("When they're close")},
        {"d": arrow((930, 436), (930, 516)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("a phone call")},
        {"d": arrow((1110, 456), (1030, 520)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("a short ride"), "label": lbl("MINUTES", 1180, 500, 20, "accent3")},
        {"d": arrow((1060, 575), (1400, 575), -0.15), "color": "risk", "width": 6, "kind": "arrow", "start": C("Move the assembler far away")},
        {"d": rect(1410, 530, 120, 90), "color": "risk", "width": 5, "kind": "box", "start": C("Move the assembler far away", 0.6), "label": lbl("FAR AWAY", 1470, 580, 18, "risk")},
        {"d": dot(1230, 470), "color": "risk", "width": 1, "start": C("a container"), "label": lbl("CONTAINER", 1230, 470, 20, "risk")},
        {"d": dot(1230, 650), "color": "risk", "width": 1, "start": C("a customs"), "label": lbl("CUSTOMS FORM", 1230, 650, 20, "risk")},
        {"d": dot(1230, 690), "color": "risk", "width": 1, "start": C("weeks at sea"), "label": lbl("WEEKS AT SEA", 1230, 690, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("weeks at sea", 0.1), "dur": 1.4, "target": [1230, 580]}],
    "scale": 0.86, "floor": 1040})
stage("s15_ev", "a2_ev", {
    **W1("megafloor", hi=3, board="BATTERY DAY"),
    "cam": cam((0, 1000, 520, 1.0), (C("For the materials"), 1000, 500, 1.0, 1.2)), "drift": 3,
    "items": [chart([{"label": "ELECTRIC CARS", "value": 70, "color": TEAL, "at": C("of the world's electric cars", -0.4), "display": "70–75%"},
                     {"label": "BATTERY CELLS", "value": 80, "color": ORANGE, "at": C("of battery cells", -0.5), "display": "> 80%"},
                     {"label": "CATHODE MATERIAL", "value": 85, "color": RED, "at": C("of cathode material", -0.5), "display": "≈ 85%"},
                     {"label": "ANODE MATERIAL", "value": 90, "color": PURPLE, "at": C("of anode material", -0.5), "display": "> 90%"}],
                    at=0.2, max=100, title="CHINA'S SHARE OF WORLD PRODUCTION, 2025 (IEA)", x=260, y=210, w=1150, h=500),
              WEI(1750, 0.3, face="happy", pose="point", hold="clipboard", faces=[[0, "happy"], [C("higher still"), "smug"]])]},
    sources=["iea_gevo"])
stage("s16_ev2", "a2_ev2", {
    **W1("partsstreet", asmX=2550, shops=["LITHIUM REFINING", "CATHODES", "ANODES", "CELLS", "PACKS", "MOTORS", "WIRING"], gap=330,
         lit=[[C("from refining minerals"), 0], [C("from refining minerals", 0.5), 1], [C("from refining minerals", 1.0), 2], [C("to building the car", -0.6), 3], [C("to building the car", -0.2), 4], [C("to building the car", 0.2), 5], [C("to building the car", 0.6), 6]]),
    "cam": cam((0, 300, 500, 0.95), (C("from refining minerals"), 1200, 500, 0.85, 2.4), (C("And it shows up"), 2200, 520, 1.0, 1.4)), "drift": 4,
    "items": [it("toonwords", text="'A TIGHTLY CLUSTERED SUPPLY CHAIN'", x=1100, y=70, at=C("The agency calls it"), until=C("And it shows up"), size=48),
              sign("— IEA GLOBAL EV OUTLOOK 2026", 1100, 190, C("tightly clustered"), color="#FFFFFF", size=24, until=C("And it shows up")),
              sign("BATTERY PACKS IN CHINA: 30% CHEAPER THAN NORTH AMERICA (2025)", 2150, 150, C("battery packs in China"), color="#FFF59D", size=28, sub="IEA GLOBAL EV OUTLOOK 2026")]},
    sources=["iea_gevo"])
stage("s17_solar", "a2_solar", {
    **W1("solarline", lineX=0, gap=480),
    "cam": cam((0, 300, 500, 1.05), (C("from polysilicon"), 300, 480, 1.0, 1.0), (C("wafers"), 900, 480, 1.0, 1.0), (C("cells and modules"), 1600, 480, 0.95, 1.2),
               (C("The ten biggest"), 1200, 480, 0.85, 1.6), (C("And making panels"), 1000, 500, 1.0, 1.2)), "drift": 4,
    "items": [it("toonwords", text="SOLAR: SAME STORY", x=700, y=60, at=0.2, until=C("from polysilicon"), size=64),
              sign("> 80% OF EVERY STAGE · IEA, 2022", 1100, 60, C("was above"), color="#FFF59D", size=32),
              sign("TOP 10 PANEL-MACHINE MAKERS: CHINESE (2022)", 1100, 190, C("The ten biggest"), color="#C8E6C9", size=28),
              sign("COSTS ≈ 20% LOWER THAN THE U.S. (2022)", 1100, 320, C("And making panels"), color="#BBDEFB", size=28),
              WEI(1900, C("cells and modules"), face="happy", pose="point")]},
    sources=["iea_pv"])
scenes[-1]["params"]["zones"][0]["hiAt"] = [[C("from polysilicon"), 0], [C("wafers", -0.3), 2], [C("cells and modules"), 3], [C("cells and modules", 0.8), 4], [C("The ten biggest"), "all"]]
stage("s18_rare", "a2_rare", {
    **W1("refinery", mineX=-300, tankX=400, stages=8, flowAt=C("They have to be separated"), jarsAt=C("For magnet rare earths"), board="SEPARATION + REFINING"),
    "cam": cam((0, 300, 560, 1.0), (C("Digging them up"), -250, 560, 1.15, 1.2), (C("They have to be separated"), 900, 520, 0.9, 1.8),
               (C("For magnet rare earths"), 1700, 520, 1.0, 1.4), (C("And in April"), 1300, 500, 0.95, 1.2)), "drift": 4,
    "items": [it("toonwords", text="RARE EARTHS → MAGNETS", x=400, y=60, at=0.3, until=C("Digging them up"), size=58),
              sign("MINING = THE START", -250, 120, C("Digging them up"), color="#FFE0B2", size=30),
              it("counter", x=1700, y=150, at=C("For magnet rare earths"), suffix="%", steps=[[0, 90], [C("For magnet rare earths"), 90], [C("in twenty twenty-five"), 85]],
                 text="CHINA'S SHARE OF REFINING, MAGNET RARE EARTHS (IEA)"),
              sign("2024: 90% → 2025: 85%", 1700, 330, C("down from"), color="#FFF59D", size=30),
              it("docs", x=1000, y=860, at=C("And in April"), text="APR 4, 2025 · CHINA", scale=0.85, stamp="EXPORT CONTROLS: 7 HEAVY RARE EARTHS", stampAt=C("put export controls")),
              WK(2, [[0, -600], [C("They have to be separated"), 200]], 0.3, hold="box", face="happy")]},
    sources=["iea_gcmo"])
stage("s19_port", "a2_port", {
    **W1("megaport", quayX=1500, fill=[[0, 0.3], [C("containers"), 1.0]], board="SHANGHAI · 2025"),
    "cam": cam((0, 1300, 480, 0.9), (C("The port of Los Angeles"), 700, 500, 1.0, 1.4), (C("That's"), 900, 480, 0.95, WHIP)), "drift": 4,
    "items": [it("counter", x=700, y=180, at=C("the port of Shanghai"), suffix="M TEU", decimals=1, steps=[[0, 0], [C("the port of Shanghai"), 0], [C("containers"), 55.1]], text="SHANGHAI, 2025 (PORT OPERATOR SIPG)", until=C("The port of Los Angeles", -0.2)),
              chart([{"label": "SHANGHAI", "value": 55.1, "color": RED, "at": C("The port of Los Angeles", -0.2), "display": "55.1M TEU"},
                     {"label": "LOS ANGELES", "value": 10.2, "color": TEAL, "at": C("handled", 0.2), "display": "10.2M TEU"}],
                    at=C("The port of Los Angeles", -0.3), max=60, title="CONTAINERS HANDLED, 2025 (TWENTY-FOOT UNITS)", x=260, y=200, w=760, h=440),
              sign("> 5× · OUR CALCULATION (SIPG; PORT OF L.A.)", 640, 800, C("by our calculation", -0.8), color="#FFF59D", size=26),
              it("stackbox", x=2000, y=860, at=0.3, cols=3, rows=4, fill=[[0, 0.2], [C("containers"), 1]], text="TODAY")]},
    sources=["sipg", "pola"])
stage("s20_people", "a2_people", {
    **W1("megafloor", hi=None, board="LAUNCH DAY", boardX=-1400),
    "cam": cam((0, 1100, 520, 0.95), (C("Not one cheap factory"), 1100, 520, 1.1, WHIP), (C("A whole neighborhood"), 1100, 480, 0.85, 1.6)), "drift": 4,
    "items": [WEI(700, 0.2, face="happy", hold="clipboard", pose="clipboard", label="TOOLING ENGINEER", labelUntil=C("line managers", 0.8)),
              WK(5, 1100, C("line managers"), pose="talk", label="LINE MANAGER", labelUntil=C("technicians", 1.0)),
              WK(6, 1500, C("technicians"), pose="point", label="TECHNICIAN", labelUntil=C("launched products", 1.5)),
              it("toonwords", text="NOT ONE CHEAP FACTORY", x=1100, y=120, at=C("Not one cheap factory"), until=C("A whole neighborhood"), size=60),
              it("toonwords", text="A WHOLE NEIGHBORHOOD", x=1100, y=120, at=C("A whole neighborhood"), size=70, color="#FFFFFF")]})

# ====================================================================== ACT 3: the tariff wall
bumper("s21_b3", "a3_card", "3", "ACT THREE", "THE TARIFF WALL", "Some walls are made of paperwork", RED, 3, ["LEVER", "KNOB"])
R18 = [{"at": C("put a"), "label": "JUL 2018 · 25% · ≈ $34B", "h": 56},
       {"at": C("more"), "label": "AUG 2018 · 25% · ≈ $16B", "h": 50, "color": "#B5563A"},
       {"at": C("In September"), "label": "SEP 2018 · 10% · ≈ $200B", "h": 64, "color": "#A84B33"},
       {"at": C("the next spring"), "label": "MAY 2019 · → 25%", "h": 40, "color": "#8E3B2A"},
       {"at": C("Another round"), "label": "2019 · 15% → 7.5%", "h": 46, "color": "#C76B4A"}]
stage("s22_2018", "a3_2018", {
    **W1("tariffwall", wallX=1100, rows=R18, leftLabel="FACTORY", rightLabel="U.S. STORE"),
    "cam": cam((0, 1100, 600, 1.2), (C("In September"), 1100, 560, 1.1, 1.4), (C("cut in half"), 1150, 560, 1.2, WHIP)), "drift": 3,
    "items": [it("toonwords", text="THE TARIFF WALL", x=1100, y=60, at=0.2, until=C("put a"), size=72),
              sign("USTR · SECTION 301 · FEDERAL REGISTER", 1700, 140, C("U.S. Trade Representative"), color="#FFF8E1", size=24),
              sign("PART CUT IN HALF · JAN 2020 NOTICE", 1700, 260, C("cut in half"), color="#C8E6C9", size=26),
              KIP(2100, 0.3, face="smug", pose="stand", label="KIP · RELOCATION CONSULTANT", labelUntil=C("In September"), faces=[[0, "smug"], [C("In September"), "shock"]])]},
    sources=["fr_301_2018"])
R18_0 = [{**r, "at": 0.0} for r in R18]
R24 = [{"at": C("a review raised"), "label": "2024 REVIEW · EVs 100%", "h": 60, "color": "#7B2E22"},
       {"at": C("on solar cells", -0.5), "label": "SOLAR CELLS 50%", "h": 44, "color": "#9C4030"},
       {"at": C("on semiconductors", -0.5), "label": "CHIPS 50% (2025)", "h": 44, "color": "#B5563A"}]
stage("s23_2024", "a3_2024", {
    **W1("tariffwall", wallX=1100, rows=R18_0 + R24, leftLabel="FACTORY", rightLabel="U.S. STORE"),
    "cam": cam((0, 1100, 500, 1.05), (C("on semiconductors"), 1100, 440, 1.0, 1.4)), "drift": 3,
    "items": [sign("89 FR 76581 · SEPT 2024", 1750, 140, C("a review raised"), color="#FFF8E1", size=24),
              it("homebox", x=[[0, 500], [8, 800]], at=0.2, label="EV", face="worry")]},
    sources=["fr_301_2024"])
R24_0 = [{**r, "at": 0.0} for r in R24]
stage("s24_2025", "a3_2025", {
    **W1("tariffwall", wallX=1100, leftLabel="FACTORY", rightLabel="U.S. STORE",
         rows=R18_0 + R24_0 + [{"at": C("were stacked on top"), "label": "2025 · EMERGENCY-POWERS TARIFFS", "h": 70, "color": "#D2453C", "out": C("does not authorize tariffs")},
                               {"at": C("reached"), "label": "APR 2025 · 'RECIPROCAL' 125%", "h": 180, "color": RED, "out": C("cut back in May")},
                               {"at": C("cut back in May", 0.6), "label": "MAY 2025 · CUT TO 10%", "h": 40, "color": "#E06A55", "out": C("does not authorize tariffs", 0.2)},
                               {"at": C("Since July twenty twenty-six"), "label": "JUL 2026 · 12.5%", "h": 50, "color": "#A84B33"}]),
    "cam": cam((0, 1100, 380, 0.85), (C("reached"), 1100, 240, 0.75, 1.4), (C("In February"), 1100, 420, 0.9, 1.4), (C("Since July"), 1100, 460, 0.95, 1.2)), "drift": 2,
    "items": [it("gavel", x=1750, y=400, at=C("In February"), hits=[C("ruled that the law"), C("does not authorize tariffs")], scale=1.2),
              sign("SUPREME COURT · FEB 20, 2026 · 6–3", 1750, 200, C("the Supreme"), color="#FFF8E1", size=28, until=C("Other laws took over", 1.0)),
              sign("AS OF NOV 2026 · USTR SECTION 301", 1750, 200, C("Since July"), color="#FFF59D", size=26),
              KIP(400, 0.3, face="shock", pose="armsup", faces=[[0, "shock"], [C("does not authorize"), "dizzy"], [C("Since July"), "worry"]])]},
    sources=["fr_ieepa", "scotus", "crs_2026", "fr_301_2026"])
add("p25_who", "a3_who", "engine_draw", {
    "title": "Who pays a tariff (simplified)", "board": BOARD, "draw_start": C("Remember who pays"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 520, 200, 100), "color": "ink", "width": 6, "kind": "box", "start": C("Remember who pays"), "label": lbl("FACTORY ABROAD", 660, 578, 20, "ink")},
        {"d": arrow((770, 570), (900, 570)), "color": "accent", "width": 6, "kind": "arrow", "start": C("collected at the border")},
        {"d": rect(910, 500, 240, 140), "color": "risk", "width": 7, "kind": "box", "start": C("the American company"), "label": lbl("U.S. IMPORTER", 1030, 560, 24, "risk")},
        {"d": dot(1030, 600), "color": "risk", "width": 1, "start": C("imports the goods"), "label": lbl("PAYS THE TARIFF", 1030, 605, 18, "risk")},
        {"d": arrow((1160, 570), (1290, 570)), "color": "accent", "width": 6, "kind": "arrow", "start": C("Some of it reaches shoppers")},
        {"d": rect(1300, 520, 200, 100), "color": "accent2", "width": 6, "kind": "box", "start": C("Some of it reaches shoppers", 0.4), "label": lbl("SHOPPERS", 1400, 578, 22, "accent2")},
        {"d": dot(1400, 470), "color": "accent2", "width": 1, "start": C("at least"), "label": lbl("≥ 30% IN RETAIL PRICES (FED ESTIMATE)", 1230, 460, 20, "accent2")},
        {"d": dot(1030, 700), "color": "muted", "width": 1, "start": C("The rest was absorbed"), "label": lbl("REST: ABSORBED ALONG THE WAY", 1030, 700, 20, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("collected at the border", 0.3), "dur": 1.4, "target": [1030, 570]}],
    "scale": 0.86, "floor": 1040}, sources=["fed_feds"])
stage("s26_effect", "a3_effect", {
    **W1("megaport", quayX=1700, fill=[[0, 1.0], [C("In twenty twenty-five"), 0.55]]),
    "cam": cam((0, 960, 520, 1.0), (C("they fell"), 1000, 500, 1.05, 1.4)), "drift": 3,
    "items": [chart([{"label": "2018 (PEAK)", "value": 538.5, "color": RED, "at": C("peaked at", 0.3), "display": "$538.5B"},
                     {"label": "2024", "value": 440.3, "color": ORANGE, "at": C("In twenty twenty-five", -0.4), "display": "$440.3B"},
                     {"label": "2025", "value": 308.7, "color": TEAL, "at": C("in a single year"), "display": "$308.7B"}],
                    at=0.2, max=600, title="U.S. GOODS IMPORTS FROM CHINA (CENSUS)", x=280, y=200, w=1000, h=480),
              sign("−29% IN ONE YEAR (WTO)", 1600, 220, C("they fell by"), color="#FFCDD2", size=34),
              KIP(1700, 0.3, face="smug", pose="stand", faces=[[0, "worry"], [C("in a single year"), "smug"]], hops=[C("in a single year", 0.5)])]},
    sources=["census_cn", "wto_gtos"])
MONTHS = [("JAN", 21.06), ("FEB", 18.96), ("MAR", 20.86), ("APR", 19.79), ("MAY", 23.51), ("JUN", 25.15), ("JUL", 27.07), ("AUG", 27.13), ("SEP", 31.48)]
stage("s27_back", "a3_back", {
    **W1("tariffwall", wallX=1100, rows=[{"at": 0.0, "label": "2026", "h": 50}], leftLabel="FACTORY", rightLabel="U.S. STORE"),
    "cam": cam((0, 1000, 520, 1.0), (C("Month by month"), 1000, 470, 0.95, 1.4)), "drift": 3,
    "items": [chart([{"label": m, "value": v, "color": TEAL if k else RED, "at": (0.6 + k * 0.6 if k < 3 else C("Month by month", (k - 3) * 0.4)), "display": f"${v:.1f}B"} for k, (m, v) in enumerate(MONTHS)],
                    at=0.2, max=35, title="U.S. IMPORTS FROM CHINA, MONTHLY, 2026 (CENSUS, NOT SEAS. ADJ.)", x=200, y=170, w=1500, h=470),
              sign("JAN–SEP 2026: −11.5% VS 2025 · OUR CALCULATION", 960, 820, C("were down about"), color="#FFF8E1", size=26),
              *[it("homebox", x=[[0, 2700 + k * 170], [C("Month by month"), 2700 + k * 170], [C("in September"), 1400 + k * 170]], at=0.2, label="MADE IN CHINA",
                   face="grin", scale=0.7, y=1000) for k in range(4)]]},
    sources=["census_cn"])

# ====================================================================== ACT 4: China plus one
bumper("s28_b4", "a4_card", "4", "ACT FOUR", "CHINA PLUS ONE", "Now with one more country. Some restrictions apply.", GREEN, 5, ["PLUG", "FEET"])
stage("s29_plus1", "a4_plus1", {
    **W1("movingday", oldX=300, newX=2200, build=[[0, 0.15], [C("add one more country"), 0.5]], newName="+1 COUNTRY"),
    "cam": cam((0, 700, 520, 1.0), (C("add one more country"), 1500, 520, 0.95, 1.6), (C("China plus"), 1250, 500, 0.85, WHIP)), "drift": 4,
    "items": [KIP([[0, 900], [C("add one more country"), 1900]], 0.2, face="smug", pose="point", label="KIP · RELOCATION CONSULTANT", labelUntil=C("add one more")),
              it("toonwords", text="CHINA + 1", x=1250, y=150, at=C("China plus"), size=110),
              sign("WHERE DID THE ORDERS GO?", 1250, 330, C("where the orders went"), color="#FFF59D", size=32),
              it("homebox", x=[[C("add one more country"), 500], [C("China plus"), 1300]], at=C("Keep China"), label="ORDERS", face="happy")]})
SH = [("CHINA", 21.6, 7.7, "risk"), ("MEXICO", 13.4, 17.3, "accent3"), ("VIETNAM", 2.0, 7.4, "accent2"), ("TAIWAN", 1.8, 7.7, "accent"), ("INDIA", 2.1, 2.8, "muted")]
SHCUE = {"CHINA": ("In twenty seventeen", "In the first nine months"), "VIETNAM": ("Vietnam went from", "Vietnam went from"), "TAIWAN": ("Taiwan, from", "Taiwan, from"),
         "MEXICO": ("Mexico, from", "Mexico, from"), "INDIA": ("India grew too", "India grew too")}
_strokes = [{"d": "M 560 820 L 1520 820", "color": "ink", "width": 5, "start": C("Let me chart")}]
for k, (nm, a17, a26, colr) in enumerate(SH):
    x = 600 + k * 185
    h17, h26 = a17 * 17, a26 * 17
    c17, c26 = SHCUE[nm]
    off = 0.0 if nm == "CHINA" else 0.4
    _strokes.append({"d": f"M {x} 820 L {x} {820 - h17:.0f} L {x + 70} {820 - h17:.0f} L {x + 70} 820 Z", "color": colr, "width": 3, "fill": colr, "fillOpacity": 0.25,
                     "kind": "bar", "start": C(c17, off), "label": lbl(f"{a17:g}%", x + 35, 800 - h17, 18, colr)})
    _strokes.append({"d": f"M {x + 80} 820 L {x + 80} {820 - h26:.0f} L {x + 150} {820 - h26:.0f} L {x + 150} 820 Z", "color": colr, "width": 3, "fill": colr, "fillOpacity": 0.7,
                     "kind": "bar", "start": C(c26, off + (0.0 if nm == "CHINA" else 1.0)), "label": lbl(f"{a26:g}%", x + 115, 800 - h26, 18, colr)})
    _strokes.append({"d": dot(x + 75, 850), "color": "ink", "width": 1, "start": C(c17, off), "label": lbl(nm, x + 75, 856, 20, "ink")})
_strokes.append({"d": dot(1040, 892), "color": "muted", "width": 1, "start": C("India grew too", 0.8), "label": lbl("SHARE OF U.S. GOODS IMPORTS · LIGHT = 2017 · DARK = JAN–SEP 2026 · CENSUS, OUR CALC.", 1040, 892, 16, "muted")})
add("p30_shares", "a4_draw", "engine_draw", {
    "title": "Who sells America its goods (share of U.S. imports)", "board": BOARD, "draw_start": C("Let me chart"), "speed": 1600, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3}, "strokes": _strokes,
    "actions": [{"kind": "point", "at": C("Vietnam went from", 0.6), "dur": 1.4, "target": [1015, 720]}],
    "scale": 0.86, "floor": 1040}, sources=["census_cn", "census_world", "census_partners"])
stage("s31_parts", "a4_parts", {
    **W1("movingday", oldX=300, newX=2200, build=[[0, 0.55], [8, 0.65]], newName="NEW ASSEMBLY PLANT"),
    "cam": cam((0, 1250, 500, 0.85), (C("The WTO notes"), 1250, 500, 0.9, 1.2), (C("A new factory can move"), 1800, 520, 1.0, 1.4), (C("still come from"), 700, 520, 1.0, 1.4)), "drift": 3,
    "items": [it("counter", x=1250, y=130, at=C("China's exports to Southeast Asia"), prefix="+", suffix="%", decimals=1, steps=[[0, 0], [C("China's exports to Southeast Asia"), 0], [C("rose"), 13.4]],
                 text="CHINA'S EXPORTS TO ASEAN, 2025 (WTO)", until=C("A new factory can move")),
              sign("PART OF IT: PARTS & MATERIALS (WTO)", 1250, 330, C("parts and materials"), color="#FFF59D", size=30, until=C("A new factory can move")),
              *[it("drone", x=[[0, 300 - k * 200], [8 + k, 2200]], y=180 + k * 70, at=0.3 + k * 0.5, carry=["PARTS", "CHIPS", "MOTORS"][k], scale=0.75) for k in range(3)],
              it("toonwords", text="FINAL ASSEMBLY MOVES. PARTS... NOT YET.", x=1250, y=100, at=C("A new factory can move"), size=46)]},
    sources=["wto_gtos"])
stage("s32_move", "a4_move", {
    **W1("movingday", oldX=300, newX=2200, build=[[0, 0.6], [C("Until all of that"), 0.7]], newName="NEW PLANT"),
    "cam": cam((0, 1900, 520, 1.0), (C("roads and ports"), 1800, 500, 0.95, 1.2), (C("Until all of that arrives"), 1250, 520, 0.85, 1.6), (C("the boxes keep coming back"), 900, 560, 1.15, WHIP)), "drift": 3,
    "items": [sign("SUPPLIERS ✗", 1700, 120, C("suppliers that don't exist"), color="#FFCDD2", size=28),
              sign("ROADS & PORTS ✗", 1700, 220, C("roads and ports"), color="#FFCDD2", size=28),
              sign("STEADY POWER ✗", 2300, 120, C("steady power"), color="#FFCDD2", size=28),
              sign("TRAINED PEOPLE ✗", 2300, 220, C("people trained"), color="#FFCDD2", size=28),
              KIP(1850, 0.2, face="worry", pose="clipboard", hold="clipboard", faces=[[0, "smug"], [C("roads and ports"), "worry"], [C("the boxes keep coming back"), "panic"]], takes=[C("the boxes keep coming back")]),
              *[it("homebox", x=[[0, 2000 + k * 120], [C("Until all of that"), 2000 + k * 120], [C("the boxes keep coming back", 1.5), 500 + k * 130]], at=0.3 + k * 0.1,
                   label="MADE IN CHINA", face="grin", scale=0.8, hops=[C("the boxes keep coming back", 0.2 + k * 0.15)]) for k in range(5)]]},
    sfx=[{"kind": "whoosh", "cue": "the boxes keep coming back", "gain": 0.25}])
stage("s33_where", "a4_where", {
    **W1("movingday", oldX=300, newX=2200, build=[[0, 0.7], [C("Still, it is happening"), 1.0]], newName="NEW PLANT", suppliersAt=C("Still, it is happening", 0.8), supplierName="SUPPLIER #1"),
    "cam": cam((0, 2000, 520, 1.0), (C("Battery factory capacity"), 1800, 480, 0.9, 1.4), (C("And in Southeast Asia"), 1700, 500, 0.95, 1.2)), "drift": 3,
    "items": [it("toonwords", text="IT IS HAPPENING", x=2000, y=80, at=C("Still, it is happening"), until=C("The IEA says"), size=64),
              sign("U.S. EV IMPORTS 2025: LARGEST SHARE FROM MEXICO", 1700, 100, C("the largest share"), color="#C8E6C9", size=26, sub="IEA GLOBAL EV OUTLOOK 2026"),
              sign("BATTERY CAPACITY GREW FASTER IN EU & U.S. THAN CHINA", 1700, 250, C("Battery factory capacity"), color="#BBDEFB", size=26),
              sign("SE ASIA EV SALES: 1/3 FROM A VIETNAMESE CARMAKER", 1700, 390, C("And in Southeast Asia"), color="#FFF59D", size=26),
              KIP(2350, 0.3, face="happy", pose="cheer", hops=[C("Still, it is happening", 0.5)])]},
    sources=["iea_gevo"])
stage("s34_risk", "a4_risk", {
    **W1("tariffwall", wallX=1100, leftLabel="NEW PLANT", rightLabel="U.S. STORE",
         rows=[{"at": C("Vietnam's rate"), "label": "VIETNAM · 12.5% · JUL 2026", "h": 60, "color": "#A84B33"},
               {"at": C("Mexico's is"), "label": "MEXICO · 10% (USMCA EXEMPTIONS)", "h": 50, "color": "#C76B4A"}]),
    "cam": cam((0, 1100, 560, 1.1), (C("Since July"), 1100, 520, 1.0, 1.2)), "drift": 3,
    "items": [it("toonwords", text="NEW PLACE, SAME WALL", x=1100, y=100, at=0.3, until=C("Since July"), size=66),
              sign("SAME AS CHINA'S RATE (USTR, 91 FR 47318)", 1700, 160, C("the same as China's"), color="#FFF8E1", size=24),
              KIP(400, 0.3, face="shock", pose="facepalm", faces=[[0, "worry"], [C("the same as China's"), "shock"]])]},
    sources=["fr_301_2026", "crs_2026"])

# ====================================================================== PAYOFF + TEASER + BUTTON
stage("s35_payoff", "payoff", {
    **W1("partsstreet", asmX=2600, shopX=-200, gap=330, lit=[[C("Suppliers down the street"), 1], [C("refiners"), 3], [C("ports that never sleep"), 5], [C("engineers who have"), 6]]),
    "cam": cam((0, 1100, 480, 0.85), (C("Because of a neighborhood"), 1200, 500, 0.82, 1.6), (C("Tariffs can move"), 2300, 520, 1.0, 1.4),
               (C("That's why"), 1200, 480, 0.82, 1.4), (C("The next factory"), 1600, 500, 0.9, 1.4)), "drift": 2,
    "items": [it("toonwords", text="NOT ONE CHEAP WAGE", x=1100, y=40, at=C("Not because"), until=C("Because of a neighborhood"), size=56),
              it("toonwords", text="A NEIGHBORHOOD", x=1200, y=40, at=C("Because of a neighborhood"), until=C("Tariffs can move"), size=70, color="#FFFFFF"),
              sign("TARIFFS MOVE THE LAST STEP", 2300, 120, C("Tariffs can move"), color="#FFCDD2", size=28, until=C("That's why")),
              sign("THE NEIGHBORHOOD MOVES SLOWLY", 2300, 240, C("Rebuilding the whole"), color="#C8E6C9", size=28, until=C("That's why")),
              it("toonwords", text="> 1/4 OF WORLD MANUFACTURING", x=1200, y=40, at=C("more than a quarter"), until=C("The next factory"), size=54),
              sign("THE HARD PART: THE PARTS LIST", 1600, 160, C("Its parts list"), color="#FFF59D", size=30),
              MEL(800, 0.2, face="happy", pose="wave", hold="phone"), WEI(1300, 0.3, face="happy", pose="talk", talk=[[C("Suppliers down"), C("done it before", 0.5)]]),
              KIP(1900, 0.4, face="smug", pose="stand", hops=[C("The next factory")]),
              it("homebox", x=[[0, -300], [12, 2400]], at=0.3, label="PARTS", face="happy", scale=0.7, y=1000)]},
    sources=["wdi_mva"])
add("s36_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s37_button", "button", {
    **W1("kitchen", counterX=300, windowX=1250, tagText="MADE IN CHINA"),
    "cam": cam((0, 850, 520, 1.2), (3.0, 960, 540, 1.35, WHIP)), "drift": 0, "min_seconds": 5.6,
    "items": [gz(7, x=760, y=610, at=0.0, scale=0.55, face="happy", toastAt=1.4, faces=[[0, "happy"], [3.0, "worry"]],
                 stamp="PLUG: MADE IN CHINA", stampAt=3.0, stampX=250, stampY=-60),
              it("toonwords", text="MADE IN MEL'S KITCHEN!", x=850, y=170, at=0.4, until=2.8, size=56),
              MEL(1100, 0.0, face="grin", pose="cheer", faces=[[0, "grin"], [3.0, "deadpan"]], hops=[1.5], scale=1.3),
              it("toonwords", text="...STILL.", x=980, y=330, at=3.4, size=90, color="#FFFFFF")]},
    sfx=[{"kind": "hit", "at": 3.0, "gain": 0.3}])

write(OUT, "# GENERATED by tools/gen_chinafactories_storyboard.py; edit the generator, not this file.\n"
           "# Episode 60 storyboard (China factories): sitcom-style episode; bespoke worlds in CartoonStage/factory.tsx; tones from visual_direction.yaml.\n")
