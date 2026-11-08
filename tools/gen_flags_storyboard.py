"""Generates projects/why-ships-fly-foreign-flags/deliverables/documentary/storyboard.yaml (Episode 11).

Bespoke CartoonStage worlds: a container port with gantry cranes, a 1920s ship saloon, the Suez canal, a registry
office with stamps, the ship's passport, a rolling crew cabin at night. Ships carry TEXT pennants (country names as
labels, never real flag designs) that can switch mid-scene; abandoned ships rust and their crews turn sad. Five parts, internal only.
Run: python tools/gen_flags_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-ships-fly-foreign-flags/deliverables/documentary/storyboard.yaml"
LL = {"athens": [23.7, 37.98], "shanghai": [121.47, 31.23], "tokyo": [139.7, 35.7], "monrovia": [-10.8, 6.3],
      "panama": [-79.5, 8.98], "majuro": [171.38, 7.09], "virginia": [-77.45, 38.95], "suez": [32.55, 29.97]}
FLAGS3 = ["LIBERIA", "PANAMA", "MARSHALL IS."]

F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
PORT = lambda x0=-1600, x1=4600, **kw: Z("port", x0, x1, **kw)


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 1, "skin": k, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


# ====================================================================== HOOK
stage("s01_ships", "h_question", {
    "zones": [PORT()], "worldW": 2400,
    "cam": [{"at": 0, "x": 1500, "y": 520, "zoom": 1.1}, {"at": C("registered"), "x": 1200, "y": 500, "zoom": 0.9, "dur": 3.0},
            {"at": C("choice of flag"), "x": 1000, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 0,
    "items": [it("ship", x=[[0, 2700], [20, 1300]], flag="LIBERIA", flip=True, crew=3),
              it("ship", x=[[0, 3600], [24, 2300]], flag="PANAMA", flip=True, type="tanker", scale=0.8),
              it("ship", x=[[0, 1300], [24, 200]], flag="MARSHALL IS.", flip=True, scale=0.75),
              it("sign", x=600, y=330, text="RULES ON BOARD", at=C("the rules on board"), color="#FFF59D", size=30, hang=True, swing=True),
              it("sign", x=1000, y=250, text="TAXES", at=C("the taxes"), color="#FFF59D", size=30, hang=True, swing=True),
              it("sign", x=1400, y=330, text="WHO PROTECTS THE CREW?", at=C("protects the crew"), color="#FFCDD2", size=30, hang=True, swing=True)],
    "callouts": [co("your phone · your clothes · your coffee", 960, 960, C("your phone"), "white", screen=True, size=36),
                 co("Registered… where?", 960, 150, C("registered"), "gold", screen=True, size=44, until=C("choice of flag", -0.4))]},
    sfx=[{"kind": "hit", "cue": "registered", "gain": 0.3}])
add("s02_share", "h_stakes", "engine_chart", {"chart": "donut", "cx": 960, "cy": 600, "r": 250, "thick": 90, "start": C("just three flags"),
    "data": [{"label": "Liberia · Panama · Marshall Islands", "value": 45.1, "display": "45.1%"}, {"label": "every other flag", "value": 54.9, "display": "54.9%"}],
    "center": "{{top3.display}}", "centerSub": "of world shipping capacity (1 Jan 2025)",
    "title": "Three flags", "subtitle": "biggest owners: Greece · China · Japan (UNCTAD)"},
    sources=["unctad_2025"])

# ====================================================================== PART 1: whose ship is it
card("s03_c1", "m1_card", "Whose Ship Is It?", "One ship, many countries")
stage("s04_q1", "m1_question", {"min_seconds": 9.0,
    "zones": [PORT()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.2}, {"at": C("stranger"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("ship", x=1050, flag="?", flip=True, crew=2),
              it("letters", x=960, y=200, text="?", at=C("Whose ship"), size=150, color="gold"),
              it("sign", x=420, y=420, text="OWNER?", at=C("really"), size=30), it("sign", x=960, y=420, text="FLAG?", at=C("really", 0.3), size=30),
              it("sign", x=1500, y=420, text="CREW?", at=C("really", 0.6), size=30)],
    "callouts": [co("Whose ship is it?", 960, 150, C("Whose ship"), "gold", screen=True, size=48, until=C("stranger", -0.3)),
                 co("Stranger than you think", 960, 150, C("stranger"), "white", screen=True, size=44)]})
# ---- PRESENTER A: the flag is a passport
add("p05_flag", "m1_flag", "engine_draw", {
    "title": "A flag is a ship's passport", "board": BOARD, "draw_start": C("Every ship"), "speed": 1300,
    "enter": {"from": -260, "to": 430, "at": C("Every ship", -0.6), "dur": 1.3},
    "strokes": [
        {"d": "M 600 560 L 1000 560 L 950 640 L 640 640 Z", "color": "accent2", "width": 6, "start": C("Every ship"), "kind": "box", "label": lbl("SHIP", 800, 610, 30, "accent2")},
        {"d": rect(700, 380, 160, 120), "color": "accent", "width": 5, "start": C("flag state"), "label": lbl("FLAG", 780, 450, 30, "accent")},
        {"d": arrow((1010, 520), (1240, 380), -0.1), "color": "ink", "width": 4, "start": C("decides")},
        {"d": rect(1250, 330, 420, 90), "color": "accent3", "width": 5, "start": C("safety rules"), "label": lbl("SAFETY RULES", 1460, 388, 30, "accent3")},
        {"d": arrow((1010, 590), (1240, 520)), "color": "ink", "width": 4, "start": C("labor rules", -0.3)},
        {"d": rect(1250, 470, 420, 90), "color": "accent3", "width": 5, "start": C("labor rules"), "label": lbl("LABOR RULES", 1460, 528, 30, "accent3")},
        {"d": arrow((1010, 640), (1240, 660), 0.1), "color": "ink", "width": 4, "start": C("and taxes", -0.3)},
        {"d": rect(1250, 610, 420, 90), "color": "accent", "width": 5, "start": C("and taxes"), "label": lbl("TAXES", 1460, 668, 30, "accent")},
        {"d": dot(800, 760), "color": "ink", "width": 1, "start": C("passport"), "label": lbl("= THE SHIP'S PASSPORT", 800, 760, 34, "risk")},
    ],
    "push": 0.004, "actions": [{"kind": "point", "at": C("passport", 0.2), "dur": 1.4, "target": [800, 610]}, {"kind": "smile", "at": C("passport", 1.6), "dur": 1.5},
                {"kind": "walk", "at": C("In theory"), "dur": 1.4, "to": 1780}, {"kind": "explain", "at": C("make sure"), "dur": 2.5}, {"kind": "point", "at": C("wherever it sails"), "dur": 1.4, "target": [1460, 520]}],
    "scale": 0.86, "floor": 1040})
stage("s06_evergiven", "m1_evergiven", {
    "zones": [Z("canal")], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("One ship"), "x": 1350, "y": 500, "zoom": 0.9, "dur": 2.4}], "drift": 0,
    "items": [it("ship", x=900, flag=[[0, ""], [{"cue": "flagged in"}, "PANAMA"]], name="EVER GIVEN", scale=1.0, smoke=False, crew=2),
              it("sign", x=330, y=300, text="OWNER: JAPAN", at=C("Japanese company"), size=30),
              it("sign", x=780, y=220, text="OPERATOR: TAIWAN", at=C("Taiwanese"), size=30),
              it("sign", x=1250, y=300, text="FLAG: PANAMA", at=C("flagged in"), color="#FFF59D", size=30),
              it("sign", x=1700, y=740, text="STUCK IN: EGYPT", at=C("stuck in Egypt"), color="#FFCDD2", size=30, post=True),
              it("passport", x=2000, y=420, at=C("One ship", -0.4), openAt=C("One ship"), scale=0.8,
                 fields=[["SHIP", "EVER GIVEN"], ["OWNER", "Japan"], ["OPERATOR", "Taiwan"], ["FLAG", "Panama"], ["STUCK IN", "Egypt"]])],
    "callouts": [co("Suez Canal, 2021", 960, 150, C("Suez Canal"), "white", screen=True, until=C("One ship", -0.3)),
                 co("One ship, four countries", 960, 150, C("One ship"), "green", screen=True, size=44, until=C("morass", -0.4)),
                 co("“An international morass”", 960, 150, C("morass"), "gold", screen=True, sub="Associated Press")]},
    sources=["ap_evergiven"])
add("s07_map", "m1_owners", "engine_map", {
    "title": "Who owns the ships · whose flags they fly", "subtitle": "Greece owns {{owners.display}} of capacity · Asian owners {{regs_2026.asia_display}} · European {{regs_2026.europe_display}}",
    "cameras": [{"at": 0, "lon": 60, "lat": 30, "span": 200}, {"at": C("look at the flags"), "lon": 20, "lat": 15, "span": 330, "dur": 3.0}],
    "drift": {"lon": 0.2, "zoom": 0.003}, "tilt": [[0, 12], [20, 5]],
    "highlights": [{"iso": "GRC", "color": "accent2", "at": C("Greek owners")}, {"iso": "CHN", "color": "accent2", "at": C("Asian companies")}, {"iso": "JPN", "color": "accent2", "at": C("Asian companies", 0.3)},
                   {"iso": "LBR", "color": "accent", "at": C("look at the flags")}, {"iso": "PAN", "color": "accent", "at": C("look at the flags", 0.3)}, {"iso": "MHL", "color": "accent", "at": C("look at the flags", 0.6)}],
    "hubs": [{"id": "g", "at": LL["athens"], "label": "Greece", "sub": "owners", "color": "accent2", "time": C("Greek owners")},
             {"id": "c", "at": LL["shanghai"], "label": "China", "sub": "owners", "color": "accent2", "time": C("Asian companies")},
             {"id": "j", "at": LL["tokyo"], "label": "Japan", "sub": "owners", "color": "accent2", "time": C("Asian companies", 0.3)},
             {"id": "l", "at": LL["monrovia"], "label": "Liberia", "sub": "flag", "color": "accent", "time": C("look at the flags")},
             {"id": "p", "at": LL["panama"], "label": "Panama", "sub": "flag", "color": "accent", "time": C("look at the flags", 0.3), "anchor": "end"},
             {"id": "m", "at": LL["majuro"], "label": "Marshall Islands", "sub": "flag", "color": "accent", "time": C("look at the flags", 0.6)}],
    "routes": [{"from": LL["athens"], "to": LL["monrovia"], "at": C("small countries"), "dur": 1.2, "color": "accent", "tokenShape": "box", "lift": 0.2},
               {"from": LL["shanghai"], "to": LL["majuro"], "at": C("small countries", 0.4), "dur": 1.2, "color": "accent", "tokenShape": "box", "lift": 0.2},
               {"from": LL["tokyo"], "to": LL["panama"], "at": C("small countries", 0.8), "dur": 1.6, "color": "accent", "tokenShape": "box", "lift": 0.15}],
    "caption": "Real locations (Natural Earth) · arrows are schematic"},
    sources=["unctad_2025", "unctadstat_2026", "natural_earth"], assets=GEO)
kinetic("s08_t1", "m1_transition", [("How did a few small countries", 54, "So how", None, True), ("end up flying the world's fleet?", 64, "flying the world", "accent", False),
                                    ("It started with a drink", 44, "with a drink", "accent2", True)])

# ====================================================================== PART 2: how it started
card("s09_c2", "m2_card", "How It Started", "A drink, a war and an office in Virginia")
stage("s10_q2", "m2_question", {"min_seconds": 9.0,
    "zones": [PORT()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.15}, {"at": 4, "x": 960, "y": 520, "zoom": 1.0, "dur": 3}], "drift": 0,
    "items": [it("ship", x=1000, flag=[[0, "MY OWN FLAG"], [{"cue": "borrowing"}, "BORROWED?"]], flip=True, crew=2),
              it("letters", x=1500, y=260, text="?", at=C("borrowing", 0.5), size=130, color="gold")],
    "callouts": [co("Borrow another country's flag?", 960, 150, C("borrowing"), "gold", screen=True, size=44)]})
stage("s11_prohibition", "m2_prohibition", {
    "zones": [Z("saloon", -1600, 1700), PORT(1700, 6000)], "worldW": 3600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("registered their ships"), "x": 2600, "y": 520, "zoom": 1.0, "dur": 2.6},
            {"at": C("more and more owners"), "x": 2700, "y": 500, "zoom": 0.85, "dur": 2.6}], "drift": 0,
    "items": [it("sign", x=900, y=240, text="1920s · U.S.: ALCOHOL BANNED", at=C("alcohol was banned"), color="#FFCDD2", size=34, hang=True, swing=True),
              *crowd([500, 700, 1100, 1300], "cheer", at=C("serve drinks"), until=C("registered their ships", 1.0), scale=0.9),
              it("ship", x=2500, type="liner", flag=[[0, "U.S."], [{"cue": "registered their ships", "offset": 0.6}, "PANAMA"]], flip=True, crew=3),
              it("ship", x=[[0, 4200], [{"cue": "more and more owners"}, 4200], [{"cue": "more and more owners", "offset": 5}, 3300]], flag="PANAMA", flip=True, scale=0.7, at=C("more and more owners")),
              it("sign", x=2500, y=200, text="THE FIRST OPEN REGISTRY", sub="any owner, from any country", at=C("first open registry"), color="#C8E6C9", size=32)],
    "callouts": [co("Drinks on board!", 960, 150, C("serve drinks"), "gold", screen=True, until=C("registered their ships", -0.3)),
                 co("Re-registered in Panama", 960, 150, C("registered their ships"), "white", screen=True, until=C("first open registry", -0.3)),
                 co("Panama: the first open registry", 960, 960, C("first open registry"), "green", screen=True, sub="Windward")]},
    sources=["windward_foc"])
add("s12_liberia", "m2_liberia", "engine_map", {
    "title": "From Panama to Liberia", "subtitle": "a new registry opened with Liberia's government in 1948",
    "cameras": [{"at": 0, "lon": -70, "lat": 15, "span": 100}, {"at": C("government of Liberia"), "lon": -40, "lat": 20, "span": 120, "dur": 2.6}],
    "drift": {"lon": 0.1, "zoom": 0.004}, "tilt": [[0, 12], [20, 5]],
    "highlights": [{"iso": "PAN", "color": "risk", "at": C("private payments")}, {"iso": "LBR", "color": "accent", "at": C("government of Liberia")}],
    "hubs": [{"id": "p", "at": LL["panama"], "label": "Panama", "sub": "private payments demanded (Carlisle)", "color": "risk", "time": C("Panama's officials"), "anchor": "end"},
             {"id": "l", "at": LL["monrovia"], "label": "Liberia", "sub": "{{liberia_1948.display}} · Edward Stettinius", "color": "accent", "time": C("government of Liberia")},
             {"id": "v", "at": LL["virginia"], "label": "Virginia, U.S.", "sub": "where the registry is run today", "color": "accent2", "time": C("Virginia")}],
    "routes": [{"from": LL["panama"], "to": LL["monrovia"], "at": C("an alternative"), "dur": 1.6, "color": "accent", "tokenShape": "box", "lift": 0.2},
               {"from": LL["virginia"], "to": LL["monrovia"], "at": C("Virginia", 0.4), "dur": 1.4, "color": "accent2", "tokenShape": "packet", "lift": 0.18}],
    "caption": "Real locations (Natural Earth) · arrows are schematic"},
    sources=["carlisle_1980", "windward_foc", "natural_earth"], assets=GEO)
kinetic("s13_term", "m2_term", [("1950s: a new name", 44, "nineteen fifties", "muted", True), ("“Flag of convenience”", 88, "calling it", "accent", False),
                                ("chosen not for where the ship comes from, but for what it saves", 36, "not for where", None, True)])
# ---- PRESENTER B: how an open registry works
add("p14_registry", "m2_draw", "engine_draw", {
    "title": "How an open registry works", "board": BOARD, "draw_start": C("A ship owner"), "speed": 1400,
    "enter": {"from": 2200, "to": 1620, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(520, 330, 300, 110), "color": "accent2", "width": 5, "start": C("A ship owner"), "label": lbl("SHIP OWNER", 670, 395, 30, "accent2")},
        {"d": dot(670, 470), "color": "muted", "width": 1, "start": C("Athens"), "label": lbl("Athens · Shanghai · Tokyo", 670, 470, 22, "muted")},
        {"d": arrow((830, 385), (960, 385)), "color": "ink", "width": 4, "start": C("picks a flag")},
        {"d": rect(970, 300, 300, 200), "color": "accent", "width": 5, "start": C("from a menu"), "label": lbl("FLAG MENU", 1120, 340, 26, "accent")},
        {"d": dot(1120, 400), "color": "ink", "width": 1, "start": C("from a menu", 0.3), "label": lbl("LIBERIA  ·  PANAMA", 1120, 400, 22, "ink")},
        {"d": dot(1120, 440), "color": "ink", "width": 1, "start": C("from a menu", 0.6), "label": lbl("MARSHALL IS.  ·  …", 1120, 440, 22, "ink")},
        {"d": arrow((1120, 510), (1120, 600)), "color": "ink", "width": 4, "start": C("The registry")},
        {"d": rect(930, 610, 380, 120), "color": "accent3", "width": 5, "start": C("private company"), "label": lbl("REGISTRY COMPANY", 1120, 678, 28, "accent3")},
        {"d": arrow((920, 690), (760, 820), 0.06), "color": "accent", "width": 5, "start": C("sends part")},
        {"d": rect(470, 820, 360, 110), "color": "accent", "width": 5, "start": C("to the government"), "label": lbl("FLAG GOVERNMENT", 650, 885, 28, "accent")},
        {"d": dot(1120, 800), "color": "risk", "width": 1, "start": C("never has to visit"), "label": lbl("the ship never visits", 1120, 800, 26, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("never has to visit", 0.4), "dur": 1.4, "target": [1120, 790]}],
    "scale": 0.86, "floor": 1040}, sources=["windward_foc", "allafrica_2026"])
kinetic("s15_t2", "m2_transition", [("A flag you choose like a product", 58, "A flag you can choose", None, True), ("Why a faraway flag?", 80, "faraway flag", "accent", False)])

# ====================================================================== PART 3: why owners do it
card("s16_c3", "m3_card", "Why Owners Do It", "Lighter rules, lower costs")
stage("s17_q3", "m3_question", {"min_seconds": 9.0,
    "zones": [Z("office")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.15}, {"at": C("in return"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [*crowd([480], "point", at=0.2, tie=True), it("sign", x=480, y=470, text="SHIP OWNER", at=0.4, size=26),
              it("docs", x=960, y=F, at=0.5, text="REGISTRATION", stampAt=C("actually gain"), stamp="REGISTERED", color="green"),
              *crowd([1440], "read", at=0.3, glasses=True, hair=3), it("sign", x=1440, y=470, text="SMALL COUNTRY", at=C("small country"), size=26),
              it("coins", **{"from": [520, 560], "to": [1400, 560]}, at=C("in return"), rate=4)],
    "callouts": [co("What does the owner gain?", 960, 150, C("actually gain"), "gold", screen=True, size=42, until=C("in return", -0.3)),
                 co("…and the small country?", 960, 150, C("in return"), "white", screen=True, size=42)]})
stage("s18_reasons", "m3_reasons", {
    "zones": [PORT(x1=1900), Z("office", 1900, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("Panama, for example"), "x": 2500, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("ship", x=1000, flag="FLAG OF CONVENIENCE", flip=True, crew=2, scale=0.9),
              it("sign", x=330, y=430, text="FEWER RULES", at=C("stricter rules"), color="#C8E6C9", size=30, hang=True, swing=True),
              it("sign", x=760, y=520, text="LOWER COSTS", at=C("operating costs"), color="#C8E6C9", size=30, hang=True, swing=True),
              it("sign", x=1200, y=430, text="LOWER TAXES", at=C("high taxes"), color="#C8E6C9", size=30, hang=True, swing=True),
              it("sign", x=1620, y=520, text="WEAKER CREW PROTECTION", at=C("worst cases"), color="#FFCDD2", size=30, hang=True, swing=True),
              it("browser", x=2400, y=420, at=C("Panama, for example"), url="register-a-ship.online", typeAt=C("registration online"), w=600, h=360, page="price", text="REGISTER", sub="online", button="SUBMIT", scale=0.9),
              *crowd([2850, 2960, 3070], "stand", at=C("low-cost crews"), scale=0.7, hat="#1E3A6E")],
    "callouts": [co("Why owners choose it", 960, 150, C("According to"), "white", screen=True, sub="Windward", until=C("Panama, for example", -0.3)),
                 co("Panama: register online, hire low-cost crews", 960, 150, C("Panama, for example"), "white", screen=True, sub="Windward")]},
    sources=["windward_foc"])
stage("s19_scale", "m3_scale", {
    "zones": [PORT()], "worldW": 2600,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("Liberia alone"), "x": 1500, "y": 480, "zoom": 0.85, "dur": 2.6}], "drift": 0,
    "items": [it("ship", x=[[0, 2900], [14, 600]], flag="LIBERIA", flip=True, scale=0.8),
              it("ship", x=[[0, 3800], [20, 1500]], flag="LIBERIA", flip=True, type="tanker", scale=0.7),
              it("ship", x=[[0, 4800], [26, 2400]], flag="LIBERIA", flip=True, scale=0.75),
              it("counter", x=960, y=260, at=C("first registry"), steps=[[0, 0], [{"cue": "flying its flag", "offset": -0.5}, 0], [{"cue": "flying its flag", "offset": 2}, 6092]], suffix=" ships", text="flying Liberia's flag, 2026 (IHS)"),
              it("sign", x=1900, y=280, text="{{top3.liberia_display}} OF WORLD CAPACITY", sub="Liberia alone (UNCTAD)", at=C("Liberia alone"), color="#FFF59D", size=30),
              it("sign", x=1900, y=480, text="≈ A QUARTER OF CONTAINER SHIPS", sub="the registry's own figure: {{liberia_new.container_display}}", at=C("container ships"), color="#BBDEFB", size=28)],
    "callouts": [co("2026: first registry ever past {{liberia_2026.display}}", 960, 150, C("first registry"), "gold", screen=True, size=40, until=C("Liberia alone", -0.3))]},
    sources=["fpa_2026", "unctad_2025", "liscr_2026"])
stage("s20_money", "m3_money", {
    "zones": [Z("office", -1600, 1500), PORT(1500, 6000)], "worldW": 3400,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("tiny slice"), "x": 2300, "y": 500, "zoom": 0.85, "dur": 2.8},
            {"at": C("exactly how much"), "x": 800, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("docs", x=500, y=F, at=0.3, text="FEES · TONNAGE TAX", stampAt=C("inspections"), stamp="PAID", color="green", scale=0.8),
              it("stack", x=1050, at=C("maritime revenue"), h=[[0, 20], [{"cue": "maritime revenue"}, 20], [{"cue": "maritime revenue", "offset": 2}, 110]], text="{{liberia_rev.display}}", sub="a year (researcher's estimate)", color="gold"),
              it("ship", x=2400, flag="LIBERIA", flip=True, scale=1.15, crew=2),
              it("sign", x=2400, y=180, text="THE WORLD'S TRADE", at=C("carries the world"), color="#BBDEFB", size=32),
              it("sign", x=700, y=300, text="FULL RECORDS?", sub="only the registry + the maritime authority", at=C("full records"), color="#FFCDD2", size=34)],
    "callouts": [co("Fees · tonnage taxes · inspections", 960, 150, C("Registration fees"), "white", screen=True, until=C("maritime revenue", -0.3)),
                 co("{{liberia_rev.display}} a year", 960, 150, C("maritime revenue"), "gold", screen=True, size=46, sub="researcher's estimate, 2026 (AllAfrica)", until=C("tiny slice", -0.3)),
                 co("A tiny slice of world shipping", 960, 150, C("tiny slice"), "risk", screen=True, until=C("exactly how much", -0.3)),
                 co("He calls for more transparency", 960, 150, C("transparency"), "white", screen=True)]},
    sources=["allafrica_2026"])
kinetic("s21_t3", "m3_transition", [("Cheaper · simpler · lighter rules", 52, "Cheaper", None, True), ("Who is responsible at sea?", 74, "who is responsible", "risk", False)])

# ====================================================================== PART 4: the dark side
card("s22_c4", "m4_card", "The Dark Side", "Abandoned crews and false flags")
stage("s23_q4", "m4_question", {"min_seconds": 9.0,
    "zones": [Z("cabin", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.15}, {"at": C("On paper"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [*crowd([500, 640, 1300], "worry", at=0.3, hat="#1E3A6E", scale=0.95),
              it("sign", x=960, y=260, text="OWNER: ???", at=C("disappears"), color="#FFCDD2", size=40, hang=True, swing=True),
              it("sign", x=960, y=430, text="FLAG STATE: ON PAPER", at=C("On paper"), color="#FFF59D", size=28)],
    "callouts": [co("The owner disappears…", 960, 150, C("disappears"), "risk", screen=True, size=44, until=C("In practice", -0.3)),
                 co("In practice, often no one steps in", 960, 150, C("In practice"), "white", screen=True)]})
add("s24_abandon", "m4_abandon", "engine_chart", {"chart": "bar", "box": {"x": 460, "y": 330, "w": 1000, "h": 500}, "start": C("up from"), "stagger": 1.6,
    "title": "Seafarers abandoned by ship owners", "note": "ITF report to the IMO (via gCaptain)",
    "data": [{"label": "2023", "value": 1676, "display": "{{abandon.prev_display}}"}, {"label": "2024", "value": 3133, "display": "{{abandon.display}}"}],
    "highlight": 1, "highlightAt": C("Left on board"), "color": "accent2", "highlightColor": "risk"},
    sources=["itf_2024"])
stage("s25_ships", "m4_ships", {
    "zones": [PORT()], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Each one"), "x": 1300, "y": 540, "zoom": 1.2, "dur": 3.0}], "drift": 0,
    "items": [it("ship", x=700, flag="?", rustAt=0.5, sadAt=0.3, crew=3, smoke=False, scale=0.85),
              it("ship", x=1700, flag="?", rustAt=1.5, sadAt=1.0, crew=2, smoke=False, flip=True, type="tanker", scale=0.8),
              it("counter", x=1200, y=260, at=C("In total"), steps=[[0, 0], [{"cue": "In total"}, 0], [{"cue": "In total", "offset": 2.5}, 312]], suffix=" ships", text="abandoned in 2024 (ITF)"),
              it("calendar", x=330, y=300, at=C("waiting"), pages=[[0, "DAY 1", "STILL WAITING"], [{"cue": "waiting", "offset": 1}, "DAY 90", "STILL WAITING"], [{"cue": "waiting", "offset": 2.2}, "DAY 300", "STILL WAITING"]], scale=0.7)],
    "callouts": [co("{{abandon.ships_display}} ships abandoned in 2024", 960, 960, C("In total"), "risk", screen=True, size=44, until=C("twice as many", -0.3)),
                 co("more than twice 2023", 960, 960, C("twice as many"), "white", screen=True, until=C("Each one", -0.3)),
                 co("Each one: a crew stuck in a foreign port", 960, 960, C("Each one"), "white", screen=True)]},
    sources=["itf_2024"])
add("s26_foc", "m4_foc", "engine_chart", {"chart": "donut", "cx": 960, "cy": 600, "r": 250, "thick": 90, "start": C("abandoned ships were"),
    "data": [{"label": "flag of convenience", "value": 81, "display": "81%"}, {"label": "other flags", "value": 19, "display": "19%"}],
    "center": "{{abandon.foc_display}}", "centerSub": "of abandoned ships, 2024",
    "title": "Abandoned ships and their flags", "subtitle": "most abandonments: Panama (43) · ITF"},
    sources=["itf_2024"])
# ---- PRESENTER C: five countries, no one responsible
add("p27_five", "m4_draw", "engine_draw", {
    "title": "Five countries, no one responsible", "board": BOARD, "draw_start": C("The owner lives"), "speed": 1500,
    "enter": {"from": -260, "to": 420, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 1000 600 L 1300 600 L 1260 660 L 1040 660 Z", "color": "accent2", "width": 6, "kind": "box", "start": C("The owner lives", -0.5), "label": lbl("SHIP", 1150, 640, 26, "accent2")},
        {"d": rect(560, 300, 260, 90), "color": "ink", "width": 4, "start": C("The owner lives"), "label": lbl("1 · OWNER", 690, 357, 26)},
        {"d": rect(1480, 300, 280, 90), "color": "ink", "width": 4, "start": C("legally owns"), "label": lbl("2 · COMPANY", 1620, 357, 26)},
        {"d": rect(1480, 760, 280, 90), "color": "accent", "width": 4, "start": C("The flag"), "label": lbl("3 · FLAG", 1620, 817, 26, "accent")},
        {"d": rect(1010, 800, 280, 90), "color": "ink", "width": 4, "start": C("The crew"), "label": lbl("4 · CREW", 1150, 857, 26)},
        {"d": rect(560, 760, 260, 90), "color": "risk", "width": 4, "start": C("stuck in the port"), "label": lbl("5 · PORT", 690, 817, 26, "risk")},
        {"d": arrow((820, 390), (1010, 590), 0.05), "color": "muted", "width": 3, "start": C("stuck in the port", 0.6)},
        {"d": arrow((1480, 390), (1300, 590), -0.05), "color": "muted", "width": 3, "start": C("stuck in the port", 0.8)},
        {"d": dot(1150, 470), "color": "risk", "width": 1, "start": C("not my problem"), "label": lbl("“NOT MY PROBLEM”", 1150, 470, 40, "risk")},
    ],
    "actions": [{"kind": "explain", "at": C("The crew", 0.3), "dur": 2.0}, {"kind": "react", "at": C("not my problem", 0.3)}],
    "scale": 0.86, "floor": 1040})
stage("s28_false", "m4_falseflags", {
    "zones": [PORT(night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.1}, {"at": C("shadow fleet"), "x": 1400, "y": 500, "zoom": 0.9, "dur": 2.6}], "drift": 0,
    "items": [it("ship", x=[[0, 1300], [30, 800]], type="tanker", flip=True, smoke=False,
                 flag=[[0, "FLAG A"], [{"cue": "not real"}, "NOT REAL"], [{"cue": "dodge sanctions"}, "FLAG B?"], [{"cue": "new homes"}, "FLAG C?"]]),
              it("docs", x=360, y=F, at=C("Researchers"), text="SHIP REGISTER CHECK", stampAt=C("false flag"), stamp="FALSE FLAG", scale=0.8),
              it("ship", x=[[0, 3200], [{"cue": "new homes"}, 3200], [{"cue": "new homes", "offset": 6}, 2000]], type="tanker", flip=True, smoke=False, scale=0.7, flag="NEW HOME?"),
              it("counter", x=1500, y=360, at=C("counted"), steps=[[0, 0], [{"cue": "counted"}, 0], [{"cue": "counted", "offset": 2}, 113]], suffix=" vessels", text="Russian, false flags, Jan–Sep 2025 (CREA)")],
    "callouts": [co("Flags that aren't real", 960, 150, C("not real"), "risk", screen=True, size=44, until=C("counted", -0.3)),
                 co("…often to dodge oil sanctions", 960, 150, C("dodge sanctions"), "white", screen=True, until=C("shadow fleet", -0.3)),
                 co("6 new registries · 162 shadow vessels", 960, 150, C("shadow fleet"), "gold", screen=True, sub="registries that had never flagged a Russian ship before the invasion (CREA)")]},
    sources=["crea_2025"])
kinetic("s29_t4", "m4_transition", [("So why doesn't the world", 56, "So why", None, True), ("simply ban it?", 88, "ban it", "accent", False)])

# ====================================================================== PART 5: why it survives
card("s30_c5", "m5_card", "Why It Survives", "Everyone gains something")
stage("s31_q5", "m5_question", {"min_seconds": 9.0,
    "zones": [PORT()], "worldW": 2200,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.1}, {"at": C("keep growing"), "x": 1100, "y": 500, "zoom": 0.9, "dur": 3}], "drift": 0,
    "items": [it("ship", x=[[0, 2500], [14, 700]], flag="OPEN REGISTRY", flip=True, scale=0.8),
              it("ship", x=[[0, 3400], [{"cue": "keep growing"}, 3400], [{"cue": "keep growing", "offset": 6}, 1700]], flag="OPEN REGISTRY", flip=True, type="tanker", scale=0.7),
              it("sign", x=700, y=260, text="SCANDALS", at=C("so many problems"), color="#FFCDD2", size=34, hang=True, swing=True)],
    "callouts": [co("So many problems…", 960, 150, C("so many problems"), "risk", screen=True, until=C("keep growing", -0.3)),
                 co("…and they keep growing", 960, 150, C("keep growing"), "gold", screen=True, size=44)]})
# ---- PRESENTER D: who gains
add("p32_gains", "m5_everyone", "engine_draw", {
    "title": "Who gains?", "board": BOARD, "draw_start": C("Owners save"), "speed": 1400,
    "enter": {"from": 2200, "to": 1640, "at": C("Because almost", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 560 900 L 1420 900", "color": "border", "width": 4, "start": C("Owners save", -0.4)},
        {"d": "M 620 900 L 620 520 L 800 520 L 800 900", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.35, "kind": "bar", "start": C("Owners save"), "label": lbl("OWNERS SAVE", 710, 495, 26, "accent2")},
        {"d": "M 900 900 L 900 700 L 1080 700 L 1080 900", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.35, "kind": "bar", "start": C("earn fees"), "label": lbl("FLAGS EARN FEES", 990, 675, 26, "accent")},
        {"d": "M 1180 900 L 1180 600 L 1360 600 L 1360 900", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.35, "kind": "bar", "start": C("stays cheap"), "label": lbl("CHEAP SHIPPING", 1270, 575, 26, "accent3")},
        {"d": dot(990, 950), "color": "muted", "width": 1, "start": C("local store"), "label": lbl("schematic, not to scale", 990, 950, 22, "muted")},
        {"d": dot(990, 360), "color": "ink", "width": 1, "start": C("cargo capacity"), "label": lbl("world fleet: {{regs_2026.display}}", 990, 360, 34, "ink")},
    ],
    "push": 0.004, "actions": [{"kind": "point", "at": C("stays cheap", 0.6), "dur": 1.3, "target": [1270, 700]},
                {"kind": "walk", "at": C("Changing that"), "dur": 1.3, "to": 400}, {"kind": "explain", "at": C("less income"), "dur": 2.5}, {"kind": "react", "at": C("higher prices")}],
    "scale": 0.86, "floor": 1040}, sources=["unctadstat_2026"])
stage("s33_quality", "m5_quality", {
    "zones": [Z("office", -1600, 1500), PORT(1500, 6000)], "worldW": 3400,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("abandoned ships tells"), "x": 2400, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("passport", x=700, y=470, at=0.3, openAt=C("newly built", -0.6), stampAt=C("joining its flag"), stamp="NEW SHIP", scale=0.85,
                 fields=[["SHIP", "brand new"], ["FLAG", "Liberia"], ["SHARE OF NEW SHIPS", "{{liberia_new.display}}"]]),
              it("board", x=2400, y=80, w=820, at=C("abandoned ships tells"), text="MOST ABANDONED SHIPS, 2024",
                 rows=[{"name": "PANAMA", "value": "43", "color": "red"}, {"name": "PALAU", "value": "37", "color": "red"}, {"name": "TANZANIA", "value": "30", "color": "red"}, {"name": "COMOROS", "value": "29", "color": "red"}]),
              it("ship", x=2400, flag="?", rust=True, smoke=False, crew=2, sadAt=0, scale=0.6)],
    "callouts": [co("Registries compete to look safe", 960, 150, C("compete hard"), "white", screen=True, until=C("newly built", -0.3)),
                 co("Liberia: {{liberia_new.display}} of new ships", 960, 150, C("newly built"), "green", screen=True, sub="the registry's own figure", until=C("abandoned ships tells", -0.3)),
                 co("Abandonments: a mixed story", 960, 960, C("abandoned ships tells"), "risk", screen=True, sub="ITF, 2024")]},
    sources=["liscr_2026", "itf_2024"])
kinetic("s34_lesson", "m5_lesson", [("Not where a ship is registered", 54, "The real question", None, True), ("but whether anyone is truly responsible", 60, "truly responsible", "accent", False)])

# ====================================================================== PAYOFF
stage("s35_payoff", "payoff", {
    "zones": [PORT()], "worldW": 3000,
    "cam": [{"at": 0, "x": 1500, "y": 500, "zoom": 0.9}, {"at": C("look at the back"), "x": 900, "y": 760, "zoom": 1.5, "dur": 2.6},
            {"at": C("chosen like a product"), "x": 1500, "y": 500, "zoom": 0.85, "dur": 3.0}, {"at": C("who is really"), "x": 1500, "y": 480, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("ship", x=[[0, 1300], [40, 1500]], flag="LIBERIA", port="MONROVIA", scale=1.0, crew=2),
              it("ship", x=[[0, 3600], [{"cue": "chosen like a product"}, 3600], [{"cue": "chosen like a product", "offset": 6}, 2500]], flag="PANAMA", port="PANAMA", flip=True, scale=0.7, type="tanker"),
              it("ship", x=[[0, -800], [{"cue": "chosen like a product"}, -800], [{"cue": "chosen like a product", "offset": 6}, 300]], flag="MARSHALL IS.", port="MAJURO", scale=0.65),
              it("letters", x=1500, y=200, text="?", at=C("who is really"), size=150, color="gold")],
    "callouts": [co("Look at the stern", 960, 150, C("look at the back"), "gold", screen=True, size=44, until=C("Monrovia", -0.2)),
                 co("Monrovia · Panama · Majuro", 960, 150, C("Monrovia"), "white", screen=True, size=44, until=C("chosen like a product", -0.3)),
                 co("A flag chosen like a product", 960, 150, C("chosen like a product"), "green", screen=True, size=44, until=C("Three small flags", -0.3)),
                 co("3 small flags ≈ almost half of capacity", 960, 150, C("Three small flags"), "gold", screen=True, sub="{{top3.display}} (UNCTAD)", until=C("who is really", -0.3)),
                 co("Who is really in charge out there?", 960, 960, C("who is really"), "white", screen=True, size=44)]},
    sources=["unctad_2025"])
add("s36_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})

write(OUT, "# GENERATED by tools/gen_flags_storyboard.py; edit the generator, not this file.\n"
           "# Episode 11 storyboard: cartoon-first. The channel intro is inserted automatically after the hook.\n")
