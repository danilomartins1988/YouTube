"""Generates projects/why-switzerland-is-so-rich/deliverables/documentary/storyboard.yaml (Episode 01 pilot, cartoon redo).

Bespoke CartoonStage worlds for Switzerland: the Alps with a lake, chalets, a red cable car and a red train; a bank vault
for banking secrecy; the stock-exchange floor for the franc battles; a pharmaceutical lab in Basel; a giant wristwatch;
a workshop full of apprentices; a border barrier for the 2025 US tariffs. Four presenter boards (the four forces, what
output per person means, why predictability pays, how a safe haven hurts exporters). Chart values are data-derived from
the World Bank dossier at generation time. The project is currency-exempt (approved before the dollar rule).
Run: python tools/gen_switzerland_cartoon_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cartoon_kit import *  # noqa: E402,F403
from hiddeneco.config import project_paths  # noqa: E402
from hiddeneco.pipeline import research  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SLUG = "why-switzerland-is-so-rich"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
DOS = research(project_paths(SLUG, deliverable="documentary"))
F = 860
GEO = ["geo:remotion_world", "font:inter"]
WB = ["wb_gdppc_indicator", "wb_gdp_mirror", "wb_pop_mirror"]
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
ALPS = lambda x0=-1600, x1=4600, **kw: Z("swiss", x0, x1, **kw)


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


bars = [{"label": d["name"].replace("United States", "U.S.").replace("United Kingdom", "U.K."), "value": round(d["value"])} for d in DOS.claim("gdppc_chart_2023").value]
che = next(s for s in DOS.claim("gdppc_series_2000_2023").value if s["code"] == "CHE")["points"]
line = [{"label": str(p["year"]) if p["year"] % 5 == 0 or p["year"] == 2023 else "", "value": round(p["value"])} for p in che]
gdppc = round(DOS.claim("gdppc_che_2023").value)

# ====================================================================== THE PUZZLE
stage("d01_open_map", "open_map", {
    "zones": [ALPS()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 300, "zoom": 1.3}, {"at": C("no coastline"), "x": 960, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("sign", x=480, y=330, text="LANDLOCKED", sub="no coastline, no sea", at=C("no coastline"), color="#FFF59D", size=36),
              it("sign", x=1450, y=330, text="{{pop_che_2023.display}} PEOPLE", at=C("people"), color="#C8E6C9", size=32),
              *crowd([1300, 1420, 1540], "stand", at=C("larger, louder"), scale=0.6)],
    "callouts": [co("A small country in the middle of a continent", 960, 960, C("in the middle"), "white", screen=True)]},
    sources=["wb_pop_mirror"])
stage("d02_open_number", "open_number", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.05}], "drift": 4,
    "items": [it("counter", x=960, y=260, at=C("this country produced", -1), steps=[[0, 0], [{"cue": "this country produced", "offset": -1}, 0], [{"cue": "this country produced", "offset": 1.8}, gdppc]], prefix="$", text="output per person, {{gdppc_che_2023.year}} (World Bank)"),
              it("sign", x=600, y=560, text="{{ratio_che_deu_2023.display}} GERMANY", at=C("Germany's figure"), color="#FFF59D", size=34),
              it("sign", x=1320, y=560, text="{{ratio_che_euu_2023.display}} THE EU AVERAGE", at=C("European Union"), color="#BBDEFB", size=34)],
    "callouts": [co("And yet…", 960, 960, C("And yet"), "gold", screen=True)]},
    sources=WB)
stage("d03_open_promise", "open_promise", {
    "zones": [Z("vault", -1600, 1200), ALPS(1200, 6000)], "worldW": 2600,
    "cam": [{"at": 0, "x": 760, "y": 500, "zoom": 1.0}, {"at": C("The real story"), "x": 1800, "y": 500, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("vaultdoor", x=500, r=230, label="BANKS"), it("watch", x=950, y=430, at=C("watches"), scale=0.55, text="WATCHES"),
              it("sign", x=760, y=180, text="CHOCOLATE?", at=C("chocolate"), color="#D7CCC8", size=34),
              it("letters", x=1800, y=280, text="?", at=C("stranger"), size=140, color="gold"),
              it("sign", x=2150, y=460, text="…AND HIDDEN COSTS", at=C("costs that rarely"), color="#FFCDD2", size=30)],
    "callouts": [co("How did Switzerland get this rich?", 960, 150, C("How did"), "gold", screen=True)]})
board("p03b_roadmap", "open_roadmap", "Follow the money: four forces", C("four forces"), [
    {"d": rect(540, 330, 300, 100), "color": "accent2", "width": 5, "start": C("Stability"), "label": lbl("1 · STABILITY", 690, 390, 26, "accent2")},
    {"d": rect(880, 330, 300, 100), "color": "accent", "width": 5, "start": C("Money, and"), "label": lbl("2 · MONEY", 1030, 390, 26, "accent")},
    {"d": rect(540, 470, 300, 100), "color": "accent3", "width": 5, "start": C("Specialisation"), "label": lbl("3 · SPECIALISATION", 690, 530, 22, "accent3")},
    {"d": rect(880, 470, 300, 100), "color": "accent3", "width": 5, "start": C("And skills"), "label": lbl("4 · SKILLS", 1030, 530, 26, "accent3")},
    {"d": rect(700, 650, 320, 110), "color": "risk", "width": 6, "dash": "12 10", "start": C("the bill"), "label": lbl("THE BILL", 860, 715, 32, "risk")}],
    [{"kind": "point", "at": C("the bill", 0.3), "dur": 1.3, "target": [860, 700]}], enter_from=2200, enter_to=1600)
card("d04_act1", "act1_card", "The Puzzle", "A small country, a big number")
add("d05_bars", "puzzle_bars", "engine_chart", {"chart": "bar", "box": {"x": 300, "y": 330, "w": 1320, "h": 500}, "start": C("Measured as output"), "stagger": 0.5,
    "title": "GDP per person, {{gdppc_chart_2023.year}}", "note": "current US dollars (World Bank)", "valuePrefix": "$", "data": bars,
    "highlight": 0, "highlightAt": C("well above"), "color": "accent2", "highlightColor": "accent"}, sources=WB)
add("d06_line", "puzzle_line", "engine_chart", {"chart": "line", "box": {"x": 300, "y": 330, "w": 1320, "h": 500}, "start": C("Follow the data"), "draw": 5.0,
    "title": "Switzerland: GDP per person, 2000–2023", "note": "current US dollars · above Germany and the EU average in every year (World Bank, our check)",
    "valuePrefix": "$", "data": line, "color": "accent"}, sources=WB)
board("p06b_caveat", "puzzle_caveat", "What this number is, and isn't", C("Output per person measures"), [
    {"d": rect(540, 330, 420, 110), "color": "accent2", "width": 5, "start": C("how much an economy produces"), "label": lbl("ALL OUTPUT ÷ ALL PEOPLE", 750, 395, 24, "accent2")},
    {"d": rect(1000, 330, 380, 110), "color": "risk", "width": 5, "dash": "12 10", "start": C("not the same"), "label": lbl("≠ MONEY IN YOUR POCKET", 1190, 395, 22, "risk")},
    {"d": rect(540, 490, 420, 110), "color": "accent", "width": 5, "start": C("measured in US dollars"), "label": lbl("IN US$ → EXCHANGE RATES MOVE IT", 750, 555, 20, "accent")},
    {"d": rect(1000, 490, 380, 110), "color": "muted", "width": 5, "start": C("everyday prices"), "label": lbl("PRICES: LATER", 1190, 555, 24, "muted")},
    {"d": rect(700, 680, 520, 110), "color": "accent3", "width": 7, "start": C("productive"), "label": lbl("A GOOD MEASURE OF PRODUCTIVITY", 960, 745, 24, "accent3")}],
    [{"kind": "point", "at": C("productive", 0.4), "dur": 1.3, "target": [960, 735]}], enter_from=2200, enter_to=1640)
# ====================================================================== STABILITY
card("d07_act2", "act2_card", "Stability", "Two centuries of predictability")
stage("d08_timeline", "stab_timeline", {
    "zones": [ALPS()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("calendar", x=330, y=280, at=0.2, scale=0.75, pages=[[0, "{{neutrality_1815.display}}", "NEUTRALITY"], [{"cue": "a new constitution"}, "{{constitution_1848.display}}", "FEDERAL STATE"]]),
              it("sign", x=960, y=230, text="NEUTRALITY RECOGNISED", sub="end of the Napoleonic wars", at=C("formally recognised"), color="#FFF59D", size=30),
              it("building", x=1450, style="gov", color="#ECEFF1", text="PARLIAMENT · GOVERNMENT · COURT", at=C("a parliament"), scale=0.6)],
    "callouts": [co("The first force: stability", 960, 960, C("The first force"), "gold", screen=True)]},
    sources=["admin_neutrality", "eda_neutrality", "parlament_constitution", "bar_new_authorities"])
stage("d09_eu_map", "stab_eu", {
    "zones": [Z("office")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("sign", x=480, y=260, text="NOT IN THE EU", at=C("not a member"), color="#FFCDD2", size=36),
              it("docs", x=960, y=F, at=C("bilateral agreements", -0.5), text="BILATERAL AGREEMENTS", stampAt=C("sector by sector"), stamp="SECTOR BY SECTOR", color="blue"),
              *crowd([1450, 1580], "read", at=C("negotiated"), tie=True)],
    "callouts": [co("An independent streak", 960, 150, C("independent streak"), "white", screen=True)]},
    sources=["eda_bilateral"])
board("p10_meaning", "stab_meaning", "Why predictability pays", C("capital hates surprises"), [
    {"d": rect(540, 340, 380, 110), "color": "accent2", "width": 5, "start": C("rules change slowly"), "label": lbl("RULES CHANGE SLOWLY", 730, 405, 24, "accent2")},
    {"d": rect(540, 480, 380, 110), "color": "accent2", "width": 5, "start": C("in public"), "label": lbl("…AND IN PUBLIC", 730, 545, 24, "accent2")},
    {"d": arrow((930, 470), (1060, 470)), "color": "ink", "width": 5, "start": C("can plan")},
    {"d": rect(1070, 330, 330, 80), "color": "accent3", "width": 5, "start": C("a factory"), "label": lbl("FACTORY", 1235, 380, 24, "accent3")},
    {"d": rect(1070, 430, 330, 80), "color": "accent3", "width": 5, "start": C("a laboratory"), "label": lbl("LABORATORY", 1235, 480, 24, "accent3")},
    {"d": rect(1070, 530, 330, 80), "color": "accent3", "width": 5, "start": C("savings account"), "label": lbl("SAVINGS", 1235, 580, 24, "accent3")},
    {"d": dot(960, 760), "color": "accent", "width": 1, "start": C("plan for decades"), "label": lbl("PLAN FOR DECADES", 960, 765, 40, "accent")}],
    [{"kind": "point", "at": C("plan for decades", 0.3), "dur": 1.3, "target": [960, 750]}])
# ====================================================================== MONEY
card("d11_act3", "act3_card", "Money", "Secrecy, safe haven and the franc")
stage("d12_1934", "money_1934", {
    "zones": [Z("vault")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 4,
    "items": [it("vaultdoor", x=1300, r=250, label="CLIENT SECRETS"),
              it("docs", x=500, y=F, at=C("federal banking law", -0.5), text="BANKING ACT {{banking_act_1934.display}}", stampAt=C("criminal offence"), stamp="CRIMINAL OFFENCE", color="red", scale=0.8),
              it("calendar", x=500, y=230, at=0.3, pages=[[0, "{{banking_act_1934.display}}", "NEW LAW"]], scale=0.6)],
    "callouts": [co("Before: civil law · now: prosecution", 960, 150, C("Before that"), "white", screen=True)]},
    sources=["iheid_banking_secrecy", "goldblum_secrecy"])
stage("d13_pressure", "money_pressure", {
    "zones": [Z("vault")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.0}], "drift": 4,
    "items": [it("vaultdoor", x=960, r=250, label="DISCRETION"),
              it("storm", x=[[0, 1800], [12, 1200]], y=150, at=C("pressure from abroad")),
              *crowd([300, 420, 1600], "point", at=C("pressure from abroad"), tie=True)],
    "callouts": [co("Privacy… or hiding money from governments?", 960, 960, C("hiding money"), "risk", screen=True)]})
stage("d14_aeoi", "money_aeoi", {
    "zones": [Z("office", -1600, 1500), Z("airport", 1500, 6000)], "worldW": 2600,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.0}, {"at": C("foreign tax"), "x": 1800, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("docs", x=600, y=F, at=0.2, text="ACCOUNT INFORMATION", stampAt=C("automatically shared"), stamp="SHARED", color="green", scale=0.8),
              it("counter", x=1100, y=260, at=C("first exchange"), steps=[[0, 0], [{"cue": "first exchange"}, 0], [{"cue": "first exchange", "offset": 2.5}, 2000000]], prefix="≈ ", text="accounts in the first exchange ({{aeoi_2018.year}})", scale=0.8),
              it("plane", x=[[0, 1600], [{"cue": "foreign tax"}, 1600], [{"cue": "foreign tax", "offset": 6}, 3200]], y=[[0, 700], [{"cue": "foreign tax", "offset": 6}, 200]], text="DATA", scale=0.6, tilt=-12)],
    "callouts": [co("The turning point came quietly", 960, 150, C("turning point"), "gold", screen=True)]},
    sources=["fta_aeoi_2018", "iheid_banking_secrecy"])
stage("d14b_haven", "money_haven", {
    "zones": [ALPS()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("storm", x=[[0, 300], [14, 500]], y=180, at=C("In times of crisis"), scale=1.2),
              it("coins", **{"from": [200, 300], "to": [1300, 600]}, at=C("park their wealth"), rate=6, shape="note"),
              it("sign", x=1300, y=330, text="SAFE HAVEN", sub="the Swiss franc", at=C("safe haven"), color="#C8E6C9", size=40)],
    "callouts": [co("Stable, and unlikely to inflate it away", 960, 960, C("politically stable"), "white", screen=True)]})
stage("d15_floor", "money_floor_2011", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.0}], "drift": 4,
    "items": [it("chart", x=960, y=360, w=900, h=420, at=0.3, dur=2.5, text="EURO IN FRANCS (schematic)", pts=[0.8, 0.6, 0.45, 0.35, 0.36]),
              it("sign", x=960, y=640, text="FLOOR: 1 EURO = {{snb_floor_2011.display}} FRANCS", sub="Swiss National Bank, 6 Sept 2011", at=C("line in the sand"), color="#FFF59D", size=30)],
    "callouts": [co("A strong currency makes exports pricier", 960, 960, C("strong currency"), "risk", screen=True, until=C("line in the sand", -0.3))]},
    sources=["ecb_snb_2011"])
stage("d16_floor_end", "money_floor_2015", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.0}], "drift": 4,
    "shake": [{"at": C("abandoned"), "dur": 1.6, "amp": 12}],
    "items": [it("chart", x=960, y=360, w=900, h=420, at=0.3, dur=2, text="EURO IN FRANCS (schematic)", pts=[0.5, 0.5, 0.5], crashAt=C("abandoned")),
              it("coins", **{"from": [300, 700], "to": [1700, 300]}, at=C("again and again"), until=C("abandoned"), rate=6, shape="note"),
              it("calendar", x=1600, y=640, at=C("abandoned", -0.4), pages=[[0, "15", "JANUARY 2015"]], scale=0.6)],
    "callouts": [co("Interventions of rapidly increasing size", 960, 150, C("rapidly increasing"), "white", screen=True, until=C("abandoned", -0.3)),
                 co("The floor is gone. The franc jumps.", 960, 150, C("abandoned"), "risk", screen=True)]},
    sources=["snb_speech_2015_04", "bis_jordan_2015", "swissinfo_floor_2015"])
stage("d16b_after", "money_after", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.0}], "drift": 4,
    "items": [it("stack", x=600, at=C("sold"), h=[[0, 20], [{"cue": "sold"}, 20], [{"cue": "sold", "offset": 2.5}, 520]], text="{{snb_fx_2024.sold_display}}", sub="foreign currency SOLD, 2023", color="#FFCDD2"),
              it("stack", x=1320, at=C("buying again"), h=[[0, 20], [{"cue": "buying again"}, 20], [{"cue": "buying again", "offset": 1.5}, 40]], text="{{snb_fx_2024.display}}", sub="BOUGHT, 2024", color="#C8E6C9")],
    "callouts": [co("The battle over the franc never ended", 960, 150, C("never really ended"), "gold", screen=True)]},
    sources=["swi_snb_2024"])
stage("d17_cs", "money_cs", {
    "zones": [Z("city", label="nochurch")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("tower", x=700, text="CREDIT SUISSE", color="#1E3A6E", crumbleAt=C("taken over"), scale=0.9),
              it("tower", x=1250, text="UBS", color="#E53935", at=0.2, h=[[0, 420], [{"cue": "taken over"}, 420], [{"cue": "taken over", "offset": 2}, 640]], scale=1.0),
              it("sign", x=1650, y=300, text="BACKED BY THE STATE + CENTRAL BANK", at=C("backed by"), color="#FFF59D", size=24)],
    "callouts": [co("{{cs_ubs_2023.month_spoken}}: a banking crisis", 960, 150, C("not immune"), "risk", screen=True)]},
    sources=["finma_cs_ubs", "efd_cs_timeline"])
# ====================================================================== SPECIALISATION
card("d18_act4", "act4_card", "Specialisation", "What the world finds hard to copy")
add("d19_ring", "spec_ring", "engine_chart", {"chart": "donut", "cx": 960, "cy": 610, "r": 240, "thick": 90, "start": C("chemical and pharmaceutical"),
    "data": [{"label": "Chemicals + pharmaceuticals", "value": 52.7, "display": "52.7%"}, {"label": "everything else", "value": 47.3, "display": "47.3%"}],
    "center": "{{pharma_share_2024.display}}", "centerSub": "of Swiss exports, 2024", "title": "What Switzerland ships abroad", "subtitle": "banks barely appear"},
    sources=["bazg_trade_2024"])
stage("d20_basel", "spec_basel", {
    "zones": [ALPS()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("tower", x=700, text="ROCHE", color="#1E88E5", at=C("Roche"), scale=0.95),
              it("tower", x=1250, text="NOVARTIS", color="#F57C00", at=C("Novartis"), scale=0.85),
              it("sign", x=960, y=180, text="BASEL · ON THE RHINE", sub="near France and Germany", at=C("Basel"), color="#FFF59D", size=32)],
    "callouts": [co("Global headquarters, both in Basel", 960, 960, C("global headquarters"), "white", screen=True)]},
    sources=["swissinfo_roche_hq"])
stage("d21_why", "spec_why", {
    "zones": [Z("fab")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("conveyor", x0=300, x1=1600, y=F - 30, goods="box", label="MEDICINE", n=7, speed=110),
              it("sign", x=480, y=260, text="LIGHT", at=C("they are light"), color="#C8E6C9", size=34),
              it("sign", x=960, y=260, text="VALUABLE", at=C("valuable"), color="#FFF59D", size=34),
              it("sign", x=1440, y=260, text="PATENTS + KNOW-HOW", at=C("patents"), color="#BBDEFB", size=30)],
    "callouts": [co("Not what is cheap to make: what is hard to copy", 960, 960, C("hard to copy"), "gold", screen=True)]})
stage("d21b_watches", "spec_watches", {
    "zones": [ALPS()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.05}], "drift": 4,
    "items": [it("watch", x=650, y=470, at=0.2, scale=0.9, text="SWISS WATCHES"),
              it("stack", x=1350, at=C("exports were worth"), h=[[0, 20], [{"cue": "exports were worth"}, 20], [{"cue": "exports were worth", "offset": 2.5}, 300]], text="{{watches_2024.display}}", sub="watch exports, 2024 ({{watches_2024.change_display}})", color="gold")],
    "callouts": [co("Small, light, expensive, hard to copy", 960, 150, C("same lesson"), "green", screen=True)]},
    sources=["swi_watches_2024"])
# ====================================================================== SKILLS
card("d22_act5", "act5_card", "Skills", "Classrooms and workshops")
stage("d23_vet", "skills_vet", {
    "zones": [Z("carplant", idle=0)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [*crowd([400, 520, 640, 1280, 1400, 1520], "cheer", at=C("young people"), hat="#FFC93C", scale=0.75),
              it("sign", x=520, y=300, text="2 IN 3 YOUNG PEOPLE", sub="vocational education + training", at=C("of young people"), color="#C8E6C9", size=30),
              it("sign", x=1400, y=300, text="CLASSROOM + REAL WORK", sub="apprenticeships", at=C("combine the classroom"), color="#BBDEFB", size=30)],
    "callouts": [co("Here, it is the mainstream", 960, 960, C("the mainstream"), "gold", screen=True)]},
    sources=["seri_vet"])
stage("d24_gii", "skills_gii", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 420, "zoom": 1.05}], "drift": 4,
    "items": [it("board", x=960, y=80, w=900, at=C("Skills feed ideas"), text="GLOBAL INNOVATION INDEX {{gii_2025_rank.year}}",
                 rows=[{"name": "1 · SWITZERLAND", "value": "#1", "color": "gold"}, {"name": "2 · SWEDEN", "value": ""}, {"name": "3 · UNITED STATES", "value": ""},
                       {"name": "4 · SOUTH KOREA", "value": ""}, {"name": "5 · SINGAPORE", "value": ""}])],
    "callouts": [co("{{gii_2025_rank.display}} economies (WIPO)", 960, 960, C("Global Innovation Index"), "gold", screen=True)]},
    sources=["wipo_gii_2025", "ige_gii_2025"])
stage("d24b_jobs", "skills_jobs", {
    "zones": [ALPS()], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}, {"at": C("cross-border commuters"), "x": 1450, "y": 480, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("counter", x=700, y=250, at=C("average unemployment"), steps=[[0, 0], [{"cue": "average unemployment"}, 0], [{"cue": "average unemployment", "offset": 2}, 2.4]], suffix="%", decimals=1, text="unemployment, 2024 average (SECO)", scale=0.85),
              it("person", x=[[0, 2600], [{"cue": "pull people in"}, 2600], [{"cue": "pull people in", "offset": 6}, 1300]], pose="walk", flip=True, at=C("pull people in"), scale=0.8, hair=1),
              it("person", x=[[0, 2800], [{"cue": "pull people in", "offset": 0.5}, 2800], [{"cue": "pull people in", "offset": 6.5}, 1450]], pose="walk", flip=True, at=C("pull people in"), scale=0.8, hair=3),
              it("person", x=[[0, 3000], [{"cue": "pull people in", "offset": 1}, 3000], [{"cue": "pull people in", "offset": 7}, 1600]], pose="walk", flip=True, at=C("pull people in"), scale=0.8, hair=4),
              it("sign", x=1600, y=280, text="{{crossborder_2024.display}} CROSS-BORDER COMMUTERS", sub="end of Sept 2024 (FSO) · most live in France, Italy, Germany", at=C("cross-border commuters"), color="#FFF59D", size=28)],
    "callouts": [co("Skills keep people in work", 960, 960, C("keep people in work"), "green", screen=True)]},
    sources=["swi_unemployment_2024", "swi_crossborder_2024"])
# ====================================================================== THE HIDDEN COSTS
card("d25_act6", "act6_card", "The Hidden Costs", "Prices, the franc and concentration")
stage("d26_prices", "cost_prices", {
    "zones": [Z("city", label="nochurch")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.05}], "drift": 4,
    "items": [it("letters", x=960, y=300, text="{{price_level_2024.display}}", at=C("highest price level"), size=150, color="risk"),
              it("sign", x=960, y=470, text="PRICE LEVEL · EU AVERAGE = 100", sub="highest of all countries compared by Eurostat, 2024", at=C("highest price level", 0.4), size=28),
              *crowd([500, 1420], "worry", at=C("Success is expensive"))],
    "callouts": [co("Success is expensive, literally", 960, 960, C("Success is expensive"), "risk", screen=True)]},
    sources=["eurostat_price_levels", "bluewin_price_2024"])
board("p27_franc", "cost_franc", "When a safe haven hurts", C("High prices"), [
    {"d": rect(540, 340, 300, 100), "color": "accent2", "width": 5, "start": C("High prices"), "label": lbl("HIGH PRICES", 690, 400, 26, "accent2")},
    {"d": rect(540, 480, 300, 100), "color": "accent2", "width": 5, "start": C("a strong franc"), "label": lbl("STRONG FRANC", 690, 540, 26, "accent2")},
    {"d": arrow((850, 460), (1010, 460)), "color": "ink", "width": 5, "start": C("squeeze")},
    {"d": rect(1020, 410, 340, 100), "color": "risk", "width": 6, "start": C("compete from Switzerland"), "label": lbl("EXPORTERS SQUEEZED", 1190, 470, 24, "risk")},
    {"d": dot(960, 700), "color": "accent", "width": 1, "start": C("central bank was fighting"), "label": lbl("WHAT THE CENTRAL BANK FOUGHT, 2011–2015", 960, 705, 26, "accent")},
    {"d": dot(960, 820), "color": "risk", "width": 1, "start": C("the bill arrives"), "label": lbl("A PRIVILEGE… BILLED TO EXPORTERS", 960, 825, 30, "risk")}],
    [{"kind": "point", "at": C("the bill arrives", 0.3), "dur": 1.3, "target": [960, 810]}], enter_from=2200, enter_to=1640)
stage("d27b_tariff", "cost_tariff", {
    "zones": [Z("port", -1600, 1600), Z("airport", 1600, 6000)], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 500, "zoom": 1.0}, {"at": C("In November"), "x": 1900, "y": 500, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("barrier", x=1150, at=0.2, closeAt=C("faced a tariff"), openAt=C("would fall"), text="U.S. TARIFF"),
              it("ship", x=[[0, 300], [{"cue": "faced a tariff"}, 900], [{"cue": "would fall", "offset": 1}, 900], [{"cue": "would fall", "offset": 9}, 2600]], scale=0.5, flag="SWISS GOODS"),
              it("sign", x=1150, y=330, text="39%", sub="from 7 August 2025", at=C("faced a tariff"), until=C("would fall"), color="#FFCDD2", size=56),
              it("sign", x=1150, y=330, text="15%", sub="November 2025 · in line with the EU", at=C("would fall"), color="#C8E6C9", size=56),
              it("sign", x=2200, y=300, text="{{tariff_2025.invest_display}} PLANNED", sub="Swiss investment in the U.S. by end-2028", at=C("Swiss companies planned"), color="#FFF59D", size=28)],
    "callouts": [co("Swiss government: unjustified, a heavy burden", 960, 150, C("called it unjustified"), "white", screen=True, until=C("In November", -0.3)),
                 co("A non-binding memorandum", 960, 150, C("non-binding"), "gold", screen=True)]},
    sources=["kmu_tariff_2025", "swi_tariff15_2025"])
stage("d28_concentration", "cost_concentration", {
    "zones": [ALPS()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.0}], "drift": 4,
    "items": [it("tower", x=700, text="PHARMA {{pharma_share_2024.display}}", color="#1E88E5", at=0.2, scale=1.1),
              *[it("building", x=1150 + k * 230, style="office", color=["#C8E6C9", "#FFE0B2", "#E1BEE7"][k], text="", scale=0.45, at=0.4) for k in range(3)],
              it("storm", x=[[0, 1600], [10, 800]], y=150, at=C("a shock to that industry")),
              it("sign", x=1400, y=230, text="A GREAT FINANCIAL CENTRE = A NATIONAL RISK", at=C("Credit Suisse rescue"), color="#FFCDD2", size=24)],
    "callouts": [co("Concentration cuts both ways", 960, 960, C("cuts both ways"), "risk", screen=True)]},
    sources=["bazg_trade_2024", "finma_cs_ubs"])
# ====================================================================== CONCLUSION
card("d29_act7", "act7_card", "Conclusion", "Built, not found")
stage("d30_close", "close", {
    "zones": [ALPS()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 420, "zoom": 1.2}, {"at": C("Stability that investors"), "x": 960, "y": 500, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("sign", x=480, y=260, text="STABILITY", at=C("Stability that investors"), color="#BBDEFB", size=34, hang=True, swing=True),
              it("sign", x=1440, y=260, text="A FINANCE SECTOR REINVENTED", at=C("A financial system"), color="#FFF59D", size=28, hang=True, swing=True),
              it("sign", x=480, y=520, text="HARD-TO-COPY PRODUCTS", at=C("Specialisation in products"), color="#C8E6C9", size=28),
              it("sign", x=1440, y=520, text="SKILLS", at=C("And skills"), color="#E1BEE7", size=34),
              it("sign", x=960, y=700, text="THE PRICE: STRONG FRANC · HIGH PRICES · FEW GIANTS", at=C("the price of the model"), color="#FFCDD2", size=24),
              it("letters", x=960, y=380, text="?", at=C("The question for the next decade"), size=120, color="gold")],
    "callouts": [co("Not what lies under the ground, but what it built", 960, 960, C("Not because"), "gold", screen=True, until=C("Stability that investors", -0.3))]})

write(OUT, "# GENERATED by tools/gen_switzerland_cartoon_storyboard.py; edit the generator, not this file.\n"
           "# Switzerland storyboard in bespoke CartoonStage worlds + four presenter boards (Remotion).\n")
