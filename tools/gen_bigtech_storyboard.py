"""Generates projects/how-big-tech-really-makes-money-from-ai/deliverables/documentary/storyboard.yaml (Episode 28,
How Big Tech Really Makes Money From AI).

First episode built on the diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md):
- a different visual LANGUAGE per part: typography + isometric data centers (hook), full-screen data charts (part 1),
  the data-center campus (part 2), the cartoon internet with browsers and phones (part 3), an evidence board with red
  string (part 4), a dark studio with chips (part 5);
- fewer bottom-centre callouts: many scenes carry text on objects, at the top, or with a tail; varied camera moves;
- the hook is four short beats (cold open on the number), no separate part-question scenes, channel intro after part 1.
New engine pieces: `studio` and `corkboard` sets; `bigchart`, `pinboard` and `isodc` items.
No company logos (names in text only), no real UI, no likeness of real people.
Run: python tools/gen_bigtech_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-big-tech-really-makes-money-from-ai/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
CO = ["#2F6FD1", "#E89A00", "#23995A", "#7E57C2"]  # Amazon, Alphabet, Microsoft, Meta (neutral colours, not brand colours)


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def chart(bars, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars, at=at, **kw)


# ====================================================================== HOOK (4 beats, cold open)
stage("s01_open", "h_open", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.3}, {"at": 1.2, "x": 960, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("counter", x=960, y=300, at=0.05, prefix="≈ $", suffix="bn", steps=[[0.05, 0], [1.6, 200]], text="SPENT IN 3 MONTHS", scale=1.6),
              it("isodc", x=960, y=640, at=1.4, n=9, step=0.18, cols=3, scale=0.8, glow=True)]},
    sources=["msft_q1", "goog_q3", "amzn_q3", "meta_call"])
stage("s02_who", "h_who", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}, {"at": C("Much of that money"), "x": 960, "y": 560, "zoom": 1.08, "dur": 2.0}], "drift": 1,
    "items": [it("sign", x=330, y=300, text="MICROSOFT", at=C("Microsoft"), color="#C8E6C9", size=64),
              it("sign", x=770, y=300, text="ALPHABET", sub="owner of Google", at=C("Alphabet"), color="#FFE0B2", size=64),
              it("sign", x=1180, y=300, text="AMAZON", at=C("Amazon"), color="#BBDEFB", size=64),
              it("sign", x=1590, y=300, text="META", sub="Facebook · Instagram", at=C("And Meta"), color="#E1BEE7", size=64),
              it("isodc", x=960, y=700, at=0.3, n=9, step=0.25, cols=3, scale=0.75, glow=True),
              it("letters", x=960, y=520, text="DATA CENTERS + AI CHIPS", at=C("Much of that money"), size=70, color="gold")]},
    sources=["msft_call"])
stage("s03_question", "h_question", {
    "zones": [Z("web")], "worldW": 2400,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.15}, {"at": C("So how does"), "x": 1400, "y": 520, "zoom": 1.0, "dur": 1.2}], "drift": 2,
    "items": [it("browser", x=700, y=430, at=0.1, url="chatbot.example", page="chat", scale=0.75),
              it("letters", x=1500, y=300, text="CHATBOT → $ ?", at=C("So how does"), size=90, color="gold")],
    "callouts": [co("How does AI turn into money?", 960, 140, C("So how does"), "gold", screen=True, size=44)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.1}, {"at": 2.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("sign", x=480, y=360, text="1 · RENT", at=C("the three ways", 0.2), color="#BBDEFB", size=48),
              it("sign", x=960, y=360, text="2 · ADS", at=C("the three ways", 0.6), color="#FFE0B2", size=48),
              it("sign", x=1440, y=360, text="3 · LOCK-IN", at=C("the three ways", 1.0), color="#C8E6C9", size=48),
              it("letters", x=960, y=640, text="+ THE ONE NUMBER TO WATCH", at=C("and the one number"), size=56, color="risk")]})

# ====================================================================== PART 1: the spending spree (data language)
card("s05_c1", "m1_card", "The Spending Spree", "2025-2026")
stage("s06_size", "m1_size", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}, {"at": 6, "x": 960, "y": 540, "zoom": 1.0, "dur": 4}], "drift": 0,
    "items": [chart([{"label": "AMAZON", "value": 717, "color": CO[0], "at": C("Amazon sold")},
                     {"label": "ALPHABET", "value": 403, "color": CO[1], "at": C("Alphabet took in")},
                     {"label": "MICROSOFT", "value": 332, "color": CO[2], "at": C("Microsoft,"), "sub": "FY to June 2026"},
                     {"label": "META", "value": 201, "color": CO[3], "at": C("Meta,")}],
                    at=0.2, prefix="$", suffix="bn", max=760, title="LATEST FULL-YEAR REVENUE")]},
    sources=["amzn_fy25", "goog_fy25", "msft_fy26", "meta_fy25"])
stage("s07_quarter", "m1_quarter", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.1}, {"at": C("For Amazon, Alphabet"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 0,
    "items": [chart([{"label": "AMAZON", "value": 77.3, "color": CO[0], "at": C("Amazon spent")},
                     {"label": "ALPHABET", "value": 51.4, "color": CO[1], "at": C("Alphabet, about")},
                     {"label": "MICROSOFT", "value": 39.4, "color": CO[2], "at": C("Microsoft, about")},
                     {"label": "META", "value": 34.9, "color": CO[3], "at": C("Meta, about"), "sub": "incl. finance leases"}],
                    at=0.2, prefix="$", suffix="bn", decimals=1, max=85, dark=True, title="CAPEX, LATEST QUARTER"),
              it("letters", x=1460, y=330, text="≈ 2× A YEAR AGO", at=C("roughly double"), size=50, color="gold"),
              it("letters", x=960, y=980, text="≈ $2.2BN A DAY (OUR CALCULATION)", at=C("every single day"), size=44, color="risk")]},
    sources=["amzn_q3", "goog_q3", "msft_q1", "meta_call"])
stage("s08_year", "m1_year", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.25}, {"at": 1.5, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("counter", x=960, y=380, at=C("Add up"), prefix="≈ $", suffix="bn", steps=[[0, 0], [{"cue": "and you get", "offset": 1.5}, 730]], text="2026 SPENDING PLANS · 4 COMPANIES", scale=1.7),
              it("letters", x=960, y=700, text="ESTIMATE: EACH COUNTS IT DIFFERENTLY", at=C("so treat it as an estimate"), size=40, color="gold")]},
    sources=["msft_call", "goog_call", "amzn_q3", "meta_call"])
add("p09_dc", "m1_draw", "engine_draw", {
    "title": "Where the money goes", "board": BOARD, "draw_start": C("Here is a data center"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 380, 300, 200), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is a data center"), "label": lbl("DATA CENTER", 1010, 470, 26, "accent2")},
        {"d": rect(900, 500, 220, 60), "color": "accent", "width": 5, "kind": "box", "start": C("Inside are the chips"), "label": lbl("CHIPS · SERVERS", 1010, 538, 20, "accent")},
        {"d": rect(560, 700, 240, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("Around it, the land"), "label": lbl("LAND · POWER", 680, 762, 22, "accent3")},
        {"d": arrow((800, 700), (880, 590), 0.0), "color": "ink", "width": 5, "start": C("the power and the cooling")},
        {"d": rect(1220, 700, 260, 110), "color": "risk", "width": 6, "kind": "box", "start": C("short-lived assets"), "label": lbl("~3/4 SHORT-LIVED", 1350, 762, 22, "risk")},
        {"d": arrow((1140, 590), (1260, 700), 0.0), "color": "risk", "width": 5, "start": C("mainly processors")},
        {"d": "M 1250 840 Q 1350 900 1450 840 L 1430 820 M 1450 840 L 1470 818", "color": "risk", "width": 5, "start": C("It comes back again and again"), "label": lbl("REPLACE EVERY FEW YEARS", 1350, 900, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("It comes back again and again", 0.3), "dur": 1.4, "target": [1350, 760]}],
    "scale": 0.86, "floor": 1040}, sources=["msft_call"])
stage("s10_supply", "m1_supply", {
    "zones": [Z("datacenter")], "worldW": 2600,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("And the spending is already visible"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 3,
    "items": [it("queue", x=200, at=0.3, n=12, gap=70, move=4, scale=0.55, label="CUSTOMERS WAITING"),
              it("sign", x=900, y=300, text="DEMAND > SUPPLY", sub="Microsoft", at=C("customer demand"), color="#FFCDD2", size=44),
              it("stack", x=1800, h=[[0, 360], [{"cue": "free cash flow fell", "offset": 1}, 140]], at=C("And the spending is already visible"), text="AMAZON FREE CASH FLOW", color="#2F6FD1")],
    "callouts": [co("Cash flow down: 'investments in AI'", 1700, 150, C("Amazon said"), "white", screen=True, size=36, sub="Amazon Q3 2026")]},
    sources=["msft_call", "amzn_q3"])
kinetic("s11_t1", "m1_transition", [("Three ways back.", 64, "There are three ways", None, False), ("Way 1: rent the machines", 60, "Renting the machines", "gold", False)])

# ====================================================================== PART 2: rent the machines (data-center campus)
card("s12_c2", "m2_card", "Way One: Rent the Machines", "The cloud")
stage("s13_rent", "m2_rent", {
    "zones": [Z("site")], "worldW": 2800,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.0}, {"at": C("Or it can rent"), "x": 1700, "y": 480, "zoom": 0.9, "dur": 1.4}], "drift": 3,
    "items": [it("isodc", x=600, y=760, at=0.3, n=3, step=0.5, cols=3, scale=0.55, label="BUILD YOUR OWN?"),
              it("isodc", x=1800, y=760, at=C("Or it can rent"), n=9, step=0.12, cols=3, scale=0.7, glow=True, label="RENT FROM THE CLOUD"),
              *crowd([2350, 2450, 2550], "cheer", at=C("gold rush"), scale=0.6)],
    "callouts": [co("AI turned the cloud into a gold rush", 960, 140, C("That is the cloud business"), "gold", screen=True, size=40)]})
stage("s14_aws", "m2_aws", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "AWS SALES", "value": 46.0, "color": CO[0], "at": C("its sales grew")},
                     {"label": "AWS OPERATING PROFIT", "value": 17.8, "color": "#23995A", "at": C("operating profit")}],
                    at=0.2, prefix="$", suffix="bn", decimals=1, max=50, title="AMAZON'S CLOUD, LATEST QUARTER", x=460, w=1000),
              it("letters", x=1500, y=150, text="+39%", at=C("thirty-nine percent"), size=110, color="gold")]},
    sources=["amzn_q3"])
stage("s15_margin", "m2_margin", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.1}, {"at": C("So the cloud earns"), "x": 960, "y": 540, "zoom": 1.0, "dur": 1.5}], "drift": 0,
    "items": [chart([{"label": "AWS", "value": 38.6, "color": CO[0], "at": C("almost thirty-nine cents"), "display": "39¢"},
                     {"label": "AMAZON OVERALL", "value": 13.9, "color": "#90A4AE", "at": C("Amazon as a whole"), "display": "14¢"}],
                    at=0.2, suffix="¢", max=45, dark=True, title="OPERATING PROFIT PER $1 OF SALES (OUR CALCULATION)", x=520, w=880),
              it("letters", x=960, y=980, text="≈ 3× THE MARGIN", at=C("almost three times"), size=56, color="gold")]},
    sources=["amzn_q3"])
stage("s16_google", "m2_google", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("And its profit"), "x": 1300, "y": 500, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [chart([{"label": "Q3 2025", "value": 15.2, "color": "#90A4AE", "at": 0.4},
                     {"label": "Q3 2026", "value": 30.7, "color": CO[1], "at": C("Its revenue rose")}],
                    at=0.2, prefix="$", suffix="bn", decimals=1, max=34, title="GOOGLE CLOUD REVENUE", x=380, w=760, h=520),
              it("counter", x=1600, y=320, at=C("And its profit"), prefix="$", suffix="bn", decimals=1, steps=[[0, 3.6], [{"cue": "more than tripled", "offset": 0.5}, 11.1]], text="GOOGLE CLOUD OPERATING PROFIT")]},
    sources=["goog_q3"])
stage("s17_azure", "m2_azure", {
    "zones": [Z("datacenter", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Over Microsoft's last"), "x": 1500, "y": 500, "zoom": 1.05, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=900, y=260, text="AZURE +48%", at=C("grew"), size=110, color="gold"),
              it("counter", x=1600, y=320, at=C("Over Microsoft's last"), prefix="$", suffix="bn+", steps=[[0, 0], [{"cue": "for the first time", "offset": 0}, 100]], text="AZURE REVENUE, FY TO JUNE 2026")]},
    sources=["msft_q1", "msft_fy26"])
stage("s18_foundry", "m2_foundry", {
    "zones": [Z("district")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("And it says"), "x": 1600, "y": 520, "zoom": 0.95, "dur": 1.6}], "drift": 3,
    "items": [it("counter", x=900, y=230, at=0.2, prefix="$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "in a single quarter", "offset": 0}, 63.9]], text="MICROSOFT CLOUD, ONE QUARTER (+30%)"),
              *crowd([1300 + 95 * k for k in range(9)], "walk", at=C("And it says"), scale=0.55),
              it("counter", x=1700, y=230, at=C("And it says"), suffix="+", steps=[[0, 0], [{"cue": "customers now build", "offset": 1}, 120000]], text="FOUNDRY AI CUSTOMERS")]},
    sources=["msft_q1", "msft_call"])
add("p19_rent", "m2_draw", "engine_draw", {
    "title": "The rental model", "board": BOARD, "draw_start": C("On one side"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 420, 280, 140), "color": "accent2", "width": 6, "kind": "box", "start": C("On one side"), "label": lbl("CLOUD (OWNS CHIPS)", 700, 498, 22, "accent2")},
        {"d": rect(1180, 420, 280, 140), "color": "accent3", "width": 6, "kind": "box", "start": C("On the other"), "label": lbl("THOUSANDS OF USERS", 1320, 498, 22, "accent3")},
        {"d": arrow((850, 450), (1170, 450), -0.1), "color": "accent2", "width": 5, "start": C("Money flows one way"), "label": lbl("computing power", 1010, 410, 20, "accent2")},
        {"d": arrow((1170, 540), (850, 540), -0.1), "color": "accent", "width": 6, "start": C("rent flows back"), "label": lbl("$ rent", 1010, 600, 24, "accent")},
        {"d": "M 700 600 L 700 800 L 760 760 M 700 800 L 640 760", "color": "accent", "width": 6, "start": C("the more rent the landlord"), "label": lbl("MORE AI = MORE RENT", 700, 840, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("the more rent the landlord", 0.3), "dur": 1.4, "target": [700, 760]}],
    "scale": 0.86, "floor": 1040}, sources=["amzn_q3", "goog_q3", "msft_q1"])
kinetic("s20_t2", "m2_transition", [("Two of them earn most money", 54, "But two of these", None, True), ("…a different way", 64, "a completely different way", "gold", False)])

# ====================================================================== PART 3: sell better ads (the cartoon internet)
card("s21_c3", "m3_card", "Way Two: Sell Better Ads", "Search · YouTube · Facebook · Instagram")
stage("s22_ads", "m3_ads", {
    "zones": [Z("web")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Meta's apps"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 1.4}], "drift": 3,
    "items": [it("browser", x=700, y=420, at=0.2, url="search.example", page="site", scale=0.7),
              it("counter", x=700, y=150, at=C("Google's search business"), prefix="$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "and YouTube ads", "offset": -0.5}, 63.4]], text="SEARCH ADS, ONE QUARTER"),
              it("device", type="phone", x=1700, y=F, at=C("Meta's apps"), scale=1.3),
              it("counter", x=1750, y=150, at=C("Meta's apps"), prefix="$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "from ads", "offset": 0.5}, 63.1]], text="META ADS, ONE QUARTER"),
              it("letters", x=1750, y=420, text="+26% A YEAR", at=C("grew twenty-six percent"), size=60, color="gold")],
    "callouts": [co("YouTube ads: $11.2bn", 900, 640, C("YouTube ads"), "white", size=34, sub="Alphabet Q3 2026", tail=[700, 520])]},
    sources=["goog_q3", "meta_q3"])
stage("s23_better", "m3_better", {
    "zones": [Z("web")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("A few percent"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("device", type="phone", x=800, y=F, at=0.2, scale=1.2),
              it("burst", x=800, y=420, at=C("decides which ad you see")),
              it("letters", x=1450, y=300, text="+9.6%", at=C("raised conversions"), size=150, color="gold"),
              it("letters", x=1450, y=470, text="APP AD CONVERSIONS (META)", at=C("raised conversions", 0.3), size=36, color="white"),
              it("letters", x=1450, y=640, text="× $60BN OF ADS", at=C("On sixty billion"), size=60, color="risk")]},
    sources=["meta_call"])
stage("s24_assist", "m3_assist", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "ALPHABET ADS", "value": 82.0, "color": CO[1], "at": C("the advertising business")},
                     {"label": "META ADS", "value": 63.1, "color": CO[3], "at": C("And Meta says")}],
                    at=0.2, prefix="$", suffix="bn", decimals=1, max=90, title="AD REVENUE, ONE QUARTER", x=360, w=820),
              it("sign", x=1500, y=380, text="+~5% CONVERSIONS", sub="Meta AI business assistant, same cost", at=C("almost five percent"), color="#C8E6C9", size=40)]},
    sources=["goog_q3", "meta_call"])
add("p25_ads", "m3_draw", "engine_draw", {
    "title": "Who pays for the AI?", "board": BOARD, "draw_start": C("Here is an advertiser"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 400, 260, 130), "color": "accent", "width": 6, "kind": "box", "start": C("Here is an advertiser"), "label": lbl("ADVERTISER $", 690, 472, 24, "accent")},
        {"d": rect(1200, 400, 260, 130), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the ad system"), "label": lbl("AI AD SYSTEM", 1330, 472, 24, "accent2")},
        {"d": arrow((830, 465), (1190, 465), 0.0), "color": "ink", "width": 5, "start": C("Here is the ad system", 0.6)},
        {"d": rect(1200, 680, 260, 130), "color": "accent3", "width": 6, "kind": "box", "start": C("more people click"), "label": lbl("CLICKS · SALES", 1330, 752, 24, "accent3")},
        {"d": arrow((1330, 540), (1330, 670), 0.0), "color": "accent3", "width": 5, "start": C("more people click")},
        {"d": arrow((1190, 745), (700, 545), -0.2), "color": "accent", "width": 6, "start": C("so they spend more dollars"), "label": lbl("spend more", 900, 700, 24, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("The advertiser does", 0.2), "dur": 1.4, "target": [690, 470]}],
    "scale": 0.86, "floor": 1040}, sources=["meta_call"])
kinetic("s26_t3", "m3_transition", [("Rent + ads = today's bills", 58, "Rent and ads", None, True), ("Way 3: money not yet arrived", 56, "money that has not arrived", "gold", False)])

# ====================================================================== PART 4: lock in the future (evidence board)
card("s27_c4", "m4_card", "Way Three: Lock In the Future", "Backlog")
stage("s28_backlog", "m4_backlog", {
    "zones": [Z("corkboard")], "worldW": 2400,
    "cam": [{"at": 0, "x": 800, "y": 480, "zoom": 1.15}, {"at": C("Google Cloud reports"), "x": 1400, "y": 480, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("pinboard", cards=[
                {"x": 880, "y": 330, "text": "CLOUD CONTRACT", "sub": "money arrives over years", "at": 0.4, "size": 34},
                {"x": 1180, "y": 600, "text": "MICROSOFT $677BN", "sub": "commercial backlog, +73%", "at": C("Microsoft says"), "w": 380, "size": 38},
                {"x": 1650, "y": 360, "text": "GOOGLE CLOUD $561BN", "sub": "backlog · ~55% within 2 years", "at": C("Google Cloud reports"), "w": 420, "size": 36}],
              links=[[0, 1, C("Microsoft says", 0.6)], [1, 2, C("Google Cloud reports", 0.6)]])]},
    sources=["msft_q1", "goog_call"])
stage("s29_sum", "m4_sum", {
    "zones": [Z("corkboard")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1300, "y": 480, "zoom": 1.0}, {"at": C("Microsoft's figure covers"), "x": 1300, "y": 460, "zoom": 1.1, "dur": 1.6}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 900, "y": 330, "text": "$677BN", "at": 0.1, "size": 48, "w": 240, "h": 140},
                {"x": 1700, "y": 330, "text": "$561BN", "at": 0.1, "size": 48, "w": 240, "h": 140},
                {"x": 1300, "y": 620, "text": "≈ $1.24 TRILLION", "sub": "signed, not yet paid (our sum)", "at": C("and you get"), "w": 460, "size": 44}],
              links=[[0, 2, C("and you get", 0.3)], [1, 2, C("and you get", 0.6)]], stamp="SIGNED", stampAt=C("of business already signed"))],
    "callouts": [co("Microsoft's figure isn't only AI", 1300, 140, C("Microsoft's figure covers"), "white", screen=True, size=36)]},
    sources=["msft_q1", "goog_call"])
stage("s30_users", "m4_users", {
    "zones": [Z("web")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.2}, {"at": 2.0, "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1100, y=300, at=0.3, steps=[[0, 0], [{"cue": "one billion users", "offset": 0.5}, 1000000000]], text="GEMINI APP USERS", scale=1.4),
              *crowd([500 + 120 * k for k in range(12)], "cheer", at=C("Users today"), scale=0.45)]},
    sources=["goog_call"])
stage("s31_tokens", "m4_tokens", {
    "zones": [Z("datacenter", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Every one of those tokens"), "x": 1500, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 3,
    "items": [it("counter", x=1150, y=250, at=C("Google says"), suffix="BN / MIN", steps=[[0, 0], [{"cue": "tokens a minute", "offset": 0}, 32]], text="TOKENS PROCESSED (NEARLY)"),
              it("letters", x=1150, y=470, text="> 4× A YEAR AGO", at=C("more than four times"), size=64, color="gold"),
              it("hbm", x=1850, y=430, at=C("Every one of those tokens"), scale=0.8)]},
    sources=["goog_call"])
add("p32_three", "m4_draw", "engine_draw", {
    "title": "Three ways vs. one bill", "board": BOARD, "draw_start": C("Rent, money coming in now"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1480 860", "color": "ink", "width": 4, "start": C("Rent, money coming in now")},
        {"d": "M 600 860 L 600 720 L 720 720 L 720 860", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Rent, money"), "label": lbl("RENT", 660, 700, 24, "accent2")},
        {"d": "M 780 860 L 780 700 L 900 700 L 900 860", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("Ads, money"), "label": lbl("ADS", 840, 680, 24, "accent")},
        {"d": "M 960 860 L 960 640 L 1080 640 L 1080 860", "color": "accent3", "width": 6, "fill": "accent3", "fillOpacity": 0.15, "kind": "bar", "start": C("And backlog"), "label": lbl("BACKLOG (LATER)", 1020, 620, 22, "accent3")},
        {"d": "M 1220 860 L 1220 380 L 1400 380 L 1400 860", "color": "risk", "width": 7, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("one huge bar"), "label": lbl("SPENDING", 1310, 360, 28, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("The spending", 0.2), "dur": 1.4, "target": [1310, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["msft_q1", "goog_call", "msft_call"])
kinetic("s33_t4", "m4_transition", [("Is it worth it?", 76, "Is it worth it", "gold", False)])

# ====================================================================== PART 5: the bet (dark studio, chips)
card("s34_c5", "m5_card", "The Bet", "2027 and beyond")
stage("s35_risk", "m5_risk", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}, {"at": C("And because so much"), "x": 960, "y": 520, "zoom": 1.08, "dur": 2.0}], "drift": 0,
    "items": [chart([{"label": "AMAZON", "value": 220, "color": CO[0], "at": 0.4, "display": "≈$220bn"},
                     {"label": "ALPHABET", "value": 200, "color": CO[1], "at": 0.7, "display": "$195–205bn"},
                     {"label": "MICROSOFT", "value": 170, "color": CO[2], "at": 1.0, "display": "≈$170bn", "sub": "calendar 2026"},
                     {"label": "META", "value": 140, "color": CO[3], "at": 1.3, "display": "$135–145bn"}],
                    at=0.2, prefix="$", suffix="bn", max=240, dark=True, title="2026 SPENDING PLANS"),
              it("letters", x=1480, y=985, text="2027: EVEN MORE", at=C("significantly again"), size=60, color="risk")]},
    sources=["amzn_q3", "goog_call", "msft_call", "meta_call"])
stage("s36_chips", "m5_chips", {
    "zones": [Z("fab")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("And Microsoft expects"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("hbm", x=800, y=430, at=0.3, scale=0.9),
              it("counter", x=800, y=150, at=C("Amazon says"), prefix="$", suffix="bn+", steps=[[0, 0], [{"cue": "combined annual revenue", "offset": 1.5}, 10]], text="AMAZON IN-HOUSE CHIPS · RUN RATE"),
              it("letters", x=1600, y=320, text="> $50BN NEXT QUARTER", at=C("And Microsoft expects"), size=60, color="gold"),
              it("letters", x=1600, y=430, text="MICROSOFT CAPEX PLAN", at=C("And Microsoft expects", 0.3), size=34, color="white")]},
    sources=["amzn_fy25", "msft_call"])
stage("s37_number", "m5_number", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.25}, {"at": C("As long as"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 1.8}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 1100, "y": 380, "text": "THE BACKLOG", "sub": "the one number to watch", "at": 0.3, "w": 440, "size": 54},
                {"x": 650, "y": 650, "text": "GROWS → BET PAYS", "at": C("As long as"), "w": 380, "color": "#C8E6C9", "size": 34},
                {"x": 1550, "y": 650, "text": "STALLS → EMPTY ROOMS", "at": C("If the backlog stops"), "w": 420, "color": "#FFCDD2", "size": 32}],
              links=[[0, 1, C("As long as", 0.4)], [0, 2, C("If the backlog stops", 0.4)]])]},
    sources=["msft_q1", "goog_call"])

# ====================================================================== PAYOFF
stage("s38_payoff", "payoff", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.15}, {"at": C("The chatbot is the shop window"), "x": 960, "y": 600, "zoom": 0.95, "dur": 3.0}], "drift": 0,
    "items": [it("sign", x=480, y=240, text="RENT", at=C("By renting"), color="#BBDEFB", size=64),
              it("sign", x=960, y=240, text="ADS", at=C("by selling better ads"), color="#FFE0B2", size=64),
              it("sign", x=1440, y=240, text="LOCK-IN", at=C("by locking in"), color="#C8E6C9", size=64),
              it("browser", x=960, y=560, at=0.3, url="chatbot.example", page="chat", scale=0.75, until=C("The real business", 0.5)),
              it("isodc", x=960, y=720, at=C("The real business"), n=9, step=0.1, cols=3, scale=0.75, glow=True)]})
add("s39_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_bigtech_storyboard.py; edit the generator, not this file.\n"
           "# Episode 28 storyboard (Big Tech and AI): first episode on the diversity rules; tones from visual_direction.yaml.\n")
