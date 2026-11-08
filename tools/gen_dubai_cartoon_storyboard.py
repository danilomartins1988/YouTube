"""Generates projects/how-dubai-really-makes-money/deliverables/documentary/storyboard.yaml (Episode 02, cartoon redo).

Bespoke CartoonStage worlds for Dubai: the modern skyline with a needle-like supertall over the desert and the sea, the
old creek with dhows, wind towers and a souk, the offshore oil field, Jebel Ali's container port, the airport, a
construction site for the migrant workers, the DIFC courtroom, the stock-exchange floor. Four presenter boards explain
oil as seed money, the hub, the tax rules and "the place in between". Maps and charts of the first cut are kept from
tools/data/dubai_storyboard_v1.yaml. Narration and figures are unchanged (the project is currency-exempt, as approved).
Run: python tools/gen_dubai_cartoon_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "projects/how-dubai-really-makes-money/deliverables/documentary/storyboard.yaml"
BASE = {s["id"]: s for s in yaml.safe_load((ROOT / "tools/data/dubai_storyboard_v1.yaml").read_text())["scenes"]}
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
GULF = lambda x0=-1600, x1=4600, **kw: Z("gulf", x0, x1, **kw)
CREEK = lambda x0=-1600, x1=4600, **kw: Z("creek", x0, x1, **kw)
PORT = lambda x0=-1600, x1=4600, **kw: Z("port", x0, x1, **kw)
AIR = lambda x0=-1600, x1=4600, **kw: Z("airport", x0, x1, **kw)
DHOW = lambda x, **kw: it("ship", type="dhow", x=x, scale=kw.pop("scale", 0.5), flag="", smoke=False, **kw)
PLANE = lambda x, y, **kw: it("plane", x=x, y=y, color=kw.pop("color", "#C62828"), scale=kw.pop("scale", 0.6), **kw)

GEO = ["geo:remotion_world", "font:inter"]
LL = {"dubai": [55.27, 25.2], "abudhabi": [54.37, 24.45], "lingeh": [54.88, 26.56], "jebelali": [55.03, 25.01],
      "shanghai": [121.5, 31.2], "rotterdam": [4.1, 51.95], "mombasa": [39.67, -4.05], "mumbai": [72.85, 18.95]}


def emap(id_, seg, params, sources):
    add(id_, seg, "engine_map", params, sources=list(sources) + ["natural_earth"], assets=GEO)


def keep(*ids):
    for i in ids:
        cartoon_kit.scenes.append(BASE[i])


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 1, "skin": k, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def board(id_, seg, title, start, strokes, actions, enter_from=-260, enter_to=430, sources=(), min_s=None):
    p = {"title": title, "board": BOARD, "draw_start": start, "speed": 1400, "push": 0.003,
         "enter": {"from": enter_from, "to": enter_to, "at": 0.2, "dur": 1.3},
         "strokes": strokes, "actions": actions, "scale": 0.86, "floor": 1040}
    if min_s:
        p["min_seconds"] = min_s
    add(id_, seg, "engine_draw", p, sources=sources)


# ====================================================================== OPENING
stage("d01_hook", "open_hook", {
    "zones": [GULF(cx=960)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 380, "zoom": 1.3}, {"at": C("Its own government"), "x": 960, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("sign", x=480, y=330, text="OIL?", at=C("got rich on oil"), until=C("Its own government"), color="#FFCDD2", size=44),
              it("letters", x=1450, y=320, text="{{non_oil_share.display}}", at=C("nothing to do with oil"), size=110, color="gold"),
              it("sign", x=1450, y=470, text="NOT FROM OIL", sub="Dubai government", at=C("nothing to do with oil", 0.3), color="#C8E6C9", size=30),
              it("letters", x=480, y=320, text="?", at=C("where does the money"), size=130, color="gold")],
    "callouts": [co("Most people assume: oil", 960, 150, C("Most people"), "white", screen=True, until=C("Its own government", -0.3)),
                 co("So where does the money come from?", 960, 150, C("where does the money"), "gold", screen=True, size=42)]},
    sources=["dubai_ae_economy"])
stage("d02_puzzle", "open_puzzle", {
    "zones": [AIR(-1600, 1500), GULF(1500, 6000)], "worldW": 2800,
    "cam": [{"at": 0, "x": 2200, "y": 500, "zoom": 1.0}, {"at": C("runs"), "x": 900, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [PLANE([[0, 300], [12, 1800]], [[0, 760], [12, 200]], tilt=-12, at=C("runs")),
              PLANE([[0, -500], [14, 900]], [[0, 300], [14, 700]], tilt=8, flip=False, at=C("runs", 1.5)),
              it("counter", x=900, y=230, at=C("passengers passed", -1.5), steps=[[0, 0], [{"cue": "passengers passed", "offset": -1.5}, 0], [{"cue": "passengers passed", "offset": 1.0}, 95.2]], suffix="m passengers", decimals=1, text="through Dubai's airport, 2025"),
              it("sign", x=2200, y=330, text="{{pop_dubai_2025.display}} PEOPLE", at=C("desert city"), color="#FFF59D", size=32)],
    "callouts": [co("The world's busiest international airport ({{dxb_intl_rank_2025.display}})", 960, 960, C("runs"), "gold", screen=True)]},
    sources=["dmo_dxb_2025", "aci_2025", "wam_population_2025"])
stage("d03_promise", "open_promise", {
    "zones": [PORT(-1600, 1100), AIR(1100, 2300), GULF(2300, 3700), Z("office", 3700, 7000)], "worldW": 4600,
    "cam": [{"at": 0, "x": 2900, "y": 500, "zoom": 1.0}, {"at": C("the ships"), "x": 500, "y": 520, "zoom": 1.0, "dur": 1.6},
            {"at": C("the planes"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 1.6}, {"at": C("the buildings"), "x": 2900, "y": 480, "zoom": 1.0, "dur": 1.6},
            {"at": C("the rules"), "x": 4200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 0,
    "items": [it("ship", x=[[0, 900], [20, 300]], flip=True, scale=0.55, flag="CARGO"),
              PLANE([[0, 1200], [20, 2200]], 300),
              it("docs", x=4200, y=F, at=0.3, text="THE RULES", stampAt=C("the rules", 0.6), stamp="APPROVED", color="green", scale=0.8),
              *crowd([4600], "point", at=C("who pays"), tie=True)],
    "callouts": [co("Something harder to see than oil", 960, 150, C("harder to see"), "gold", screen=True, until=C("the ships", -0.3)),
                 co("Ships · planes · buildings · rules", 960, 150, C("the ships"), "white", screen=True, until=C("who pays", -0.3)),
                 co("…and who pays the bill", 960, 150, C("who pays"), "risk", screen=True)]})
card("d04_act1", "act1_card", "The City That Looks Impossible", "Dubai is not the UAE")
emap("d05_emirates_map", "a1_map", {
    "title": "Dubai is not a country", "subtitle": "one of the {{uae_seven.display}} emirates of the UAE",
    "cameras": [{"at": 0, "lon": 52, "lat": 25, "span": 40}, {"at": C("emirates that form"), "lon": 54.6, "lat": 24.8, "span": 9, "dur": 2.6}],
    "drift": {"lon": 0.05, "zoom": 0.006}, "tilt": [[0, 10], [10, 4]],
    "highlights": [{"iso": "ARE", "color": "accent", "at": C("emirates that form")}],
    "hubs": [{"id": "d", "at": LL["dubai"], "label": "Dubai", "color": "accent", "time": 0.4},
             {"id": "a", "at": LL["abudhabi"], "label": "Abu Dhabi", "sub": "federal capital", "color": "accent2", "time": C("Abu Dhabi"), "anchor": "end"}],
    "caption": "Real locations (Natural Earth) · emirate borders not shown"}, ["uae_constitution"])
stage("d06_oil_split", "a1_oil_split", {
    "zones": [GULF(cx=1700)], "worldW": 2200,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.0}], "drift": 4,
    "items": [it("docs", x=360, y=F, at=C("constitution"), text="UAE CONSTITUTION", stampAt=C("its own natural resources"), stamp="EACH OWNS ITS OWN", color="blue", scale=0.75),
              it("stack", x=900, at=C("Abu Dhabi holds"), h=[[0, 20], [{"cue": "Abu Dhabi holds"}, 20], [{"cue": "Abu Dhabi holds", "offset": 2.5}, 600]], text="ABU DHABI {{reserves_split.display}}", sub="of the UAE's oil reserves", color="#424242"),
              it("stack", x=1350, at=C("Dubai holds"), h=[[0, 20], [{"cue": "Dubai holds"}, 20], [{"cue": "Dubai holds", "offset": 2}, 40]], text="DUBAI {{reserves_split.dubai_display}}", sub="of the reserves", color="gold")],
    "callouts": [co("That difference matters", 960, 150, C("difference matters"), "white", screen=True)]},
    sources=["uae_constitution", "trade_gov_uae_energy"])
stage("d07_question", "a1_question", {
    "zones": [GULF(-1600, 1300, cx=600), CREEK(1300, 6000)], "worldW": 2800,
    "cam": [{"at": 0, "x": 760, "y": 470, "zoom": 1.0}, {"at": C("go back"), "x": 2050, "y": 500, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("sign", x=1100, y=300, text="ANOTHER BUSINESS MODEL", at=C("another business model"), color="#FFF59D", size=30),
              DHOW([[0, 2600], [20, 1800]], flip=True),
              it("calendar", x=2400, y=230, at=C("go back"), pages=[[0, "PAST", "BEFORE THE TOWERS"]], scale=0.6)],
    "callouts": [co("Dubai never had Abu Dhabi's oil wealth", 960, 150, C("never had"), "white", screen=True, until=C("go back", -0.3)),
                 co("Back to before the skyscrapers", 960, 150, C("go back"), "gold", screen=True)]},
    sources=["trade_gov_uae_energy"])
card("d08_act2", "act2_card", "Before the Skyscrapers", "Pearls, merchants and a creek")
stage("d09_creek", "a2_creek", {
    "zones": [CREEK()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.1}], "drift": 6,
    "items": [DHOW([[0, 1500], [20, 700]], flip=True), DHOW([[0, 200], [20, 900]], scale=0.4),
              it("sign", x=960, y=230, text="PEARLS", sub="gathered by divers, sold to distant markets", at=C("pearls"), color="#ECEFF1", size=40),
              it("coins", **{"from": [960, 600], "to": [2200, 200]}, at=C("sold on"), rate=3, shape="note")],
    "callouts": [co("A small trading town on a creek", 960, 960, C("small trading town"), "white", screen=True)]},
    sources=["qdl_pearls"])
stage("d10_pearls", "a2_pearls", {
    "zones": [CREEK()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("chart", x=1200, y=360, w=640, h=360, at=0.3, dur=1.5, text="PEARL TRADE", pts=[0.7, 0.8], crashAt=C("crash")),
              it("calendar", x=380, y=280, at=C("Japan began"), pages=[[0, "1916", "CULTURED PEARLS"], [{"cue": "crash"}, "1929", "THE CRASH"]], scale=0.75),
              DHOW(1500, scale=0.35)],
    "callouts": [co("Then the pearl trade collapsed", 960, 960, C("collapsed"), "risk", screen=True)]},
    sources=["qdl_pearls"])
emap("d11_merchants", "a2_merchants", {
    "title": "Merchants cross the water", "subtitle": "from Lingeh (Persia) to Dubai · {{lingah_shift.display}} (Lorimer's Gazetteer)",
    "cameras": [{"at": 0, "lon": 55, "lat": 26, "span": 14}, {"at": C("merchants moved"), "lon": 55.2, "lat": 25.9, "span": 6, "dur": 2.6}],
    "drift": {"lon": 0.03, "zoom": 0.006}, "tilt": [[0, 8], [10, 3]],
    "hubs": [{"id": "l", "at": LL["lingeh"], "label": "Lingeh", "color": "muted", "time": C("Lingeh")},
             {"id": "d", "at": LL["dubai"], "label": "Dubai", "sub": "openness, not resources", "color": "accent", "time": C("main trading centre")}],
    "routes": [{"from": LL["lingeh"], "to": LL["dubai"], "at": C("merchants moved"), "dur": 2.0, "color": "accent", "tokenShape": "box", "tokens": 20, "tokenEvery": 0.5, "lift": 0.2}],
    "caption": "Real locations (Natural Earth) · route schematic"}, ["qdl_lorimer"])
stage("d12_dredge", "a2_dredge", {
    "zones": [CREEK()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("crane", x=700, text="DREDGING THE CREEK", at=0.2, progress=[[0, 0.2], [20, 0.9]], scale=0.8),
              it("calendar", x=330, y=250, at=0.3, pages=[[0, "{{creek_dredging.display}}", "DREDGING"]], scale=0.7),
              it("sign", x=1400, y=300, text="BORROWED, LARGELY FROM KUWAIT", at=C("Kuwait"), color="#FFF59D", size=28),
              it("ship", x=[[0, 2400], [{"cue": "bigger ships"}, 2400], [{"cue": "bigger ships", "offset": 6}, 1400]], flip=True, scale=0.5, flag="", at=C("bigger ships"))],
    "callouts": [co("Trade infrastructure before any oil", 960, 960, C("before it had found"), "gold", screen=True)]},
    sources=["gulfnews_creek", "gulfnews_oil"])
card("d13_act3", "act3_card", "Oil: The Seed Money", "A small endowment spent on permanence")
stage("d14_offshore", "a3_offshore", {
    "zones": [Z("northsea")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.05}], "drift": 4,
    "items": [it("rig", x=700, at=0.2, drillAt=0.3, strikeAt=C("oil was finally found"), text="FATEH FIELD"),
              it("calendar", x=1500, y=260, at=0.3, pages=[[0, "{{oil_discovery.display}}", "OIL FOUND"], [{"cue": "first cargo"}, "{{oil_first_export.display}}", "FIRST EXPORT"]], scale=0.7),
              it("ship", type="tanker", x=[[0, 1200], [{"cue": "first cargo"}, 1200], [{"cue": "first cargo", "offset": 6}, 2400]], scale=0.5, flag="", at=C("first cargo"))],
    "callouts": [co("Offshore, in the Fateh field", 960, 960, C("Fateh"), "gold", screen=True)]},
    sources=["gulfnews_oil"], sfx=[{"kind": "hit", "cue": "oil was finally found", "gain": 0.3}])
stage("d15_peak", "a3_peak", {
    "zones": [Z("northsea", -1600, 1300), PORT(1300, 6000)], "worldW": 2800,
    "cam": [{"at": 0, "x": 760, "y": 470, "zoom": 1.0}, {"at": C("Jebel Ali"), "x": 2050, "y": 500, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("chart", x=760, y=340, w=600, h=340, at=0.3, dur=4, text="DUBAI OIL OUTPUT (schematic)", pts=[0.1, 0.5, 0.85, 0.7, 0.45, 0.25]),
              it("sign", x=760, y=600, text="PEAK: {{oil_peak.display}}", at=C("peaked"), color="#FFCDD2", size=32),
              it("calendar", x=1650, y=250, at=C("Jebel Ali", -0.5), pages=[[0, "{{jebel_ali_opened.display}}", "JEBEL ALI OPENS"]], scale=0.7),
              it("ship", x=[[0, 3200], [20, 2200]], flip=True, scale=0.55, flag="CARGO", at=C("Jebel Ali"))],
    "callouts": [co("Oil money → roads, a port, a harbour", 960, 150, C("more permanent"), "gold", screen=True)]},
    sources=["gulfnews_oil", "gulfnews_jebelali"])
board("p16_insight", "a3_insight", "Oil was the seed money", C("Oil was not"), [
    {"d": "M 640 700 Q 700 620 760 700 Q 700 760 640 700 Z", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.3, "start": C("Oil was not"), "label": lbl("OIL = SEED", 700, 800, 28, "accent")},
    {"d": "M 700 640 L 700 470 M 700 560 Q 640 520 620 470 M 700 520 Q 760 480 790 440", "color": "accent3", "width": 7, "start": C("seed money")},
    {"d": rect(900, 360, 300, 90), "color": "accent2", "width": 5, "start": C("business built"), "label": lbl("PORTS", 1050, 415, 28, "accent2")},
    {"d": rect(900, 480, 300, 90), "color": "accent2", "width": 5, "start": C("moving other"), "label": lbl("ROADS + PLANES", 1050, 535, 26, "accent2")},
    {"d": rect(900, 600, 300, 90), "color": "accent2", "width": 5, "start": C("people's goods"), "label": lbl("OTHER PEOPLE'S GOODS", 1050, 655, 22, "accent2")},
    {"d": arrow((790, 520), (890, 520)), "color": "ink", "width": 4, "start": C("business built", -0.3)}],
    [{"kind": "point", "at": C("people's goods", 0.3), "dur": 1.3, "target": [1050, 650]}], enter_from=2200, enter_to=1600, min_s=11.0)
card("d17_act4", "act4_card", "The Trading Machine", "Jebel Ali and DP World")
emap("d18_routes", "a4_routes", {
    "title": "The place in between", "subtitle": "Asia's factories · Europe's consumers · East Africa's markets",
    "cameras": [{"at": 0, "lon": 55.3, "lat": 25.2, "span": 20}, {"at": C("factories of Asia"), "lon": 60, "lat": 25, "span": 150, "dur": 3.0}],
    "drift": {"lon": 0.1, "zoom": 0.004}, "tilt": [[0, 10], [14, 4]],
    "hubs": [{"id": "j", "at": LL["jebelali"], "label": "Jebel Ali", "color": "accent", "time": 0.4},
             {"id": "s", "at": LL["shanghai"], "label": "Shanghai", "color": "accent2", "time": C("factories of Asia")},
             {"id": "r", "at": LL["rotterdam"], "label": "Rotterdam", "color": "accent2", "time": C("consumers of Europe")},
             {"id": "m", "at": LL["mombasa"], "label": "Mombasa", "color": "accent2", "time": C("East Africa")},
             {"id": "b", "at": LL["mumbai"], "label": "Mumbai", "color": "accent2", "time": C("shipped on")}],
    "routes": [{"from": LL["shanghai"], "to": LL["jebelali"], "at": C("factories of Asia"), "dur": 2.0, "color": "accent2", "tokenShape": "box", "tokens": 30, "tokenEvery": 0.4, "lift": 0.15},
               {"from": LL["jebelali"], "to": LL["rotterdam"], "at": C("consumers of Europe"), "dur": 2.2, "color": "accent", "tokenShape": "box", "tokens": 30, "tokenEvery": 0.4, "lift": 0.2},
               {"from": LL["jebelali"], "to": LL["mombasa"], "at": C("East Africa"), "dur": 1.6, "color": "accent", "tokenShape": "box", "tokens": 20, "tokenEvery": 0.5, "lift": 0.2},
               {"from": LL["jebelali"], "to": LL["mumbai"], "at": C("shipped on"), "dur": 1.2, "color": "accent", "tokenShape": "box", "tokens": 20, "tokenEvery": 0.5, "lift": 0.2}],
    "caption": "Real locations (Natural Earth) · arrows schematic, not shipping lanes"}, [])
stage("d19_jafza", "a4_jafza", {
    "zones": [PORT()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("counter", x=960, y=230, at=C("It started with"), steps=[[0, 19], [{"cue": "Today it hosts"}, 19], [{"cue": "Today it hosts", "offset": 2.5}, 11000]], suffix=" companies", text="Jebel Ali Free Zone ({{jafza_firms.year_founded}} → today)"),
              it("building", x=420, style="office", color="#FFE0B2", text="FREE ZONE", at=C("Free Zone"), scale=0.6),
              it("ship", x=[[0, 2300], [20, 1300]], flip=True, scale=0.5, flag="CARGO")],
    "callouts": [co("Today: {{jafza_firms.display}} businesses", 960, 960, C("Today it hosts"), "gold", screen=True)]},
    sources=["dmo_jafza_2025"])
stage("d20_trade", "a4_trade", {
    "zones": [PORT()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("stack", x=600, at=C("handled"), h=[[0, 20], [{"cue": "handled"}, 20], [{"cue": "handled", "offset": 2.5}, 380]], text="{{jafza_trade_2024.display}}", sub="non-oil trade, 2024", color="gold"),
              it("letters", x=1350, y=360, text="{{jafza_port_gdp.display}}", at=C("account for"), size=120, color="green"),
              it("sign", x=1350, y=520, text="OF DUBAI'S ECONOMY", sub="zone + port (government estimate)", at=C("account for", 0.3), size=28)],
    "callouts": [co("The zone and the port: a third of the economy", 960, 960, C("account for"), "white", screen=True)]},
    sources=["dmo_jafza_2025"])
stage("d21_port", "a4_port", {
    "zones": [PORT()], "worldW": 2200,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}, {"at": C("busiest container"), "x": 1200, "y": 480, "zoom": 0.92, "dur": 2.4}], "drift": 0,
    "items": [it("ship", x=[[0, 2500], [20, 1100]], flip=True, scale=0.75, flag="JEBEL ALI", crew=2),
              it("counter", x=960, y=230, at=0.4, steps=[[0, 0], [0.6, 0], [3.2, 15.6]], suffix="m TEU", decimals=1, text="containers handled, 2025"),
              it("sign", x=1700, y=330, text="WORLD NO. 9", sub="Lloyd's List", at=C("busiest container"), color="#FFF59D", size=36)]},
    sources=["lloyds_list_dubai", "dmo_dpworld_2025"])
stage("d22_dpworld", "a4_dpworld", {
    "zones": [PORT()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("tower", x=480, text="DP WORLD", color="#1E88E5", at=0.2, scale=0.9),
              it("stack", x=1300, at=C("reported"), h=[[0, 20], [{"cue": "reported"}, 20], [{"cue": "reported", "offset": 2.5}, 420]], text="{{dpworld_revenue_2025.display}}", sub="revenue, 2025", color="gold"),
              it("sign", x=960, y=200, text="GLOBAL · OWNED BY THE DUBAI GOVERNMENT", at=C("global business"), color="#BBDEFB", size=28)],
    "callouts": [co("No longer just Dubai's port operator", 960, 960, C("no longer"), "white", screen=True)]},
    sources=["dmo_dpworld_2025", "dmo_dpworld_delist"])
card("d23_act5", "act5_card", "The Hub Strategy", "Emirates and the airport")
stage("d24_launch", "a5_launch", {
    "zones": [AIR()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 4,
    "items": [PLANE([[0, 300], [10, 1300]], [[0, 760], [10, 300]], tilt=-12, text="1"), PLANE([[0, -300], [12, 900]], [[0, 760], [12, 400]], tilt=-12, text="2", at=1.5),
              it("calendar", x=1550, y=280, at=0.3, pages=[[0, "{{emirates_launch.year}}", "EMIRATES LAUNCHES"]], scale=0.7),
              it("sign", x=1550, y=560, text="{{emirates_launch.display}} + 2 LEASED PLANES", at=C("leased planes"), color="#FFF59D", size=28)],
    "callouts": [co("Aviation followed the same logic", 960, 150, C("same logic"), "white", screen=True)]},
    sources=["gulfnews_emirates_launch"])
board("p25_reach", "a5_reach", "Fly them through, not to", C("The pitch"), [
    {"d": "M 960 560 m -60 0 a 60 60 0 1 0 120 0 a 60 60 0 1 0 -120 0", "color": "accent", "width": 7, "fill": "accent", "fillOpacity": 0.3, "start": C("The pitch"), "label": lbl("DUBAI", 960, 570, 26, "ink")},
    {"d": "M 960 560 m -260 0 a 260 200 0 1 0 520 0 a 260 200 0 1 0 -520 0", "color": "accent2", "width": 4, "dash": "12 10", "start": C("lives within"), "label": lbl("1/3 OF THE WORLD WITHIN 4 H (Dubai's claim)", 960, 330, 24, "accent2")},
    {"d": arrow((560, 400), (900, 540), 0.05), "color": "ink", "width": 4, "start": C("instead of flying")},
    {"d": arrow((1020, 540), (1380, 400), 0.05), "color": "ink", "width": 4, "start": C("through it")},
    {"d": arrow((560, 720), (900, 580), -0.05), "color": "ink", "width": 4, "start": C("through it", 0.3)},
    {"d": arrow((1020, 580), (1380, 720), -0.05), "color": "ink", "width": 4, "start": C("through it", 0.6)},
    {"d": dot(960, 860), "color": "accent", "width": 1, "start": C("through it", 0.9), "label": lbl("A HUB: CHANGE PLANES HERE", 960, 865, 30, "accent")}],
    [{"kind": "point", "at": C("through it", 0.4), "dur": 1.3, "target": [960, 560]}], enter_from=2200, enter_to=1620,
    sources=["invest_dubai_hub"], min_s=12.0)
add("d26_results", "a5_results", "engine_chart", {"chart": "bar", "box": {"x": 360, "y": 330, "w": 1200, "h": 480}, "start": C("Emirates Group made"), "stagger": 1.2,
    "title": "Emirates Group, {{emirates_fy26.year}}", "note": "AED billion · dividend paid to its owner, the Investment Corporation of Dubai",
    "valuePrefix": "AED ", "valueSuffix": "bn", "data": [{"label": "Revenue", "value": 150.5}, {"label": "Profit after tax", "value": 21.0}, {"label": "Dividend to owner", "value": 3.5}],
    "highlight": 1, "highlightAt": C("profit after tax"), "color": "accent2", "highlightColor": "accent"}, sources=["dmo_emirates_2026"])
stage("d27_dwc", "a5_dxb", {
    "zones": [Z("site")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("crane", x=700, text="NEW TERMINAL · AL MAKTOUM", at=0.2, progress=[[0, 0.1], [20, 0.6]], scale=1.0),
              it("counter", x=1350, y=230, at=C("approved"), steps=[[0, 0], [{"cue": "approved"}, 0], [{"cue": "approved", "offset": 2.5}, 128]], prefix="AED ", suffix="bn", text="approved terminal ({{dwc_plan.year}})"),
              it("sign", x=1350, y=520, text="UP TO {{dwc_plan.capacity_display}} PASSENGERS / YEAR", at=C("designed for"), color="#FFF59D", size=28),
              PLANE([[0, 2200], [20, -300]], 180, flip=True)]},
    sources=["dmo_dwc_2024", "dmo_dxb_2025"])
card("d28_act6", "act6_card", "Tourism, Luxury, Real Estate", "The most visible engines")
add("d29_visitors", "a6_visitors", "engine_chart", {"chart": "bar", "box": {"x": 460, "y": 330, "w": 1000, "h": 480}, "start": C("All those flights"), "stagger": 1.0,
    "title": "Overnight visitors to Dubai", "note": "millions per year · hotel occupancy {{visitors_2025.year}}: {{hotel_occupancy_2025.display}}",
    "valueSuffix": "m", "data": [{"label": "2019", "value": 16.73}, {"label": "2024", "value": 18.72}, {"label": "2025", "value": 19.59}],
    "highlight": 2, "highlightAt": C("international overnight"), "color": "accent2", "highlightColor": "accent"}, sources=["dmo_tourism_2025", "wam_tourism_2019"])
stage("d30_property", "a6_property", {
    "zones": [GULF(cx=600)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 450, "zoom": 1.0}], "drift": 4,
    "items": [it("crane", x=1450, text="NEW TOWER", at=0.2, progress=[[0, 0.3], [20, 0.95]], scale=0.9),
              it("counter", x=960, y=200, at=C("were worth"), steps=[[0, 761], [{"cue": "were worth"}, 761], [{"cue": "were worth", "offset": 2.5}, 917]], prefix="AED ", suffix="bn", text="real estate transactions, 2024 → 2025")],
    "callouts": [co("Property: the most visible engine", 960, 960, C("most visible"), "gold", screen=True)]},
    sources=["dmo_realestate_2025", "dld_2024"])
stage("d31_who", "a6_who", {
    "zones": [GULF(cx=500)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.0}], "drift": 4,
    "items": [it("tower", x=1000, text="EMAAR", color="#90A4AE", at=C("Emaar"), scale=0.9),
              it("sign", x=1000, y=160, text="LARGEST SHAREHOLDER: DUBAI HOLDING", sub="a government-owned group", at=C("largest shareholder"), color="#FFF59D", size=26),
              it("coins", **{"from": [1700, 700], "to": [1100, 500]}, at=C("pay cash"), rate=5, shape="note"),
              it("sign", x=1600, y=420, text="{{imf_prices.cash_display}} PAID CASH", sub="no mortgage, 2024 (IMF)", at=C("used no mortgage"), color="#C8E6C9", size=30)],
    "callouts": [co("The state is never far away", 960, 960, C("never far away"), "white", screen=True)]},
    sources=["dmo_emaar_2026", "imf_cr25327"])
stage("d32_prices", "a6_prices", {
    "zones": [GULF(cx=1700)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 450, "zoom": 1.0}], "drift": 4,
    "items": [it("chart", x=900, y=360, w=760, h=400, at=0.3, dur=3, text="VILLA PRICES (IMF)", pts=[0.15, 0.2, 0.35, 0.55, 0.75, 0.92]),
              it("letters", x=900, y=650, text="{{imf_prices.display}}", at=C("villa prices"), size=100, color="green")],
    "callouts": [co("{{imf_prices.period_display}}", 960, 960, C("villa prices"), "white", screen=True)]},
    sources=["imf_cr25327"])
card("d33_act7", "act7_card", "Rules as a Product", "Free zones, finance and tax")
stage("d34_freezones", "a7_freezones", {
    "zones": [Z("office")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("sign", x=480, y=300, text="{{free_zones.display}} FREE ZONES", at=C("free zones"), color="#FFF59D", size=36),
              it("docs", x=960, y=F, at=C("wholly foreign-owned", -0.6), text="COMPANY LICENCE", stampAt=C("wholly foreign-owned"), stamp="100% FOREIGN OK", color="green"),
              it("calendar", x=1500, y=280, at=C("full foreign ownership", -0.4), pages=[[0, "{{onshore_ownership.display}}", "ONSHORE TOO"]], scale=0.7)],
    "callouts": [co("Dubai's other export: its rulebook", 960, 150, C("rulebook"), "gold", screen=True)]},
    sources=["invest_dubai_hub", "wam_ownership_2021"])
stage("d35_difc", "a7_difc", {
    "zones": [Z("court", cx=960)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.05}], "drift": 4,
    "items": [it("gavel", x=960, y=F - 414, hits=[C("common-law courts"), C("common-law courts", 0.8)]),
              it("sign", x=960, y=180, text="ENGLISH-LANGUAGE, COMMON-LAW COURTS", sub="DIFC, {{difc_courts.display}}", at=C("its own English"), color="#FFF59D", size=28),
              it("counter", x=1550, y=420, at=C("active companies", -1.5), steps=[[0, 0], [{"cue": "active companies", "offset": -1.5}, 0], [{"cue": "active companies", "offset": 1}, 8844]], suffix=" firms", text="end of 2025", scale=0.7)],
    "callouts": [co("In finance, Dubai went further", 960, 960, C("went further"), "white", screen=True)]},
    sources=["dmo_difc_2025", "difc_courts_framework"])
board("p36_tax", "a7_tax", "Taxes: no longer zero", C("Most companies"), [
    {"d": rect(540, 330, 600, 80), "color": "accent", "width": 5, "start": C("Most companies"), "label": lbl("COMPANIES: {{ct_rate.display}} (profits > {{ct_rate.threshold_display}})", 840, 380, 22, "accent")},
    {"d": rect(540, 430, 600, 80), "color": "accent3", "width": 5, "start": C("Qualifying free-zone"), "label": lbl("QUALIFYING FREE-ZONE INCOME: {{qfzp.display}}", 840, 480, 22, "accent3")},
    {"d": rect(540, 530, 600, 80), "color": "accent2", "width": 5, "start": C("Large multinationals"), "label": lbl("LARGE MULTINATIONALS: {{dmtt.display}} MINIMUM", 840, 580, 22, "accent2")},
    {"d": rect(540, 630, 600, 80), "color": "accent2", "width": 5, "start": C("VAT"), "label": lbl("VAT: {{vat.display}}", 840, 680, 24, "accent2")},
    {"d": rect(540, 760, 600, 90), "color": "accent3", "width": 7, "start": C("no income tax"), "label": lbl("SALARIES: NO INCOME TAX", 840, 815, 28, "accent3")}],
    [{"kind": "point", "at": C("no income tax", 0.3), "dur": 1.3, "target": [840, 805]}], enter_from=2200, enter_to=1600,
    sources=["uae_ct", "fta_qfzp", "mof_dmtt", "mof_tax", "pwc_uae_individual"])
add("d37_sectors", "a7_sectors", "engine_chart", {"chart": "donut", "cx": 960, "cy": 610, "r": 240, "thick": 90, "start": C("Put it all together"),
    "data": [{"label": "Trade", "value": 20.5, "display": "20.5%"}, {"label": "Finance & insurance", "value": 14.0, "display": "14.0%"},
             {"label": "Real estate", "value": 11.8, "display": "11.8%"}, {"label": "Transport & storage", "value": 10.7, "display": "10.7%"},
             {"label": "Everything else (incl. oil)", "value": 43.0, "display": "43.0%"}],
    "center": "{{sectors_h1_2026.trade_display}}", "centerSub": "trade, the largest slice ({{sectors_h1_2026.year}})",
    "title": "What Dubai's economy is made of", "subtitle": "share of real GDP · oil is a small part of everything else"}, sources=["wam_gdp_h1_2026", "dubai_ae_economy"])
card("d38_act8", "act8_card", "Who Benefits - and the Risks", "Workers, debt, property, shocks")
stage("d39_workers", "a8_workers", {
    "zones": [Z("site")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("crane", x=1450, text="TOWER", at=0.2, progress=[[0, 0.4], [20, 0.8]], scale=0.9),
              *crowd([300, 420, 540, 660, 780, 900], "stand", at=C("migrant workers"), hat="#FFC93C", scale=0.7),
              it("letters", x=600, y=330, text="{{migrant_share.display}}", at=C("make up"), size=120, color="gold"),
              it("sign", x=600, y=480, text="OF THE UAE'S POPULATION", sub="migrant workers (Human Rights Watch)", at=C("make up", 0.3), size=26)],
    "callouts": [co("They build, staff and drive the city", 960, 960, C("They build"), "white", screen=True)]},
    sources=["hrw_2023"])
stage("d40_labour", "a8_labour", {
    "zones": [Z("site")], "worldW": 2200,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}, {"at": C("The government points"), "x": 1300, "y": 480, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("docs", x=500, y=F, at=0.2, text="RECRUITMENT FEES · KAFALA", stampAt=C("unpaid-wage cases"), stamp="{{hrw_findings.display}} CASES", color="red", scale=0.8),
              it("sign", x=1000, y=300, text="KAFALA", sub="visa tied to the employer", at=C("kafala"), color="#FFCDD2", size=36),
              it("sign", x=1600, y=300, text="SUMMER MIDDAY WORK BAN", sub="{{midday_break.display}}", at=C("summer ban"), color="#FFF59D", size=30),
              *crowd([1600, 1720], "worry", at=C("not enough"), hat="#FFC93C", scale=0.7)],
    "callouts": [co("Human Rights Watch: not enough", 960, 960, C("not enough"), "risk", screen=True)]},
    sources=["hrw_2023", "mohre_midday_2025"])
stage("d41_crash", "a8_crash", {
    "zones": [GULF(night=True, cx=1500)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 450, "zoom": 1.0}], "drift": 4,
    "items": [it("chart", x=700, y=330, w=620, h=340, at=0.3, dur=1.2, text="PROPERTY PRICES", pts=[0.7, 0.85], crashAt=C("fell by")),
              it("letters", x=700, y=620, text="{{crash_2009.display}}", at=C("fell by", 0.6), size=100, color="risk"),
              it("docs", x=1500, y=F, at=C("asked creditors"), text="DUBAI WORLD DEBT {{standstill_2009.display}}", stampAt=C("a pause"), stamp="PAUSE?", color="red", scale=0.75),
              it("storm", x=[[0, 1700], [12, 1000]], y=140, at=C("financial crisis"))]},
    sources=["gulfnews_prices_2009", "gulfnews_dubai_world_2009"])
stage("d42_bailout", "a8_bailout", {
    "zones": [GULF(cx=1400)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 450, "zoom": 1.0}], "drift": 4,
    "items": [it("building", x=380, style="gov", color="#ECEFF1", text="ABU DHABI", at=0.2, scale=0.6),
              it("coins", **{"from": [380, 500], "to": [1300, 600]}, at=C("stepped in"), rate=6, shape="note"),
              it("sign", x=820, y=300, text="{{bailout_2009.display}}", at=C("stepped in"), color="#C8E6C9", size=40),
              it("sign", x=1400, y=160, text="BURJ DUBAI", at=C("tallest tower"), until=C("Burj Khalifa"), color="#ECEFF1", size=34),
              it("sign", x=1400, y=160, text="BURJ KHALIFA", sub="named after Abu Dhabi's ruler ({{burj_renamed.display}})", at=C("Burj Khalifa"), color="#FFF59D", size=34)]},
    sources=["ibtimes_bailout_2009", "csm_burj_2010"])
stage("d43_imf", "a8_imf", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.0}], "drift": 4,
    "items": [it("chart", x=700, y=340, w=600, h=340, at=0.3, dur=3, text="PRICES: A CORRECTION? (risk)", pts=[0.3, 0.5, 0.7, 0.85], crashAt=C("price correction")),
              it("storm", x=[[0, 1700], [12, 1100]], y=140, at=C("reversal")),
              it("docs", x=1450, y=F, at=C("government-related"), text="GOVERNMENT-RELATED COMPANIES", stampAt=C("not published"), stamp="DATA INCOMPLETE", color="orange", scale=0.75)],
    "callouts": [co("The IMF's warning", 960, 960, C("the IMF warns"), "risk", screen=True)]},
    sources=["imf_cr25327"])
stage("d44_war", "a8_war", {
    "zones": [AIR(night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("barrier", x=700, at=0.2, closeAt=C("disrupting travel"), text="FLIGHTS"),
              it("chart", x=1350, y=340, w=560, h=320, at=0.4, dur=1.2, text="DUBAI GDP, H1 2026", pts=[0.6, 0.7], crashAt=C("smaller than")),
              it("letters", x=1350, y=620, text="{{gdp_h1_2026.display}}", at=C("smaller than", 0.5), size=90, color="risk")],
    "callouts": [co("A regional war: {{war_2026.display}}", 960, 150, C("regional war"), "risk", screen=True)]},
    sources=["wam_gdp_h1_2026", "dmo_gdp_q1_2026", "national_iran_war_q1"])
card("d45_act9", "act9_card", "The Real Economic Engine", "The place in between")
board("p46_engine", "a9_engine", "The place in between", C("the place in between"), [
    {"d": "M 960 580 m -90 0 a 90 90 0 1 0 180 0 a 90 90 0 1 0 -180 0", "color": "accent", "width": 7, "fill": "accent", "fillOpacity": 0.25, "start": C("the place in between"), "label": lbl("DUBAI", 960, 590, 30, "ink")},
    {"d": rect(540, 330, 260, 80), "color": "accent2", "width": 5, "start": C("goods change ships"), "label": lbl("GOODS CHANGE SHIPS", 670, 378, 20, "accent2")},
    {"d": rect(1120, 330, 260, 80), "color": "accent2", "width": 5, "start": C("passengers change planes"), "label": lbl("PEOPLE CHANGE PLANES", 1250, 378, 20, "accent2")},
    {"d": rect(540, 760, 260, 80), "color": "accent2", "width": 5, "start": C("capital finds a home"), "label": lbl("CAPITAL FINDS A HOME", 670, 808, 20, "accent2")},
    {"d": rect(1120, 760, 260, 80), "color": "accent2", "width": 5, "start": C("rules they trust"), "label": lbl("RULES THEY TRUST", 1250, 808, 20, "accent2")},
    {"d": "M 800 410 L 890 510 M 1120 410 L 1030 510 M 800 760 L 890 650 M 1120 760 L 1030 650", "color": "ink", "width": 4, "start": C("rules they trust", 0.4)},
    {"d": dot(960, 940), "color": "accent3", "width": 1, "start": C("The state builds"), "label": lbl("THE STATE BUILDS THE HUB · FOREIGN MONEY + WORKERS FILL IT", 960, 945, 22, "accent3")}],
    [{"kind": "point", "at": C("the place in between", 0.4), "dur": 1.3, "target": [960, 580]}], sources=[])
stage("d47_balance", "a9_balance", {
    "zones": [CREEK(-1600, 900), GULF(900, 6000, cx=1700)], "worldW": 2600,
    "cam": [{"at": 0, "x": 760, "y": 480, "zoom": 1.0}, {"at": C("Its own plan"), "x": 1700, "y": 460, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("sign", x=400, y=250, text="✓ END OF PEARLING", at=C("end of pearling"), color="#C8E6C9", size=28),
              it("sign", x=760, y=360, text="✓ DECLINE OF OIL", at=C("decline of oil"), color="#C8E6C9", size=28),
              it("sign", x=1120, y=470, text="✓ THE DEBT CRISIS", at=C("debt crisis"), color="#C8E6C9", size=28),
              it("letters", x=2100, y=330, text="{{d33_goal.display}}", at=C("Its own plan"), size=130, color="gold"),
              it("sign", x=2100, y=480, text="ECONOMY IN A DECADE (D33)", at=C("Its own plan", 0.3), size=26),
              PLANE([[0, 1000], [30, 2800]], 160, at=C("flows Dubai")), it("ship", x=[[0, 2900], [30, 1200]], flip=True, scale=0.4, flag="", at=C("flows Dubai"))],
    "callouts": [co("…but it depends on flows it does not control", 960, 960, C("flows Dubai"), "risk", screen=True)]},
    sources=["dmo_d33"])
keep("d48_end")

write(OUT, "# GENERATED by tools/gen_dubai_cartoon_storyboard.py; edit the generator, not this file.\n"
           "# Episode 02 storyboard in bespoke CartoonStage worlds + four presenter boards.\n")
