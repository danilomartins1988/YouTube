"""Generates projects/the-10-billion-cyberattack-that-froze-maersk/deliverables/documentary/storyboard.yaml (Episode 20, NotPetya).

Bespoke worlds (tones from visual_direction.yaml: thriller -> crisis -> strategy -> reflective): a night server room in Kyiv
where a tax-software update is poisoned, the new `pcgrid` item (a wall of office PCs that the wiper turns red in a spreading
wave, and that are rebuilt one by one) as the through-line, a frozen container terminal with a closed gate and stuck trucks,
a recovery war-room in Maidenhead, a relay flight Ghana -> Nigeria -> London carrying one hard drive, a damage bar chart,
and a courtroom where the insurers' war clause is tested.
Presenter: how the worm spreads (box -> arrow), the domain-controller trap (boxes + arrows), the scale of the bill (bars).
No company logos, no real ransom-screen UI, no likeness of real people (names in text only), no flags.
Run: python tools/gen_notpetya_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-10-billion-cyberattack-that-froze-maersk/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
BLUE = "#1E5AA8"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def trucks(x0, n, at, gap=170, scale=0.55, until=None):
    return [it("device", type="car", x=x0 + k * gap, at=at + 0.2 * k if isinstance(at, (int, float)) else at, scale=scale, color=["#E53935", "#FFB300", "#43A047", "#1E88E5"][k % 4],
               **({"until": until} if until is not None else {})) for k in range(n)]


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("office", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": C("end up stopping trucks"), "x": 1300, "y": 520, "zoom": 0.9, "dur": 2.6}], "drift": 2,
    "items": [it("pcgrid", x=1000, y=440, at=0.2, cols=7, rows=4, cell=120, origin=[0, 0], infectAt=C("end up stopping trucks"), speed=3.5, count=True, scale=0.9),
              it("counter", x=2050, y=230, at=C("costing the world"), prefix="$", suffix="bn+", steps=[[0, 0], [{"cue": "costing the world", "offset": 2}, 10]], text="DAMAGE (WHITE HOUSE EST.)")],
    "callouts": [co("One small software update in Ukraine…", 960, 960, C("How does a small update"), "white", screen=True, size=38, until=C("end up stopping trucks", -0.3)),
                 co("…trucks stuck in New Jersey, drug production halted…", 960, 960, C("end up stopping trucks"), "risk", screen=True, size=36, until=C("costing the world", -0.3)),
                 co("…more than $10 billion in damage", 960, 960, C("costing the world"), "gold", screen=True, size=40)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("port", -1600, 1500), Z("office", 1500, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("Within half an hour"), "x": 2100, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("And what saved it"), "x": 2500, "y": 500, "zoom": 1.15, "dur": 2.4}], "drift": 3,
    "items": [it("ship", type="container", x=700, at=C("One victim was Maersk"), scale=0.8),
              it("letters", x=700, y=200, text="NotPetya", at=0.3, size=90, color="risk"),
              *crowd([1800, 1950, 2100], "worry", at=C("Within half an hour"), scale=0.7),
              it("device", type="laptop", x=1950, y=F, at=C("Within half an hour"), redAt=C("unplug their computers"), scale=0.8),
              it("device", type="server", x=2600, y=F, at=C("a single server in Africa"), scale=0.8, text="OFFLINE")],
    "callouts": [co("NotPetya: {{total.display}} in damage (White House est.)", 960, 960, C("The code was called"), "gold", screen=True, size=38, sub="WIRED", until=C("One victim was Maersk", -0.3)),
                 co("Victim: the world's largest shipping conglomerate", 960, 960, C("One victim was Maersk"), "white", screen=True, size=36, until=C("Within half an hour", -0.3)),
                 co("'Unplug your computers!'", 960, 960, C("Within half an hour"), "risk", screen=True, size=42, until=C("And what saved it", -0.3)),
                 co("Saved by one server that happened to be offline", 960, 960, C("And what saved it"), "gold", screen=True, size=38)]},
    sources=["wired", "wh_2018"])

# ====================================================================== PART 1: the update
card("s03_c1", "m1_card", "The Update", "Kyiv, June 2017")
stage("s04_q1", "m1_question", {
    "zones": [Z("datacenter", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("pcgrid", x=960, y=420, at=0.2, cols=6, rows=3, cell=110, origin=[2.5, 1], infectAt=4.0, speed=2.5, scale=0.9)],
    "callouts": [co("How do you hit a whole country at once?", 960, 150, C("How do you hit"), "gold", screen=True, size=42)]})
stage("s05_mdoc", "m1_mdoc", {
    "zones": [Z("datacenter", night=True)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("Like most software"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("In the spring"), "x": 2200, "y": 500, "zoom": 1.1, "dur": 2.4}], "drift": 3,
    "items": [it("sign", x=700, y=300, text="LINKOS GROUP", sub="small family-run software firm, Kyiv", at=C("A small family-run company"), color="#BBDEFB", size=32),
              it("browser", x=800, y=560, w=420, h=240, at=C("an accounting program"), url="M.E.Doc · tax filing", pages=[[0, "FILE YOUR TAXES"]]),
              it("device", type="server", x=1500, y=F, at=C("Like most software"), scale=0.9, text="UPDATE SERVER"),
              it("conveyor", x=1900, y=F - 40, at=C("it updated itself"), n=5, speed=1.0, goods="box"),
              it("docs", x=2300, y=560, at=C("took over its update servers"), text="UPDATE (+ HIDDEN CODE)", scale=0.6, stamp="ALLEGED", stampAt=C("slipped their own code"))],
    "callouts": [co("Go through software everybody trusts", 960, 960, C("You go through software"), "gold", screen=True, size=40, until=C("A small family-run company", -0.3)),
                 co("M.E.Doc: Ukrainian tax-filing software", 960, 960, C("A small family-run company"), "white", screen=True, size=38, sub="WIRED", until=C("In the spring", -0.3)),
                 co("Spring 2017: update servers hijacked (per US prosecutors)", 960, 960, C("In the spring"), "risk", screen=True, size=34, sub="DOJ indictment via Lawfare")]},
    sources=["wired", "lawfare_doj"])
stage("s06_launch", "m1_launch", {
    "zones": [Z("city", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("A Ukrainian security firm"), "x": 1700, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=0.2, pages=[[0, "JUN 27", "2017"]], scale=0.85),
              it("pcgrid", x=1250, y=360, at=C("they used that back door"), cols=6, rows=3, cell=100, origin=[0, 2], infectAt=C("The malware spread"), speed=4, scale=0.8, text="BANK NETWORK"),
              it("counter", x=1750, y=220, at=C("A Ukrainian security firm"), suffix=" s", steps=[[0, 0], [{"cue": "bring down the network", "offset": 1.5}, 45]], text="BANK NETWORK DOWN"),
              it("counter", x=2250, y=220, at=C("Part of a major transit hub"), suffix=" s", steps=[[0, 0], [{"cue": "Part of a major transit hub", "offset": 1.5}, 16]], text="TRANSIT HUB INFECTED")],
    "callouts": [co("27 June 2017: the eve of a national holiday", 960, 960, C("On June"), "white", screen=True, size=38, sub="WIRED", until=C("A Ukrainian security firm", -0.3)),
                 co("A bank down in 45 s · a transit hub in 16 s", 960, 960, C("A Ukrainian security firm"), "risk", screen=True, size=38, sub="ISSP, via WIRED")]},
    sources=["wired"])
stage("s07_weapons", "m1_weapons", {
    "zones": [Z("office", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("The second"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("sign", x=800, y=280, text="ETERNALBLUE", sub="built by the NSA · leaked in 2017", at=C("The first was EternalBlue"), color="#FFCDD2", size=34),
              it("device", type="laptop", x=800, y=F, at=C("It broke into"), redAt=C("a security fix"), scale=0.9, text="NOT PATCHED"),
              it("sign", x=1700, y=280, text="MIMIKATZ", sub="pulls passwords out of memory", at=C("The second, Mimikatz"), color="#FFE082", size=34),
              it("device", type="laptop", x=1700, y=F, at=C("those passwords"), redAt=C("had been fixed"), scale=0.9, text="PATCHED"),
              it("magnifier", x=[[0, 1500], [6, 1800]], y=[[0, 520], [6, 480]], at=C("pulled passwords"), scale=0.7)],
    "callouts": [co("Weapon 1: EternalBlue (leaked NSA tool)", 960, 960, C("The first was EternalBlue"), "risk", screen=True, size=38, sub="WIRED", until=C("The second", -0.3)),
                 co("Weapon 2: Mimikatz (stolen passwords)", 960, 960, C("The second"), "gold", screen=True, size=38)]},
    sources=["wired", "reg_2018"])
add("p08_spread", "m1_draw", "engine_draw", {
    "title": "How one computer becomes thousands", "board": BOARD, "draw_start": C("One infected machine"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 420, 200, 130), "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.25, "kind": "box", "start": C("One infected machine"), "label": lbl("INFECTED", 660, 490, 24, "risk")},
        {"d": arrow((770, 485), (930, 485), 0.15), "color": "ink", "width": 4, "start": C("missed the security fix")},
        {"d": rect(940, 420, 200, 130), "color": "accent", "width": 6, "kind": "box", "start": C("missed the security fix"), "label": lbl("NO FIX", 1040, 490, 24, "accent")},
        {"d": "M 960 600 L 1120 600", "color": "accent2", "width": 5, "start": C("reads the passwords"), "label": lbl("passwords", 1040, 640, 22, "accent2")},
        {"d": arrow((1150, 485), (1310, 485), 0.15), "color": "ink", "width": 4, "start": C("open a third machine")},
        {"d": rect(1320, 420, 200, 130), "color": "accent3", "width": 6, "kind": "box", "start": C("open a third machine"), "label": lbl("UPDATED", 1420, 490, 24, "accent3")},
        {"d": arrow((1420, 560), (660, 760), -0.2), "color": "risk", "width": 4, "start": C("Every victim becomes"), "label": lbl("…and again, and again", 1040, 820, 24, "risk")},
        {"d": rect(540, 380, 1000, 480), "color": "muted", "width": 3, "kind": "box", "start": C("inside a big company"), "label": lbl("ONE TRUSTED NETWORK: NO WALL", 1040, 900, 24, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("no wall to stop it", 0.2), "dur": 1.4, "target": [1040, 860]}],
    "scale": 0.86, "floor": 1040}, sources=["wired"])
stage("s09_ransom", "m1_ransom", {
    "zones": [Z("office", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("But it was a disguise"), "x": 1350, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 2,
    "items": [it("pcgrid", x=900, y=420, at=0.2, cols=5, rows=3, cell=120, origin=[2, 1], infectAt=C("Then the screens changed"), speed=3, scale=0.85),
              it("pricetag", x=1150, y=700, at=C("asked for"), pages=[[0, "$300 IN BITCOIN"]], sub="the 'ransom'"),
              it("docs", x=1700, y=560, at=C("But it was a disguise"), text="FILES: UNRECOVERABLE", scale=0.65, stamp="WIPER", stampAt=C("It was a wiper")),
              it("letters", x=1700, y=200, text="PAYING CHANGED NOTHING", at=C("Paying changed nothing"), size=50, color="risk")],
    "callouts": [co("'Oops, your important files are encrypted'", 960, 960, C("Others said"), "white", screen=True, size=38, sub="WIRED", until=C("But it was a disguise", -0.3)),
                 co("Not even the hackers could undo it", 960, 960, C("According to the charges"), "risk", screen=True, size=40, sub="DOJ indictment via Lawfare", until=C("This was not a ransom", -0.3)),
                 co("Not ransomware: a wiper", 960, 960, C("This was not a ransom"), "gold", screen=True, size=44)]},
    sources=["wired", "lawfare_doj"])
stage("s10_ukraine", "m1_ukraine", {
    "zones": [Z("city")], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("It even shut down"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("One senior official"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("device", type="hospital", x=500, y=F, at=C("it hit hospitals"), redAt=C("it hit hospitals", 0.6), scale=0.7),
              it("plane", x=900, y=330, at=C("two airports"), scale=0.6, tilt=0),
              it("device", type="server", x=1150, y=F, at=C("banks"), redAt=C("cash machines"), scale=0.7, text="BANK"),
              it("sign", x=1650, y=320, text="CHERNOBYL CLEAN-UP SITE", sub="computers shut down", at=C("It even shut down"), color="#FFE082", size=28),
              it("counter", x=2300, y=150, at=C("One senior official"), suffix="%", steps=[[0, 0], [{"cue": "One senior official", "offset": 2}, 10]], text="COMPUTERS WIPED (1 ESTIMATE)"),
              it("pcgrid", x=2300, y=420, at=C("One senior official"), cols=10, rows=2, cell=70, origin=[0, 0], infectAt=C("were wiped", -1), speed=0.5, scale=0.9)],
    "callouts": [co("Hospitals, 6 power firms, 2 airports, 22+ banks", 960, 960, C("In Ukraine"), "risk", screen=True, size=36, sub="WIRED", until=C("It even shut down", -0.3)),
                 co("Even Chernobyl's clean-up site", 960, 960, C("It even shut down"), "white", screen=True, size=40, until=C("One senior official", -0.3)),
                 co("One official's estimate: {{ukraine.display}} of computers wiped", 960, 960, C("One senior official"), "gold", screen=True, size=36)]},
    sources=["wired"])
kinetic("s11_t1", "m1_transition", [("But the code did not stay in Ukraine", 52, "did not stay in Ukraine", None, True), ("It travelled inside global companies", 54, "inside the networks", "risk", True)])

# ====================================================================== PART 2: Copenhagen goes dark
card("s12_c2", "m2_card", "Copenhagen Goes Dark", "A fifth of world shipping, offline")
stage("s13_q2", "m2_question", {
    "zones": [Z("port")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("ship", type="container", x=900, at=0.2, scale=0.9),
              it("device", type="laptop", x=1500, y=F, at=0.6, redAt=3.5, scale=0.8)],
    "callouts": [co("A fifth of world shipping… without computers?", 960, 150, C("What happens"), "gold", screen=True, size=40)]})
stage("s14_door", "m2_door", {
    "zones": [Z("office", -1600, 1600), Z("city", 1600, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.05}, {"at": C("Through Maersk's global network"), "x": 2200, "y": 520, "zoom": 0.95, "dur": 2.6}], "drift": 3,
    "items": [it("device", type="laptop", x=800, y=F, at=0.2, redAt=C("That was enough"), scale=1.0, text="UKRAINE OFFICE"),
              it("browser", x=800, y=340, w=360, h=200, at=C("asked for"), url="install: M.E.Doc", pages=[[0, "ONE MACHINE"]]),
              it("arrow", **{"from": [1050, 500], "to": [1900, 420]}, at=C("Through Maersk's global network")),
              it("sign", x=2300, y=170, text="HQ · COPENHAGEN", sub="a sunny summer afternoon", at=C("reached its headquarters"), color="#BBDEFB", size=34),
              it("pcgrid", x=2300, y=400, at=C("reached its headquarters"), cols=6, rows=2, cell=100, origin=[0, 0], infectAt=C("the rest of the company", -1), speed=4, scale=0.9)],
    "callouts": [co("The door: one PC in Ukraine with M.E.Doc", 960, 960, C("Maersk's door"), "risk", screen=True, size=38, sub="WIRED", until=C("Through Maersk's global network", -0.3)),
                 co("Then headquarters, then everything", 960, 960, C("Through Maersk's global network"), "white", screen=True, size=40)]},
    sources=["wired"])
stage("s15_scale", "m2_scale", {
    "zones": [Z("port")], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 0.9}, {"at": C("Every container"), "x": 1900, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 4,
    "items": [it("ship", type="container", x=700, at=0.2, scale=0.8),
              it("ship", type="container", x=1500, at=C("vessels"), scale=0.6, flip=True),
              it("counter", x=900, y=200, at=C("This was the world's largest"), steps=[[0, 0], [{"cue": "port terminals", "offset": 1}, 76]], text="TERMINALS"),
              it("counter", x=1500, y=200, at=C("vessels"), steps=[[0, 0], [{"cue": "vessels", "offset": 1.2}, 800]], prefix="≈ ", text="VESSELS"),
              it("pcgrid", x=2200, y=480, at=C("Every container"), cols=5, rows=3, cell=100, origin=[2, 1], infectAt=C("And the computers were gone", -0.5), speed=6, scale=0.85, text="TRACK · BOOK · CLEAR")],
    "callouts": [co("{{fleet.display}} · ≈ 800 vessels · ≈ 1/5 of world capacity", 960, 960, C("This was the world's largest"), "gold", screen=True, size=36, sub="WIRED", until=C("Every container", -0.3)),
                 co("Every box runs on computers", 960, 960, C("Every container"), "white", screen=True, size=40)]},
    sources=["wired"])
stage("s16_port", "m2_port", {
    "zones": [Z("port")], "worldW": 3400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Hundreds of trucks"), "x": 1500, "y": 520, "zoom": 0.85, "dur": 2.6},
            {"at": C("The same thing happened"), "x": 2400, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 4,
    "items": [it("barrier", x=600, at=0.2, closeAt=C("the gates stopped working"), scale=1.0),
              *trucks(820, 8, C("Hundreds of trucks")),
              it("sign", x=1300, y=280, text="TERMINAL CLOSED", sub="for the rest of the day", at=C("the terminal was closed"), color="#FFCDD2", size=34),
              it("counter", x=2400, y=220, at=C("The same thing happened"), steps=[[0, 0], [{"cue": "The same thing happened", "offset": 1.5}, 17]], text="TERMINALS DOWN OF 76"),
              it("crane", x=2600, at=C("Cranes frozen", -1), progress=0.9, scale=0.7),
              it("letters", x=2400, y=520, text="GATES DOWN · CRANES FROZEN", at=C("Gates down"), size=44, color="risk")],
    "callouts": [co("Elizabeth, NJ: ≈ 3,000 trucks on a good day", 960, 960, C("At the terminal in Elizabeth"), "white", screen=True, size=38, sub="WIRED", until=C("Hundreds of trucks", -0.3)),
                 co("Miles of trucks; terminal closed for the day", 960, 960, C("Hundreds of trucks"), "risk", screen=True, size=38, until=C("The same thing happened", -0.3)),
                 co("{{terminals.display}} terminals hit: LA, Rotterdam, Mumbai…", 960, 960, C("The same thing happened"), "gold", screen=True, size=36)]},
    sources=["wired"])
stage("s17_ships", "m2_ships", {
    "zones": [Z("port", -1600, 1500), Z("office", 1500, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("Staff fell back"), "x": 2100, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("ship", type="container", x=[[0, 400], [12, 1100]], at=0.2, scale=0.7),
              it("letters", x=900, y=220, text="A PARKING LOT", at=C("a port becomes a parking lot"), size=60, color="risk"),
              it("device", type="phone", x=1900, y=700, at=C("Staff fell back"), scale=1.2),
              it("paper", x=2300, y=380, at=C("One customer remembered"), text="'500 containers via WhatsApp'", name="WIRED", scale=0.7),
              *crowd([1700, 2550], "phone", at=C("personal email"), scale=0.65)],
    "callouts": [co("The ships kept sailing; the ports could not", 960, 960, C("The ships themselves"), "white", screen=True, size=38, sub="Maersk Q2 2017 / WIRED", until=C("Staff fell back", -0.3)),
                 co("Bookings by personal email, spreadsheets, WhatsApp", 960, 960, C("Staff fell back"), "gold", screen=True, size=36, sub="WIRED")]},
    sources=["maersk_q2", "wired"])
kinetic("s18_t2", "m2_transition", [("To come back, rebuild everything", 54, "rebuild everything", None, True), ("…and find one missing thing", 60, "one thing it could not find", "risk", False)])

# ====================================================================== PART 3: the search for one server
card("s19_c3", "m3_card", "The Search for One Server", "Maidenhead, summer 2017")
stage("s20_q3", "m3_question", {
    "zones": [Z("datacenter")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("pcgrid", x=960, y=420, at=0.2, cols=6, rows=3, cell=110, origin=[0, 0], infectAt=0.3, speed=20, scale=0.9),
              it("magnifier", x=[[0, 600], [8, 1300]], y=[[0, 520], [8, 480]], at=1.0, scale=0.8)],
    "callouts": [co("What do you rebuild first?", 960, 150, C("What do you rebuild"), "gold", screen=True, size=44)]})
stage("s21_maidenhead", "m3_maidenhead", {
    "zones": [Z("office")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Staff kept arriving"), "x": 1500, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("The good news"), "x": 2100, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("sign", x=800, y=300, text="RECOVERY CENTER · MAIDENHEAD", sub="run with Deloitte", at=C("Maersk turned an office"), color="#BBDEFB", size=30),
              it("desk", x=800, at=C("into a recovery center"), scale=0.9, pile=True),
              *[it("person", x=[[0, 2600 + 120 * k], [{"cue": "luggage in hand", "offset": 2}, 1300 + 120 * k]], pose="walk", at=C("Staff kept arriving", 0.3 * k), scale=0.65, hair=k + 1, skin=k % 4) for k in range(4)],
              it("device", type="server", x=2100, y=F, at=C("The good news"), scale=0.8, text="BACKUPS ✓"),
              it("device", type="server", x=2350, y=F, at=C("almost all"), scale=0.8, text="BACKUPS ✓")],
    "callouts": [co("A war room west of London", 960, 960, C("Maersk turned an office"), "white", screen=True, size=40, sub="WIRED", until=C("The good news", -0.3)),
                 co("Good news: backups of almost every server", 960, 960, C("The good news"), "green", screen=True, size=38)]},
    sources=["wired"])
stage("s22_map", "m3_map", {
    "zones": [Z("datacenter")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Maersk had"), "x": 1500, "y": 520, "zoom": 0.9, "dur": 2.4},
            {"at": C("All of them wiped"), "x": 1500, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("board", x=950, y=360, at=C("domain controllers"), text="DOMAIN CONTROLLER = MASTER LIST", rows=[{"name": "WHO MAY LOG IN"}, {"name": "TO WHAT"}, {"name": "FROM WHERE", "color": "gold"}]),
              *[it("device", type="server", x=1500 + 120 * k, y=F, at=C("Maersk had", 0.2 * k), redAt=C("All of them wiped", 0.15 * k), scale=0.6) for k in range(7)],
              it("letters", x=1700, y=200, text="≈ 150 COPIES", at=C("Maersk had"), size=60, color="gold"),
              it("letters", x=1700, y=320, text="NO SEPARATE BACKUP", at=C("there was no separate backup"), size=54, color="risk")],
    "callouts": [co("Domain controllers: the network's master list", 960, 960, C("The bad news was the map"), "white", screen=True, size=36, sub="WIRED", until=C("Maersk had", -0.3)),
                 co("≈ 150 copies, each a backup of the others", 960, 960, C("Maersk had"), "gold", screen=True, size=38, until=C("All of them wiped", -0.3)),
                 co("All wiped at once. No separate backup.", 960, 960, C("All of them wiped"), "risk", screen=True, size=40)]},
    sources=["wired"])
add("p23_trap", "m3_draw", "engine_draw", {
    "title": "The trap", "board": BOARD, "draw_start": C("Here are the servers"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(900, 360, 240, 120), "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.25, "kind": "box", "start": C("all connected to the master list"), "label": lbl("MASTER LIST", 1020, 425, 24, "accent")},
        {"d": rect(560, 640, 180, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("each one a box"), "label": lbl("SERVER", 650, 700, 22, "accent2")},
        {"d": rect(930, 640, 180, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("each one a box", 0.4), "label": lbl("SERVER", 1020, 700, 22, "accent2")},
        {"d": rect(1300, 640, 180, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("each one a box", 0.8), "label": lbl("SERVER", 1390, 700, 22, "accent2")},
        {"d": arrow((960, 490), (660, 630), 0.1), "color": "ink", "width": 4, "start": C("all connected to the master list", 0.4)},
        {"d": arrow((1020, 490), (1020, 630), 0.0), "color": "ink", "width": 4, "start": C("all connected to the master list", 0.6)},
        {"d": arrow((1080, 490), (1380, 630), -0.1), "color": "ink", "width": 4, "start": C("all connected to the master list", 0.8)},
        {"d": "M 880 340 L 1160 500 M 1160 340 L 880 500", "color": "risk", "width": 8, "start": C("reached every copy"), "label": lbl("ALL COPIES WIPED", 1020, 320, 26, "risk")},
        {"d": "M 540 800 L 1500 800", "color": "risk", "width": 5, "start": C("the backups of all the other servers were useless"), "label": lbl("BACKUPS EXIST, BUT NOBODY CAN LOG IN", 1020, 850, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("nobody could log in", 0.2), "dur": 1.4, "target": [1020, 420]}],
    "scale": 0.86, "floor": 1040}, sources=["wired"])
stage("s24_ghana", "m3_ghana", {
    "zones": [Z("office", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("A single domain controller"), "x": 1700, "y": 500, "zoom": 1.1, "dur": 2.4}], "drift": 2,
    "items": [*crowd([600, 740, 880], "phone", at=C("After calling hundreds"), until=C("A single domain controller", 2), scale=0.7),
              it("storm", x=1700, y=200, at=C("A power cut"), scale=0.7),
              it("device", type="server", x=1700, y=F, at=C("A single domain controller"), scale=1.0, text="GHANA · OFFLINE"),
              it("letters", x=1700, y=380, text="SURVIVOR", at=C("they found one survivor"), size=70, color="green"),
              it("burst", x=1700, y=500, at=C("A blackout had saved"))],
    "callouts": [co("One survivor: a domain controller in Ghana", 960, 960, C("they found one survivor"), "gold", screen=True, size=38, sub="WIRED", until=C("A power cut", -0.3)),
                 co("Offline in a power cut, untouched by the malware", 960, 960, C("A power cut"), "green", screen=True, size=36)]},
    sources=["wired"])
stage("s25_relay", "m3_relay", {
    "zones": [Z("airport")], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("so it became a relay race"), "x": 1500, "y": 500, "zoom": 0.9, "dur": 2.4},
            {"at": C("who carried it"), "x": 2300, "y": 480, "zoom": 0.95, "dur": 2.6}], "drift": 3,
    "items": [it("chart", x=850, y=380, w=420, h=260, at=C("so slow"), dur=3, text="UPLOAD: DAYS", pts=[0.05, 0.08, 0.1, 0.12, 0.14], color="risk"),
              it("passport", x=1300, y=420, at=C("Nobody in the Ghana office"), fields=[["VISA (UK)", "NONE"]], openAt=C("Nobody in the Ghana office", 0.6), scale=0.7, until=C("One employee flew", 1)),
              it("plane", x=[[0, 1100], [{"cue": "One employee flew", "offset": 4}, 1700]], y=[[0, 420], [{"cue": "One employee flew", "offset": 4}, 360]], at=C("One employee flew"), until=C("who carried it"), text="GHANA → NIGERIA", scale=0.6),
              it("sign", x=1800, y=640, text="NIGERIA: AIRPORT HAND-OFF", sub="one hard drive", at=C("handed it over"), color="#FFE082", size=26),
              it("plane", x=[[0, 1900], [{"cue": "who carried it", "offset": 6}, 2800]], y=[[0, 400], [{"cue": "who carried it", "offset": 6}, 300]], at=C("who carried it"), text="NIGERIA → LONDON · 6.5 h", scale=0.65)],
    "callouts": [co("Too slow to send: days of upload", 960, 960, C("But the connection in Ghana"), "risk", screen=True, size=38, sub="WIRED", until=C("Nobody in the Ghana office", -0.3)),
                 co("No UK visa, so: a relay race", 960, 960, C("Nobody in the Ghana office"), "white", screen=True, size=40, until=C("who carried it", -0.3)),
                 co("A 6½-hour flight with the company's keystone", 960, 960, C("who carried it"), "gold", screen=True, size=36)]},
    sources=["wired"])
stage("s26_rebuilt", "m3_rebuilt", {
    "zones": [Z("office")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 0.95}, {"at": C("Full recovery"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("pcgrid", x=1000, y=440, at=0.2, cols=8, rows=4, cell=110, origin=[0, 0], infectAt=0.0, speed=50, healAt=C("With that drive", 1), healSpeed=4, count=True, scale=0.85),
              it("calendar", x=1850, y=300, at=C("it took"), pages=[[0, "10 DAYS", "network rebuilt"], [{"cue": "Full recovery"}, "≈ 2 MONTHS", "full recovery"]], scale=0.85)],
    "callouts": [co("10 days: {{rebuild.display}} rebuilt", 960, 960, C("According to Maersk's chairman"), "green", screen=True, size=38, sub="Snabe at Davos, via WIRED", until=C("Full recovery", -0.3)),
                 co("Full recovery: close to two months", 960, 960, C("Full recovery"), "white", screen=True, size=40)]},
    sources=["wired"])
kinetic("s27_t3", "m3_transition", [("Then came the bill", 66, "Then came the bill", None, False), ("Maersk was only one victim", 58, "only one of the victims", "risk", False)])

# ====================================================================== PART 4: the bill
card("s28_c4", "m4_card", "The Bill", "Counting the damage")
stage("s29_q4", "m4_question", {
    "zones": [Z("vault")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("vaultdoor", x=960, at=0.2, openAt=1.0, scale=0.8),
              it("coins", **{"from": [960, 500], "to": [2200, 300]}, at=1.5, rate=6)],
    "callouts": [co("What can a few lines of code cost?", 960, 150, C("How much can"), "gold", screen=True, size=42)]})
stage("s30_maersk", "m4_maersk", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Its chairman later"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("paper", x=800, y=380, at=C("In August"), text="Q2 2017: USD 200–300m hit", name="MAERSK REPORT", scale=0.75),
              it("stack", x=1500, h=[[0, 40], [{"cue": "Its chairman later", "offset": 1.5}, 300]], at=C("Its chairman later"), text="$250–300M", sub="chairman's estimate"),
              *crowd([2050, 2180], "worry", at=C("privately suspected"), scale=0.7),
              it("letters", x=2100, y=250, text="TOO LOW?", at=C("even that was too low"), size=64, color="risk")],
    "callouts": [co("Maersk: a hit of {{maersk_cost.display}}", 960, 960, C("In August"), "gold", screen=True, size=40, sub="Maersk Q2 2017 report", until=C("Its chairman later", -0.3)),
                 co("Chairman: $250–300M. Staff suspected more.", 960, 960, C("Its chairman later"), "white", screen=True, size=38, sub="WIRED")]},
    sources=["maersk_q2", "wired"])
stage("s31_victims", "m4_victims", {
    "zones": [Z("city")], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("FedEx"), "x": 1500, "y": 520, "zoom": 0.95, "dur": 2.2},
            {"at": C("Saint-Gobain"), "x": 2200, "y": 520, "zoom": 0.95, "dur": 2.2}], "drift": 4,
    "items": [it("tower", x=700, text="MERCK $870M", color="#C62828", h=[[0, 20], [{"cue": "reported a loss", "offset": 1.2}, 609]], at=C("The drug maker Merck"), scale=0.8),
              it("tower", x=1200, text="FEDEX / TNT $400M", color="#6A1B9A", h=[[0, 20], [{"cue": "FedEx", "offset": 1.2}, 280]], at=C("FedEx"), scale=0.8),
              it("tower", x=1700, text="SAINT-GOBAIN $384M", color="#1565C0", h=[[0, 20], [{"cue": "Saint-Gobain", "offset": 1.2}, 269]], at=C("Saint-Gobain"), scale=0.8),
              it("tower", x=2200, text="MAERSK $300M", color=BLUE, h=210, at=C("Saint-Gobain", 1), scale=0.8),
              it("tower", x=2700, text="MONDELEZ $188M", color="#EF6C00", h=[[0, 20], [{"cue": "The snack maker", "offset": 1.2}, 132]], at=C("The snack maker"), scale=0.8)],
    "callouts": [co("Merck: {{victims.display}}; some drug production halted", 960, 960, C("The drug maker Merck"), "risk", screen=True, size=36, sub="WIRED", until=C("FedEx", -0.3)),
                 co("FedEx/TNT $400M · Saint-Gobain $384M", 960, 960, C("FedEx"), "white", screen=True, size=38, until=C("The snack maker", -0.3)),
                 co("Mondelez $188M (company-reported losses)", 960, 960, C("The snack maker"), "gold", screen=True, size=36)]},
    sources=["wired"])
add("p32_scale", "m4_draw", "engine_draw", {
    "title": "The scale of the bill", "board": BOARD, "draw_start": C("Here is a typical ransomware attack"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 760 820 L 1600 820 M 760 820 L 760 330", "color": "ink", "width": 4, "start": C("Here is a typical ransomware attack")},
        {"d": "M 800 820 L 800 818 L 880 818 L 880 820", "color": "accent3", "width": 5, "kind": "bar", "start": C("costing"), "label": lbl("ATLANTA $10M", 820, 860, 20, "accent3")},
        {"d": "M 940 820 L 940 805 L 1020 805 L 1020 820", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.4, "kind": "bar", "start": C("Next to it, Maersk"), "label": lbl("MAERSK $300M", 980, 900, 20, "accent2")},
        {"d": "M 1080 820 L 1080 800 L 1160 800 L 1160 820", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.4, "kind": "bar", "start": C("Then FedEx"), "label": lbl("FEDEX $400M", 1120, 860, 20, "accent")},
        {"d": "M 1220 820 L 1220 777 L 1300 777 L 1300 820", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.4, "kind": "bar", "start": C("Then Merck"), "label": lbl("MERCK $870M", 1260, 900, 20, "risk")},
        {"d": "M 1380 820 L 1380 340 L 1560 340 L 1560 820", "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.25, "kind": "bar", "start": C("And then the total"), "label": lbl("TOTAL $10BN+ (WH EST.)", 1470, 310, 22, "risk")},
        {"d": "M 840 790 Q 1050 600 1360 380", "color": "ink", "width": 4, "start": C("barely a line"), "label": lbl("Atlanta ≈ 0.1% of NotPetya", 1000, 600, 22, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("a tenth of one percent", 0.2), "dur": 1.4, "target": [840, 815]}],
    "scale": 0.86, "floor": 1040}, sources=["wired"])
stage("s33_hospitals", "m4_hospitals", {
    "zones": [Z("city")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("For more than a week"), "x": 1500, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("device", type="hospital", x=800, y=F, at=C("In Pennsylvania"), redAt=C("NotPetya hit"), scale=0.9),
              it("device", type="hospital", x=1150, y=F, at=C("two hospitals"), redAt=C("two hospitals", 0.5), scale=0.6),
              it("board", x=1700, y=380, at=C("For more than a week"), text="OFFLINE > 1 WEEK", rows=[{"name": "CARDIOLOGY"}, {"name": "NUCLEAR MEDICINE"}, {"name": "RADIOLOGY"}, {"name": "SURGERY", "color": "risk"}])],
    "callouts": [co("Heritage Valley: 2 hospitals + 78 facilities", 960, 960, C("In Pennsylvania"), "risk", screen=True, size=38, sub="DOJ indictment via Lawfare", until=C("For more than a week", -0.3)),
                 co("Clinical systems out for more than a week", 960, 960, C("For more than a week"), "white", screen=True, size=38)]},
    sources=["lawfare_doj"])
kinetic("s34_t4", "m4_transition", [("Somebody had launched it", 60, "Somebody had launched it", None, False), ("Somebody would have to pay", 62, "somebody would have to pay", "gold", False)])

# ====================================================================== PART 5: who pays
card("s35_c5", "m5_card", "Who Pays", "Blame, charges and insurance")
stage("s36_q5", "m5_question", {
    "zones": [Z("court")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("gavel", x=960, y=420, hits=[2.0, 5.0]),
              it("pcgrid", x=1500, y=420, at=0.5, cols=3, rows=2, cell=100, origin=[0, 0], infectAt=1.5, speed=2, scale=0.8)],
    "callouts": [co("Who answers for a weapon that misses its target?", 960, 150, C("Who is responsible"), "gold", screen=True, size=38)]})
stage("s37_blame", "m5_blame", {
    "zones": [Z("parliament")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("The White House called"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("Russia's government rejected"), "x": 2100, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("docs", x=950, y=560, at=C("In February"), text="UK NCSC: 'ALMOST CERTAINLY'", scale=0.6, stamp="RUSSIAN MILITARY", stampAt=C("responsible")),
              it("paper", x=1500, y=380, at=C("The White House called"), text="'most destructive and costly'", name="WHITE HOUSE", scale=0.75),
              it("docs", x=2200, y=560, at=C("Russia's government rejected"), text="KREMLIN: 'GROUNDLESS'", scale=0.6, stamp="DENIED", stampAt=C("as groundless"))],
    "callouts": [co("UK, Feb 2018: Russian military 'almost certainly' responsible", 960, 960, C("In February"), "white", screen=True, size=34, sub="The Register", until=C("The White House called", -0.3)),
                 co("US: 'the most destructive and costly cyber-attack in history'", 960, 960, C("The White House called"), "risk", screen=True, size=34, sub="White House", until=C("Russia's government rejected", -0.3)),
                 co("Kremlin: 'unsubstantiated and groundless'", 960, 960, C("Russia's government rejected"), "gold", screen=True, size=38, sub="Fortune")]},
    sources=["reg_2018", "wh_2018", "fortune_2018"])
stage("s38_doj", "m5_doj", {
    "zones": [Z("court")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("They said just three"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("gavel", x=900, y=420, hits=[C("charged", 0.4)]),
              it("docs", x=1000, y=600, at=C("American prosecutors charged"), text="INDICTMENT: 6 GRU OFFICERS", scale=0.6, stamp="CHARGED", stampAt=C("charged")),
              it("counter", x=1700, y=230, at=C("They said just three"), prefix="≈ $", suffix="bn", steps=[[0, 0], [{"cue": "They said just three", "offset": 1.5}, 1]], text="3 US VICTIMS (DOJ)"),
              it("letters", x=1700, y=560, text="ACCUSATIONS ≠ CONVICTIONS", at=C("These are accusations"), size=46, color="gold")],
    "callouts": [co("Oct 2020: six GRU officers charged ('Sandworm')", 960, 960, C("In October"), "white", screen=True, size=36, sub="Lawfare / Infosecurity", until=C("They said just three", -0.3)),
                 co("Three US victims: close to $1 billion", 960, 960, C("They said just three"), "risk", screen=True, size=38, until=C("These are accusations", -0.3)),
                 co("Charges, not convictions", 960, 960, C("These are accusations"), "gold", screen=True, size=40)]},
    sources=["lawfare_doj", "infosec_doj"])
stage("s39_insurance", "m5_insurance", {
    "zones": [Z("office")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("If a government's military"), "x": 1500, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("contract", x=900, y=430, at=C("So the victims turned"), text="INSURANCE POLICY", sub="'all risk'", scale=0.65),
              it("magnifier", x=[[0, 800], [5, 1000]], y=[[0, 560], [5, 500]], at=C("an old clause"), scale=0.7),
              it("sign", x=1600, y=300, text="'HOSTILE / WARLIKE ACTS' EXCLUDED", sub="the insurers' argument", at=C("If a government's military"), color="#FFCDD2", size=28),
              it("stack", x=2200, h=[[0, 40], [{"cue": "Merck's fight", "offset": 1.5}, 320]], at=C("Merck's fight"), text="$1.4BN+", sub="Merck's losses in dispute")],
    "callouts": [co("Insurers: an act of war, so no payout", 960, 960, C("If a government's military"), "risk", screen=True, size=38, sub="McGuireWoods", until=C("Merck's fight", -0.3)),
                 co("Merck's dispute: {{merck_ins.display}} in losses", 960, 960, C("Merck's fight"), "gold", screen=True, size=38)]},
    sources=["mcg_merck"])
stage("s40_court", "m5_court", {
    "zones": [Z("court")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In early"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("gavel", x=1000, y=420, hits=[C("A New Jersey court disagreed", 0.4), C("An appeals court agreed", 0.4)]),
              it("docs", x=700, y=600, at=C("The war exclusion"), text="WAR CLAUSE = ARMIES, NOT MALWARE", scale=0.6, stamp="RULING", stampAt=C("not for malware")),
              it("contract", x=1700, y=430, at=C("Merck settled"), text="SETTLED", sub="terms not disclosed", scale=0.65),
              it("calendar", x=2200, y=300, at=C("In early"), pages=[[0, "EARLY", "2024"]], scale=0.8)],
    "callouts": [co("NJ courts: the war exclusion did not apply", 960, 960, C("A New Jersey court disagreed"), "green", screen=True, size=38, sub="McGuireWoods", until=C("In early", -0.3)),
                 co("2024: settled days before the state supreme court", 960, 960, C("In early"), "white", screen=True, size=36)]},
    sources=["mcg_merck"])

# ====================================================================== PAYOFF
stage("s41_payoff", "payoff", {
    "zones": [Z("port", -1600, 1400), Z("office", 1400, 6000, night=True)], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Networks where everything trusts"), "x": 1600, "y": 520, "zoom": 0.9, "dur": 2.6},
            {"at": C("And in the end"), "x": 2100, "y": 500, "zoom": 1.1, "dur": 2.6}], "drift": 2,
    "items": [it("ship", type="container", x=700, at=0.2, scale=0.7),
              it("letters", x=900, y=200, text="NOT THE TARGET. IN THE WAY.", at=C("Maersk was not the target"), size=48, color="risk"),
              it("pcgrid", x=1600, y=440, at=C("Networks where everything trusts"), cols=6, rows=3, cell=100, origin=[0, 1], infectAt=C("They are also fragile", -0.3), speed=6, scale=0.85, text="EFFICIENT · FRAGILE"),
              it("storm", x=2300, y=200, at=C("And in the end"), scale=0.6),
              it("device", type="server", x=2300, y=F, at=C("And in the end"), scale=0.9, text="GHANA")],
    "callouts": [co("You don't have to be the target", 960, 150, C("That the attack"), "white", screen=True, size=40, until=C("Networks where everything trusts", -0.3)),
                 co("Trust everywhere: efficient, and fragile", 960, 150, C("Networks where everything trusts"), "risk", screen=True, size=40, until=C("And in the end", -0.3)),
                 co("Rescued not by a plan, but by a power cut", 960, 150, C("And in the end"), "gold", screen=True, size=40)]},
    sources=["wired"])
add("s42_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_notpetya_storyboard.py; edit the generator, not this file.\n"
           "# Episode 20 storyboard (NotPetya / Maersk): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
