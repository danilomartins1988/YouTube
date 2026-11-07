"""Generates projects/the-island-getting-rich-from-ai/deliverables/documentary/storyboard.yaml (Episode 10).

Cartoon-first (user decision of 2026-11-06): most beats are engine_cartoon worlds (island, ".ai" letters, coins,
offices, planes, a storm, a piggy bank); presenter boards, charts and maps use the bright cartoon palette of the
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


# ====================================================================== HOOK
cart("s01_island", "h_question", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 420, "zoom": 1.25}, {"at": C("Just two letters"), "x": 1300, "y": 360, "zoom": 1.0, "dur": 2.0}],
    "drift": 0, "actors": [island(), letters(at=C("Just two letters")), coins(2100, -60, [1300, 300], C("Just two letters", 0.8), rate=5)],
    "callouts": [co("No factories", 600, 200, C("No factories"), "risk", until=C("Just two letters")),
                 co("No data centers", 960, 140, C("no data centers"), "risk", until=C("Just two letters")),
                 co("No tech giants", 1320, 200, C("no tech giants"), "risk", until=C("Just two letters"))]},
    sfx=[{"kind": "hit", "cue": "Just two letters", "gain": 0.35}])
add("s02_map", "h_stakes", "engine_map", {
    "title": "Anguilla", "subtitle": "{{island.display}} people · {{rev_2026.display}} from .ai in 7 months of 2026 ({{rev_2026.share_display}} of revenue)",
    "cameras": [{"at": 0, "lon": -40, "lat": 25, "span": 120}, {"at": C("Anguilla"), "lon": -63.05, "lat": 18.3, "span": 9, "dur": 2.6},
                {"at": C("two letters"), "lon": -62.5, "lat": 18.0, "span": 26, "dur": 3.0}, {"at": C("of all the money"), "lon": -63.05, "lat": 18.25, "span": 12, "dur": 3.0}],
    "drift": {"lon": 0.08, "zoom": 0.012}, "tilt": [[0, 14], [10, 4]],
    "highlights": [{"iso": "AIA", "color": "gold", "at": C("Anguilla")}],
    "hubs": [{"id": "a", "at": AXA, "label": "Anguilla", "sub": "British Overseas Territory · 91 km²", "color": "gold", "time": C("a Caribbean island")}],
    "routes": [{"from": [-77.0, 38.9], "to": AXA, "at": C("from two letters"), "dur": 1.4, "color": "accent2", "tokenShape": "coin", "tokens": 8, "tokenEvery": 0.35, "lift": 0.25},
               {"from": [-0.1, 51.5], "to": AXA, "at": C("from two letters", 0.4), "dur": 1.6, "color": "accent2", "tokenShape": "coin", "tokens": 8, "tokenEvery": 0.35, "lift": 0.25},
               {"from": [-122.4, 37.8], "to": AXA, "at": C("from two letters", 0.8), "dur": 1.6, "color": "accent2", "tokenShape": "coin", "tokens": 8, "tokenEvery": 0.35, "lift": 0.25}],
    "caption": "Real location (Natural Earth) · arrows schematic: payments arrive from buyers worldwide"},
    sources=["ap_2024", "gleaner_2026", "natural_earth"], assets=GEO)

# ====================================================================== PART 1: the lucky letters
card("s03_c1", "m1_card", "The Lucky Letters", "How an island got .ai")
cart("s04_q1", "m1_question", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 420, "zoom": 1.15}], "drift": 8,
    "actors": [island(), letters(at=C("most wanted"), color="blue")],
    "callouts": [co("No tech industry?", 1650, 230, C("no tech industry"), "gold", tail=[1420, 300]),
                 co("The most wanted letters online", 960, 860, C("most wanted"), "white", screen=True)]})
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
cart("s06_codes", "m1_codes", {
    "worldW": 2600, "coasts": {"left": True, "right": True, "leftLabel": "BRAZIL", "rightLabel": "JAPAN"},
    "cam": [{"at": 0, "x": 1300, "y": 420, "zoom": 0.75}], "drift": 0,
    "actors": [island(), letters(x=330, y=120, at=C("Brazil is"), size=110, text=".br", color="green"),
               letters(x=2270, y=120, at=C("Japan is"), size=110, text=".jp", color="blue"),
               letters(x=1260, y=150, at=C("Anguilla's"), size=150)],
    "callouts": [co("Every country gets two letters", 960, 960, C("Every country"), "white", screen=True, size=40),
                 co("from its official country code", 960, 1030, C("official code"), "gold", screen=True, size=28)]},
    sfx=[{"kind": "hit", "cue": "And Anguilla's", "gain": 0.3}])
cart("s07_1995", "m1_assigned", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.1}], "drift": 6,
    "actors": [island(), letters(at=0.6, color="grey")],
    "callouts": [co("1995", 700, 180, C("Anguilla was assigned"), "gold", size=60),
                 co("AI = a niche lab idea", 1880, 200, C("niche idea"), "white", until=C("Its official")),
                 co("Worth almost nothing", 1880, 300, C("almost nothing"), "risk", until=C("Its official")),
                 co("Manager: Government of Anguilla", 1880, 250, C("Its official"), "green", sub="IANA delegation record")]},
    sources=["ap_2024", "afnic_2025", "iana_ai"])
cart("s08_cate", "m1_cate", {
    "worldW": 3400, "coasts": {"right": True, "rightLabel": "TAIWAN"},
    "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.0}, {"at": C("company in Taiwan"), "x": 2300, "y": 400, "zoom": 0.85, "dur": 2.2},
            {"at": C("recovered"), "x": 1400, "y": 400, "zoom": 1.0, "dur": 2.0}],
    "drift": 0,
    "actors": [island(), {"kind": "plane", "x": [[0, -400], [{"cue": "moved to the island", "offset": 1.0}, 1100]], "y": 170, "text": "1994", "scale": 0.8},
               {"kind": "letters", "text": ".ai", "y": 150, "at": 0.4, "size": 130,
                "x": [[0, 1260], [{"cue": "company in Taiwan"}, 1260], [{"cue": "company in Taiwan", "offset": 2.0}, 3000], [{"cue": "recovered", "offset": -1.0}, 3000], [{"cue": "recovered", "offset": 1.0}, 1260]]}],
    "callouts": [co("Vince Cate, software developer", 960, 960, C("Vince Cate"), "white", sub="his own account (IEEE Spectrum)", screen=True),
                 co("“Do you want to run .ai?”", 1300, 300, C("whether he wanted"), "gold", until=C("For a while")),
                 co("A company in Taiwan…", 2700, 230, C("company in Taiwan", 1.2), "white", until=C("disappeared", 1.5)),
                 co("…disappeared!", 2700, 330, C("disappeared"), "risk", until=C("recovered")),
                 co("Recovered", 1700, 220, C("recovered", 1.0), "green")]},
    sources=["ieee_2024"])
kinetic("s09_t1", "m1_transition", [("Two letters, given away almost by accident", 50, "Two letters", None, True), ("How do they turn into money?", 76, "turn into money", "accent", False)])

# ====================================================================== PART 2: the money machine
card("s10_c2", "m2_card", "The Money Machine", "Two letters, paid again and again")
cart("s11_q2", "m2_question", {
    "worldW": 2600, "coasts": {"left": True},
    "cam": [{"at": 0, "x": 1000, "y": 420, "zoom": 0.9}], "drift": 10,
    "actors": [office(140, "START-UP", "purple"), office(300, "AI LAB", "blue", scale=0.8), island(x=1700),
               coins(260, 120, [1700, 260], C("Who actually"), rate=3)],
    "callouts": [co("Who pays?", 1000, 160, C("Who actually"), "gold", size=44), co("For two letters?!", 1000, 260, C("two letters"), "white")]})
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
cart("s13_price", "m2_price", {
    "worldW": 2600, "coasts": {"left": True},
    "cam": [{"at": 0, "x": 1100, "y": 420, "zoom": 0.95}, {"at": C("auctioned"), "x": 1500, "y": 400, "zoom": 1.05, "dur": 2.0}], "drift": 6,
    "actors": [office(160, "START-UP", "green"), island(x=1800), coins(260, 120, [1800, 260], C("The price"), rate=2),
               coins(260, 120, [1800, 260], C("auctioned"), rate=8, until=C("auctioned", 3.0))],
    "callouts": [co("{{price.display}} for 2 years", 560, 170, C("costs about"), "gold", size=48, sub="a new .ai name (IMF)", screen=True),
                 co("…then pay again to keep it", 560, 290, C("pay again"), "white", screen=True),
                 co("litigate.ai: {{price.auction_display}}", 1360, 170, C("litigate"), "green", sub="auction, 2023 (IMF)", size=40, screen=True),
                 co("Expired names resold → paid again", 1360, 290, C("expires"), "white", screen=True)]},
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
cart("s15_why", "m2_why", {
    "worldW": 2600, "coasts": {"left": True},
    "cam": [{"at": 0, "x": 500, "y": 330, "zoom": 1.2}, {"at": C("everyone wants"), "x": 1200, "y": 400, "zoom": 0.9, "dur": 2.4}], "drift": 0,
    "actors": [office(180, "yourco.ai", "blue", scale=1.2), office(560, "START-UP", "purple", at=C("so many")), office(800, "NEW APP", "green", at=C("so many", 0.4)),
               island(x=1900), coins(560, 100, [1900, 260], C("everyone wants"), rate=6)],
    "callouts": [co("“We do AI” in two letters", 600, 160, C("two letters"), "gold", size=40), co("A brand", 900, 260, C("like a brand"), "green")]})
cart("s16_manager", "m2_manager", {
    "worldW": 2600, "coasts": {"right": True, "rightLabel": "UNITED STATES"},
    "cam": [{"at": 0, "x": 1100, "y": 420, "zoom": 0.9}], "drift": 12,
    "actors": [island(x=800), office(2300, "IDENTITY DIGITAL", "gold", at=C("Identity")),
               coins(2300, 160, [800, 260], C("more money"), rate=4)],
    "cables": [{"from": 900, "to": 2400, "lightAt": C("run the registry")}],
    "callouts": [co("2024: a U.S. company runs the registry", 1300, 150, C("signed a deal"), "white", sub="Identity Digital (AP)"),
                 co("More money + a safer system", 1300, 260, C("more money"), "green", sub="the government's words")]},
    sources=["ap_2024", "iana_ai"])
kinetic("s17_t2", "m2_transition", [("A small fee, paid again and again", 54, "A small fee", None, True), ("× the AI boom", 96, "multiply", "accent", False)])

# ====================================================================== PART 3: the boom
card("s18_c3", "m3_card", "The Boom", "When the world wanted .ai")
cart("s19_q3", "m3_question", {
    "worldW": 2600, "coasts": {"left": True},
    "cam": [{"at": 0, "x": 900, "y": 420, "zoom": 0.85}], "drift": 14,
    "actors": [office(120 + i * 0, n, c, at=C("chatbots", i * 0.35), scale=0.75) | {"x": 90 + i * 70} for i, (n, c) in enumerate([("BOT", "blue"), ("CHAT", "green"), ("LAB", "purple"), ("APP", "gold")])]
              + [island(x=1900), coins(300, 80, [1900, 260], C("suddenly wanted"), rate=9)],
    "callouts": [co("How big did it get?", 1150, 160, C("How big"), "gold", size=46)]})
add("s20_regs", "m3_regs", "engine_chart", {"chart": "bar", "box": {"x": 300, "y": 330, "w": 1320, "h": 500}, "start": C("In twenty twenty-two"), "stagger": 1.6,
    "title": "Registered .ai names", "note": "IMF (2022, 2023) · official count (Jan 2025) · government announcement (Jan 2026)",
    "data": [{"label": "2022", "value": 144, "display": "{{regs.display}}"}, {"label": "2023", "value": 354, "display": "354,000"},
             {"label": "Jan 2025", "value": 598, "display": "598,007"}, {"label": "Jan 2026", "value": 1000, "display": "1 million+"}],
    "highlight": 3, "highlightAt": C("passed"), "color": "accent2", "highlightColor": "accent"},
    sources=["imf_2024", "dnw_2026"])
cart("s21_cate", "m3_cate", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 420, "zoom": 1.1}], "drift": 0,
    "actors": [island(), office(1200, "REGISTRY", "gold", scale=0.8) | {"y": 314}, coins(2400, -100, [1250, 200], 0.5, rate=7)],
    "callouts": [co("Sales ≈ ×4", 750, 200, C("almost four times"), "green", size=48),
                 co("“about {{cate_sales.display}}”", 1800, 200, C("about 3 million"), "gold", sub="Vince Cate, early 2024 (IEEE Spectrum)", size=40)]},
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
cart("s26_q4", "m4_question", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 380, "zoom": 1.35}], "drift": 0,
    "actors": [island(), coins(2400, -120, [1300, 260], 0.3, rate=4)],
    "callouts": [co("Where does it go?", 1300, 120, C("Where does"), "gold", size=46), co("…and how much per person?", 1300, 210, C("how much"), "white")]})
cart("s27_uses", "m4_uses", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 380, "zoom": 1.0}], "drift": 0,
    "actors": [island(), {"kind": "plane", "x": [[0, 2900], [{"cue": "the airport", "offset": 2.5}, 1500]], "y": 160, "flip": True, "text": "AIRPORT", "scale": 0.8}],
    "callouts": [co("Airport", 600, 150, C("the airport"), "gold"), co("Roads", 600, 250, C("new roads"), "gold"),
                 co("Tax relief", 1950, 150, C("tax relief"), "green"), co("Health services", 1950, 250, C("health services"), "green"),
                 co("Free care for seniors", 1300, 870, C("free medical"), "white", screen=True), co("Debt paid down", 1300, 960, C("pay down debt"), "white", screen=True)]},
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
add("s29_budget", "m4_budget", "compare", {"chapter": "What the money buys", "title": "How big is that?", "sides": [
    {"kicker": "Whole government revenue, 2026 plan", "value": "{{budget_2026.display}}", "label": "converted at EC$2.70 = US$1", "cue": "plans to collect"},
    {"kicker": ".ai alone, Jan–Jul 2026", "value": "{{rev_2026.display}}", "label": "The Gleaner", "cue": "A big part"}]},
    sources=["focus_budget_2026", "gleaner_2026", "eccb_peg"])
cart("s30_tourism", "m4_tourism", {
    "worldW": 3000, "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.0}, {"at": C("second engine"), "x": 1700, "y": 480, "zoom": 0.9, "dur": 2.2}], "drift": 0,
    "actors": [island(darkAt=C("powerful hurricane"), lightAt=C("then by the pandemic", 1.5)),
               {"kind": "plane", "x": [[0, -300], [{"cue": "Tourism makes up", "offset": 3}, 900], [{"cue": "powerful hurricane"}, 900], [{"cue": "powerful hurricane", "offset": 2}, -400]], "y": 160, "text": "TOURISTS", "scale": 0.8},
               {"kind": "storm", "x": [[0, 2300], [{"cue": "powerful hurricane", "offset": 2}, 1400]], "y": 120, "at": C("powerful hurricane"), "until": C("then by the pandemic", 1.5)},
               coins(2900, 300, [1400, 300], C("second engine"), rate=5)],
    "cables": [{"from": 1400, "to": 3200, "lightAt": C("second engine")}],
    "callouts": [co("Tourism = {{tourism.display}} of the economy", 960, 960, C("Tourism makes up"), "gold", screen=True, size=40, sub="IMF"),
                 co("Hurricane, then pandemic", 960, 1040, C("powerful hurricane"), "risk", screen=True, until=C("second engine")),
                 co("A second engine, online", 2100, 230, C("second engine"), "green")]},
    sources=["imf_2024", "ap_2024"], sfx=[{"kind": "hit", "cue": "powerful hurricane", "gain": 0.3}])
kinetic("s31_t4", "m4_transition", [("Money that falls from the sky", 56, "But money", None, True), ("can stop falling", 80, "stop falling", "risk", False)])

# ====================================================================== PART 5: can it last?
card("s32_c5", "m5_card", "Can It Last?", "When the hype cools")
cart("s33_q5", "m5_question", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.1}], "drift": 0, "night": True,
    "actors": [island(), letters(at=0.3, color="grey"), coins(2400, -100, [1300, 260], 0.2, rate=1.5)],
    "callouts": [co("What if the AI boom cools?", 1300, 120, C("What happens"), "gold", size=44)]})
kinetic("s34_quote", "m5_quote", [
    ("“You can't predict how long this", 50, "You can't predict", None, False), ("is going to last.”", 50, "going to last", None, False),
    ("Premier Ellis Webster, 2024 (AP)", 30, "we can't rely", "muted", True),
    ("Expected ≈ {{risk_quote.display}} of revenue → actual {{rev_2026.share_display}} (Jan–Jul 2026)", 38, "shot far higher", "accent", True)], chapter="Can it last")
cart("s35_renew", "m5_renewals", {
    "worldW": 2600, "coasts": {"left": True},
    "cam": [{"at": 0, "x": 1000, "y": 420, "zoom": 0.9}], "drift": 0,
    "actors": [office(140, "START-UP", "purple"), office(300, "AI APP", "green", scale=0.8), island(x=1800),
               coins(260, 120, [1800, 260], 0.2, rate=8, until=C("hype fades")), coins(260, 120, [1800, 260], C("hype fades", 1.0), rate=1.2)],
    "coasts_dark": C("owners stop renewing"),
    "callouts": [co("Renewals = the real test", 1000, 160, C("real test"), "gold", size=44),
                 co("Stop renewing → less money, two years later", 1000, 270, C("owners stop"), "risk"),
                 co("A slow leak?", 1500, 400, C("slow leak"), "white")]})
add("s36_tv", "m5_tv", "engine_map", {
    "title": ".tv · Tuvalu", "subtitle": "a hit with video sites, including Twitch · {{tv_io.display}} names at its peak, now in decline (Afnic)",
    "cameras": [{"at": 0, "lon": -120, "lat": 10, "span": 200}, {"at": C("Tuvalu"), "lon": 179.2, "lat": -8.5, "span": 30, "dur": 2.6},
                {"at": C("Twitch"), "lon": 175, "lat": -6, "span": 60, "dur": 3.0}, {"at": C("in decline"), "lon": 179.2, "lat": -8.5, "span": 22, "dur": 3.0}],
    "drift": {"lon": 0.1, "zoom": 0.012}, "tilt": [[0, 12], [12, 4]],
    "highlights": [{"iso": "TUV", "color": "accent2", "at": C("Tuvalu")}],
    "hubs": [{"id": "t", "at": LL["tuvalu"], "label": "Tuvalu", "sub": ".tv", "color": "accent2", "time": C("owns dot T V")}],
    "routes": [{"from": [-122.4, 37.8], "to": LL["tuvalu"], "at": C("video sites"), "dur": 1.6, "color": "accent2", "tokenShape": "coin", "tokens": 8, "tokenEvery": 0.4, "lift": 0.2},
               {"from": [139.7, 35.7], "to": LL["tuvalu"], "at": C("Twitch"), "dur": 1.4, "color": "accent2", "tokenShape": "coin", "tokens": 6, "tokenEvery": 0.4, "lift": 0.2}],
    "caption": "Real location (Natural Earth, public domain)"},
    sources=["afnic_2025", "theworld_tv", "natural_earth"], assets=GEO)
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
cart("s38_save", "m5_save", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 380, "zoom": 1.1}], "drift": 0,
    "actors": [island(), {"kind": "piggy", "x": 1700, "y": 230, "at": C("saving part"), "scale": 0.9},
               coins(2400, -100, [1700, 200], C("saving part"), rate=5)],
    "callouts": [co("2025 surplus ≈ {{surplus_2025.display}}", 800, 170, C("surplus"), "green", size=42, sub="converted at EC$2.70 = US$1"),
                 co("Debt cut with .ai money", 800, 290, C("cut its debt"), "gold")]},
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
cart("s40_payoff", "payoff", {
    "worldW": 4200, "coasts": {"left": True},
    "cam": [{"at": 0, "x": 2600, "y": 380, "zoom": 1.1}, {"at": C("every time someone"), "x": 600, "y": 400, "zoom": 1.0, "dur": 2.6},
            {"at": C("travels across"), "x": 2300, "y": 380, "zoom": 0.8, "dur": 4.0}, {"at": C("The lesson"), "x": 3300, "y": 380, "zoom": 1.05, "dur": 2.6}],
    "drift": 0,
    "actors": [office(140, "NEW AI CO", "blue"), office(300, "START-UP", "purple", scale=0.8), island(x=3300), letters(x=3260, y=150, at=0.5),
               coins(300, 100, [3300, 260], C("every time someone"), rate=5), {"kind": "piggy", "x": 3650, "y": 230, "at": C("The lesson"), "scale": 0.7},
               {"kind": "whale", "x": [[0, 2600], [40, 1600]], "y": 720, "flip": True}],
    "cables": [{"from": 330, "to": 3100, "lightAt": C("every time someone")}],
    "callouts": [co("No AI invented", 2600, 150, C("didn't invent"), "white", until=C("every time someone")),
                 co("No data center", 2600, 250, C("data center"), "white", until=C("every time someone")),
                 co("Right letters, right moment", 2300, 150, C("right two letters"), "gold", until=C("every time someone")),
                 co("Spend it, or make it last?", 3300, 120, C("spend it"), "green", size=44)]},
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
