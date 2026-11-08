"""Generates projects/the-hidden-business-of-formula-1/deliverables/documentary/storyboard.yaml (Episode 03, cartoon redo).

Bespoke CartoonStage worlds for Formula One: a circuit with a grandstand of waving fans and generic boards (text only, no
logos), cartoon race cars and motorbikes, the pit lane with team garages, a fan's living room where the TV shows the race,
host cities, the stock-exchange floor for the big deals. Four presenter boards replace the earlier whiteboards (the sport
in one drawing, the business model, the three pots, the host-city deal). The race-track, circuit-map, chart and map scenes
of the first cut are kept from tools/data/f1_storyboard_v1.yaml. Narration and figures are unchanged.
Run: python tools/gen_f1_cartoon_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "projects/the-hidden-business-of-formula-1/deliverables/documentary/storyboard.yaml"
BASE = {s["id"]: s for s in yaml.safe_load((ROOT / "tools/data/f1_storyboard_v1.yaml").read_text())["scenes"]}
CARDS = {s["id"]: s for s in BASE.values() if s["type"] == "act_title"}
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
TRACK = lambda x0=-1600, x1=4600, **kw: Z("circuit", x0, x1, **kw)
CARS = lambda n=3, sp=900, **kw: [it("racecar", loop=sp, phase=k * 700, color=["#E53935", "#1E88E5", "#FF9800", "#00897B", "#7E57C2"][k % 5], text=str(k + 1), **kw) for k in range(n)]


def keep(*ids):
    for i in ids:
        cartoon_kit.scenes.append(BASE[i])


def kcard(id_):
    p = CARDS[id_]["params"]
    card(id_, CARDS[id_]["segment"], p["title"], p["subtitle"])


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
keep("s01_hook")
stage("s02_revenue", "open_revenue", {
    "zones": [TRACK()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.05}], "drift": 4,
    "items": [*CARS(3), it("counter", x=960, y=230, at=0.3, steps=[[0, 0], [0.5, 0], [3.0, 3.87]], prefix="$", suffix="bn", decimals=2, text="Formula One revenue, 2025")],
    "callouts": [co("{{f1_revenue_2025.growth_display}} in a year", 960, 960, C("more than the year before"), "green", screen=True, size=42)]},
    sources=["liberty_fy2025"])
stage("s03_question", "open_question", {
    "zones": [TRACK()], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.1}, {"at": C("line up to host"), "x": 960, "y": 470, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [*CARS(2, 700), it("letters", x=480, y=250, text="WHO PAYS?", at=C("Who pays"), size=70, color="gold"),
              it("letters", x=1450, y=250, text="WHO GETS PAID?", at=C("who gets paid"), size=70, color="green")],
    "callouts": [co("Why do cities line up to host a race?", 960, 960, C("line up to host"), "white", screen=True, size=40)]})
kcard("s04_p1")
board("p05_sketch", "p1_sketch", "Formula One, in one drawing", C("A handful of teams"), [
    {"d": rect(560, 380, 250, 100), "color": "accent2", "width": 5, "start": C("A handful of teams"), "label": lbl("TEAMS", 685, 440, 30, "accent2")},
    {"d": arrow((820, 430), (950, 430)), "color": "ink", "width": 4, "start": C("design their own")},
    {"d": rect(960, 380, 250, 100), "color": "accent2", "width": 5, "start": C("design their own", 0.3), "label": lbl("OWN CARS", 1085, 440, 30, "accent2")},
    {"d": arrow((1220, 430), (1350, 430)), "color": "ink", "width": 4, "start": C("race them")},
    {"d": "M 1440 430 m -80 0 a 80 50 0 1 0 160 0 a 80 50 0 1 0 -160 0", "color": "accent3", "width": 5, "start": C("race them", 0.3), "label": lbl("RACE THE WORLD", 1440, 520, 24, "accent3")},
    {"d": rect(760, 640, 560, 130), "color": "accent", "width": 7, "start": C("packaged and sold"), "label": lbl("THE SHOW, PACKAGED + SOLD", 1040, 715, 32, "accent")},
    {"d": arrow((1040, 560), (1040, 630)), "color": "accent", "width": 5, "start": C("The business began")}],
    [{"kind": "point", "at": C("packaged and sold", 0.4), "dur": 1.4, "target": [1040, 700]}])
stage("s06_history", "p1_history", {
    "zones": [Z("den", -1600, 1500, cx=760), TRACK(1500, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.05}, {"at": C("CVC took"), "x": 2300, "y": 500, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("person", x=380, pose="cheer", at=0.2, scale=0.85, hair=2),
              it("sign", x=760, y=180, text="SOLD TO TV AS ONE PACKAGE", at=C("one package"), color="#FFF59D", size=30),
              it("calendar", x=1850, y=260, at=C("CVC took"), pages=[[0, "{{cvc_2006.display}}", "CVC IN CHARGE"]], scale=0.7),
              it("sign", x=2450, y=260, text="16 → 22 RACES", sub="according to CVC", at=C("the calendar grew"), color="#C8E6C9", size=40),
              *CARS(2, 800, x0=1500, x1=4500)],
    "callouts": [co("Bernie Ecclestone sold the sport to TV", 960, 150, C("sold the sport"), "white", screen=True, until=C("CVC took", -0.3)),
                 co("2006: the investment firm CVC takes control", 960, 150, C("CVC took"), "gold", screen=True)]},
    sources=["liberty_close_2017", "cvc_case"])
stage("s07_liberty", "p1_liberty", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.05}], "drift": 4,
    "items": [it("counter", x=960, y=260, at=0.3, steps=[[0, 0], [{"cue": "valuing the business"}, 0], [{"cue": "valuing the business", "offset": 2.5}, 8.0]], prefix="$", suffix="bn", decimals=1, text="value including debt ({{liberty_deal.year_display}})"),
              it("sign", x=480, y=560, text="LIBERTY MEDIA", sub="American media company", at=C("Liberty Media"), color="#BBDEFB", size=32),
              it("calendar", x=1500, y=560, at=C("The deal closed"), pages=[[0, "2017", "DEAL CLOSES"]], scale=0.7)],
    "callouts": [co("A new era begins", 960, 960, C("a new era"), "gold", screen=True, size=42)]},
    sources=["liberty_deal_2016", "liberty_close_2017"])
kcard("s08_p2")
stage("s09_layers", "p2_layers", {
    "zones": [Z("pitlane")], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 0.95}, {"at": C("Liberty's own filings"), "x": 1200, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("building", x=420, style="gov", color="#ECEFF1", text="FIA · RULES", at=C("The FIA"), scale=0.6),
              it("building", x=1100, style="office", color="#FFCDD2", text="FORMULA ONE · SELLS THE SHOW", at=C("holds the commercial"), scale=0.6),
              it("sign", x=1100, y=260, text="OWNED BY LIBERTY MEDIA", at=C("owned by Liberty"), color="#BBDEFB", size=26),
              *crowd([1700, 1820, 1940], "cheer", at=C("the teams compete"), color="#E53935"),
              it("sign", x=1820, y=420, text="TEAMS · SHARE THE MONEY", at=C("sharing in the money"), color="#C8E6C9", size=26),
              it("sign", x=1200, y=160, text="FIA: SAFETY + SPORT FIRST", at=C("safety and sporting"), color="#FFF59D", size=30)],
    "callouts": [co("Three layers", 960, 960, C("three layers"), "gold", screen=True, size=44)]},
    sources=["liberty_10k_2025"])
stage("s10_motogp", "p2_motogp", {
    "zones": [TRACK(boards=["MOTOGP", "SPONSOR", "MOTOGP", "BRAND"])], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}], "drift": 4,
    "items": [it("racecar", loop=1000, bike=True, color="#1E88E5"), it("racecar", loop=1000, bike=True, phase=900, color="#FF9800"),
              it("racecar", loop=800, phase=1600, color="#E53935"),
              it("sign", x=960, y=230, text="TWO WORLD SERIES, ONE OWNER", at=C("Two world series"), color="#FFF59D", size=36)],
    "callouts": [co("{{liberty_motogp.display}}: Liberty buys most of MotoGP", 960, 960, C("MotoGP"), "white", screen=True)]},
    sources=["liberty_fy2025"])
kcard("s11_p3")
board("p12_sketch", "p3_sketch", "The business model", C("In the middle"), [
    {"d": rect(860, 470, 300, 140), "color": "accent", "width": 7, "start": C("In the middle"), "label": lbl("FORMULA ONE", 1010, 550, 34, "accent")},
    {"d": rect(520, 300, 240, 90), "color": "accent2", "width": 5, "start": C("from broadcasters"), "label": lbl("BROADCASTERS", 640, 355, 24, "accent2")},
    {"d": arrow((760, 360), (880, 470), 0.1), "color": "accent2", "width": 5, "start": C("from broadcasters", 0.3)},
    {"d": rect(520, 500, 240, 90), "color": "accent2", "width": 5, "start": C("race promoters"), "label": lbl("PROMOTERS", 640, 555, 24, "accent2")},
    {"d": arrow((770, 545), (850, 545)), "color": "accent2", "width": 5, "start": C("race promoters", 0.3)},
    {"d": rect(520, 700, 240, 90), "color": "accent2", "width": 5, "start": C("from sponsors"), "label": lbl("SPONSORS", 640, 755, 24, "accent2")},
    {"d": arrow((760, 740), (880, 610), -0.1), "color": "accent2", "width": 5, "start": C("from sponsors", 0.3)},
    {"d": arrow((1170, 540), (1350, 540)), "color": "accent3", "width": 7, "start": C("flows back out")},
    {"d": rect(1360, 490, 240, 100), "color": "accent3", "width": 6, "start": C("to the teams"), "label": lbl("THE TEAMS", 1480, 550, 28, "accent3")}],
    [{"kind": "point", "at": C("flows back out", 0.3), "dur": 1.3, "target": [1480, 540]}], enter_from=2200, enter_to=1700,
    sources=["liberty_10k_2025", "liberty_fy2025"])
keep("s13_mix", "s14_growth")
kcard("s15_p4")
stage("s16_media", "p4_media", {
    "zones": [Z("den", -1600, 1700, cx=900), Z("exchange", 1700, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("its own streaming"), "x": 2300, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [*crowd([480, 600], "cheer", at=0.2, scale=0.8),
              it("counter", x=900, y=160, at=C("By our calculation"), steps=[[0, 0], [{"cue": "By our calculation"}, 0], [{"cue": "By our calculation", "offset": 2.5}, 1.21]], prefix="≈ $", suffix="bn", decimals=2, text="media rights, 2025 (our calculation)"),
              it("browser", x=2300, y=430, at=C("its own streaming"), url="f1-streaming.tv", w=620, h=380, page="price", text="WATCH LIVE", button="SUBSCRIBE", scale=0.85)],
    "callouts": [co("Broadcasters pay to show every session", 960, 960, C("Broadcasters pay"), "white", screen=True, until=C("its own streaming", -0.3)),
                 co("…and F1 sells its own streaming service", 960, 960, C("its own streaming"), "gold", screen=True)]},
    sources=["liberty_10k_2025", "liberty_fy2025"])
stage("s17_apple", "p4_apple", {
    "zones": [Z("den", cx=960)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 4,
    "items": [it("sign", x=960, y=150, text="EXCLUSIVE U.S. BROADCASTER", sub="Apple · {{apple_deal.years_display}} · from {{apple_deal.from_display}}", at=C("exclusive broadcaster"), color="#ECEFF1", size=32),
              it("stack", x=1550, at=C("reportedly"), h=[[0, 20], [{"cue": "reportedly"}, 20], [{"cue": "reportedly", "offset": 2}, 160]], text="{{apple_deal.display}}", sub="reported, not disclosed", color="gold"),
              *crowd([380], "cheer", at=0.3)],
    "callouts": [co("The biggest new deal: America", 960, 960, C("biggest new deal"), "gold", screen=True)]},
    sources=["apple_f1_2025", "cnbc_apple_value"])
keep("s18_audience")
kcard("s19_p5")
keep("s20_fees")
stage("s21_governments", "p5_governments", {
    "zones": [Z("tropic", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.05}], "drift": 4,
    "items": [*CARS(2, 900), it("sign", x=480, y=230, text="SINGAPORE NIGHT RACE", sub="2022", at=C("In Singapore"), color="#FFF59D", size=32),
              it("stack", x=1250, at=C("cost"), h=[[0, 20], [{"cue": "cost"}, 20], [{"cue": "cost", "offset": 2}, 300]], text="{{singapore_2022.display}}", sub="to stage the race"),
              it("stack", x=1600, at=C("government covered"), h=[[0, 20], [{"cue": "government covered"}, 20], [{"cue": "government covered", "offset": 2}, 180]], text="{{singapore_2022.gov_display}}", sub="paid by the government", color="#FFCC80")],
    "callouts": [co("Fees are almost never published", 960, 960, C("almost never published"), "white", screen=True, until=C("In Singapore", -0.3)),
                 co("Often, governments pay", 960, 960, C("In Singapore"), "gold", screen=True)]},
    sources=["mti_singapore_2023", "fed_h10"])
keep("s22_vegas")
kcard("s23_p6")
stage("s24_sponsors", "p6_sponsors", {
    "zones": [TRACK(boards=["LVMH · 10 YEARS", "ARAMCO", "SPONSOR", "YOUR BRAND HERE"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("Aramco joined"), "x": 1500, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [*CARS(3, 1000, x1=4000), it("chart", x=700, y=330, w=560, h=300, at=0.3, dur=2.5, text="SPONSORSHIP SHARE", pts=[0.45, 0.62]),
              it("sign", x=700, y=550, text="{{revenue_mix_2025.spons_prev_display}} → {{revenue_mix_2025.spons_display}}", at=C("up from"), color="#C8E6C9", size=32),
              it("sign", x=1500, y=300, text="LVMH: {{lvmh_deal.display}}", sub="global partnership", at=C("LVMH"), color="#FFF59D", size=32),
              it("sign", x=1950, y=420, text="ARAMCO: {{aramco_deal.display}}", sub="the audience F1 promised", at=C("Aramco joined"), color="#BBDEFB", size=30)],
    "callouts": [co("Sponsorship: growing fast", 960, 960, C("growing fast"), "gold", screen=True)]},
    sources=["liberty_10k_2025", "f1_lvmh_2024", "f1_aramco_2020"])
keep("s25_hospitality")
kcard("s26_p7")
keep("s27_payments")
stage("s28_own", "p7_own", {
    "zones": [Z("pitlane", teams=["MERCEDES", "TEAM B", "TEAM C"])], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}], "drift": 4,
    "items": [it("racecar", x=480, y=F + 70, color="#90A4AE", text="1", at=0.3),
              it("sign", x=480, y=250, text="LOGOS: CAR · OVERALLS · GARAGE", at=C("their own sponsors"), color="#FFF59D", size=26),
              it("stack", x=1150, at=C("reported revenue"), h=[[0, 20], [{"cue": "reported revenue"}, 20], [{"cue": "reported revenue", "offset": 2}, 400]], text="{{mercedes_2024.display}}", sub="Mercedes team revenue, 2024"),
              it("sign", x=1150, y=330, text="{{mercedes_2024.spons_display}} SPONSORS + LICENSING", at=C("sponsorship and licensing"), color="#C8E6C9", size=24),
              it("stack", x=1650, at=C("Its profit"), h=[[0, 20], [{"cue": "Its profit"}, 20], [{"cue": "Its profit", "offset": 2}, 90]], text="{{mercedes_2024.profit_display}}", sub="profit", color="gold")],
    "callouts": [co("Second: their own sponsors", 960, 960, C("Second"), "white", screen=True)]},
    sources=["blackbook_mercedes_2024", "fed_h10"])
board("p29_pots", "p7_pots", "Three pots of money", C("three pots"), [
    {"d": "M 600 420 L 620 640 L 820 640 L 840 420 Z", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.2, "start": C("Formula One's own"), "label": lbl("F1'S REVENUE", 720, 540, 26, "accent")},
    {"d": "M 900 420 L 920 640 L 1120 640 L 1140 420 Z", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.2, "start": C("The teams' revenue"), "label": lbl("TEAMS' REVENUE", 1020, 540, 24, "accent2")},
    {"d": "M 1200 420 L 1220 640 L 1420 640 L 1440 420 Z", "color": "accent3", "width": 6, "fill": "accent3", "fillOpacity": 0.2, "start": C("the promoters"), "label": lbl("PROMOTERS", 1320, 540, 26, "accent3")},
    {"d": dot(1320, 720), "color": "muted", "width": 1, "start": C("hosting fee"), "label": lbl("pay the fee · sell the tickets", 1320, 725, 22, "muted")},
    {"d": "M 860 380 L 860 700 M 1170 380 L 1170 700", "color": "risk", "width": 5, "dash": "12 10", "start": C("apart")}],
    [{"kind": "point", "at": C("the promoters", 0.3), "dur": 1.3, "target": [1320, 540]}], enter_from=2200, enter_to=1650)
kcard("s30_p8")
keep("s31_cap")
stage("s32_breach", "p8_breach", {
    "zones": [Z("office")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 4,
    "items": [it("docs", x=700, y=F, at=0.3, text="RED BULL RACING · 2021 SPEND", stampAt=C("went over"), stamp="OVER BY {{redbull_breach.over_display}}", color="red"),
              it("sign", x=1350, y=300, text="{{redbull_breach.display}}", at=C("fine"), color="#FFCDD2", size=40),
              it("sign", x=1350, y=480, text="{{redbull_breach.aero_display}}", at=C("less aerodynamic"), color="#FFCDD2", size=34),
              it("gavel", x=1350, y=F - 20, hits=[C("The penalty"), C("The penalty", 0.8)], scale=1.1)],
    "callouts": [co("The cap has teeth", 960, 150, C("has teeth"), "risk", screen=True, size=44)]},
    sources=["fia_rbr_2022", "autosport_rbr_2022"])
stage("s33_values", "p8_values", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.0}], "drift": 4,
    "items": [it("stack", x=600, at=C("average team"), h=[[0, 20], [{"cue": "average team"}, 20], [{"cue": "average team", "offset": 2}, 300]], text="{{forbes_values.display}}", sub="average team value (Forbes)"),
              it("stack", x=1300, at=C("Ferrari on top"), h=[[0, 20], [{"cue": "Ferrari on top"}, 20], [{"cue": "Ferrari on top", "offset": 2.5}, 540]], text="{{forbes_values.top_display}}", sub="Ferrari, the most valuable", color="gold")],
    "callouts": [co("Teams now look like profitable franchises", 960, 150, C("profitable franchises"), "white", screen=True)]},
    sources=["forbes_teams_2025"])
stage("s34_entry", "p8_entry", {
    "zones": [Z("pitlane", teams=["TEAM 1", "TEAM 2", "TEAM 3", "TEAM 4", "TEAM 5"])], "worldW": 2600,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 0.95}, {"at": C("more than double"), "x": 1400, "y": 500, "zoom": 0.9, "dur": 2.4}], "drift": 0,
    "items": [it("racecar", x=[[0, -400], [{"cue": "eleventh team"}, -400], [{"cue": "eleventh team", "offset": 3}, 500]], color="#263238", text="11"),
              it("sign", x=500, y=250, text="CADILLAC: TEAM NO. 11", at=C("eleventh team"), color="#ECEFF1", size=32),
              it("coins", **{"from": [600, 600], "to": [2200, 400]}, at=C("agreed to pay"), rate=6),
              it("sign", x=1600, y=230, text="{{cadillac_entry.display}}", sub="reported · old rules: {{cadillac_entry.old_display}}", at=C("agreed to pay"), color="#FFF59D", size=36)],
    "callouts": [co("Prize money shared eleven ways", 960, 960, C("eleven ways"), "white", screen=True)]},
    sources=["f1_cadillac_2025", "theRace_antidilution"])
kcard("s35_p9")
stage("s36_fans", "p9_fans", {
    "zones": [TRACK()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 450, "zoom": 1.1}, {"at": C("are women"), "x": 960, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [*CARS(3), it("counter", x=960, y=220, at=C("fans last year", -1.0), steps=[[0, 0], [{"cue": "fans last year", "offset": -1.0}, 0], [{"cue": "fans last year", "offset": 1.5}, 827]], suffix="m fans", text="2025, according to Formula One"),
              it("sign", x=1500, y=560, text="{{fanbase_2025.female_display}} WOMEN", at=C("are women"), color="#F8BBD0", size=36)],
    "callouts": [co("{{fanbase_2025.growth_display}}", 960, 960, C("since twenty eighteen"), "green", screen=True, size=40)]},
    sources=["f1_2025_numbers"])
keep("s37_why")
kcard("s38_p10")
stage("s39_netflix", "p10_netflix", {
    "zones": [Z("den", -1600, 1600, cx=800), Z("exchange", 1600, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.05}, {"at": C("Then came Hollywood"), "x": 2300, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [*crowd([380, 500], "cheer", at=C("Drive to Survive")),
              it("sign", x=800, y=160, text="DRIVE TO SURVIVE", sub="Netflix · {{dts_2019.display}}", at=C("Drive to Survive"), color="#FFCDD2", size=36),
              it("sign", x=1300, y=300, text="SOCIAL MEDIA + STREAMING", at=C("social media"), color="#BBDEFB", size=28),
              it("stack", x=2300, at=C("box office"), h=[[0, 20], [{"cue": "box office"}, 20], [{"cue": "box office", "offset": 2}, 320]], text="{{f1_movie.display}}", sub="box office, the F1 movie", color="gold")],
    "callouts": [co("Drivers and team bosses became characters", 960, 960, C("turned drivers"), "white", screen=True, until=C("Then came Hollywood", -0.3)),
                 co("Then came Hollywood", 960, 960, C("Then came Hollywood"), "gold", screen=True)]},
    sources=["f1_dts_2019", "boxofficemojo_f1", "liberty_close_2017"])
keep("s40_map")
kcard("s41_p11")
board("p42_sketch", "p11_sketch", "The host-city deal", C("On one side"), [
    {"d": "M 960 320 L 960 820", "color": "ink", "width": 4, "start": C("two sides")},
    {"d": dot(720, 350), "color": "accent3", "width": 1, "start": C("On one side"), "label": lbl("WHAT THE CITY GETS", 720, 355, 28, "accent3")},
    {"d": rect(580, 420, 280, 70), "color": "accent3", "width": 5, "start": C("global audience"), "label": lbl("GLOBAL AUDIENCE", 720, 465, 22, "accent3")},
    {"d": rect(580, 520, 280, 70), "color": "accent3", "width": 5, "start": C("full hotels"), "label": lbl("FULL HOTELS", 720, 565, 22, "accent3")},
    {"d": rect(580, 620, 280, 70), "color": "accent3", "width": 5, "start": C("famous name"), "label": lbl("A FAMOUS NAME", 720, 665, 22, "accent3")},
    {"d": dot(1200, 350), "color": "risk", "width": 1, "start": C("On the other"), "label": lbl("WHAT IT PAYS", 1200, 355, 28, "risk")},
    {"d": rect(1060, 420, 280, 70), "color": "risk", "width": 5, "start": C("the fee"), "label": lbl("THE FEE", 1200, 465, 22, "risk")},
    {"d": rect(1060, 520, 280, 70), "color": "risk", "width": 5, "start": C("the track"), "label": lbl("THE TRACK", 1200, 565, 22, "risk")},
    {"d": rect(1060, 620, 280, 70), "color": "risk", "width": 5, "start": C("disruption"), "label": lbl("WEEKS OF DISRUPTION", 1200, 665, 20, "risk")}],
    [{"kind": "point", "at": C("disruption", 0.3), "dur": 1.2, "target": [1200, 650]}], enter_from=2200, enter_to=1650, min_s=13.0)
stage("s43_costs", "p11_costs", {
    "zones": [Z("city", -1600, 1500, label="nochurch"), Z("tropic", 1500, 6000, night=True)], "worldW": 3000,
    "cam": [{"at": 0, "x": 760, "y": 500, "zoom": 1.0}, {"at": C("In Las Vegas"), "x": 2250, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("stack", x=760, at=C("Victorian taxpayers"), h=[[0, 20], [{"cue": "Victorian taxpayers"}, 20], [{"cue": "Victorian taxpayers", "offset": 2}, 220]], text="{{australia_2024.display}}", sub="Australian GP 2024: cost to taxpayers", color="#FFCDD2"),
              it("stack", x=2100, at=C("economic impact"), h=[[0, 20], [{"cue": "economic impact"}, 20], [{"cue": "economic impact", "offset": 2.5}, 480]], text="{{vegas_impact_2024.display}}", sub="Las Vegas impact (study paid for by F1)", color="gold"),
              it("stack", x=2500, at=C("direct taxes"), h=[[0, 20], [{"cue": "direct taxes"}, 20], [{"cue": "direct taxes", "offset": 2}, 80]], text="{{vegas_impact_2024.tax_display}}", sub="direct taxes")],
    "callouts": [co("The bills can be large", 960, 150, C("bills can be large"), "risk", screen=True)]},
    sources=["aap_agp_2024", "fed_h10", "lvgp_impact_2024"])
stage("s44_doubt", "p11_doubt", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.0}, {"at": C("local businesses"), "x": 1450, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [*crowd([480, 620], "read", at=0.2, glasses=True),
              it("docs", x=1000, y=F, at=C("Independent studies"), text="PROMISED BENEFITS", stampAt=C("exaggerated"), stamp="EXAGGERATED", color="red"),
              it("sign", x=1000, y=230, text="AUDITOR (2005 RACE): COSTS > BENEFITS", at=C("Auditor-General"), color="#FFCDD2", size=26),
              it("sign", x=1850, y=330, text="LAS VEGAS: {{vegas_settle.display}}", sub="local businesses complained of lost trade", at=C("local businesses"), color="#FFF59D", size=28)],
    "callouts": [co("Economists are sceptical", 960, 150, C("Economists are sceptical"), "risk", screen=True)]},
    sources=["matheson_2006", "vago_2007", "vegas_settle_2025"])
kcard("s45_p12")
stage("s46_risks", "p12_risks", {
    "zones": [TRACK(night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.0}, {"at": C("Rights groups"), "x": 1450, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("barrier", x=600, at=0.2, closeAt=C("called off"), text="BAHRAIN · SAUDI"),
              it("storm", x=[[0, 1200], [14, 700]], y=150, at=C("conflict")),
              it("chart", x=1300, y=360, w=520, h=300, at=C("Fewer races"), dur=1.2, text="F1 REVENUE, H1 2026", pts=[0.7, 0.75], crashAt=C("revenue fell")),
              it("sign", x=1300, y=600, text="{{h1_2026.display}}", at=C("revenue fell"), color="#FFCDD2", size=40),
              it("sign", x=1900, y=300, text="“SPORTSWASHING”", sub="rights groups' accusation", at=C("Rights groups"), color="#FFF59D", size=30),
              it("sign", x=1900, y=500, text="RECESSION → SPONSORS CUT", at=C("sponsors cut"), color="#ECEFF1", size=26)],
    "callouts": [co("Two races called off this spring", 960, 960, C("called off"), "risk", screen=True)]},
    sources=["gulf_cancel_2026", "liberty_q2_2026", "hrw_2020", "liberty_10k_2025"])
keep("s47_opps", "s48_outro")

write(OUT, "# GENERATED by tools/gen_f1_cartoon_storyboard.py; edit the generator, not this file.\n"
           "# Episode 03 storyboard in bespoke CartoonStage worlds + four presenter boards; race scenes kept.\n")
