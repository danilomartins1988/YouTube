"""Generates projects/the-island-getting-rich-from-ai/deliverables/documentary/storyboard.yaml (Episode 10).

Bespoke CartoonStage worlds: a Caribbean beach (pastel houses, palms, a sailboat), a cartoon internet where browser
windows type ".ai" names, renewal clocks, auctions, a registry data center, a hurricane, savings and debt stacks; presenter boards, charts and maps use the bright cartoon palette of the
project. The five parts are an internal structure only. Run: python tools/gen_anguilla_storyboard.py
"""
from __future__ import annotations

import math
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parents[1] / "projects/the-island-getting-rich-from-ai/deliverables/documentary/storyboard.yaml"
INTER = ["font:inter"]
GEO = ["geo:remotion_world", "font:inter"]
BOARD = {"x": 470, "y": 230, "w": 1370, "h": 800}
C = lambda cue, off=None: ({"cue": cue, "offset": off} if off is not None else {"cue": cue})
AXA = [-63.05, 18.22]                     # Anguilla
LL = {"tuvalu": [179.2, -8.5], "chagos": [72.4, -7.3], "mauritius": [57.55, -20.2]}
scenes: list[dict] = []


def add(id_, segment, type_, params, sources=(), assets=INTER, sfx=None):
    if type_ == "engine_draw":
        for st in params.get("strokes", []):
            d = st["d"]
            if "kind" not in st:
                st["kind"] = "box" if d.rstrip().endswith("Z") and d.count(" L ") == 3 else ("arrow" if " Q " in d and d.count("M ") == 2 else "stroke")
    s = {"id": id_, "segment": segment, "type": type_, "params": params}
    if sfx:
        s["sfx"] = sfx
    if sources:
        s["sources"] = list(sources)
    s["assets"] = list(assets)
    scenes.append(s)


def cart(id_, seg, params, sources=(), sfx=None):
    params.setdefault("fish", 3)
    add(id_, seg, "engine_cartoon", params, sources, sfx=sfx)


def card(id_, seg, title, sub):
    add(id_, seg, "act_title", {"number": "", "title": title, "subtitle": sub, "min_seconds": 5.4}, sfx=[{"kind": "hit", "at": 0.1, "gain": 0.25}])


def kinetic(id_, seg, lines, chapter=None):
    p = {"align": "center", "lines": [{"text": tx, "size": sz, "cue": cu, **({"color": co} if co else {}), **({"style": "body"} if st else {})}
                                      for tx, sz, cu, co, st in lines]}
    if chapter:
        p["chapter"] = chapter
    add(id_, seg, "kinetic_text", p)


def rect(x, y, w, h):
    return f"M {x} {y} L {x + w} {y} L {x + w} {y + h} L {x} {y + h} Z"


def arrow(a, b, bend=0.0):
    mx, my = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend
    ang = math.atan2(b[1] - my, b[0] - mx)
    h1 = (b[0] - 24 * math.cos(ang - 0.45), b[1] - 24 * math.sin(ang - 0.45))
    h2 = (b[0] - 24 * math.cos(ang + 0.45), b[1] - 24 * math.sin(ang + 0.45))
    return f"M {a[0]} {a[1]} Q {mx:.0f} {my:.0f} {b[0]} {b[1]} M {h1[0]:.0f} {h1[1]:.0f} L {b[0]} {b[1]} L {h2[0]:.0f} {h2[1]:.0f}"


def lbl(text, x, y, size=30, color="ink", anchor="middle"):
    return {"text": text, "x": x, "y": y, "size": size, "color": color, "anchor": anchor}


def dot(x, y):
    return f"M {x} {y} L {x} {y}"


def island(x=1300, w=440, **kw):
    return {"kind": "island", "x": x, "w": w, "text": "ANGUILLA", **kw}


def letters(x=1260, y=150, at=0.0, size=150, **kw):
    return {"kind": "letters", "text": ".ai", "x": x, "y": y, "at": at, "size": size, **kw}


def coins(x, y, to, at, rate=4, until=None):
    c = {"kind": "coins", "x": x, "y": y, "to": to, "at": at, "rate": rate}
    if until is not None:
        c["until"] = until
    return c


def office(x, text, color="purple", at=None, scale=1.0):
    o = {"kind": "office", "x": x, "text": text, "color": color, "scale": scale}
    if at is not None:
        o["at"] = at
    return o


def co(text, x, y, at, color="white", sub=None, tail=None, until=None, size=None, screen=False):
    c = {"text": text, "x": x, "y": y, "at": at, "color": color}
    for k, v in (("sub", sub), ("tail", tail), ("until", until), ("size", size)):
        if v is not None:
            c[k] = v
    if screen:
        c["screen"] = True
    return c


def stage(id_, seg, params, sources=(), sfx=None):
    """A bespoke CartoonStage world (beach, cartoon web, browser windows, office, data center, airport)."""
    add(id_, seg, "engine_cartoon", params, sources, sfx=sfx)


def it(kind, **kw):
    return {"kind": kind, **kw}


F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
BEACH = lambda x0=-1600, x1=4600, **kw: Z("beach", x0, x1, **kw)


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 1, "skin": k, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


# ====================================================================== HOOK
stage("s01_island", "h_question", {
    "zones": [BEACH()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.2}, {"at": C("Just two letters"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("sign", x=480, y=430, text="NO FACTORIES", at=C("No factories"), until=C("Just two letters"), color="#FFCDD2", size=36),
              it("sign", x=960, y=330, text="NO DATA CENTERS", at=C("no data centers"), until=C("Just two letters"), color="#FFCDD2", size=36),
              it("sign", x=1440, y=430, text="NO TECH GIANTS", at=C("no tech giants"), until=C("Just two letters"), color="#FFCDD2", size=36),
              it("letters", x=960, y=380, text=".ai", at=C("Just two letters"), size=260, color="gold"),
              it("burst", x=960, y=380, at=C("Just two letters", 0.2)),
              *crowd([300, 1650], "cheer", at=C("Just two letters", 0.3))],
    "callouts": [co("An island getting rich from AI?", 960, 150, C("tiny island"), "gold", screen=True, size=44, until=C("No factories", -0.3))]},
    sources=["ap_2024", "gleaner_2026"])
add("s02_map", "h_stakes", "engine_map", {
    "title": "Anguilla", "subtitle": "{{island.display}} people · {{rev_2026.display}} from .ai in 7 months of 2026 ({{rev_2026.share_display}} of revenue)",
    "cameras": [{"at": 0, "lon": -40, "lat": 25, "span": 120}, {"at": C("Anguilla"), "lon": -63.05, "lat": 18.3, "span": 9, "dur": 2.6},
                {"at": C("two letters"), "lon": -62.5, "lat": 18.0, "span": 26, "dur": 3.0}, {"at": C("of all the money"), "lon": -63.05, "lat": 18.25, "span": 12, "dur": 3.0}],
    "drift": {"lon": 0.08, "zoom": 0.012}, "tilt": [[0, 14], [10, 4]],
    "highlights": [{"iso": "AIA", "color": "gold", "at": C("Anguilla")}],
    "hubs": [{"id": "a", "at": AXA, "label": "Anguilla", "sub": "British Overseas Territory · 91 km²", "color": "gold", "time": C("a Caribbean island")}],
    "routes": [{"from": [-77.0, 38.9], "to": AXA, "at": C("a Caribbean island", 1.0), "dur": 1.4, "color": "accent2", "tokenShape": "coin", "tokens": 8, "tokenEvery": 0.35, "lift": 0.25},
               {"from": [-0.1, 51.5], "to": AXA, "at": C("a Caribbean island", 1.6), "dur": 1.6, "color": "accent2", "tokenShape": "coin", "tokens": 8, "tokenEvery": 0.35, "lift": 0.25},
               {"from": [-122.4, 37.8], "to": AXA, "at": C("a Caribbean island", 2.2), "dur": 1.6, "color": "accent2", "tokenShape": "coin", "tokens": 8, "tokenEvery": 0.35, "lift": 0.25}],
    "caption": "Real location (Natural Earth) · arrows schematic: payments arrive from buyers worldwide"},
    sources=["ap_2024", "gleaner_2026", "natural_earth"], assets=GEO)

# ====================================================================== PART 1: the lucky letters
card("s03_c1", "m1_card", "The Lucky Letters", "How an island got .ai")
stage("s04_q1", "m1_question", {
    "zones": [Z("web")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.2}, {"at": C("most wanted"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("browser", x=960, y=470, at=0.2, url="the-most-wanted-letters.ai", typeAt=0.6, typeDur=3.0),
              it("letters", x=1600, y=260, text="?", at=C("no tech industry"), size=130, color="purple")],
    "callouts": [co("No tech industry?", 960, 150, C("no tech industry"), "gold", screen=True, until=C("most wanted", -0.3)),
                 co("The most wanted letters online", 960, 960, C("most wanted"), "white", screen=True)]})
# ---- PRESENTER A: what a domain name is
add("p05_what", "m1_what", "engine_draw", {
    "title": "What is a domain name?", "board": BOARD, "draw_start": C("Every website"), "speed": 1300,
    "enter": {"from": -260, "to": 430, "at": C("First", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(1180, 330, 520, 300), "color": "accent2", "width": 6, "start": C("Every website"), "label": lbl("WEBSITE", 1440, 470, 40, "accent2")},
        {"d": dot(1440, 540), "color": "ink", "width": 1, "start": C("phone number"), "label": lbl("203.0.113.7", 1440, 540, 34, "ink")},
        {"d": rect(600, 420, 380, 110), "color": "accent", "width": 6, "start": C("easy name"), "label": lbl("shop.ai", 790, 492, 44, "accent")},
        {"d": arrow((990, 475), (1170, 475)), "color": "ink", "width": 5, "start": C("points to")},
        {"d": "M 820 560 Q 880 600 940 560", "color": "risk", "width": 6, "start": C("the last part"), "label": lbl("THE ENDING", 880, 640, 30, "risk")},
        {"d": dot(1440, 600), "color": "muted", "width": 1, "start": C("computers use"), "label": lbl("(example number)", 1440, 600, 22, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("the last part", 0.5), "dur": 1.4, "target": [880, 560]}, {"kind": "smile", "at": C("is called", 0.2), "dur": 2.0}],
    "scale": 0.86, "floor": 1040})
stage("s06_codes", "m1_codes", {
    "zones": [Z("web")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("Anguilla's code"), "x": 1400, "y": 520, "zoom": 1.15, "dur": 2.4}], "drift": 0,
    "items": [it("browser", x=480, y=470, w=520, h=330, at=C("Brazil"), url="example.br", typeAt=C("Brazil", 0.2), typeDur=1.0, scale=0.9),
              it("browser", x=960, y=470, w=520, h=330, at=C("Japan"), url="example.jp", typeAt=C("Japan", 0.2), typeDur=1.0, scale=0.9),
              it("browser", x=1440, y=470, w=520, h=330, at=C("Anguilla's code"), url="example.ai", typeAt=C("Anguilla's code", 0.2), typeDur=1.0, scale=0.9),
              it("sign", x=480, y=760, text="BRAZIL", at=C("Brazil"), size=30), it("sign", x=960, y=760, text="JAPAN", at=C("Japan"), size=30),
              it("sign", x=1440, y=760, text="ANGUILLA", at=C("Anguilla's code"), color="#FFF59D", size=30)],
    "callouts": [co("Every country gets two letters", 960, 150, C("Every country"), "white", screen=True, size=40, until=C("official code", -0.3)),
                 co("…from its official country code", 960, 150, C("official code"), "gold", screen=True, size=40)]},
    sources=["iana_ai"])
stage("s07_1995", "m1_assigned", {
    "zones": [BEACH()], "worldW": 2600,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.05}, {"at": C("Its official"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("calendar", x=330, y=320, at=0.2, pages=[[0, "{{assigned.display}}", "ASSIGNED"]], scale=0.8),
              it("letters", x=800, y=360, text=".ai", at=C("Anguilla was assigned"), size=180, color="gold"),
              it("sign", x=800, y=590, text="WORTH ALMOST NOTHING", at=C("almost nothing"), color="#FFCDD2", size=28),
              it("sign", x=1250, y=300, text="“AI” = A NICHE LAB IDEA", at=C("niche idea"), color="#E1BEE7", size=28, hang=True, swing=True),
              it("building", x=1850, style="gov", color="#FFE082", text="GOVERNMENT OF ANGUILLA", at=C("Its official"), scale=0.75)],
    "callouts": [co("Manager today: Government of Anguilla", 960, 150, C("Its official"), "green", screen=True, sub="IANA delegation record")]},
    sources=["ap_2024", "afnic_2025", "iana_ai"])
stage("s08_cate", "m1_cate", {
    "zones": [Z("beach", -1600, 1500), Z("office", 1500, 6000)], "worldW": 3400,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("whether he wanted"), "x": 2050, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("For a while"), "x": 2700, "y": 520, "zoom": 1.0, "dur": 2.4}, {"at": C("For years"), "x": 2050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("plane", x=[[0, -300], [{"cue": "moved to the island"}, -300], [{"cue": "moved to the island", "offset": 5}, 1300]], y=[[0, 200], [{"cue": "moved to the island", "offset": 5}, 520]], tilt=8, scale=0.6),
              it("calendar", x=330, y=320, at=C("moved to the island"), pages=[[0, "1994", "ARRIVES"]], scale=0.7),
              it("desk", x=2050, glow="green", pile=True), it("person", x=1980, pose="type", glasses=True, at=C("whether he wanted", -0.6), hair=1),
              it("letters", x=2150, y=330, text=".ai", at=C("run dot"), size=120, color="gold"),
              it("building", x=2900, style="office", color="#B0BEC5", text="A COMPANY IN TAIWAN", at=C("company in Taiwan"), until=C("disappeared", 0.6), scale=0.7),
              it("letters", x=2900, y=330, text="?!", at=C("disappeared"), until=C("recovered", 0.5), size=120, color="risk"),
              it("arrow", **{"from": [2850, 300], "to": [2250, 300]}, at=C("recovered"), until=C("For years"), color="green", text="RECOVERED"),
              it("sign", x=2450, y=300, text="GOVERNMENT = OFFICIAL CONTACT", at=C("official contact"), color="#C8E6C9", size=28)],
    "callouts": [co("Vince Cate, software developer", 960, 960, C("Vince Cate"), "white", sub="his own account (IEEE Spectrum)", screen=True, until=C("For a while", -0.3)),
                 co("“Do you want to run .ai?”", 960, 150, C("whether he wanted"), "gold", screen=True, until=C("For a while", -0.3)),
                 co("Handed to a company in Taiwan… that disappeared", 960, 150, C("For a while"), "risk", screen=True, until=C("For years", -0.3)),
                 co("He ran sales for the government", 960, 150, C("For years"), "white", screen=True)]},
    sources=["ieee_2024"])
kinetic("s09_t1", "m1_transition", [("Two letters, given away almost by accident", 50, "Two letters", None, True), ("How do they turn into money?", 76, "turn into money", "accent", False)])

# ====================================================================== PART 2: the money machine
card("s10_c2", "m2_card", "The Money Machine", "Two letters, paid again and again")
stage("s11_q2", "m2_question", {
    "zones": [Z("web")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.15}, {"at": C("two letters"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("browser", x=700, y=470, at=0.2, url="checkout.ai", typeAt=0.5, page="price", text="PAY", sub="for two letters?", button="PAY"),
              it("coins", **{"from": [800, 560], "to": [1700, 300]}, at=1.2, rate=3),
              it("letters", x=1650, y=280, text=".ai", at=C("two letters"), size=130, color="gold")],
    "callouts": [co("Who pays?", 960, 150, C("Who actually"), "gold", screen=True, size=44, until=C("two letters", -0.3)),
                 co("For two letters?!", 960, 150, C("two letters"), "white", screen=True, size=44)]})
# ---- PRESENTER B: the money machine
add("p12_chain", "m2_draw", "engine_draw", {
    "title": "The money machine", "board": BOARD, "draw_start": C("A start-up"), "speed": 1400,
    "enter": {"from": 2200, "to": 1600, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(540, 330, 260, 110), "color": "accent2", "width": 5, "start": C("A start-up"), "label": lbl("START-UP", 670, 395, 30, "accent2")},
        {"d": arrow((810, 385), (960, 385)), "color": "ink", "width": 4, "start": C("buys it")},
        {"d": rect(970, 330, 280, 110), "color": "accent3", "width": 5, "start": C("sells domain names"), "label": lbl("NAME SELLER", 1110, 395, 28, "accent3")},
        {"d": arrow((1110, 450), (1110, 560)), "color": "ink", "width": 4, "start": C("passes the order")},
        {"d": rect(940, 570, 340, 130), "color": "accent", "width": 6, "start": C("the registry"), "label": lbl("REGISTRY", 1110, 630, 32, "accent")},
        {"d": dot(1110, 672), "color": "ink", "width": 1, "start": C("master list"), "label": lbl("master list of .ai names", 1110, 672, 22, "muted")},
        {"d": arrow((950, 700), (760, 820), 0.08), "color": "accent", "width": 5, "start": C("pays the Government")},
        {"d": rect(470, 820, 380, 120), "color": "accent", "width": 6, "start": C("Government of Anguilla"), "label": lbl("GOVERNMENT OF ANGUILLA", 660, 890, 24, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("Government of Anguilla", 0.8), "dur": 1.4, "target": [660, 880]}, {"kind": "smile", "at": C("Government of Anguilla", 2.2), "dur": 1.5}],
    "scale": 0.86, "floor": 1040}, sources=["ap_2024"])
stage("s13_price", "m2_price", {
    "zones": [Z("web")], "worldW": 2800,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("auctioned"), "x": 1650, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("expires"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("browser", x=640, y=470, at=0.2, url="your-name.ai", page="price", text="{{price.display}}", sub="for two years", button="BUY", w=640),
              it("clock", x=1150, y=560, at=C("pay again"), period=2.5, text="RENEW", scale=0.8),
              it("gavel", x=1650, y=F - 20, hits=[C("litigate"), C("litigate", 0.8)], scale=1.3),
              it("sign", x=1650, y=380, text="litigate.ai", sub="auctioned in 2023", at=C("litigate"), color="#FFF59D", size=40),
              it("browser", x=2300, y=470, at=C("expires"), url="old-name.ai", page="expired", w=560, h=400,
                 pages=[[0, "expired"], [{"cue": "sold again"}, "sold"]], text="SOLD AGAIN", button="PAID"),
              it("coins", **{"from": [2300, 400], "to": [2900, 100]}, at=C("paid once more"), rate=4)],
    "callouts": [co("{{price.display}} for 2 years", 960, 150, C("costs about"), "gold", screen=True, size=48, sub="a new .ai name (IMF)", until=C("pay again", -0.3)),
                 co("…then pay again to keep it", 960, 150, C("pay again"), "white", screen=True, until=C("auctioned", -0.3)),
                 co("litigate.ai: {{price.auction_display}}", 960, 150, C("litigate"), "green", sub="auction, 2023 (IMF)", size=40, screen=True, until=C("expires", -0.3)),
                 co("Expired names resold → paid again", 960, 150, C("expires"), "white", screen=True)]},
    sources=["imf_2024", "ap_2024"])
add("s14_renew", "m2_renew", "engine_flow", {
    "title": "Rented, not bought", "subtitle": "every renewal pays the island again", "cardW": 280, "cardH": 220,
    "stages": [
        {"id": "b", "label": "Register", "sub": "{{price.display}} · 2 years", "x": 420, "y": 600, "kind": "customer", "color": "accent2", "appear": 0.3, "output": "coin"},
        {"id": "w", "label": "Two years", "sub": "the name is yours", "x": 960, "y": 380, "kind": "warehouse", "color": "accent3", "appear": 0.45, "output": "packet"},
        {"id": "r", "label": "Renew", "sub": "or lose the name", "x": 1500, "y": 600, "kind": "company", "color": "accent", "appear": 0.6, "output": "coin"},
        {"id": "g", "label": "Anguilla", "sub": "paid every time", "x": 960, "y": 850, "kind": "bank", "color": "accent", "appear": 0.75, "output": "coin"}],
    "links": [{"from": "b", "to": "w", "appear": 0.9}, {"from": "w", "to": "r", "appear": 1.0}, {"from": "r", "to": "g", "appear": 1.1}, {"from": "g", "to": "b", "appear": 1.2}],
    "items": {"starts": [C("never really bought"), C("comes back"), C("two years after")], "route": ["b", "w", "r", "g", "b"], "travel": 0.8, "process": 0.9}},
    sources=["imf_2024", "ap_2024"])
stage("s15_why", "m2_why", {
    "zones": [Z("office")], "worldW": 1920,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.15}, {"at": C("so many new"), "x": 960, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 0,
    "items": [it("desk", x=560, glow="purple"), it("person", x=490, pose="type", at=0.2, hair=2),
              it("browser", x=560, y=330, w=520, h=300, at=C("for an AI company"), url="robot-chef.ai", typeAt=C("for an AI company", 0.3), scale=0.75),
              it("sign", x=1150, y=330, text="“WE DO AI”", sub="in two letters", at=C("two letters"), color="#FFF59D", size=40, hang=True, swing=True),
              it("letters", x=1150, y=560, text="BRAND", at=C("like a brand"), size=80, color="green"),
              *crowd([1400, 1520, 1640, 1760], "cheer", at=C("so many new"), scale=0.7)],
    "callouts": [co("Everyone wants one", 960, 150, C("everyone wants"), "gold", screen=True, size=44)]})
stage("s16_manager", "m2_manager", {
    "zones": [BEACH(x1=1300), Z("datacenter", 1300, 5000)], "worldW": 2800,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("American company"), "x": 1900, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("building", x=650, style="gov", color="#FFE082", text="GOVERNMENT", at=0.2, scale=0.75),
              it("device", type="server", x=1700, y=F, at=C("run the registry"), text="REGISTRY"),
              it("sign", x=2150, y=330, text="IDENTITY DIGITAL", sub="American company · since 2024", at=C("Identity Digital"), color="#BBDEFB", size=34),
              it("arrow", **{"from": [900, 400], "to": [1550, 400]}, at=C("signed a deal"), color="gold", text="DEAL"),
              it("letters", x=2400, y=640, text=".au", at=C("dot A U"), size=100, color="cyan")],
    "callouts": [co("2024: a U.S. company runs the registry", 960, 150, C("signed a deal"), "white", screen=True, sub="Identity Digital (AP)", until=C("more money", -0.3)),
                 co("More money + a safer system", 960, 150, C("more money"), "green", screen=True, sub="the government's words", until=C("Australia", -0.3)),
                 co("It also runs Australia's .au", 960, 150, C("Australia"), "white", screen=True)]},
    sources=["ap_2024", "iana_ai"])
kinetic("s17_t2", "m2_transition", [("A small fee, paid again and again", 54, "A small fee", None, True), ("× the AI boom", 96, "multiply", "accent", False)])

# ====================================================================== PART 3: the boom
card("s18_c3", "m3_card", "The Boom", "When the world wanted .ai")
stage("s19_q3", "m3_question", {
    "zones": [Z("web")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.15}, {"at": C("wanted dot"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("browser", x=700, y=470, at=0.2, url="chatbot.ai", page="chat", w=700),
              it("browser", x=1450, y=380, at=C("wanted dot"), url="new-startup.ai", scale=0.6, tilt=4),
              it("browser", x=1500, y=700, at=C("wanted dot", 0.5), url="ai-anything.ai", scale=0.55, tilt=-3)],
    "callouts": [co("How big did it get?", 960, 150, C("How big"), "gold", screen=True, size=46)]})
add("s20_regs", "m3_regs", "engine_chart", {"chart": "bar", "box": {"x": 300, "y": 330, "w": 1320, "h": 500}, "start": C("In twenty twenty-two"), "stagger": 1.6,
    "title": "Registered .ai names", "note": "IMF (2022, 2023) · official count (Jan 2025) · government announcement (Jan 2026)",
    "data": [{"label": "2022", "value": 144, "display": "{{regs.display}}"}, {"label": "2023", "value": 354, "display": "354,000"},
             {"label": "Jan 2025", "value": 598, "display": "598,007"}, {"label": "Jan 2026", "value": 1000, "display": "1 million+"}],
    "highlight": 3, "highlightAt": C("passed"), "color": "accent2", "highlightColor": "accent"},
    sources=["imf_2024", "dnw_2026"])
stage("s21_cate", "m3_cate", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.05}, {"at": C("premier said"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("desk", x=560, glow="green", pile=True), it("person", x=490, pose="cheer", glasses=True, at=0.2, hair=1),
              it("chart", x=1250, y=380, w=600, h=340, at=C("almost four times", -0.6), dur=2.5, text="MONTHLY SALES", pts=[0.1, 0.12, 0.15, 0.25, 0.4, 0.6]),
              it("letters", x=1250, y=640, text="×4", at=C("almost four times"), size=110, color="green"),
              it("sign", x=1800, y=330, text="“COULD EVEN DOUBLE”", sub="the premier, 2024", at=C("premier said"), color="#FFF59D", size=30),
              it("letters", x=1800, y=600, text="×3", at=C("nearly tripled"), size=110, color="gold")],
    "callouts": [co("Sales ≈ ×4: about {{cate_sales.display}}", 960, 150, C("almost four times"), "green", screen=True, sub="Vince Cate, early 2024 (IEEE Spectrum)", until=C("premier said", -0.3)),
                 co("By 2025: nearly tripled", 960, 150, C("nearly tripled"), "gold", screen=True)]},
    sources=["ieee_2024"])
add("s22_rev", "m3_revenue", "engine_chart", {"chart": "bar", "box": {"x": 360, "y": 330, "w": 1200, "h": 500}, "start": C("In twenty twenty-three"), "stagger": 1.8,
    "title": ".ai revenue (US dollars)", "note": "IMF (2023) · draft estimates and Anguilla Focus (2025) · converted at EC$2.70 = US$1",
    "valuePrefix": "$", "valueSuffix": "m",
    "data": [{"label": "2023", "value": 32, "display": "{{rev_2023.display}}"}, {"label": "2025 plan", "value": 49, "display": "{{rev_2025.proj_display}}"},
             {"label": "2025 actual", "value": 85.3, "display": "{{rev_2025.display}}"}],
    "highlight": 2, "highlightAt": C("far more"), "color": "accent2", "highlightColor": "accent"},
    sources=["imf_2024", "focus_2025", "eccb_peg"])
add("s23_share", "m3_peak", "engine_chart", {"chart": "donut", "cx": 960, "cy": 590, "r": 250, "thick": 90, "start": C("first seven months"),
    "data": [{"label": ".ai domain", "value": 47.5, "display": "47.5%"}, {"label": "everything else", "value": 52.5, "display": "52.5%"}],
    "center": "{{rev_2026.share_display}}", "centerSub": "of government revenue · Jan–Jul 2026",
    "title": "{{rev_2026.display}} from .ai in 7 months", "subtitle": "more than all productive-sector taxes ({{rev_2026.tax_display}})"},
    sources=["gleaner_2026", "eccb_peg"])
kinetic("s24_t3", "m3_transition", [("So what does a tiny island do", 56, "So what", None, True), ("with that much money?", 80, "that much money", "accent", False)])

# ====================================================================== PART 4: what the money buys
card("s25_c4", "m4_card", "What the Money Buys", "Airport, roads, health")
stage("s26_q4", "m4_question", {
    "zones": [BEACH()], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.2}, {"at": C("how much"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("coins", **{"from": [960, -200], "to": [960, 760]}, at=0.3, rate=5, arc=0),
              it("letters", x=960, y=300, text="?", at=C("Where does"), size=140, color="gold"),
              *crowd([600, 720, 1200, 1320], "stand", at=C("people"))],
    "callouts": [co("Where does it go?", 960, 150, C("Where does"), "gold", screen=True, size=46, until=C("how much", -0.3)),
                 co("…and how much per person?", 960, 150, C("how much"), "white", screen=True, size=44)]})
stage("s27_uses", "m4_uses", {
    "zones": [Z("airport", -1600, 1400), BEACH(1400, 3200), Z("site", 3200, 7000)], "worldW": 4600,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.0}, {"at": C("health services", -0.5), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.6},
            {"at": C("pay down debt", -0.5), "x": 2300, "y": 500, "zoom": 0.9, "dur": 2.4}, {"at": C("vocational"), "x": 3900, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("plane", x=[[0, -300], [{"cue": "the airport"}, -300], [{"cue": "the airport", "offset": 5}, 900]], y=[[0, 300], [{"cue": "the airport", "offset": 5}, 790]], tilt=6, scale=0.6),
              it("sign", x=1150, y=560, text="NEW ROADS", at=C("new roads"), post=True, color="#FFF59D", size=28),
              it("sign", x=1700, y=330, text="TAX RELIEF", at=C("tax relief"), color="#C8E6C9", size=34, hang=True, swing=True),
              it("device", type="hospital", x=2200, y=F + 40, at=C("health services"), text="HEALTH"),
              *crowd([2500, 2620], "cheer", at=C("free medical"), scale=0.7, hair=4),
              it("stack", x=2900, at=C("pay down debt", -0.5), h=[[0, 500], [{"cue": "pay down debt"}, 500], [{"cue": "pay down debt", "offset": 3}, 200]], text="DEBT", color="#FFCDD2"),
              it("crane", x=3900, text="TRAINING CENTER", at=C("vocational"), progress=[[0, 0.5], [30, 0.95]])],
    "callouts": [co("Airport · roads", 960, 150, C("the airport"), "gold", screen=True, until=C("tax relief", -0.3)),
                 co("Tax relief · health services", 960, 150, C("tax relief"), "green", screen=True, until=C("free medical", -0.3)),
                 co("Free care for seniors", 960, 150, C("free medical"), "white", screen=True, until=C("pay down debt", -0.3)),
                 co("Debt paid down", 960, 150, C("pay down debt"), "white", screen=True, until=C("vocational", -0.3)),
                 co("A new vocational training center", 960, 150, C("vocational"), "gold", screen=True)]},
    sources=["dnw_2026", "ap_2024", "imf_2024"])
# ---- PRESENTER C: the per-person maths
add("p28_person", "m4_person", "engine_draw", {
    "title": "Do the math (our calculation)", "board": BOARD, "draw_start": C("In twenty twenty-five"), "speed": 1400,
    "enter": {"from": -260, "to": 430, "at": C("Now do the math", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 600 880 L 600 480 L 780 480 L 780 880", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.35, "kind": "bar", "start": C("the island earned"),
         "label": lbl("{{rev_2025.display}}", 690, 455, 44, "accent")},
        {"d": dot(690, 930), "color": "ink", "width": 1, "start": C("from the domain"), "label": lbl(".ai, 2025", 690, 930, 26, "muted")},
        {"d": "M 880 680 L 960 680 M 914 642 A 6 6 0 1 0 926 642 A 6 6 0 1 0 914 642 M 914 718 A 6 6 0 1 0 926 718 A 6 6 0 1 0 914 718", "color": "ink", "width": 8, "start": C("Divide it")},
        {"d": rect(1010, 610, 300, 140), "color": "accent2", "width": 5, "start": C("Divide it", 0.6), "label": lbl("{{island.display}} people", 1160, 690, 30, "accent2")},
        {"d": "M 1350 660 L 1420 660 M 1350 700 L 1420 700", "color": "ink", "width": 8, "start": C("for every resident", -0.8)},
        {"d": rect(1460, 590, 330, 180), "color": "accent3", "width": 6, "start": C("for every resident"), "label": lbl("{{per_person.display}}", 1625, 695, 46, "accent3")},
        {"d": dot(1625, 810), "color": "muted", "width": 1, "start": C("two letters on a screen"), "label": lbl("each (our calculation)", 1625, 810, 24, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("for every resident", 0.8), "dur": 1.5, "target": [1625, 690]}, {"kind": "react", "at": C("two letters on a screen")}],
    "scale": 0.86, "floor": 1040}, sources=["focus_2025", "ap_2024"])
stage("s29_budget", "m4_budget", {
    "zones": [BEACH()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("A big part"), "x": 960, "y": 470, "zoom": 0.92, "dur": 2.4}], "drift": 0,
    "items": [it("stack", x=600, at=C("plans to collect"), h=[[0, 40], [{"cue": "plans to collect"}, 40], [{"cue": "plans to collect", "offset": 3}, 620]], text="{{budget_2026.display}}", sub="all government revenue, 2026 plan"),
              it("stack", x=1300, at=C("A big part"), h=[[0, 40], [{"cue": "A big part"}, 40], [{"cue": "A big part", "offset": 3}, 225]], text="{{rev_2026.display}}", sub=".ai alone, Jan–Jul 2026", color="gold"),
              it("letters", x=1300, y=820, text=".ai", at=C("dot A I"), size=90, color="gold")],
    "callouts": [co("How big is that?", 960, 150, C("For comparison"), "white", screen=True, size=44, until=C("A big part", -0.3)),
                 co("converted at EC$2.70 = US$1", 960, 1010, C("plans to collect"), "white", screen=True, size=24)]},
    sources=["focus_budget_2026", "gleaner_2026", "eccb_peg"])
stage("s30_tourism", "m4_tourism", {
    "zones": [BEACH(x1=1800), Z("web", 1800, 5000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("second engine"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "shake": [{"at": C("powerful hurricane"), "dur": 1.6, "amp": 12}],
    "items": [*crowd([500, 640, 1150], "cheer", at=C("Tourism makes up"), until=C("powerful hurricane"), hat="#FFC93C"),
              *crowd([500, 640, 1150], "worry", at=C("powerful hurricane", 0.3), hat="#FFC93C"),
              it("storm", x=[[0, 1500], [{"cue": "powerful hurricane"}, 1500], [{"cue": "powerful hurricane", "offset": 6}, 700]], y=170, at=C("powerful hurricane"), scale=1.3),
              it("sign", x=900, y=330, text="PANDEMIC: NO TOURISTS", at=C("the pandemic"), color="#FFCDD2", size=30, hang=True, swing=True),
              it("browser", x=2300, y=450, at=C("second engine", -0.4), url="island-money.ai", w=620, h=380, scale=0.9),
              it("coins", **{"from": [2300, 300], "to": [1200, 500]}, at=C("no storm"), rate=4)],
    "callouts": [co("Tourism = {{tourism.display}} of the economy", 960, 150, C("Tourism makes up"), "gold", screen=True, size=40, sub="IMF", until=C("powerful hurricane", -0.3)),
                 co("Hurricane, then pandemic", 960, 150, C("powerful hurricane"), "risk", screen=True, until=C("second engine", -0.3)),
                 co("A second engine, online", 960, 150, C("second engine"), "green", screen=True)]},
    sources=["imf_2024", "ap_2024"], sfx=[{"kind": "hit", "cue": "powerful hurricane", "gain": 0.3}])
kinetic("s31_t4", "m4_transition", [("Money that falls from the sky", 56, "But money", None, True), ("can stop falling", 80, "stop falling", "risk", False)])

# ====================================================================== PART 5: can it last?
card("s32_c5", "m5_card", "Can It Last?", "When the hype cools")
stage("s33_q5", "m5_question", {
    "zones": [BEACH(night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.15}, {"at": C("Its own leaders"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("chart", x=960, y=380, w=620, h=340, at=0.3, dur=4, text=".ai MONEY: WHAT NEXT?", pts=[0.1, 0.2, 0.4, 0.7, 0.85, 0.8]),
              it("letters", x=1450, y=280, text="?", at=C("cools down"), size=120, color="gold")],
    "callouts": [co("What if the AI boom cools?", 960, 960, C("What happens"), "gold", screen=True, size=44)]})
kinetic("s34_quote", "m5_quote", [
    ("“You can't predict how long this", 50, "You can't predict", None, False), ("is going to last.”", 50, "going to last", None, False),
    ("Premier Ellis Webster, 2024 (AP)", 30, "we can't rely", "muted", True),
    ("Expected ≈ {{risk_quote.display}} of revenue → actual {{rev_2026.share_display}} (Jan–Jul 2026)", 38, "shot far higher", "accent", True)], chapter="Can it last")
stage("s35_renew", "m5_renewals", {
    "zones": [Z("web")], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("owners stop"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("clock", x=560, y=430, at=0.3, period=2.4, stopAt=C("owners stop"), text="RENEWAL", stopText="NOT RENEWED"),
              it("browser", x=1000, y=380, w=520, h=320, scale=0.8, at=C("bought in the rush"), url="rush-buy.ai", pages=[[0, "site"], [{"cue": "owners stop"}, "expired"]]),
              it("browser", x=1550, y=380, w=520, h=320, scale=0.8, at=C("bought in the rush", 0.4), url="hype-bot.ai", pages=[[0, "site"], [{"cue": "the hype fades"}, "expired"]]),
              it("coins", **{"from": [1300, 600], "to": [2300, 700]}, at=0.5, until=C("money shrinks"), rate=5),
              it("sign", x=1300, y=760, text="POSSIBLE RISK", sub="not a forecast", at=C("If AI"), color="#FFF59D", size=28)],
    "callouts": [co("Renewals = the real test", 960, 150, C("real test"), "gold", screen=True, size=44, until=C("owners stop", -0.3)),
                 co("Stop renewing → less money, two years later", 960, 150, C("owners stop"), "risk", screen=True, until=C("slow leak", -0.3)),
                 co("A slow leak?", 960, 150, C("slow leak"), "white", screen=True, size=44)]})
stage("s36_tv", "m5_tv", {
    "zones": [BEACH()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.15}, {"at": C("At its peak"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("sign", x=330, y=560, text="TUVALU, PACIFIC", post=True, at=C("Tuvalu"), color="#FFF59D", size=28),
              it("device", type="tv", x=760, y=760, at=C("dot T V"), text=".tv", redAt=C("in decline"), scale=1.2),
              it("chart", x=1350, y=380, w=560, h=330, at=C("video sites"), dur=4, text=".tv NAMES (schematic)", pts=[0.1, 0.3, 0.6, 0.85, 0.9], crashAt=C("in decline"))],
    "callouts": [co("Tuvalu owns .tv", 960, 150, C("Tuvalu"), "white", screen=True, until=C("Twitch", -0.3)),
                 co("A hit with video sites, incl. Twitch", 960, 150, C("Twitch"), "gold", screen=True, until=C("At its peak", -0.3)),
                 co("{{tv_io.display}} names at its peak", 960, 150, C("At its peak"), "green", screen=True, size=40, sub="Afnic", until=C("in decline", -0.3)),
                 co("Now in decline", 960, 150, C("in decline"), "risk", screen=True, size=44)]},
    sources=["afnic_2025", "theworld_tv"])
add("s37_io", "m5_io", "engine_map", {
    "title": ".io · British Indian Ocean Territory", "subtitle": "loved by tech start-ups · the territory is being transferred to Mauritius (Afnic)",
    "cameras": [{"at": 0, "lon": 60, "lat": 0, "span": 120}, {"at": C("British Indian"), "lon": 66, "lat": -13, "span": 40, "dur": 2.4}],
    "drift": {"lon": 0.03, "zoom": 0.008}, "tilt": [[0, 12], [12, 4]],
    "highlights": [{"iso": "MUS", "color": "accent", "at": C("Mauritius")}],
    "hubs": [{"id": "c", "at": LL["chagos"], "label": "British Indian Ocean Territory", "sub": ".io", "color": "accent2", "time": C("belongs to")},
             {"id": "m", "at": LL["mauritius"], "label": "Mauritius", "color": "accent", "time": C("Mauritius")}],
    "routes": [{"from": LL["chagos"], "to": LL["mauritius"], "at": C("Mauritius", 0.3), "dur": 1.4, "color": "accent", "tokenShape": "box", "lift": 0.2}],
    "caption": "Real locations (Natural Earth) · arrow is schematic"},
    sources=["afnic_2025", "natural_earth"], assets=GEO)
stage("s38_save", "m5_save", {
    "zones": [BEACH()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.1}, {"at": C("cut its debt"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("piggy", x=700, at=0.2, text="SAVINGS", scale=1.1),
              it("coins", **{"from": [960, -100], "to": [700, 620]}, at=0.6, rate=4),
              it("stack", x=1350, at=0.3, h=[[0, 480], [{"cue": "cut its debt"}, 480], [{"cue": "cut its debt", "offset": 3}, 200]], text="DEBT", color="#FFCDD2")],
    "callouts": [co("2025 surplus ≈ {{surplus_2025.display}}", 960, 150, C("surplus"), "green", screen=True, size=42, sub="converted at EC$2.70 = US$1", until=C("cut its debt", -0.3)),
                 co("Debt cut with .ai money", 960, 150, C("cut its debt"), "gold", screen=True, size=42)]},
    sources=["focus_budget_2026", "eccb_peg"])
# ---- PRESENTER D: the choice
add("p39_choice", "m5_draw", "engine_draw", {
    "title": "The windfall choice", "board": BOARD, "draw_start": C("On one side"), "speed": 1300,
    "enter": {"from": 2200, "to": 1600, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(860, 300, 340, 120), "color": "accent", "width": 6, "start": C("the choice"), "label": lbl(".ai WINDFALL", 1030, 370, 34, "accent")},
        {"d": arrow((900, 430), (680, 600), -0.1), "color": "risk", "width": 5, "start": C("On one side")},
        {"d": rect(500, 610, 320, 120), "color": "risk", "width": 5, "start": C("spend the windfall"), "label": lbl("SPEND IT ALL", 660, 680, 30, "risk")},
        {"d": arrow((1160, 430), (1380, 600), 0.1), "color": "accent3", "width": 5, "start": C("On the"), "kind": "arrow"},
        {"d": rect(1240, 610, 360, 120), "color": "accent3", "width": 5, "start": C("save part"), "label": lbl("SAVE + INVEST", 1420, 680, 30, "accent3")},
        {"d": "M 1260 900 L 1260 820 L 1330 820 L 1330 900 M 1360 900 L 1360 780 L 1430 780 L 1430 900 M 1460 900 L 1460 750 L 1530 750 L 1530 900", "color": "accent3", "width": 4,
         "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("airport, roads"), "label": lbl("airport · roads · health · a cushion", 1400, 950, 22, "ink")},
    ],
    "actions": [{"kind": "explain", "at": C("On one side", 0.3), "dur": 2.5}, {"kind": "point", "at": C("a cushion", 0.2), "dur": 1.4, "target": [1420, 800]}],
    "scale": 0.86, "floor": 1040})

# ====================================================================== PAYOFF
stage("s40_payoff", "payoff", {
    "zones": [Z("web", -1600, 1400), BEACH(1400, 5000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 2200, "y": 520, "zoom": 1.1}, {"at": C("every time someone"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.6},
            {"at": C("travels across"), "x": 1700, "y": 500, "zoom": 0.8, "dur": 3.0}, {"at": C("The lesson"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("sign", x=1900, y=330, text="NO AI INVENTED", at=C("didn't invent"), until=C("every time someone"), color="#FFCDD2", size=30),
              it("sign", x=2500, y=430, text="NO DATA CENTER", at=C("data center"), until=C("every time someone"), color="#FFCDD2", size=30),
              it("letters", x=2200, y=330, text=".ai", at=C("right two letters"), size=200, color="gold"),
              it("browser", x=700, y=420, at=C("every time someone"), url="next-big-thing.ai", typeAt=C("names a new"), scale=0.8),
              it("coins", **{"from": [900, 400], "to": [2300, 700]}, at=C("travels across"), rate=4, arc=300),
              it("piggy", x=2000, at=C("spend it"), text="SAVE", scale=0.8), it("stack", x=2450, at=C("spend it", 0.4), h=260, text="SPEND"),
              it("counter", x=2200, y=280, at=C("more than a million"), steps=[[0, 0], [{"cue": "more than a million"}, 0], [{"cue": "more than a million", "offset": 2.5}, 1000000]], prefix="", suffix="+ names")],
    "callouts": [co("Right letters, right moment", 960, 150, C("right two letters"), "gold", screen=True, until=C("every time someone", -0.3)),
                 co("Spend it, or make it last?", 960, 150, C("spend it"), "green", screen=True, size=44)]},
    sources=["gleaner_2026"])
add("s41_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})

for s in scenes:
    d = s["params"].pop("coasts_dark", None)
    if d is not None:
        s["params"].setdefault("coasts", {})["darkAt"] = d
OUT.write_text("# GENERATED by tools/gen_anguilla_storyboard.py; edit the generator, not this file.\n"
               "# Episode 10 storyboard: cartoon-first. The channel intro is inserted automatically after the hook.\n"
               + yaml.safe_dump({"scenes": scenes}, sort_keys=False, allow_unicode=True, width=200))
print(f"{len(scenes)} scenes -> {OUT}")
