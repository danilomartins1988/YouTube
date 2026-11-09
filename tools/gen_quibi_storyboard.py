"""Generates projects/the-175-billion-app-that-lasted-six-months/deliverables/documentary/storyboard.yaml (Episode 19, Quibi).

Bespoke worlds (tones from visual_direction.yaml: spectacle -> crisis -> strategy -> reflective): a Hollywood night
premiere for the money, the new `bigphone` item (a giant phone playing a ten-minute show that rotates like Turnstyle and
finally goes dark) as the through-line, an empty commuter platform when the world stops commuting, a living room where
everyone watches the big TV, a funnel of users, a vault draining, a boardroom shutdown and a library sold off.
Presenter: the bet, the free-trial funnel, the rights window. No Quibi logo or app UI, no likeness of real people
(names in text only), no smiling sun, no generic city.
Run: python tools/gen_quibi_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-175-billion-app-that-lasted-six-months/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
PUR = "#7E57C2"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.2}, {"at": C("and still shut down"), "x": 1200, "y": 520, "zoom": 0.95, "dur": 2.6}], "drift": 0,
    "items": [it("bigphone", x=1200, y=430, at=0.2, scale=0.9, color=PUR, offAt=C("six months after launch")),
              it("counter", x=600, y=220, at=C("raise almost"), prefix="$", suffix="bn", decimals=2, steps=[[0, 0], [{"cue": "raise almost", "offset": 2}, 1.75]], text="RAISED"),
              *crowd([1700, 1840, 1980], "cheer", at=C("the biggest stars"), until=C("and still shut down", 1), scale=0.7)],
    "callouts": [co("Almost $2 billion, Hollywood's biggest stars…", 960, 960, C("raise almost"), "gold", screen=True, size=38, until=C("and still shut down", -0.3)),
                 co("…shut down six months after launch", 960, 960, C("and still shut down"), "risk", screen=True, size=42)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("district", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 0.9}, {"at": C("And the strangest part"), "x": 1300, "y": 500, "zoom": 1.1, "dur": 2.6}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=C("It launched in April"), pages=[[0, "APR", "2020"], [{"cue": "shutting down in October"}, "OCT", "2020"]], scale=0.85),
              it("bigphone", x=1300, y=430, at=0.2, scale=0.8, color=PUR, offAt=C("shutting down in October")),
              it("letters", x=2000, y=260, text="NOT CRAZY", at=C("the idea behind it"), size=70, color="gold")],
    "callouts": [co("Quibi: {{raised.display}} raised before one customer", 960, 960, C("It raised"), "gold", screen=True, size=38, sub="Fortune", until=C("It launched in April", -0.3)),
                 co("April 2020 → shutdown announced in October", 960, 960, C("It launched in April"), "risk", screen=True, size=40, until=C("And the strangest part", -0.3)),
                 co("The idea was not crazy at all", 960, 960, C("And the strangest part"), "white", screen=True, size=40)]},
    sources=["fortune_shut", "cnn_may"])

# ====================================================================== PART 1: quick bites
card("s03_c1", "m1_card", "Quick Bites", "The billion-dollar idea")
stage("s04_q1", "m1_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("bigphone", x=960, y=440, at=0.2, scale=0.75, color=PUR),
              it("coins", **{"from": [-200, 300], "to": [960, 400]}, at=0.6, rate=5)],
    "callouts": [co("What were investors buying?", 960, 150, C("What exactly"), "gold", screen=True, size=44)]})
stage("s05_idea", "m1_idea", {
    "zones": [Z("office", -1600, 1500), Z("port", 1500, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("The name meant"), "x": 1300, "y": 500, "zoom": 1.05, "dur": 2.2},
            {"at": C("Something to watch"), "x": 2300, "y": 520, "zoom": 0.95, "dur": 2.6}], "drift": 3,
    "items": [it("sign", x=600, y=280, text="JEFFREY KATZENBERG", sub="founder · ex-chairman, Disney's studio", at=C("Jeffrey Katzenberg"), color="#E1BEE7", size=30),
              it("sign", x=1000, y=420, text="MEG WHITMAN", sub="CEO · ex-eBay, HP", at=C("Meg Whitman"), color="#BBDEFB", size=30),
              it("letters", x=1300, y=200, text="QUI-ck BI-tes", at=C("The name meant"), size=64, color="gold"),
              it("bigphone", x=1500, y=480, at=C("ten minutes or less", -0.4), scale=0.55, color=PUR, label="≤ 10 MIN"),
              it("bus", x=[[0, 1900], [{"cue": "Something to watch", "offset": 6}, 2700]], at=C("on the bus"), scale=0.7),
              *crowd([2500, 2620, 2740], "phone", at=C("in a queue"), scale=0.7)],
    "callouts": [co("Hollywood shows in ≤ 10-minute episodes", 960, 960, C("Hollywood quality"), "gold", screen=True, size=38, sub="Variety", until=C("Something to watch", -0.3)),
                 co("Made only for your phone", 960, 960, C("Something to watch"), "white", screen=True, size=40)]},
    sources=["variety_2018", "nexttv_shut"])
stage("s06_money", "m1_money", {
    "zones": [Z("district", night=True)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("The investors read"), "x": 1600, "y": 520, "zoom": 0.85, "dur": 2.6},
            {"at": C("And before launch"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=800, y=220, at=C("first funding round"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "first funding round", "offset": 1.5}, 1]], text="FIRST ROUND, 2018"),
              it("vaultdoor", x=800, at=C("first funding round"), openAt=C("first funding round", 1), scale=0.6),
              it("board", x=1600, y=380, at=C("The investors read"), text="INVESTORS (SELECTION)", rows=[{"name": "DISNEY · NBCU · SONY"}, {"name": "WARNERMEDIA · VIACOM"}, {"name": "LIONSGATE · MGM · ALIBABA"}, {"name": "GOLDMAN · JPMORGAN", "color": "gold"}]),
              it("contract", x=2350, y=430, at=C("And before launch"), text="ADS SOLD OUT", sub="year one: $150M", scale=0.6)],
    "callouts": [co("2018: a $1 billion first round", 960, 960, C("first funding round"), "gold", screen=True, size=40, sub="Variety", until=C("The investors read", -0.3)),
                 co("A guest list of the entertainment industry", 960, 960, C("The investors read"), "white", screen=True, size=38, until=C("And before launch", -0.3)),
                 co("First-year ads sold out before launch: {{ads.display}}", 960, 960, C("And before launch"), "gold", screen=True, size=38, sub="TechCrunch")]},
    sources=["variety_2018", "tc_ads"])
stage("s07_warning", "m1_warning", {
    "zones": [Z("office", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Katzenberg insisted"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("bigphone", x=800, y=440, at=C("Go90", -0.5), scale=0.6, color="#78909C", label="GO90", offAt=C("never found an audience")),
              it("counter", x=800, y=170, at=C("wrote off"), prefix="$", suffix="M", steps=[[0, 0], [{"cue": "wrote off", "offset": 1.5}, 658]], text="VERIZON WRITE-OFF"),
              it("bigphone", x=1650, y=440, at=C("Katzenberg insisted"), scale=0.6, color=PUR, rot=[[0, 0], [{"cue": "built from the ground up"}, 0], [{"cue": "built from the ground up", "offset": 1}, 90]])],
    "callouts": [co("2018: Verizon shuts Go90, its short-video app", 960, 960, C("There was a warning sign"), "risk", screen=True, size=38, sub="Variety", until=C("Katzenberg insisted", -0.3)),
                 co("'Fundamentally different', built for the phone", 960, 960, C("Katzenberg insisted"), "white", screen=True, size=38)]},
    sources=["variety_2018"])
add("p08_bet", "m1_draw", "engine_draw", {
    "title": "The bet", "board": BOARD, "draw_start": C("On one side"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": " ".join(rect(560 + (k % 6) * 60, 340 + (k // 6) * 90, 40, 70) for k in range(18)), "color": "accent2", "width": 3, "start": C("billions of people"), "label": lbl("PHONES × BILLIONS", 730, 640, 24, "accent2")},
        {"d": rect(1020, 380, 160, 110), "color": "accent", "width": 5, "start": C("a simple price"), "label": lbl("$ / MONTH", 1100, 445, 26, "accent")},
        {"d": "M 920 470 L 1000 450", "color": "ink", "width": 4, "start": C("If even a small slice")},
        {"d": "M 1260 700 L 1260 360 M 1260 700 L 1500 700", "color": "ink", "width": 4, "start": C("If even a small slice")},
        {"d": "M 1290 700 L 1290 640 L 1340 640 L 1340 700 M 1360 700 L 1360 540 L 1410 540 L 1410 700 M 1430 700 L 1430 400 L 1480 400 L 1480 700", "color": "accent3", "width": 4,
         "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("would be enormous"), "label": lbl("the math", 1390, 740, 24, "accent3")},
        {"d": "M 600 820 L 1480 820", "color": "risk", "width": 6, "start": C("would actually pay"), "label": lbl("PAY FOR MINUTES ALREADY FILLED FOR FREE?", 1040, 870, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("would actually pay", 0.3), "dur": 1.4, "target": [1040, 820]}],
    "scale": 0.86, "floor": 1040}, sources=["tc_launch"])
kinetic("s09_t1", "m1_transition", [("Then, just before launch", 56, "Then, just before", None, True), ("the whole world stopped commuting", 54, "stopped commuting", "risk", True)])

# ====================================================================== PART 2: the worst launch date
card("s10_c2", "m2_card", "The Worst Launch Date", "April 2020")
stage("s11_q2", "m2_question", {
    "zones": [Z("port")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("bus", x=960, at=0.2, scale=0.8, text="EMPTY"),
              it("bigphone", x=1500, y=420, at=0.6, scale=0.5, color=PUR)],
    "callouts": [co("An app for busy people, when nobody is busy?", 960, 150, C("What happens"), "gold", screen=True, size=40)]})
stage("s12_launch", "m2_launch", {
    "zones": [Z("den", -1600, 1500), Z("web", 1500, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("On launch day"), "x": 2100, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("But Disney's"), "x": 2400, "y": 520, "zoom": 0.85, "dur": 2.2}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "APR 6", "2020"]], scale=0.85),
              *crowd([700, 840], "phone", at=C("locking people inside"), scale=0.7),
              it("pricetag", x=1100, y=300, at=C("free trial"), pages=[[0, "FREE · 90 DAYS"], [{"cue": "then cost"}, "$4.99 / $7.99"]], sub="with ads / without"),
              it("tower", x=2000, text="QUIBI DAY 1", color=PUR, h=[[0, 40], [{"cue": "On launch day", "offset": 1.5}, 120]], at=C("On launch day"), scale=0.8),
              it("tower", x=2600, text="DISNEY+ LAUNCH", color="#1565C0", h=[[0, 40], [{"cue": "But Disney's", "offset": 1.5}, 560]], at=C("But Disney's"), scale=0.8)],
    "callouts": [co("6 April 2020: launch in a lockdown", 960, 960, C("Quibi launched"), "white", screen=True, size=40, sub="CNN", until=C("On launch day", -0.3)),
                 co("Day one: ≈ 300,000 downloads (Sensor Tower)", 960, 960, C("On launch day"), "gold", screen=True, size=38, sub="TechCrunch", until=C("But Disney's", -0.3)),
                 co("Disney+: ≈ 4 million installs at launch", 960, 960, C("But Disney's"), "risk", screen=True, size=38)]},
    sources=["cnn_may", "tc_launch"])
stage("s13_stars", "m2_stars", {
    "zones": [Z("district", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Apple promoted"), "x": 1800, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 4,
    "items": [it("sign", x=700, y=280, text="JENNIFER LOPEZ · LIAM HEMSWORTH", sub="and more at launch", at=C("Jennifer Lopez"), color="#FFE082", size=26),
              it("sign", x=900, y=470, text="SPIELBERG · DEL TORO", sub="projects promised", at=C("Steven Spielberg"), color="#E1BEE7", size=28),
              it("chart", x=1800, y=420, w=500, h=300, at=C("Apple promoted"), dur=2.5, text="APP STORE RANK", pts=[0.2, 0.5, 0.8, 0.9, 0.92], color="green"),
              it("letters", x=1800, y=190, text="No. 3", at=C("it climbed"), size=100, color="gold"),
              *crowd([2350, 2480, 2610], "cheer", at=C("For a few days"), scale=0.65)],
    "callouts": [co("Famous names, famous directors", 960, 960, C("The launch line-up"), "white", screen=True, size=40, sub="TechCrunch", until=C("Apple promoted", -0.3)),
                 co("No. 3 on the App Store", 960, 960, C("it climbed"), "gold", screen=True, size=42)]},
    sources=["tc_launch"])
stage("s14_phone", "m2_phone", {
    "zones": [Z("den")], "worldW": 2400, "min_seconds": 20,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Its showpiece"), "x": 1500, "y": 480, "zoom": 1.15, "dur": 2.4},
            {"at": C("But it was built"), "x": 1200, "y": 520, "zoom": 0.9, "dur": 2.4}], "drift": 2,
    "items": [it("device", type="tv", x=700, y=F, at=C("the big television"), scale=1.3),
              *crowd([500, 640, 780], "stand", at=C("People stuck at home"), scale=0.7),
              it("letters", x=700, y=250, text="✕ NO TV", at=C("could not be sent"), size=60, color="risk"),
              it("bigphone", x=1500, y=440, at=C("It only worked on phones"), scale=0.7, color=PUR,
                 rot=[[0, 0], [{"cue": "let you rotate"}, 0], [{"cue": "let you rotate", "offset": 1.2}, 90], [{"cue": "a vertical version", "offset": 0.3}, 90], [{"cue": "a vertical version", "offset": 1.5}, 0], [{"cue": "Clever", "offset": 0.3}, 90]]),
              it("sign", x=1500, y=150, text="TURNSTYLE", at=C("called Turnstyle"), color="#E1BEE7", size=36),
              it("bus", x=[[0, 2100], [{"cue": "a commuter who", "offset": 5}, 2900]], at=C("a commuter who"), text="EMPTY", scale=0.6)],
    "callouts": [co("Phone only, while everyone sat by the TV", 960, 960, C("It only worked on phones"), "risk", screen=True, size=38, until=C("Its showpiece", -0.3)),
                 co("Turnstyle: turn the phone, re-frame the scene", 960, 960, C("Its showpiece"), "white", screen=True, size=38, until=C("But it was built", -0.3)),
                 co("Built for a commuter who no longer existed", 960, 960, C("But it was built"), "gold", screen=True, size=40)]},
    sources=["tc_launch", "nexttv_shut", "verge_eko"])
stage("s15_lawsuit", "m2_lawsuit", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1200, "y": 520, "zoom": 0.95}, {"at": C("Quibi said"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("gavel", x=1200, y=420, hits=[C("sued", 0.5), C("Quibi said", 0.3)]),
              it("docs", x=700, y=540, at=C("Eko sued"), text="EKO: PATENT + TRADE SECRETS", scale=0.6, stamp="ALLEGED", stampAt=C("alleging")),
              it("docs", x=1700, y=540, at=C("Quibi said"), text="QUIBI: 'NO MERIT', OWN PATENT", scale=0.6)],
    "callouts": [co("Eko sues: patent and trade-secret allegations", 960, 960, C("Eko sued"), "risk", screen=True, size=38, sub="The Verge", until=C("Quibi said", -0.3)),
                 co("Quibi: 'absolutely no merit'", 960, 960, C("Quibi said"), "white", screen=True, size=40)]},
    sources=["verge_eko"])
kinetic("s16_t2", "m2_transition", [("The downloads came", 62, "The downloads came", None, False), ("Would anyone stay?", 72, "whether anyone would stay", "accent", False)])

# ====================================================================== PART 3: the free trial
card("s17_c3", "m3_card", "The Free Trial", "Who actually paid")
stage("s18_q3", "m3_question", {
    "zones": [Z("web")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("bigphone", x=960, y=440, at=0.2, scale=0.7, color=PUR, label="DAY 90"),
              it("pricetag", x=1450, y=300, at=0.8, pages=[[0, "FREE"], [3.5, "$4.99?"]], sub="after the trial")],
    "callouts": [co("How many actually paid?", 960, 150, C("How many"), "gold", screen=True, size=44)]})
stage("s19_may", "m3_may", {
    "zones": [Z("web")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Disney's service"), "x": 1600, "y": 520, "zoom": 0.75, "dur": 2.6}], "drift": 3,
    "items": [it("tower", x=900, text="QUIBI ≈ 1.3M", color=PUR, h=[[0, 20], [{"cue": "active users", "offset": 1}, 40]], at=C("CNN reported"), scale=0.8),
              it("tower", x=1500, text="DISNEY+ 50M+", color="#1565C0", h=[[0, 20], [{"cue": "Disney's service", "offset": 1.5}, 320]], at=C("Disney's service"), scale=0.8),
              it("tower", x=2100, text="NETFLIX 183M", color="#C62828", h=[[0, 20], [{"cue": "Netflix", "offset": 1.5}, 640]], at=C("Netflix"), scale=0.8),
              it("magnifier", x=[[0, 700], [10, 900]], y=[[0, 700], [10, 780]], at=C("rounding error"), scale=0.8)],
    "callouts": [co("May 2020: ≈ {{may.display}} users, mostly on free trials", 960, 960, C("CNN reported"), "gold", screen=True, size=36, sub="CNN", until=C("Disney's service", -0.3)),
                 co("Disney+ 50M+ · Netflix 183M", 960, 960, C("Disney's service"), "white", screen=True, size=40)]},
    sources=["cnn_may"])
stage("s20_convert", "m3_convert", {
    "zones": [Z("web")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Quibi said the estimate"), "x": 1700, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=900, y=220, at=C("signed up"), steps=[[0, 0], [{"cue": "signed up", "offset": 1.5}, 910000], [{"cue": "kept paying", "offset": -0.5}, 910000], [{"cue": "kept paying", "offset": 1.5}, 72000]], text="SIGN-UPS → PAYING (EST.)"),
              *crowd([600 + k * 90 for k in range(8)], "phone", at=C("signed up"), until=C("kept paying"), scale=0.55),
              *crowd([780, 870], "phone", at=C("kept paying"), scale=0.55),
              it("letters", x=900, y=480, text="≈ 8%", at=C("That is"), size=110, color="risk"),
              it("docs", x=1800, y=540, at=C("Quibi said the estimate"), text="QUIBI: 'WRONG BY AN ORDER OF MAGNITUDE'", scale=0.6),
              it("letters", x=1800, y=250, text="PAYING: ?", at=C("never published"), size=70, color="gold")],
    "callouts": [co("Sensor Tower: ≈ 910,000 → ≈ 72,000 paying (≈ 8%)", 960, 960, C("Sensor Tower estimated"), "risk", screen=True, size=36, sub="The Verge (an estimate)", until=C("Quibi said the estimate", -0.3)),
                 co("Quibi disputed it, and never published its paying total", 960, 960, C("Quibi said the estimate"), "white", screen=True, size=36)]},
    sources=["verge_subs"])
stage("s21_ads", "m3_ads", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Instead"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("bigphone", x=800, y=440, at=0.3, scale=0.6, color="#FFB300", label="AD · 15 s"),
              it("letters", x=800, y=150, text="NO SKIP", at=C("no skip button"), size=64, color="gold"),
              it("chart", x=1600, y=420, w=500, h=300, at=C("Instead"), dur=2.5, text="AUDIENCE: PROMISED vs REAL", pts=[0.9, 0.7, 0.5, 0.35, 0.3], color="risk"),
              *crowd([1300, 1420], "worry", at=C("disappointed"), scale=0.7)],
    "callouts": [co("6, 10 or 15-second ads, no skip button", 960, 960, C("They had paid"), "white", screen=True, size=38, sub="TechCrunch", until=C("Instead", -0.3)),
                 co("Advertisers who bought {{ads.display}}: disappointed", 960, 960, C("Instead"), "risk", screen=True, size=38, sub="Broadcasting & Cable")]},
    sources=["tc_ads", "nexttv_shut"])
add("p22_funnel", "m3_draw", "engine_draw", {
    "title": "Why a free trial can hide a problem", "board": BOARD, "draw_start": C("Imagine a funnel"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 350 L 1400 350 L 1080 640 L 1080 820 L 920 820 L 920 640 Z", "color": "accent2", "width": 6, "start": C("Imagine a funnel"), "label": lbl("FUNNEL", 1000, 330, 26, "accent2")},
        {"d": "M 640 400 L 1360 400", "color": "accent3", "width": 4, "start": C("everyone who downloads"), "label": lbl("DOWNLOADS (huge)", 1000, 430, 22, "accent3")},
        {"d": "M 790 540 L 1210 540", "color": "accent", "width": 4, "start": C("try a few shows"), "label": lbl("TRY A FEW SHOWS", 1000, 570, 22, "accent")},
        {"d": "M 930 800 L 1070 800", "color": "risk", "width": 6, "start": C("the few who pay"), "label": lbl("PAY", 1000, 860, 26, "risk")},
        {"d": "M 1420 380 Q 1500 370 1520 420", "color": "ink", "width": 4, "start": C("makes the top look huge"), "label": lbl("trial inflates this", 1530, 450, 20, "ink", "start")},
        {"d": "M 1100 800 Q 1250 820 1400 780", "color": "risk", "width": 5, "start": C("lives on the bottom"), "label": lbl("the business lives here", 1420, 760, 20, "risk", "start")},
    ],
    "actions": [{"kind": "point", "at": C("very narrow bottom", 0.2), "dur": 1.4, "target": [1000, 800]}],
    "scale": 0.86, "floor": 1040}, sources=["verge_subs"])
kinetic("s23_t3", "m3_transition", [("And all this time", 62, "And all this time", None, False), ("the money kept going out", 66, "money kept going", "risk", False)])

# ====================================================================== PART 4: the money
card("s24_c4", "m4_card", "The Money", "Where it went")
stage("s25_q4", "m4_question", {
    "zones": [Z("vault")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vaultdoor", x=960, at=0.2, openAt=1.0, scale=0.8),
              it("coins", **{"from": [960, 500], "to": [2200, 300]}, at=1.5, rate=6)],
    "callouts": [co("Where did the money go?", 960, 150, C("Where did"), "gold", screen=True, size=44)]})
stage("s26_spend", "m4_spend", {
    "zones": [Z("district", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("According to reports"), "x": 1700, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("bigphone", x=700, y=440, at=0.3, scale=0.55, color=PUR, label="8 MIN"),
              it("coins", **{"from": [1700, 300], "to": [700, 400]}, at=C("Mostly into shows"), rate=8, until=C("According to reports", 4)),
              it("counter", x=1700, y=220, at=C("expected to have spent"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "expected to have spent", "offset": 1.5}, 1]], text="SPENT BY Q3 2020 (EXPECTED)"),
              it("pricetag", x=2300, y=320, at=C("would need another"), pages=[[0, "+$200M"]], sub="needed by mid-2021")],
    "callouts": [co("Hollywood prices, minutes-long episodes", 960, 960, C("Mostly into shows"), "white", screen=True, size=38, until=C("According to reports", -0.3)),
                 co("≈ $1bn of $1.75bn expected spent by autumn 2020", 960, 960, C("expected to have spent"), "gold", screen=True, size=36, sub="NBC News", until=C("would need another", -0.3)),
                 co("…and another $200M needed by mid-2021", 960, 960, C("would need another"), "risk", screen=True, size=38)]},
    sources=["nbc_why", "fortune_shut"])
add("p27_rights", "m4_rights", "engine_draw", {
    "title": "The catch in the contracts", "board": BOARD, "draw_start": C("Quibi's deals"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 600 L 1500 600", "color": "ink", "width": 4, "start": C("Quibi's deals"), "label": lbl("time →", 1450, 640, 22, "ink")},
        {"d": rect(600, 500, 300, 80), "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.25, "kind": "box", "start": C("exclusive rights"), "label": lbl("EXCLUSIVE: 2 YEARS", 750, 480, 22, "accent")},
        {"d": rect(910, 500, 560, 80), "color": "muted", "width": 3, "start": C("would not keep"), "label": lbl("shows' rights not exclusive", 1190, 480, 22, "muted")},
        {"d": "M 620 720 Q 750 680 880 720", "color": "risk", "width": 5, "start": C("spending fortunes"), "label": lbl("$$$ in", 750, 760, 24, "risk")},
        {"d": rect(1250, 700, 220, 100), "color": "accent2", "width": 5, "start": C("a buyer would get"), "label": lbl("A WINDOW, NOT A LIBRARY", 1360, 840, 20, "accent2")},
    ],
    "actions": [{"kind": "point", "at": C("not a library", 0.2), "dur": 1.4, "target": [1360, 750]}],
    "scale": 0.86, "floor": 1040}, sources=["verge_roku"])
stage("s28_try", "m4_try", {
    "zones": [Z("den", -1600, 1500), Z("exchange", 1500, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("In September"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("device", type="tv", x=700, y=F, at=C("cast shows to the TV"), scale=1.2),
              it("bigphone", x=1100, y=480, at=0.3, scale=0.45, color=PUR, rot=90),
              it("calendar", x=330, y=300, at=C("in October"), pages=[[0, "OCT", "TV APPS"]], scale=0.75),
              it("sign", x=2200, y=330, text="FOR SALE", sub="> $200M cash on hand", at=C("started looking for a buyer"), color="#FFCDD2", size=40),
              it("letters", x=2200, y=600, text="NO BUYER", at=C("It did not find one"), size=70, color="risk")],
    "callouts": [co("Casting, then TV apps in October", 960, 960, C("Quibi tried to adapt"), "white", screen=True, size=40, sub="NBC News", until=C("In September", -0.3)),
                 co("September: looking for a buyer", 960, 960, C("In September"), "gold", screen=True, size=40, sub="Recode")]},
    sources=["nbc_why", "vox_sale"])
stage("s29_buyer", "m4_buyer", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1200, "y": 520, "zoom": 0.9}, {"at": C("For a big streaming"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("pricetag", x=700, y=320, at=C("some cash"), pages=[[0, "CASH"]], sub="on hand"),
              it("bigphone", x=1200, y=460, at=C("the Turnstyle technology"), scale=0.5, color=PUR, rot=[[0, 0], [{"cue": "rotating video"}, 90]]),
              it("clock", x=1750, y=360, at=C("a slate of shows"), period=2.0, text="SHORT WINDOW"),
              it("letters", x=1200, y=160, text="WAIT FOR THE PIECES", at=C("For a big streaming"), size=56, color="gold")],
    "callouts": [co("The pitch: cash, Turnstyle, shows on a short clock", 960, 960, C("According to Recode"), "white", screen=True, size=36, sub="Recode", until=C("For a big streaming", -0.3)),
                 co("Cheaper to wait for the leftovers", 960, 960, C("For a big streaming"), "gold", screen=True, size=40)]},
    sources=["vox_sale", "verge_roku"])
kinetic("s30_t4", "m4_transition", [("Barely six months after launch", 54, "barely six months", None, True), ("the founders made a decision", 60, "made a decision", "risk", False)])

# ====================================================================== PART 5: the end
card("s31_c5", "m5_card", "The End", "Knowing when to stop")
stage("s32_q5", "m5_question", {
    "zones": [Z("office", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("bigphone", x=960, y=440, at=0.2, scale=0.7, color=PUR, offAt=4.0, offText="THE END?")],
    "callouts": [co("When do you stop?", 960, 150, C("When do you stop"), "gold", screen=True, size=46)]})
stage("s33_shut", "m5_shut", {
    "zones": [Z("office", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("The company still had"), "x": 1600, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("Instead of spending"), "x": 2100, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "OCT 21", "2020"]], scale=0.85),
              it("bigphone", x=900, y=440, at=0.3, scale=0.6, color=PUR, offAt=C("shutting down", 0.3), offText="SHUTTING DOWN"),
              it("counter", x=1600, y=220, at=C("The company still had"), prefix="$", suffix="M", steps=[[0, 0], [{"cue": "The company still had", "offset": 1.5}, 350]], text="STILL IN THE BANK (≈)"),
              *crowd([1450, 1570, 1690, 1810], "worry", at=C("employees"), scale=0.6),
              it("coins", **{"from": [1600, 400], "to": [2600, 300]}, at=C("return as much money"), rate=5)],
    "callouts": [co("21 Oct 2020: 'no longer viable'", 960, 960, C("Quibi announced"), "risk", screen=True, size=40, sub="Next TV", until=C("The company still had", -0.3)),
                 co("≈ $350M left, ≈ 200 staff", 960, 960, C("The company still had"), "white", screen=True, size=40, sub="Deadline", until=C("Instead of spending", -0.3)),
                 co("Close, and return money to investors", 960, 960, C("Instead of spending"), "gold", screen=True, size=40)]},
    sources=["nexttv_shut", "deadline_shut"])
stage("s34_quote", "m5_quote", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1200, "y": 520, "zoom": 0.95}, {"at": C("The founders said"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("paper", x=900, y=380, at=0.3, text="'a whole lot more money'", name="DEADLINE", scale=0.8),
              *[it("person", x=1500 + k * 120, pose="read", at=C("every option", 0.3 * k), scale=0.6, hair=k + 1, skin=k) for k in range(3)],
              it("letters", x=1650, y=200, text="EVERY STONE TURNED", at=C("Every one of those"), size=52, color="gold")],
    "callouts": [co("'A whole lot more money without any value'", 960, 960, C("Keeping Quibi going"), "white", screen=True, size=38, sub="Katzenberg to Deadline", until=C("The founders said", -0.3)),
                 co("Partners, buyers, new funding: all tried", 960, 960, C("The founders said"), "gold", screen=True, size=38)]},
    sources=["deadline_shut"])
stage("s35_blame", "m5_blame", {
    "zones": [Z("den")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 0.95}, {"at": C("In their farewell letter"), "x": 1100, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("sign", x=700, y=330, text="'IT WAS THE PANDEMIC'", sub="first explanation", at=C("blamed the pandemic"), color="#FFCDD2", size=32),
              it("paper", x=1500, y=400, at=C("In their farewell letter"), text="'We were not able to do so.'", name="FAREWELL", scale=0.75)],
    "callouts": [co("First: blame the pandemic", 960, 960, C("blamed the pandemic"), "white", screen=True, size=40, until=C("In their farewell letter", -0.3)),
                 co("Later: others found their way. 'We were not able to.'", 960, 960, C("In their farewell letter"), "gold", screen=True, size=36, sub="Fortune")]},
    sources=["fortune_shut"])
stage("s36_roku", "m5_roku", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("A company that had spent"), "x": 1500, "y": 520, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "JAN", "2021"]], scale=0.8),
              it("contract", x=900, y=430, at=C("Roku bought"), text="75+ SHOWS SOLD", sub="to Roku", scale=0.6),
              it("pricetag", x=1300, y=280, at=C("reportedly"), pages=[[0, "< $100M"]], sub="reported (WSJ)"),
              it("tower", x=1900, text="SPENT ≈ $1BN", color="#C62828", h=520, at=C("A company that had spent"), scale=0.8),
              it("tower", x=2250, text="SOLD < $0.1BN", color=PUR, h=[[0, 20], [{"cue": "a small fraction", "offset": 1}, 50]], at=C("a small fraction"), scale=0.8)],
    "callouts": [co("Roku buys 75+ shows, reportedly < $100M", 960, 960, C("Roku bought"), "gold", screen=True, size=38, sub="The Verge / WSJ", until=C("A company that had spent", -0.3)),
                 co("≈ $1bn spent, a small fraction recovered", 960, 960, C("A company that had spent"), "risk", screen=True, size=38)]},
    sources=["verge_roku", "nbc_why"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("den", -1600, 1300), Z("district", 1300, 6000, night=True)], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("But underneath"), "x": 1700, "y": 520, "zoom": 0.95, "dur": 2.6},
            {"at": C("In streaming"), "x": 1400, "y": 520, "zoom": 0.8, "dur": 2.6}], "drift": 2,
    "items": [it("bigphone", x=700, y=440, at=0.2, scale=0.6, color=PUR, offAt=C("Not one thing", 2)),
              it("coins", **{"from": [2300, 300], "to": [1700, 500]}, at=C("raised the money first"), rate=6, until=C("In streaming")),
              it("letters", x=1700, y=200, text="MONEY FIRST, DEMAND LATER", at=C("raised the money first"), size=46, color="risk"),
              it("letters", x=1400, y=650, text="MONEY BUYS SHOWS · HABITS BUY VIEWERS", at=C("In streaming"), size=40, color="gold")],
    "callouts": [co("Pandemic, phone-only, no must-see show", 960, 150, C("The pandemic"), "white", screen=True, size=38, until=C("But underneath", -0.3)),
                 co("Money first, demand later", 960, 150, C("But underneath"), "risk", screen=True, size=42, until=C("In streaming", -0.3)),
                 co("Money buys shows. Only habits buy viewers.", 960, 150, C("In streaming"), "gold", screen=True, size=40)]},
    sources=["fortune_shut", "verge_subs"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_quibi_storyboard.py; edit the generator, not this file.\n"
           "# Episode 19 storyboard (Quibi): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
