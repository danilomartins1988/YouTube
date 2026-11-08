"""Generates projects/why-norway-is-so-rich/deliverables/documentary/storyboard.yaml (Episode 04, cartoon redo).

Bespoke CartoonStage worlds for Norway: a fjord with red wooden houses, a waterfall and fishing boats; the North Sea
with an oil platform that drills dry wells and then strikes Ekofisk; parliament, the finance ministry and the central
bank; the stock-exchange floor; the fund as a growing stack of money that is never spent; an ageing crowd. Four
presenter boards explain the three money streams, the resource curse, the spending rule and the wage model. Charts and
maps of the first cut are kept from tools/data/norway_storyboard_v1.yaml. Narration and figures are unchanged.
Run: python tools/gen_norway_cartoon_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "projects/why-norway-is-so-rich/deliverables/documentary/storyboard.yaml"
BASE = {s["id"]: s for s in yaml.safe_load((ROOT / "tools/data/norway_storyboard_v1.yaml").read_text())["scenes"]}
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
FJORD = lambda x0=-1600, x1=4600, **kw: Z("fjord", x0, x1, **kw)
SEA = lambda x0=-1600, x1=4600, **kw: Z("northsea", x0, x1, **kw)


USD_FIX = {   # kept first-cut charts: values are now US dollars (converted in sources.yaml, Fed H.10 annual averages)
    "n19_cashflow": {"subtitle": "US$ billion per year · converted at each year's average rate (Statistics Norway, Fed H.10)", "value_prefix": "$"},
    "n25_growth": {"subtitle": "US$ billion · converted at each year's average rate (NBIM, Fed H.10)", "value_prefix": "$", "y_max": 2400},
    "n35_insulate": {"subtitle": "Illustration of the principle: fund value (NBIM), US$ billion", "value_prefix": "$", "y_max": 2400},
}


def keep(*ids):
    for i in ids:
        sc = BASE[i]
        if i in USD_FIX:
            sc["params"].update(USD_FIX[i])
            for ev in sc["params"].get("events", []) or []:
                if isinstance(ev, dict) and "NOK" in str(ev.get("label", "")):
                    ev["label"], ev["year"] = "Passes $1 trillion", 2014   # first year >= $1,000bn in the converted series
            sc["sources"] = list(sc.get("sources", [])) + ["fed_h10"]
        cartoon_kit.scenes.append(sc)


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


FUND = lambda x, h, at=0.0, **kw: it("stack", x=x, h=h, at=at, text=kw.pop("text", "THE FUND"), color=kw.pop("color", "gold"), **kw)

# ====================================================================== OPENING
stage("n01_hook", "open_hook", {
    "zones": [SEA(-1600, 1700), FJORD(1700, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.05}, {"at": C("The money"), "x": 2300, "y": 500, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("rig", x=800, at=0.2, drillAt=0.3),
              it("coins", **{"from": [900, 300], "to": [2300, 600]}, at=C("The money"), rate=5, arc=260),
              FUND(2400, [[0, 60], [{"cue": "The money"}, 60], [{"cue": "largest investment funds"}, 520]], at=C("The money"), sub="one of the largest on Earth")],
    "callouts": [co("Somewhere in the North Sea…", 960, 150, C("Somewhere"), "white", screen=True, until=C("The money", -0.3)),
                 co("…the money ends up in a giant fund", 960, 150, C("The money"), "gold", screen=True)]})
stage("n02_value", "open_value", {
    "zones": [FJORD()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.1}, {"at": C("Divide that"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("counter", x=960, y=260, at=0.3, steps=[[0, 0], [0.6, 0], [3.4, 2.12]], prefix="$", suffix=" trillion", decimals=2, text="the oil fund, {{fund_value_q3_2026.date_display}} (at the 2025 average rate)"),
              *crowd([360, 480, 600, 1320, 1440, 1560], "cheer", at=C("every person")),
              it("coins", **{"from": [960, 340], "to": [480, 640]}, at=C("every person"), rate=4),
              it("coins", **{"from": [960, 340], "to": [1440, 640]}, at=C("every person", 0.2), rate=4)],
    "callouts": [co("{{fund_per_person.display}} for every Norwegian", 960, 960, C("Divide that"), "gold", screen=True, size=42)]},
    sources=["nbim_q3_2026", "ssb_population", "fed_h10"])
keep("n03_stake")
stage("n04_question", "open_question", {
    "zones": [FJORD(-1600, 1300), SEA(1300, 6000)], "worldW": 2800, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 2000, "y": 520, "zoom": 1.0}, {"at": C("what did Norway"), "x": 960, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("rig", x=1900, at=0.2, scale=0.7), it("rig", x=2600, at=0.4, scale=0.55, text="OTHER COUNTRIES"),
              it("letters", x=960, y=300, text="?", at=C("what did Norway"), size=150, color="gold"),
              *crowd([700, 1200], "shrug", at=C("Few have"))],
    "callouts": [co("Plenty of countries found oil", 960, 150, C("Plenty of countries"), "white", screen=True, until=C("what did Norway", -0.3)),
                 co("What did Norway do differently?", 960, 150, C("what did Norway"), "gold", screen=True, size=44)]})
card("n05_p1", "p1_card", "Before the Oil", "Fish, ships and waterfalls")
stage("n06_economy", "p1_economy", {
    "zones": [FJORD()], "worldW": 2600,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("merchant fleet"), "x": 1350, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("Norsk Hydro"), "x": 1900, "y": 480, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("ship", type="fishing", x=[[0, 200], [20, 900]], scale=0.4, flag="", smoke=False, crew=2),
              it("ship", type="container", x=[[0, 2900], [{"cue": "merchant fleet"}, 2900], [{"cue": "merchant fleet", "offset": 6}, 1300]], flip=True, scale=0.45, flag="NORWAY", at=C("merchant fleet", -0.4)),
              it("sign", x=1350, y=300, text="MERCHANT FLEET: {{merchant_fleet_1956.display}}", sub="in the world, 1950s", at=C("described as"), color="#BBDEFB", size=30),
              it("building", x=2000, style="office", color="#B0BEC5", text="NORSK HYDRO", at=C("Norsk Hydro"), scale=0.6),
              it("sign", x=2000, y=230, text="WATERFALLS → FERTILISER", sub="{{hydro_1905.display}}", at=C("waterfalls"), color="#C8E6C9", size=28)],
    "callouts": [co("The sea and the mountains", 960, 150, C("the sea and the mountains"), "white", screen=True)]},
    sources=["usni_merchant_1956", "hydro_history"])
keep("n07_neighbours")
card("n08_p2", "p2_card", "The Discovery", "The North Sea, 1960s")
stage("n09_doubt", "p2_doubt", {
    "zones": [Z("office")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.1}], "drift": 4,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "{{geology_1958.display}}", "THE VERDICT"]], scale=0.8),
              it("docs", x=960, y=F, at=0.3, text="OIL UNDER THE SEABED?", stampAt=C("discounted"), stamp="UNLIKELY", color="red"),
              *crowd([1450], "shrug", at=C("geological survey"), glasses=True)],
    "callouts": [co("Few believed there was oil at all", 960, 150, C("Few believed"), "white", screen=True)]},
    sources=["np_history"])
keep("n10_shelf")
stage("n11_ekofisk", "p2_ekofisk", {
    "zones": [SEA()], "worldW": 2400,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("Then"), "x": 1550, "y": 480, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("rig", x=650, at=0.2, drillAt=0.3, dryAt=C("came up dry"), scale=0.8),
              it("rig", x=1600, at=C("Then", -0.5), drillAt=C("Then"), strikeAt=C("Ekofisk"), text="EKOFISK", scale=0.9)],
    "callouts": [co("The first wells: dry", 960, 150, C("came up dry"), "risk", screen=True, until=C("Then", -0.3)),
                 co("{{ekofisk_1969.display}}: Ekofisk!", 960, 150, C("Ekofisk"), "gold", screen=True, size=46, until=C("At the time", -0.3)),
                 co("The largest offshore field ever found (then)", 960, 150, C("At the time"), "green", screen=True)]},
    sources=["np_history", "ekofisk_museum"], sfx=[{"kind": "hit", "cue": "Ekofisk", "gain": 0.35}])
stage("n12_production", "p2_production", {
    "zones": [SEA()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 6,
    "items": [it("rig", x=700, at=0.2, drillAt=0.2, text="EKOFISK"),
              it("ship", type="tanker", x=[[0, 2300], [12, 1400]], flip=True, scale=0.5, flag="OIL", at=0.4),
              it("calendar", x=1550, y=260, at=0.3, pages=[[0, "{{ekofisk_production.display}}", "OIL FLOWS"]], scale=0.7)],
    "callouts": [co("An oil nation almost overnight", 960, 960, C("almost overnight"), "gold", screen=True, size=42)]},
    sources=["np_history"])
card("n13_p3", "p3_card", "Who Owns the Oil", "Control first, then tax")
stage("n14_commandments", "p3_commandments", {
    "zones": [FJORD()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 4,
    "items": [it("building", x=700, style="gov", color="#FFE0B2", text="PARLIAMENT", at=0.2, scale=0.8),
              it("docs", x=1350, y=F, at=C("parliament adopted"), text="THE TEN OIL COMMANDMENTS", stampAt=C("national control"), stamp="ADOPTED", color="green"),
              it("calendar", x=330, y=260, at=0.3, pages=[[0, "{{ten_commandments.display}}", "PARLIAMENT"]], scale=0.7)],
    "callouts": [co("Decision 1: control", 960, 150, C("about control"), "gold", screen=True, size=44)]},
    sources=["storting_oljebud"])
stage("n15_statoil", "p3_statoil", {
    "zones": [FJORD()], "worldW": 2600,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("Today the government"), "x": 1700, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("calendar", x=280, y=260, at=0.2, scale=0.7, pages=[[0, "{{statoil_1972.display}}", "STATOIL"], [{"cue": "direct stakes"}, "{{sdfi_1985.display}}", "DIRECT STAKES"]]),
              it("building", x=700, style="office", color="#FFCDD2", text="STATOIL", at=C("state oil company"), scale=0.7),
              it("building", x=1150, style="gov", color="#C5CAE9", text="PETROLEUM DIRECTORATE", at=C("a regulator"), scale=0.6),
              it("tower", x=1800, text="EQUINOR", color="#E53935", at=C("Today the government"), scale=1.0),
              it("sign", x=1800, y=180, text="STATE OWNS {{equinor_67.display}}", at=C("still owns"), color="#FFF59D", size=34)],
    "callouts": [co("A state oil company and a regulator", 960, 960, C("state oil company"), "white", screen=True, until=C("direct stakes", -0.3)),
                 co("The state also holds stakes in fields", 960, 960, C("direct stakes"), "white", screen=True)]},
    sources=["sodir_50", "np_history", "np_state_org"])
stage("n16_tax", "p3_tax", {
    "zones": [FJORD()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("stack", x=500, at=C("normal"), h=[[0, 20], [{"cue": "normal"}, 20], [{"cue": "normal", "offset": 2}, 130]], text="{{petroleum_tax.ordinary_display}}", sub="normal company tax"),
              it("stack", x=960, at=C("special petroleum tax"), h=[[0, 20], [{"cue": "special petroleum tax"}, 20], [{"cue": "special petroleum tax", "offset": 2}, 420]], text="{{petroleum_tax.special_display}}", sub="special petroleum tax", color="#FFCC80"),
              it("letters", x=1450, y=360, text="{{petroleum_tax.display}}", at=C("Together"), size=130, color="gold"),
              it("sign", x=1450, y=520, text="OF PROFIT AT THE MARGIN", at=C("Together", 0.3), size=26)],
    "callouts": [co("Decision 2: tax", 960, 150, C("The second decision"), "gold", screen=True, size=44)]},
    sources=["np_revenues", "np_tax"])
board("p17_streams", "p3_streams", "Three ways the oil pays the state", C("three ways"), [
    {"d": rect(560, 380, 280, 110), "color": "accent", "width": 6, "start": C("three ways"), "label": lbl("OIL", 700, 445, 34, "accent")},
    {"d": arrow((850, 420), (1150, 360), -0.1), "color": "ink", "width": 4, "start": C("taxes on company")},
    {"d": rect(1160, 300, 360, 90), "color": "accent2", "width": 5, "start": C("taxes on company", 0.3), "label": lbl("1 · TAXES ON PROFITS", 1340, 355, 26, "accent2")},
    {"d": arrow((850, 440), (1150, 500), 0), "color": "ink", "width": 4, "start": C("its own share")},
    {"d": rect(1160, 450, 360, 90), "color": "accent2", "width": 5, "start": C("its own share", 0.3), "label": lbl("2 · ITS OWN SHARE OF FIELDS", 1340, 505, 22, "accent2")},
    {"d": arrow((850, 460), (1150, 640), 0.1), "color": "ink", "width": 4, "start": C("dividends")},
    {"d": rect(1160, 600, 360, 90), "color": "accent2", "width": 5, "start": C("dividends", 0.3), "label": lbl("3 · EQUINOR DIVIDENDS", 1340, 655, 24, "accent2")},
    {"d": "M 1340 720 L 1340 760 M 1300 760 L 1380 760 L 1380 860 L 1300 860 Z", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar",
     "start": C("Equinor", 0.5), "label": lbl("THE STATE", 1340, 900, 26, "accent3")}],
    [{"kind": "point", "at": C("dividends", 0.4), "dur": 1.3, "target": [1340, 655]}], sources=["ssb_cashflow", "np_state_org"], min_s=11.0)
card("n18_p4", "p4_card", "The Money Machine", "And its danger")
keep("n19_cashflow", "n20_exports")
board("p21_curse", "p4_problem", "The resource curse", C("Spend it all"), [
    {"d": rect(560, 360, 300, 110), "color": "accent", "width": 6, "start": C("That much money"), "label": lbl("OIL MONEY POURS IN", 710, 425, 24, "accent")},
    {"d": arrow((870, 415), (1010, 415)), "color": "ink", "width": 4, "start": C("Spend it all")},
    {"d": rect(1020, 360, 300, 110), "color": "risk", "width": 6, "start": C("Spend it all", 0.3), "label": lbl("SPENT AT HOME", 1170, 425, 26, "risk")},
    {"d": "M 1080 560 L 1080 480 L 1130 480 L 1130 560 M 1190 560 L 1190 500 L 1240 500 L 1240 560", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.3, "kind": "bar",
     "start": C("wages and prices"), "label": lbl("WAGES + PRICES ↑", 1160, 600, 24, "risk")},
    {"d": dot(1160, 660), "color": "risk", "width": 1, "start": C("currency soars"), "label": lbl("CURRENCY ↑", 1160, 665, 26, "risk")},
    {"d": "M 600 720 L 600 640 L 660 640 L 660 720 M 700 720 L 700 680 L 760 680 L 760 720", "color": "muted", "width": 4, "fill": "muted", "fillOpacity": 0.3, "kind": "bar",
     "start": C("every other industry"), "label": lbl("OTHER INDUSTRIES SHRINK", 680, 770, 24, "muted")},
    {"d": dot(960, 880), "color": "risk", "width": 1, "start": C("resource curse"), "label": lbl("= THE RESOURCE CURSE", 960, 885, 40, "risk")}],
    [{"kind": "point", "at": C("every other industry", 0.3), "dur": 1.3, "target": [680, 700]}, {"kind": "react", "at": C("resource curse", 0.4)}],
    enter_from=2200, enter_to=1620)
card("n22_p5", "p5_card", "The Fund", "Park the money abroad")
stage("n23_law", "p5_law", {
    "zones": [FJORD()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 4,
    "items": [it("calendar", x=300, y=260, at=0.2, scale=0.7, pages=[[0, "{{fund_law_1990.display}}", "FUND CREATED"], [{"cue": "the first"}, "1996", "FIRST MONEY IN"]]),
              it("building", x=760, style="gov", color="#FFE0B2", text="PARLIAMENT", at=0.3, scale=0.7),
              it("plane", x=[[0, 900], [{"cue": "park the money abroad"}, 900], [{"cue": "park the money abroad", "offset": 6}, 2400]], y=[[0, 500], [{"cue": "park the money abroad", "offset": 6}, 150]], text="$", scale=0.5, at=C("park the money abroad"), tilt=-10),
              FUND(1400, [[0, 20], [{"cue": "the first"}, 20], [{"cue": "the first", "offset": 2}, 80]], at=C("the first"), text="{{first_transfer_1996.display}}", sub="the first transfer")],
    "callouts": [co("Park the money abroad", 960, 150, C("park the money abroad"), "gold", screen=True, size=44)]},
    sources=["nbim_history", "nbim_25yrs"])
stage("n24_governance", "p5_governance", {
    "zones": [FJORD(-1600, 1700), Z("airport", 1700, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 0.95}, {"at": C("One rule"), "x": 2250, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("building", x=400, style="gov", color="#FFE0B2", text="PARLIAMENT", at=C("Parliament sets"), scale=0.6),
              it("building", x=960, style="office", color="#C5CAE9", text="FINANCE MINISTRY", at=C("finance ministry"), scale=0.6),
              it("building", x=1450, style="bank", color="#FFF59D", text="CENTRAL BANK", at=C("central bank"), scale=0.6),
              it("barrier", x=2100, at=C("One rule", -0.3), closeAt=C("not allowed"), text="INTO NORWAY"),
              it("coins", **{"from": [1700, 400], "to": [2150, 700]}, at=C("One rule"), until=C("not allowed"), rate=4)],
    "callouts": [co("Rules · owner · manager", 960, 150, C("Parliament sets"), "white", screen=True, until=C("One rule", -0.3)),
                 co("The fund may not invest in Norway at all", 960, 150, C("not allowed"), "risk", screen=True)]},
    sources=["nbim_about", "nbim_history", "nbim_ar2025"])
keep("n25_growth")
stage("n26_returns", "p5_returns", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.0}], "drift": 4,
    "items": [it("stack", x=600, at=C("oil money paid in"), h=[[0, 20], [{"cue": "oil money paid in"}, 20], [{"cue": "oil money paid in", "offset": 2}, 260]], text="OIL MONEY PAID IN", sub="less than half", color="#FFCC80"),
              it("stack", x=1300, at=C("The rest"), h=[[0, 20], [{"cue": "The rest"}, 20], [{"cue": "The rest", "offset": 2.5}, 380]], text="EARNED BY INVESTING", sub="the rest (schematic)", color="gold")],
    "callouts": [co("Here is the surprising part", 960, 150, C("surprising"), "white", screen=True)]},
    sources=["nbim_about"])
card("n27_p6", "p6_card", "How the Fund Invests", "A slice of the world economy")
keep("n28_allocation", "n29_world")
stage("n30_returns", "p6_returns", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.0}], "drift": 4,
    "items": [it("chart", x=960, y=380, w=900, h=420, at=0.3, dur=6, text="FUND RETURNS: NOT A SMOOTH RIDE (schematic)", pts=[0.2, 0.3, 0.4, 0.15, 0.4, 0.55, 0.65, 0.5, 0.7, 0.85]),
              it("sign", x=480, y=720, text="AVERAGE {{returns_since_1998.display}} A YEAR", sub="{{returns_since_1998.real_display}} after inflation and costs", at=C("returned an average"), color="#C8E6C9", size=28),
              it("sign", x=1000, y=720, text="FINANCIAL CRISIS {{bad_years.display}}", at=C("financial crisis"), color="#FFCDD2", size=28),
              it("sign", x=1500, y=720, text="2022: {{bad_years.y2022_display}}", at=C("minus 14"), color="#FFCDD2", size=28)],
    "callouts": [co("Not a smooth ride", 960, 960, C("not a smooth ride"), "risk", screen=True)]},
    sources=["nbim_ar2025", "nbim_history"])
card("n31_p7", "p7_card", "The Fiscal Rule", "Spend the return, not the capital")
board("p32_rule", "p7_rule", "The spending rule", C("rule about spending"), [
    {"d": rect(560, 360, 420, 300), "color": "accent", "width": 6, "start": C("rule about spending"), "label": lbl("THE FUND", 770, 520, 40, "accent")},
    {"d": "M 980 450 L 1180 450", "color": "accent3", "width": 6, "start": C("may only take out")},
    {"d": rect(1190, 400, 300, 100), "color": "accent3", "width": 5, "start": C("expected to earn"), "label": lbl("ONLY THE EXPECTED RETURN", 1340, 458, 20, "accent3")},
    {"d": dot(1340, 560), "color": "muted", "width": 1, "start": C("after inflation"), "label": lbl("(after inflation)", 1340, 565, 24, "muted")},
    {"d": "M 1250 760 L 1250 660 L 1320 660 L 1320 760", "color": "muted", "width": 4, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("That was set"), "label": lbl("{{fiscal_rule.old_display}}", 1285, 800, 30, "muted")},
    {"d": "M 1380 760 L 1380 690 L 1450 690 L 1450 760", "color": "accent", "width": 4, "fill": "accent", "fillOpacity": 0.4, "kind": "bar", "start": C("cut to"), "label": lbl("{{fiscal_rule.display}}", 1415, 800, 30, "accent")}],
    [{"kind": "point", "at": C("expected to earn", 0.4), "dur": 1.3, "target": [1340, 450]}, {"kind": "point", "at": C("cut to", 0.4), "dur": 1.2, "target": [1415, 720]}],
    sources=["mof_framework"])
stage("n33_budget", "p7_budget", {
    "zones": [FJORD()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.05}], "drift": 4,
    "items": [it("building", x=480, style="gov", color="#FFE0B2", text="GOVERNMENT", at=0.2, scale=0.7),
              it("counter", x=1200, y=260, at=C("planned to use"), steps=[[0, 0], [{"cue": "planned to use"}, 0], [{"cue": "planned to use", "offset": 2.5}, 55.8]], prefix="$", suffix="bn", decimals=1, text="oil money in this year's budget (2025 average rate)"),
              it("sign", x=1200, y=560, text="≈ 1/4 OF ALL PUBLIC SPENDING", sub="IMF estimate", at=C("IMF estimates"), color="#FFF59D", size=30)],
    "callouts": [co("About {{budget_2026_deficit.pct_fund_display}} of the fund", 960, 960, C("of the fund"), "gold", screen=True)]},
    sources=["mof_budget_2026", "nbim_about", "fed_h10"])
stage("n34_why", "p7_why", {
    "zones": [FJORD()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.05}], "drift": 4,
    "items": [FUND(700, 480, at=0.2, sub="never used up"),
              it("sign", x=700, y=240, text="SHARES · BONDS · BUILDINGS", at=C("converted into"), color="#BBDEFB", size=28),
              *crowd([1250, 1380, 1510], "cheer", at=C("not yet born"), scale=0.55),
              it("sign", x=1380, y=560, text="FUTURE GENERATIONS", at=C("not yet born", 0.3), color="#C8E6C9", size=28)],
    "callouts": [co("Spend the return, keep the capital", 960, 150, C("Spending only"), "gold", screen=True)]},
    sources=["mof_framework"])
keep("n35_insulate")
card("n36_p8", "p8_card", "Beyond Oil", "The Norwegian model")
keep("n37_mainland")
board("p38_model", "p8_model", "Who sets the pace of wages", C("About half"), [
    {"d": dot(960, 330), "color": "accent2", "width": 1, "start": C("About half"), "label": lbl("ABOUT HALF OF WORKERS: IN A UNION", 960, 335, 30, "accent2")},
    {"d": rect(560, 430, 380, 120), "color": "accent", "width": 6, "start": C("compete internationally"), "label": lbl("EXPORT INDUSTRIES", 750, 500, 28, "accent")},
    {"d": dot(750, 590), "color": "accent", "width": 1, "start": C("negotiate first"), "label": lbl("negotiate FIRST", 750, 595, 26, "accent")},
    {"d": arrow((950, 490), (1150, 490)), "color": "ink", "width": 5, "start": C("everyone else")},
    {"d": rect(1160, 430, 380, 120), "color": "accent3", "width": 5, "start": C("everyone else", 0.3), "label": lbl("EVERYONE ELSE", 1350, 500, 28, "accent3")},
    {"d": dot(1350, 590), "color": "accent3", "width": 1, "start": C("follows their lead"), "label": lbl("follows their lead", 1350, 595, 26, "accent3")},
    {"d": dot(960, 760), "color": "risk", "width": 1, "start": C("in step"), "label": lbl("PAY = WHAT EXPORTERS CAN AFFORD", 960, 765, 30, "risk")}],
    [{"kind": "point", "at": C("negotiate first", 0.3), "dur": 1.3, "target": [750, 500]}, {"kind": "point", "at": C("in step", 0.3), "dur": 1.2, "target": [960, 760]}],
    enter_from=2200, enter_to=1640, sources=["fafo_2025", "ssb_frontfag"])
stage("n39_trust", "p8_trust", {
    "zones": [FJORD()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 4,
    "items": [*crowd([360, 470, 580, 690], "cheer", at=C("trusted their national")), *crowd([1250, 1360, 1470], "shrug", at=C("across the OECD")),
              it("sign", x=525, y=420, text="NORWAY {{trust_2025.display}}", sub="trust the national government", at=C("trusted their national"), color="#C8E6C9", size=32),
              it("sign", x=1360, y=420, text="OECD {{trust_2025.oecd_display}}", sub="average", at=C("across the OECD"), color="#ECEFF1", size=32)],
    "callouts": [co("Even incomes, high trust", 960, 150, C("Income is spread"), "white", screen=True, until=C("Trust makes", -0.3)),
                 co("Trust makes long-term rules easier to keep", 960, 150, C("Trust makes"), "gold", screen=True)]},
    sources=["oecd_trust_2026", "ssb_gini"])
stage("n40_productivity", "p8_productivity", {
    "zones": [FJORD()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.0}], "drift": 4,
    "items": [it("chart", x=960, y=380, w=780, h=400, at=0.3, dur=3, text="LEAD IN LIVING STANDARDS (OECD)", pts=[0.85, 0.7], crashAt=C("narrowed")),
              it("sign", x=960, y=720, text="{{oecd_productivity.from_display}} → {{oecd_productivity.to_display}}", sub="in fifteen years", at=C("narrowed"), color="#FFCDD2", size=40)],
    "callouts": [co("A warning sign: productivity", 960, 150, C("warning sign"), "risk", screen=True)]},
    sources=["oecd_blog_2024"])
card("n41_p9", "p9_card", "The Risks", "Prices, time, age and markets")
stage("n42_volatility", "p9_volatility", {
    "zones": [SEA(night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("rig", x=480, at=0.2, scale=0.75, night=True),
              it("chart", x=1300, y=360, w=640, h=360, at=0.3, dur=1.5, text="OIL PRICE", pts=[0.8, 0.85], crashAt=C("oil fell")),
              it("sign", x=1150, y=650, text="CURRENCY {{oil_crash_2014.krone_display}}", at=C("currency weakened"), color="#FFCDD2", size=28),
              it("sign", x=1550, y=650, text="JOBLESS {{unemployment_2014_16.display}}", at=C("unemployment rose"), color="#FFCDD2", size=28),
              it("storm", x=[[0, 1700], [14, 900]], y=150, at=C("oil fell"))],
    "callouts": [co("Risk 1: the oil price", 960, 150, C("The first risk"), "risk", screen=True, until=C("oil fell", -0.2)),
                 co("After 2014: oil fell to a third of its level", 960, 150, C("oil fell"), "risk", screen=True)]},
    sources=["nb_papers_2016", "ssb_08517"])
keep("n43_decline")
stage("n44_ageing", "p9_ageing", {
    "zones": [FJORD()], "worldW": 2600,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.0}, {"at": C("official projections"), "x": 1650, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [*crowd([500, 620, 740], "stand", at=C("people of working age")), *crowd([960], "stand", at=C("over sixty-five"), old=True),
              it("sign", x=700, y=380, text="TODAY: {{ageing.now_display}} TO 1", at=C("people of working age"), color="#C8E6C9", size=30),
              *crowd([1450, 1570], "worry", at=C("official projections")), *crowd([1800], "stand", at=C("official projections", 0.3), old=True),
              it("sign", x=1620, y=380, text="{{ageing.future_year}}: {{ageing.future_display}} TO 1", at=C("official projections"), color="#FFCDD2", size=30)],
    "callouts": [co("Pensions and care will cost more", 960, 150, C("Pensions and care"), "risk", screen=True)]},
    sources=["ssb_14288"])
stage("n45_markets", "p9_markets", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.0}], "drift": 4,
    "items": [it("chart", x=960, y=380, w=820, h=400, at=0.3, dur=2, text="STRESS TEST: A FRAGMENTED WORLD", pts=[0.7, 0.8, 0.85], crashAt=C("could knock")),
              it("letters", x=960, y=720, text="{{stress_test.display}}", at=C("off its value"), size=110, color="risk"),
              it("storm", x=[[0, 1700], [10, 1200]], y=140, at=C("could knock"))],
    "callouts": [co("Risk 4: the world's markets", 960, 150, C("exposed"), "risk", screen=True)]},
    sources=["nbim_stress_2025"])
card("n46_p10", "p10_card", "The Real Secret", "Decisions, not just oil")
stage("n47_secret", "p10_secret", {
    "zones": [FJORD()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 4,
    "items": [it("sign", x=480, y=260, text="1 · KEPT CONTROL", at=C("kept control"), color="#C8E6C9", size=30, hang=True, swing=True),
              it("sign", x=1440, y=260, text="2 · TAXED IT HEAVILY", at=C("taxed it"), color="#FFF59D", size=30, hang=True, swing=True),
              it("sign", x=480, y=500, text="3 · SAVED IT ABROAD", at=C("saved the money"), color="#BBDEFB", size=30),
              it("sign", x=1440, y=500, text="4 · SPENDS ONLY THE RETURN", at=C("spends only"), color="#E1BEE7", size=30),
              it("letters", x=960, y=380, text="?", at=C("So why"), until=C("kept control"), size=120, color="gold")],
    "callouts": [co("Not just oil: what it decided next", 960, 960, C("Not just because"), "gold", screen=True)]})
stage("n48_end", "p10_end", {
    "zones": [SEA(-1600, 1400), FJORD(1400, 6000)], "worldW": 2800,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("The rules"), "x": 2000, "y": 500, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("rig", x=700, at=0.2, scale=0.8, flare=True),
              FUND(2000, 560, at=0.3, sub="designed to last"),
              *crowd([1650, 2350], "cheer", at=C("position of strength"))],
    "callouts": [co("The oil will run out one day", 960, 150, C("The oil will run out"), "white", screen=True, until=C("The rules", -0.3)),
                 co("The fortune is designed not to", 960, 150, C("The rules"), "gold", screen=True, until=C("position of strength", -0.3)),
                 co("“A position of strength”", 960, 150, C("position of strength"), "green", screen=True, sub="the IMF")]},
    sources=["imf_2026"])

write(OUT, "# GENERATED by tools/gen_norway_cartoon_storyboard.py; edit the generator, not this file.\n"
           "# Episode 04 storyboard in bespoke CartoonStage worlds + four presenter boards.\n")
