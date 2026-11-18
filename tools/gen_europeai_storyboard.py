"""Generates projects/could-ai-bring-europe-back-to-power/deliverables/documentary/storyboard.yaml
(Episode 63: Could AI Bring Europe Back to Power? The Economic Comeback Nobody Expected).

Premium-documentary tone carried by explanatory animation, in the channel's prime-time cartoon GENRE (original cast and sets,
human characters, day scenes). Bespoke world: remotion/src/animation-engine/CartoonStage/europe.tsx (eurocity, triad, agewave,
squeeze, smartfab, pharmachain, medplaza, lithoweb, twinfab, jetyard, ownmap, profitlab, magnet, eutitle, eubumper; items epitag,
compasspen). Cast: NORA (a researcher) and THEO (a factory engineer), both fictional; no real person is drawn.
Signature animations (brief section 8): 1 Europe between two giants (s03 triad + p04 gap board), 2 the aging workforce (s05
agewave), 3 the automated factory (s11-s13 smartfab + p15 cost-stack board), 4 the pharmaceutical value chain (p20 board + s22
pharmachain), 5 the ASML ecosystem (s26-s27 lithoweb), 6 who owns the value (s33 ownmap + p34 board), 7 the automation profit
experiment (s35 profitlab), 8 Europe's possible comeback (s44 eurocity SCENARIO). Every number is tagged on screen with the
epitag pill: FACT / MECHANISM / SCENARIO / CONJECTURE / ILLUSTRATIVE.
Presenter boards: p04 gap, p08 formula, p15 cost stack, p20 value chain, p34 who owns the value, p42 conditions.
Run: python tools/gen_europeai_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/could-ai-bring-europe-back-to-power/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE = "#2A6FDB", "#F2B33D", "#D9483B", "#2E9E6B", "#7357C9", "#1F8A8C", "#13213B", "#E07A2F"


def toon(x, at=0.0, **kw):
    return it("toon", x=x, at=at, **kw)


def NORA(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.25)
    return toon(x, at, who="shopper", v=1, skin=1, hair=2, hairStyle=3, color=BLUE, glasses=True, scarf="#FFFFFF", **kw)


def THEO(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.25)
    return toon(x, at, who="shopper", v=3, skin=0, hair=1, hairStyle=2, color=ORANGE, glasses=False, scarf=NAVY, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def words(text, x, y, at, **kw):
    kw.setdefault("size", 56)
    return it("toonwords", text=text, x=x, y=y, at=at, **kw)


def tag(*keys, at=0.0):
    """FACT / MECHANISM / SCENARIO / CONJECTURE pill, keyframed: tag((0,'FACT'), (C('...'),'SCENARIO'))"""
    return it("epitag", at=at, x=36, y=36, tags=[[k[0], k[1]] for k in keys])


def pen(x, y, at, **kw):
    return it("compasspen", x=x, y=y, at=at, **kw)


def bumper(id_, seg, num, act, title, caption, color):
    stage(id_, seg, {**W1("eubumper", num=num, act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "strategy",
                     "min_seconds": 4.4, "items": [pen([[0, 2200], [1.0, 1500]], 900, 0.3, scale=0.8, drawAt=1.1, len=700)]},
          sfx=[{"kind": "whoosh", "at": 0.05, "gain": 0.25}, {"kind": "hit", "at": 0.85, "gain": 0.3}])


# ====================================================================== ACT 1: a continent in a squeeze (Theo's town)
stage("s01_hook", "co_hook", {
    **W1("eurocity", era=[[0, 0.0], [C("But Theo's town"), 0.0], [C("What if the technology", 0.3), 1.0]], hyp=True, hypAt=C("What if the technology", 1.2),
         hypText="A HYPOTHESIS TO TEST · NOT A FORECAST", hypX=960, hypY=80),
    "cam": cam((0, 700, 560, 1.2), (C("Europe is falling behind"), 700, 520, 1.05, 1.2), (C("America has the tech giants"), 960, 500, 0.95, 1.4),
               (C("But Theo's town"), 1300, 520, 1.0, WHIP), (C("What if the technology"), 960, 520, 0.85, 1.6)), "drift": 3,
    "items": [THEO([[0, -200], [1.2, 640]], 0.0, face="happy", pose="wave", label="THEO · ENGINEER", labelUntil=C("Europe is falling behind"),
                   faces=[[0, "happy"], [C("Europe is falling behind"), "worry"], [C("But Theo's town"), "happy"], [C("What if the technology"), "shock"]]),
              it("bubble", text="EUROPE IS FALLING BEHIND.", x=1250, y=300, at=C("Europe is falling behind"), until=C("America has the tech giants"), tail=[1100, 600], size=34),
              sign("AMERICA: THE TECH GIANTS", 700, 180, C("America has the tech giants"), color="#BBDEFB", size=34, until=C("But Theo's town")),
              sign("CHINA: THE FACTORIES", 1250, 260, C("China has the factories"), color="#FFCDD2", size=34, until=C("But Theo's town")),
              sign("EUROPE: AGING TOWNS · PRICEY ENERGY · NOSTALGIA", 960, 340, C("Europe has aging towns"), color="#FFF59D", size=28, until=C("But Theo's town")),
              words("BUT...", 1300, 140, C("But Theo's town"), size=64, until=C("So here's the question")),
              NORA([[C("his sister Nora"), 2200], [C("his sister Nora", 1.0), 1500]], C("his sister Nora", -0.3), face="happy", pose="wave", label="NORA · DRUG RESEARCHER", labelUntil=C("So here's the question")),
              words("WHAT IF AI BRINGS EUROPE BACK?", 960, 190, C("What if the technology"), size=54, color="#FFFFFF"),
              tag((0, "THE COMMON VIEW"), (C("So here's the question"), "HYPOTHESIS"))]},
    sfx=[{"kind": "hit", "cue": "But Theo's town", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("eutitle", lines=["COULD AI BRING", "EUROPE BACK", "TO POWER?"], sub="THE ECONOMIC COMEBACK NOBODY EXPECTED"), "cam": STILL(), "drift": 0, "min_seconds": 5.8,
    "items": [THEO(320, 2.6, scale=1.0, face="happy", pose="wave", y=1080), NORA(1640, 2.8, scale=1.0, face="happy", pose="wave", y=1080)]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])
stage("s03_size", "a1_size", {
    **W1("triad", title="GDP 2025, IMF ESTIMATES (CURRENT U.S. DOLLARS)", scale=18,
         bars=[{"label": "UNITED STATES", "v": 30.9, "color": BLUE, "display": "$30.9T", "at": C("a little bigger than China's", 0.3)},
               {"label": "EUROPEAN UNION", "v": 21.3, "color": GOLD, "display": "$21.3T", "at": C("European Union's economy")},
               {"label": "CHINA", "v": 19.6, "color": RED, "display": "$19.6T", "at": C("a little bigger than China's")}],
         foot="SOURCE: IMF WORLD ECONOMIC OUTLOOK DATABASE, 2025 ESTIMATES · EU = 27 MEMBER STATES"),
    "cam": cam((0, 960, 560, 0.9), (C("It's a giant"), 960, 520, 1.0, 1.2), (C("It's just a giant"), 960, 480, 1.1, WHIP)), "drift": 3,
    "items": [words("EUROPE IS NOT POOR", 960, 200, 0.3, until=C("By the IMF's count"), size=58),
              sign("A GIANT...", 960, 210, C("It's a giant"), color="#FFF59D", size=40, until=C("It's just a giant")),
              sign("...THAT KEEPS SLIPPING", 960, 210, C("It's just a giant"), color="#FFCDD2", size=40),
              THEO(200, 0.2, face="happy", pose="point", scale=1.0), tag((0, "FACT"))]},
    sources=["imf_weo"])
add("p04_gap", "a1_gap", "engine_draw", {
    "title": "EU vs U.S.: a widening gap (Draghi report, 2024)", "board": BOARD, "draw_start": C("A report for the European"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 820 L 1480 820", "color": "ink", "width": 5, "start": C("A report for the European")},
        {"d": "M 700 820 L 700 700 L 860 700 L 860 820 Z", "color": "accent", "width": 3, "fill": "accent", "fillOpacity": 0.5, "kind": "bar", "start": C("has been widening"), "label": lbl("GAP 2002 · ≈15%", 780, 682, 22, "accent")},
        {"d": "M 920 820 L 920 580 L 1080 580 L 1080 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.7, "kind": "bar", "start": C("has been widening", 0.6), "label": lbl("GAP 2023 · 30%", 1000, 562, 22, "risk")},
        {"d": arrow((800, 660), (990, 540), -0.25), "color": "risk", "width": 5, "kind": "arrow", "start": C("for years")},
        {"d": rect(1160, 540, 300, 100), "color": "accent2", "width": 5, "kind": "box", "start": C("most of it comes down"), "label": lbl("MOST OF THE GAP", 1310, 600, 24, "accent2")},
        {"d": rect(1160, 680, 300, 80), "color": "risk", "width": 5, "kind": "box", "start": C("European workers simply"), "label": lbl("= PRODUCTIVITY", 1310, 728, 24, "risk")},
        {"d": arrow((1310, 644), (1310, 676), 0.0), "color": "ink", "width": 4, "kind": "arrow", "start": C("a single thing")},
        {"d": dot(1050, 875), "color": "muted", "width": 1, "start": C("A report for the European"), "label": lbl("EU vs U.S. GDP AT CONSTANT 2015 PRICES · SOURCE: DRAGHI REPORT, PART A (SEP 2024)", 1050, 875, 15, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("has been widening", 0.8), "dur": 1.4, "target": [1000, 620]}, {"kind": "point", "at": C("European workers simply", 0.1), "dur": 1.4, "target": [1310, 720]}],
    "scale": 0.86, "floor": 1040}, sources=["draghi_a"])
stage("s05_age", "a1_age", {
    **W1("agewave", workers=[[0, 3.0], [C("Draghi's report warns"), 3.0], [C("for every retiree"), 2.0]],
         years=[[0, "THEO'S TOWN · TODAY"], [C("Draghi's report warns"), "EU · THE COMING YEARS (DRAGHI REPORT)"]], glassX=1760),
    "cam": cam((0, 960, 520, 0.95), (C("Draghi's report warns"), 960, 500, 1.05, 1.4)), "drift": 3,
    "items": [it("bubble", text="LAST SHIFT. ENJOY THE FISHING!", x=600, y=300, at=C("The veterans are retiring"), until=C("Draghi's report warns"), tail=[620, 600], size=28),
              THEO(1500, 0.2, face="worry", pose="shrug", scale=1.0),
              tag((0, "STORY"), (C("Draghi's report warns"), "FACT · OFFICIAL PROJECTION"))]},
    sources=["draghi_a"])
stage("s06_squeeze", "a1_squeeze", {
    **W1("squeeze", press=[[0, 0.0], [C("Then there's the power bill"), 0.0], [C("for electricity"), 0.6], [C("Squeezed"), 1.0]], left="ENERGY", right="TECH GAP",
         meterAt=C("Then there's the power bill"), meterX=330, meterText="EU POWER BILL",
         tags=[[C("for electricity"), "POWER: 2-3× U.S."], [C("packs up and moves"), "STARTUPS LEAVE"]], tagX=1580),
    "cam": cam((0, 960, 520, 1.0), (C("And when Europe grows"), 1200, 500, 1.05, 1.2), (C("Squeezed"), 960, 480, 1.1, WHIP)), "drift": 3,
    "items": [sign("EU COMPANIES vs U.S. COMPANIES · DRAGHI REPORT 2024", 760, 180, C("European companies pay"), color="#FFF8E1", size=24, until=C("And when Europe grows")),
              it("bubble", text="SQUEEZED.", x=500, y=260, at=C("Squeezed"), tail=[300, 560], size=40),
              THEO(260, 0.2, face="worry", pose="shrug", faces=[[0, "worry"], [C("Squeezed"), "shock"]]),
              tag((0, "FACT"))]},
    sources=["draghi_a"])
stage("s07_paradox", "a1_paradox", {
    **W1("eurocity", era=0.35, smoke=0.4),
    "cam": cam((0, 960, 540, 0.9), (C("Those are the facts"), 960, 520, 1.05, WHIP)), "drift": 4,
    "items": [sign("RICH CONTINENT", 420, 200, C("A rich continent"), color="#C8E6C9", size=32),
              sign("WORLD-CLASS UNIVERSITIES", 960, 140, C("world-class universities"), color="#BBDEFB", size=32),
              sign("FAMOUS COMPANIES", 1500, 200, C("famous companies"), color="#E1D5FF", size=32),
              words("...AND A WORRIED FUTURE", 960, 290, C("and a future everyone"), size=50, until=C("Those are the facts")),
              words("NOW: THEO'S HUNCH", 960, 300, C("Now comes Theo's hunch"), size=56, color="#FFFFFF"),
              THEO(560, 0.3, face="smug", pose="point", faces=[[0, "worry"], [C("Now comes Theo's hunch"), "smug"]]),
              tag((0, "FACT"), (C("Now comes Theo's hunch"), "HYPOTHESIS"))]})

# ====================================================================== ACT 2: the old formula
bumper("s08_b2", "a2_card", "2", "ACT TWO", "THE OLD FORMULA", "Workers + machines = stuff. Simple. Until now.", ORANGE)
stage("s09_formula", "a2_formula", {
    **W1("eurocity", era=0.0, smoke=1.0),
    "cam": cam((0, 300, 560, 1.15), (C("More workers plus"), 300, 520, 1.25, 1.2), (C("Theo's great-grandfather"), 700, 520, 0.95, 1.6)), "drift": 4,
    "items": [words("WORKERS + MACHINES = STUFF", 420, 140, C("More workers plus"), size=56, until=C("Europe's industrial revolution")),
              words("THE OLD RECIPE", 700, 140, C("Europe's industrial revolution"), size=56, until=C("Theo's great-grandfather")),
              sign("GREAT-GRANDPA'S FACTORY (FULL OF PEOPLE)", 300, 230, C("Theo's great-grandfather"), color="#FFE0B2", size=30),
              THEO(980, 0.3, face="happy", pose="point"), tag((0, "MECHANISM"))]})
add("p10_formula", "a2_draw", "engine_draw", {
    "title": "Theo's problem: the growth formula", "board": BOARD, "draw_start": C("Let me draw"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(600, 470, 220, 110), "color": "accent2", "width": 6, "kind": "box", "start": C("Output equals"), "label": lbl("OUTPUT", 710, 535, 30, "accent2")},
        {"d": dot(860, 525), "color": "ink", "width": 1, "start": C("Output equals"), "label": lbl("=", 860, 540, 50, "ink")},
        {"d": rect(900, 470, 220, 110), "color": "risk", "width": 6, "kind": "box", "start": C("the number of workers"), "label": lbl("WORKERS", 1010, 535, 30, "risk")},
        {"d": dot(1160, 525), "color": "ink", "width": 1, "start": C("times what each"), "label": lbl("×", 1160, 540, 50, "ink")},
        {"d": rect(1200, 470, 260, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("times what each"), "label": lbl("PER WORKER", 1330, 535, 28, "accent3")},
        {"d": arrow((1010, 600), (1010, 740), 0.0), "color": "risk", "width": 6, "kind": "arrow", "start": C("starts falling"), "label": lbl("FALLING", 1010, 780, 24, "risk")},
        {"d": arrow((1330, 740), (1330, 600), 0.0), "color": "accent3", "width": 6, "kind": "arrow", "start": C("Each worker has to produce more"), "label": lbl("MUST RISE", 1330, 780, 24, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("starts falling", 0.1), "dur": 1.4, "target": [1010, 700]}, {"kind": "point", "at": C("Each worker has to produce more", 0.2), "dur": 1.4, "target": [1330, 680]}],
    "scale": 0.86, "floor": 1040})
stage("s11_question", "a2_question", {
    **W1("smartfab", arms=3, armX=500, armGap=480, scanX=1800, techs=1, techX=300, carts=1),
    "cam": cam((0, 960, 540, 1.0), (C("Then a shrinking workforce"), 1100, 520, 1.1, 1.2), (C("And a different question"), 960, 500, 0.95, WHIP)), "drift": 4,
    "items": [words("FAR MORE, WITH FAR FEWER?", 960, 140, C("What if technology"), size=56, until=C("And a different question")),
              sign("A SHRINKING WORKFORCE ≠ A DEATH SENTENCE", 1100, 230, C("Then a shrinking workforce"), color="#C8E6C9", size=30, until=C("And a different question")),
              words("WHO OWNS THE MACHINES?", 960, 150, C("And a different question"), size=60, color="#FFFFFF"),
              THEO(1500, 0.2, face="smug", pose="point", scale=1.1), tag((0, "HYPOTHESIS"))]})

# ====================================================================== ACT 3: when machines do the work
bumper("s12_b3", "a3_card", "3", "ACT THREE", "WHEN MACHINES DO THE WORK", "Robots shown are original designs. No viral demos were harmed.", BLUE)
stage("s13_factory", "a3_factory", {
    **W1("smartfab", arms=4, armX=100, armGap=440, scanX=1450, maintX=600, maintAt=C("Sensors warn"), carts=3, twinAt=C("a digital twin"), techs=1, techX=1750,
         hiAt=[[0, None], [C("Cameras running AI"), "vision"], [C("Sensors warn"), "maint"], [C("Self-driving carts"), "carts"], [C("a digital twin"), "twin"]]),
    "cam": cam((0, 800, 560, 1.0), (C("Cameras running AI"), 1450, 480, 1.25, 1.2), (C("Sensors warn"), 620, 420, 1.25, 1.2), (C("Self-driving carts"), 960, 700, 1.05, 1.2),
               (C("And engineers test"), 960, 420, 0.9, 1.4)), "drift": 3,
    "items": [THEO([[0, -200], [1.4, 300]], 0.0, face="shock", pose="armsup", scale=1.0),
              sign("MACHINE VISION: “INDUSTRY-GRADE” (IFR, 2026)", 1450, 140, C("calls that kind"), color="#FFF59D", size=28, until=C("Sensors warn")),
              sign("PREDICTIVE MAINTENANCE", 620, 140, C("Sensors warn"), color="#FFCDD2", size=30, until=C("Self-driving carts")),
              sign("SELF-DRIVING CARTS", 960, 600, C("Self-driving carts"), color="#BBDEFB", size=30, until=C("And engineers test")),
              tag((0, "FACT"))]},
    sources=["ifr_wr26"])
stage("s14_proven", "a3_proven", {
    **W1("smartfab", arms=4, armX=200, armGap=440, scanX=1650, maintX=900, carts=2, techs=2, techX=360, techGap=900),
    "cam": cam((0, 960, 540, 0.95), (C("So this isn't"), 960, 560, 1.1, 1.2), (C("It's a factory where"), 900, 600, 1.2, WHIP)), "drift": 3,
    "items": [it("bubble", text="ROBOTS THAT LEARN ANY JOB? NOT YET.", x=1300, y=280, at=C("Robots that can learn"), until=C("So this isn't"), tail=[1500, 600], size=28),
              words("NOT A FACTORY WITH NO PEOPLE", 960, 140, C("So this isn't"), size=52, until=C("It's a factory where")),
              words("EACH PERSON DOES FAR MORE", 960, 140, C("It's a factory where"), size=56, color="#FFFFFF"),
              THEO(1200, 0.3, face="worry", pose="clipboard", hold="clipboard", faces=[[0, "worry"], [C("Theo likes the sound"), "grin"]], hops=[C("Theo likes the sound", 0.3)]),
              tag((0, "FACT"), (C("So this isn't"), "MECHANISM"))]},
    sources=["ifr_wr26"])
stage("s15_robots", "a3_robots", {
    **W1("triad", title="ROBOTS PER 10,000 FACTORY WORKERS, 2025 (IFR)", scale=1.05, gap=420, bars=[
        {"label": "GERMANY", "v": 469, "color": GOLD, "display": "469", "at": C("Germany already runs")},
        {"label": "U.S.", "v": 323, "color": BLUE, "display": "323", "at": C("than America does")},
        {"label": "WORLD", "v": 152, "color": "#8E9AAF", "display": "152", "at": C("than the world average")}],
        foot="IFR ROBOT DENSITY RELEASE, NOV 12 2026 (DATA YEAR 2025)"),
    "cam": cam((0, 960, 520, 1.0), (C("Germany already runs"), 960, 540, 0.92, 1.4)), "drift": 2,
    "items": [words("NOT STARTING FROM SCRATCH", 960, 200, 0.3, size=50, until=C("Germany already runs")), tag((0, "FACT"))]},
    sources=["ifr_density"])
add("p16_bill", "a3_bill", "engine_draw", {
    "title": "A factory's cost stack (illustrative)", "board": BOARD, "draw_start": C("Picture a factory's costs"), "speed": 1600, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 820 L 1480 820", "color": "ink", "width": 5, "start": C("Picture a factory's costs")},
        {"d": "M 720 820 L 720 700 L 900 700 L 900 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.5, "kind": "bar", "start": C("as a stack"), "label": lbl("MATERIALS", 810, 765, 20, "ink")},
        {"d": "M 720 700 L 720 560 L 900 560 L 900 700 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.6, "kind": "bar", "start": C("as a stack", 0.4), "label": lbl("LABOR", 810, 635, 22, "ink")},
        {"d": "M 720 560 L 720 500 L 900 500 L 900 560 Z", "color": "accent", "width": 3, "fill": "accent", "fillOpacity": 0.6, "kind": "bar", "start": C("as a stack", 0.8), "label": lbl("MACHINES · TECH", 810, 535, 16, "ink")},
        {"d": dot(810, 470), "color": "ink", "width": 1, "start": C("as a stack", 0.8), "label": lbl("BEFORE", 810, 470, 24, "ink")},
        {"d": "M 1100 820 L 1100 700 L 1280 700 L 1280 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.5, "kind": "bar", "start": C("Automation shrinks"), "label": lbl("MATERIALS", 1190, 765, 20, "ink")},
        {"d": "M 1100 700 L 1100 660 L 1280 660 L 1280 700 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.6, "kind": "bar", "start": C("the labor slice"), "label": lbl("LABOR", 1190, 686, 16, "ink")},
        {"d": "M 1100 660 L 1100 520 L 1280 520 L 1280 660 Z", "color": "accent", "width": 3, "fill": "accent", "fillOpacity": 0.75, "kind": "bar", "start": C("become a bigger part"), "label": lbl("MACHINES · SOFTWARE", 1190, 590, 16, "ink")},
        {"d": dot(1190, 490), "color": "ink", "width": 1, "start": C("Automation shrinks"), "label": lbl("AFTER", 1190, 490, 24, "ink")},
        {"d": arrow((1300, 590), (1440, 450), -0.2), "color": "accent3", "width": 6, "kind": "arrow", "start": C("So the money starts flowing"), "label": lbl("→ OWNERS OF THE TECH", 1420, 420, 22, "accent3")},
        {"d": dot(1050, 875), "color": "muted", "width": 1, "start": C("Picture a factory's costs"), "label": lbl("ILLUSTRATIVE · NO REAL COST SHARES · A MECHANISM, NOT A FORECAST", 1050, 875, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("the labor slice", 0.1), "dur": 1.4, "target": [1190, 680]}, {"kind": "point", "at": C("So the money starts flowing", 0.3), "dur": 1.4, "target": [1420, 440]}],
    "scale": 0.86, "floor": 1040})
stage("s17_people", "a3_people", {
    **W1("smartfab", arms=3, armX=900, armGap=440, scanX=500, carts=1, techs=2, techX=300, techGap=1300, hi="arms"),
    "cam": cam((0, 960, 560, 1.0), (C("But if fewer hands"), 960, 520, 0.95, 1.2), (C("And Europe already owns"), 960, 500, 1.1, WHIP)), "drift": 4,
    "items": [sign("DESIGN · CODE · REPAIRS", 960, 150, C("Someone designs"), color="#C8E6C9", size=32, until=C("But if fewer hands")),
              sign("FEWER HANDS → CHEAP LABOR MATTERS LESS", 960, 150, C("But if fewer hands"), color="#FFE0B2", size=30, until=C("And Europe already owns")),
              sign("OWNING THE TECH → MAY MATTER MORE", 960, 230, C("and owning the technology"), color="#E1D5FF", size=30, until=C("And Europe already owns")),
              words("EUROPE OWNS A LOT OF IT", 960, 150, C("And Europe already owns"), size=56, color="#FFFFFF"),
              THEO(700, 0.2, face="happy", pose="clipboard", hold="clipboard"),
              NORA([[C("Nora works in"), 2200], [C("Nora works in", 0.9), 1450]], C("Nora works in", -0.3), face="happy", pose="wave"),
              tag((0, "MECHANISM"), (C("may matter more"), "CONJECTURE"))]})

# ====================================================================== ACT 4: pharma, Europe's hidden advantage
bumper("s18_b4", "a4_card", "4", "ACT FOUR", "PHARMA: EUROPE'S HIDDEN ADVANTAGE", "Nora's world: the medicine cabinet of the planet.", GREEN)
stage("s19_surplus", "a4_surplus", {
    **W1("medplaza", harbour=True, outAt=C("Last year the EU sold"), inAt=C("than it bought"), balance="EU PHARMA TRADE SURPLUS 2025 ≈ $249BN", balanceAt=C("more medicine than"), balanceX=1300, balanceY=170),
    "cam": cam((0, 700, 540, 1.0), (C("than it bought"), 1100, 520, 0.95, 1.4), (C("Its biggest customer"), 1300, 480, 1.05, 1.0)), "drift": 3,
    "items": [sign("EUROSTAT VIA EFPIA · ECB 2025 AVERAGE RATE · OUR CONVERSION", 1300, 270, C("more medicine than"), color="#FFF8E1", size=22),
              sign("BIGGEST CUSTOMER: THE U.S.", 1300, 350, C("Its biggest customer"), color="#BBDEFB", size=30),
              NORA(300, 0.2, face="happy", pose="point", scale=1.0), tag((0, "FACT"))]},
    sources=["efpia_26", "ecb_2025_avg"])
stage("s20_six", "a4_six", {
    **W1("medplaza", towers=[{"city": "BASEL", "sub": "ROCHE · SWITZERLAND", "at": C("Roche and Novartis")}, {"city": "BASEL", "sub": "NOVARTIS · SWITZERLAND", "at": C("and Novartis")},
                             {"city": "CAMBRIDGE", "sub": "ASTRAZENECA · UK", "at": C("AstraZeneca and GSK")}, {"city": "LONDON", "sub": "GSK · UK", "at": C("and GSK")},
                             {"city": "PARIS", "sub": "SANOFI · FRANCE", "at": C("Sanofi in France"), "eu": True}, {"city": "BAGSVÆRD", "sub": "NOVO NORDISK · DENMARK", "at": C("Novo Nordisk in Denmark"), "eu": True}],
         gap=300, ropeAt=C("Switzerland and Britain are"), ropeText="IN THE EU · OTHERS: EUROPE, NOT EU"),
    "cam": cam((0, 960, 560, 0.9), (C("Each of them sells"), 960, 520, 0.95, 1.2)), "drift": 2,
    "items": [words("NORA'S NEIGHBORHOOD", 960, 120, 0.2, size=50, until=C("Each of them sells")),
              sign("SELLING MEDICINE ALL OVER THE WORLD", 960, 120, C("Each of them sells"), color="#C8E6C9", size=32),
              tag((0, "FACT"))]},
    sources=["roche_fy25", "novartis_fy25", "az_fy25", "gsk_fy25", "sanofi_fy25", "novo_ar25"])
add("p21_chain", "a4_chain", "engine_draw", {
    "title": "Where a medicine's value is created", "board": BOARD, "draw_start": C("Let me draw it"), "speed": 1600, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 420, 170, 90), "color": "accent", "width": 6, "kind": "box", "start": C("Research finds"), "label": lbl("RESEARCH", 645, 474, 22, "accent")},
        {"d": arrow((735, 465), (775, 465), 0.0), "color": "ink", "width": 4, "kind": "arrow", "start": C("Patents protect")},
        {"d": rect(780, 420, 170, 90), "color": "accent", "width": 6, "kind": "box", "start": C("Patents protect"), "label": lbl("PATENTS", 865, 474, 22, "accent")},
        {"d": arrow((955, 465), (995, 465), 0.0), "color": "ink", "width": 4, "kind": "arrow", "start": C("Trials prove")},
        {"d": rect(1000, 420, 170, 90), "color": "accent", "width": 6, "kind": "box", "start": C("Trials prove"), "label": lbl("TRIALS", 1085, 474, 22, "accent")},
        {"d": arrow((1175, 465), (1215, 465), 0.0), "color": "ink", "width": 4, "kind": "arrow", "start": C("Then factories make it")},
        {"d": rect(1220, 420, 170, 90), "color": "accent2", "width": 6, "kind": "box", "start": C("Then factories make it"), "label": lbl("FACTORY", 1305, 474, 22, "accent2")},
        {"d": arrow((1305, 515), (1305, 585), 0.0), "color": "ink", "width": 4, "kind": "arrow", "start": C("ship it worldwide")},
        {"d": rect(1220, 590, 170, 90), "color": "accent2", "width": 6, "kind": "box", "start": C("ship it worldwide"), "label": lbl("WORLD SALES", 1305, 644, 20, "accent2")},
        {"d": "M 550 560 Q 760 700 1180 560", "color": "accent3", "width": 7, "start": C("Most of the value"), "label": lbl("MOST OF THE VALUE: IDEAS · PATENTS · PROOF", 860, 690, 24, "accent3")},
        {"d": dot(980, 860), "color": "muted", "width": 1, "start": C("Most of the value"), "label": lbl("A MECHANISM: WHERE VALUE IS CREATED, NOT A MEASURED SPLIT", 980, 860, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Most of the value", 0.2), "dur": 1.6, "target": [860, 600]}],
    "scale": 0.86, "floor": 1040})
stage("s22_novo", "a4_novo", {
    **W1("pharmachain", stepAt=[0.1, 0.4, 0.7, C("It's expanding its factories"), C("decades of science"), C("decades of science", 0.4)], valueAt=C("But what it really sells"), flowAt=C("decades of science"),
         flowText="THE SCIENCE IS WHAT IT REALLY SELLS"),
    "cam": cam((0, 700, 540, 0.95), (C("It's expanding"), 1300, 520, 1.0, 1.4), (C("But what it really sells"), 960, 520, 0.85, 1.4)), "drift": 3,
    "items": [sign("NOVO NORDISK · BAGSVÆRD, DENMARK (EU)", 700, 140, 0.3, color="#FFFFFF", size=30, until=C("It spends")),
              it("counter", x=600, y=150, at=C("It spends"), prefix="≈ $", suffix="BN A YEAR ON RESEARCH", decimals=1, steps=[[0, 0], [C("It spends"), 0], [C("a year on research"), 7.9]],
                 text="NOVO NORDISK ANNUAL REPORT 2025 · ECB 2025 AVG RATE · OUR CONVERSION", until=C("It's expanding")),
              NORA(250, 0.2, face="happy", pose="point", scale=1.0), tag((0, "FACT"), (C("But what it really sells"), "MECHANISM"))]},
    sources=["novo_ar25", "ecb_2025_avg"])
stage("s23_ai", "a4_ai", {
    **W1("pharmachain", stepAt=[0.1, 0.3, 0.5, 0.7, 0.9, 1.1], valueAt=None),
    "cam": cam((0, 400, 540, 1.15), (C("But a new medicine"), 960, 520, 0.85, 1.4), (C("AI may help"), 400, 520, 1.15, 1.2)), "drift": 3,
    "items": [sign("ASTRAZENECA BOUGHT MODELLA AI TO PUT AI INTO CANCER R&D · COMPANY STATEMENT", 700, 120, C("AstraZeneca bought"), color="#E1D5FF", size=24, until=C("But a new medicine")),
              sign("LAB → PHARMACY: MORE THAN A DECADE", 960, 120, C("But a new medicine"), color="#FFE0B2", size=30, until=C("AI may help")),
              sign("FOR EVERY SUCCESS, THOUSANDS FAIL", 960, 200, C("for every success"), color="#FFCDD2", size=30, until=C("AI may help")),
              words("AI: BETTER BETS, NOT GUARANTEES", 400, 140, C("AI may help"), size=50, color="#FFFFFF"),
              NORA(250, C("Can AI speed"), face="worry", pose="clipboard", hold="clipboard", faces=[[0, "worry"], [C("AI may help"), "happy"]]),
              it("bubble", text="CAREFUL. NO MAGIC PILLS.", x=600, y=330, at=C("Nora is cautious"), until=C("AstraZeneca bought"), tail=[300, 600], size=28),
              tag((0, "CONJECTURE"), (C("AstraZeneca bought"), "FACT"), (C("AI may help"), "CONJECTURE"))]},
    sources=["az_fy25", "efpia_26"])
stage("s24_reveal", "a4_reveal", {
    **W1("pharmachain", stepAt=[0.1, 0.25, 0.4, 0.55, 0.7, 0.85], valueAt=C("own, and keep improving"), flowAt=0.5),
    "cam": cam((0, 960, 520, 0.8), (C("own, and keep improving"), 600, 500, 1.05, 1.4)), "drift": 3,
    "items": [words("LESSON: NO NEED TO MAKE EVERYTHING AT HOME...", 960, 140, C("You don't have to"), size=44, until=C("You have to own")),
              words("...OWN WHAT EVERYONE NEEDS", 600, 140, C("You have to own"), size=52, color="#FFFFFF"),
              THEO(1500, 0.2, face="grin", pose="cheer", hops=[C("Theo's first big lesson", 0.3)]), tag((0, "MECHANISM"))]})

# ====================================================================== ACT 5: the machines behind the machines
bumper("s25_b5", "a5_card", "5", "ACT FIVE", "THE MACHINES BEHIND THE MACHINES", "Europe's quiet suppliers to everybody else.", PURPLE)
stage("s26_asml", "a5_asml", {
    **W1("lithoweb", machine="EUV LITHOGRAPHY · VELDHOVEN, NETHERLANDS (EU)", sups=[], fabs=[]),
    "cam": cam((0, 960, 520, 1.3), (C("Last year it kept"), 960, 520, 1.0, 1.4), (C("doesn't make a single chip"), 960, 480, 1.15, WHIP)), "drift": 3,
    "items": [sign("THE ONLY COMPANY THAT MAKES THESE MACHINES", 960, 130, C("is the only company"), color="#E1D5FF", size=32, until=C("Last year")),
              it("counter", x=960, y=180, at=C("Last year it kept"), prefix="≈ $", suffix="BN PROFIT · 2025", decimals=1, steps=[[0, 0], [C("Last year it kept"), 0], [C("in profit"), 10.8]],
                 text="ASML FY2025 NET INCOME · ECB 2025 AVG RATE · OUR CONVERSION"),
              words("ZERO CHIPS MADE", 960, 990, C("doesn't make a single chip"), size=58, color="#FFFFFF"),
              NORA(260, 0.2, face="happy", pose="point", scale=1.0), THEO(1660, 0.2, face="shock", pose="armsup", scale=1.0),
              tag((0, "FACT"))]},
    sources=["asml_fy25", "asml_ar25", "ecb_2025_avg"])
stage("s27_web", "a5_web", {
    **W1("lithoweb", machine="ONE MACHINE · A WHOLE ECOSYSTEM", coinAt=C("part of the bill"),
         sups=[{"label": "OPTICS", "at": C("feed in lenses"), "x": 240, "y": 200, "color": TEAL}, {"label": "LASERS", "at": C("lasers"), "x": 240, "y": 360, "color": BLUE},
               {"label": "PRECISION PARTS", "at": C("and parts"), "x": 240, "y": 520, "color": ORANGE}],
         fabs=[{"label": "CHIP FAB · ASIA", "at": C("Out go machines"), "x": 1700, "y": 220}, {"label": "CHIP FAB · AMERICA", "at": C("and America"), "x": 1700, "y": 430},
               {"label": "AI-CHIP FAB · ANYWHERE", "at": C("Every time anyone"), "x": 1700, "y": 640}]),
    "cam": cam((0, 700, 520, 1.0), (C("Out go machines"), 1250, 520, 1.0, 1.4), (C("Every time anyone"), 960, 520, 0.85, 1.4)), "drift": 2,
    "items": [sign("THOUSANDS OF SUPPLIERS", 420, 90, C("Thousands of suppliers"), color="#FFF59D", size=28),
              sign("A FACTORY BOOM ANYWHERE → ORDERS IN THE NETHERLANDS", 1320, 90, C("part of the bill"), color="#C8E6C9", size=28),
              tag((0, "FACT"), (C("Every time anyone"), "MECHANISM"))]},
    sources=["asml_ar25"])
stage("s28_siemens", "a5_siemens", {
    **W1("twinfab", fx=200, twinAt=C("including digital twins"), shipAt=C("When the world automates"), dests=["FACTORY · ASIA", "FACTORY · AMERICAS", "FACTORY · EUROPE", "FACTORY · AFRICA"]),
    "cam": cam((0, 700, 540, 1.0), (C("Its chief executive"), 960, 500, 0.95, 1.4), (C("When the world automates"), 1200, 520, 0.85, 1.4)), "drift": 3,
    "items": [sign("SIEMENS · MUNICH, GERMANY (EU)", 700, 130, 0.3, color="#FFFFFF", size=30, until=C("Its chief executive")),
              sign("CONTROLLERS · AUTOMATION · SOFTWARE", 700, 210, C("sells factories their controllers"), color="#BBDEFB", size=28, until=C("Its chief executive")),
              sign("“INDUSTRIAL AI IS AN EXCEPTIONAL GROWTH OPPORTUNITY” · ROLAND BUSCH, CEO", 960, 380, C("Its chief executive"), color="#FFF59D", size=24, until=C("When the world automates")),
              words("SOMEBODY SELLS THE AUTOMATION", 1200, 130, C("When the world automates"), size=50, color="#FFFFFF"),
              THEO(1700, 0.2, face="happy", pose="point", scale=1.0), tag((0, "FACT"), (C("When the world automates"), "MECHANISM"))]},
    sources=["siemens_fy26"])
stage("s29_airbus", "a5_airbus", {
    **W1("jetyard", join=[[0, 0.0], [C("Its real product"), 0.0], [C("engineered and certified"), 1.0]], joinDone=C("engineered and certified", 0.6),
         sups=[{"label": "WINGS · SITE A", "at": C("Thousands of parts"), "x": 260, "y": 620}, {"label": "FUSELAGE · SITE B", "at": C("from many countries"), "x": 960, "y": 680},
               {"label": "ENGINES · SUPPLIER C", "at": C("from many countries", 0.5), "x": 1660, "y": 620}]),
    "cam": cam((0, 960, 520, 0.95), (C("Its real product"), 960, 560, 0.9, 1.2), (C("That's exactly where"), 960, 460, 1.1, 1.2)), "drift": 3,
    "items": [sign("AIRBUS · RUN FROM NEAR TOULOUSE, FRANCE (EU)", 960, 110, 0.3, color="#FFFFFF", size=28, until=C("Its real product")),
              words("THE REAL PRODUCT: COORDINATION", 960, 120, C("Its real product"), size=50, until=C("with years of orders")),
              sign("BACKLOG: 8,754 JETS (AIRBUS, END 2025)", 960, 120, C("with years of orders"), color="#BBDEFB", size=30, until=C("That's exactly where")),
              sign("WHERE SMARTER SOFTWARE + AUTOMATION COULD PAY OFF", 960, 120, C("That's exactly where"), color="#E1D5FF", size=30),
              tag((0, "FACT"), (C("That's exactly where"), "CONJECTURE"))]},
    sources=["airbus_fy25", "airbus_agm26"])
stage("s30_limits", "a5_limits", {
    **W1("triad", title="A REALITY CHECK: ROBOTS INSTALLED IN 2025 (IFR)", scale=0.0013, bars=[
        {"label": "CHINA", "v": 354226, "color": RED, "display": "354,226", "at": C("China installs far more")},
        {"label": "EUROPE", "v": 73054, "color": GOLD, "display": "73,054", "at": C("China installs far more", 0.5)}], gap=520,
        foot="INDUSTRIAL ROBOTS INSTALLED IN 2025 (IFR WORLD ROBOTICS 2026)"),
    "cam": cam((0, 960, 540, 0.95), (C("But Europe owns"), 960, 520, 1.05, 1.2)), "drift": 2,
    "items": [words("EUROPE DOESN'T DOMINATE EVERYTHING", 960, 200, C("Europe doesn't dominate"), size=50, until=C("China installs")),
              sign("CLOUD & CONSUMER TECH: MOSTLY AMERICAN", 1500, 280, C("most cloud"), color="#BBDEFB", size=26, until=C("But Europe owns")),
              words("BUT IT OWNS CAPABILITIES THAT MAY GAIN VALUE", 960, 200, C("But Europe owns"), size=44, color="#FFFFFF"),
              THEO(1700, 0.2, face="smug", pose="shrug", scale=1.0), tag((0, "FACT"), (C("But Europe owns"), "CONJECTURE"))]},
    sources=["ifr_wr26"])

# ====================================================================== ACT 6: owning vs operating (centerpiece)
bumper("s31_b6", "a6_card", "6", "ACT SIX", "OWNING vs. OPERATING", "Theo's big idea. Made-up company, real economics.", RED)
stage("s32_old", "a6_old", {
    **W1("eurocity", era=[[0, 0.2], [C("In a more automated world"), 0.2], [C("to who owns them"), 0.9]], smoke=0.5),
    "cam": cam((0, 400, 540, 1.1), (C("In a more automated world"), 1300, 520, 1.0, 1.6), (C("And the question shifts"), 960, 520, 0.9, 1.4)), "drift": 4,
    "items": [words("THE OLD PRIZE: THE FACTORY + ITS JOBS", 400, 150, 0.3, until=C("In a more automated world"), size=48),
              sign("FEWER PEOPLE ON THE FLOOR", 1300, 160, C("may employ fewer people"), color="#FFE0B2", size=30, until=C("And the question shifts")),
              words("WHO OPERATES? → WHO OWNS?", 960, 160, C("And the question shifts"), size=60, color="#FFFFFF"),
              THEO(1100, 0.2, face="smug", pose="point"), tag((0, "HYPOTHESIS"))]})
add("p33_owner", "a6_company", "engine_draw", {
    "title": "Company E (hypothetical): who does what", "board": BOARD, "draw_start": C("So Theo sketches"), "speed": 1600, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(580, 400, 330, 300), "color": "accent2", "width": 6, "kind": "box", "start": C("Call it Company E"), "label": lbl("COMPANY E · EUROPE", 745, 440, 24, "accent2")},
        {"d": dot(745, 500), "color": "ink", "width": 1, "start": C("develop the technology"), "label": lbl("DEVELOPS THE TECH", 745, 500, 20, "ink")},
        {"d": dot(745, 545), "color": "ink", "width": 1, "start": C("It owns the patents"), "label": lbl("OWNS PATENTS + SOFTWARE", 745, 545, 18, "ink")},
        {"d": dot(745, 590), "color": "ink", "width": 1, "start": C("makes the key decisions"), "label": lbl("MAKES KEY DECISIONS", 745, 590, 18, "ink")},
        {"d": dot(745, 635), "color": "ink", "width": 1, "start": C("carries the big risks"), "label": lbl("CARRIES THE BIG RISKS", 745, 635, 18, "ink")},
        {"d": arrow((920, 500), (1180, 500), -0.15), "color": "accent", "width": 6, "kind": "arrow", "start": C("Partner factories"), "label": lbl("KNOW-HOW · LICENSE", 1050, 455, 20, "accent")},
        {"d": rect(1190, 420, 270, 260), "color": "risk", "width": 6, "kind": "box", "start": C("Partner factories"), "label": lbl("PARTNER FACTORIES", 1325, 460, 22, "risk")},
        {"d": dot(1325, 530), "color": "ink", "width": 1, "start": C("in other countries"), "label": lbl("OTHER COUNTRIES", 1325, 530, 18, "ink")},
        {"d": dot(1325, 580), "color": "ink", "width": 1, "start": C("make the product"), "label": lbl("MAKE THE PRODUCT", 1325, 580, 18, "ink")},
        {"d": arrow((1180, 640), (920, 640), -0.15), "color": "accent3", "width": 6, "kind": "arrow", "start": C("under license"), "label": lbl("PRODUCT", 1050, 700, 22, "accent3")},
        {"d": dot(1020, 860), "color": "muted", "width": 1, "start": C("So Theo sketches"), "label": lbl("HYPOTHETICAL COMPANY · NO REAL FIRM IMPLIED", 1020, 860, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("carries the big risks", 0.1), "dur": 1.4, "target": [745, 635]}, {"kind": "point", "at": C("Partner factories", 0.2), "dur": 1.4, "target": [1325, 540]}],
    "scale": 0.86, "floor": 1040})
stage("s34_numbers", "a6_numbers", {
    **W1("profitlab", colX=760, gap=560, vals=False,
         hiAt=[[0, None], [C("earns a small, steady fee"), "FACTORY FEE"], [C("Company E keeps"), "E KEEPS"], [C("its costs fall"), "FACTORY COSTS"], [C("Its fee shrinks"), "FACTORY FEE"], [C("grows by more than half"), "E KEEPS"]],
         cols=[{"name": "BEFORE AUTOMATION", "sub": "PER $100 OF SALES", "at": C("Now watch the money"),
                "blocks": [{"label": "FACTORY COSTS", "v": 60, "color": "#7E8DA3", "at": C("on top of its costs")}, {"label": "FACTORY FEE", "v": 3, "color": TEAL, "at": C("earns a small, steady fee")},
                           {"label": "E's R&D + SALES", "v": 20, "color": BLUE, "at": C("Company E keeps")}, {"label": "E KEEPS", "v": 17, "color": GOLD, "at": C("keeps what's left"), "show": True}]},
               {"name": "AFTER AUTOMATION", "sub": "SAME FEE RULE: COST + 5%", "at": C("Then the factory automates"),
                "blocks": [{"label": "FACTORY COSTS", "v": 50, "color": "#7E8DA3", "at": C("its costs fall")}, {"label": "FACTORY FEE", "v": 2.5, "color": TEAL, "at": C("Its fee shrinks")},
                           {"label": "E's R&D + SALES", "v": 20, "color": BLUE, "at": C("Its fee shrinks", 0.5)}, {"label": "E KEEPS", "v": 27.5, "color": GOLD, "at": C("grows by more than half"), "show": True}]}],
         notes=[{"at": C("earns a small, steady fee"), "text": "FACTORY: COSTS + A SMALL FEE", "sub": "A ROUTINE, LOW-RISK JOB", "x": 1640, "y": 300},
                {"at": C("grows by more than half", 0.6), "text": "E's SHARE: $17 → $27.50", "sub": "ONLY IF E REALLY DOES THE WORK", "color": GREEN, "x": 1640, "y": 440}]),
    "cam": cam((0, 960, 540, 0.95)), "drift": 1, "min_seconds": 20,
    "items": [tag((0, "ILLUSTRATIVE · MADE-UP NUMBERS"))]})
stage("s35_catch", "a6_catch", {
    **W1("ownmap", hqX=470, fX=1450, licAt=0.1, prodAt=0.2, feeAt=0.3, saleAt=0.4, glowAt=C("The real work"), hyp=True, hypAt=0, hypText="HYPOTHETICAL COMPANY E"),
    "cam": cam((0, 960, 520, 0.9), (C("while rivals automate"), 1450, 520, 1.1, 1.2), (C("And simply registering"), 470, 520, 1.15, 1.4)), "drift": 3,
    "items": [sign("CATCH: ONLY IF E DOES THE WORK · AND IF PRICES HOLD", 960, 170, C("But there are catches"), color="#FFE0B2", size=28, until=C("while rivals automate")),
              sign("RIVALS AUTOMATE TOO → PRICES MAY FALL", 1450, 170, C("while rivals automate"), color="#FFCDD2", size=28, until=C("And simply registering")),
              sign("A PATENT REGISTERED SOMEWHERE ≠ PROFIT THERE", 600, 170, C("And simply registering"), color="#FFF59D", size=28, until=C("The real work")),
              words("REAL WORK · REAL PEOPLE · REAL DECISIONS", 600, 170, C("The real work"), size=46, color="#FFFFFF"),
              tag((0, "MECHANISM"))]})
stage("s36_question", "a6_question", {
    **W1("ownmap", hqX=470, fX=1450, licAt=0.1, prodAt=0.2, saleAt=C("that profit from"), glowAt=0.2, hqText="EUROPE?", fText="AUTOMATED PRODUCTION · EVERYWHERE"),
    "cam": cam((0, 1300, 540, 1.1), (C("It's whether"), 960, 520, 0.9, 1.6)), "drift": 3,
    "items": [words("NOT: WIN BACK THE ASSEMBLY LINE", 1300, 160, 0.3, size=48, until=C("It's whether")),
              words("ATTRACT + KEEP: COMPANIES · SCIENTISTS · MONEY · IDEAS", 960, 160, C("It's whether"), size=40, color="#FFFFFF"),
              tag((0, "HYPOTHESIS"))]})
stage("s36b_energy", "a6_energy", {
    **W1("cleanpower", plantText="COMPANY E's PARTNER PLANT · ENERGY-RICH COUNTRY (SCENARIO)", billX=1640, billScale=5.5,
         factors=[{"label": "ENERGY", "at": C("Energy."), "color": "#FFF59D"}, {"label": "MONEY", "at": C("Money.")},
                  {"label": "LOGISTICS", "at": C("Logistics.")}, {"label": "STABILITY", "at": C("Stability.")},
                  {"label": "TAXES ON PRODUCING", "at": C("And the taxes on producing"), "color": "#FFCDD2"}], facX=300, facGap=330, facY=150,
         bill=[{"label": "ENERGY + GRID", "v": 55, "color": BLUE, "at": C("Yet an industry study")},
               {"label": "TAXES + CHARGES ≈45%", "v": 45, "color": RED, "at": C("goes to taxes and charges")}],
         billText="BRAZIL POWER COMPANIES' REVENUE, 2024"),
    "cam": cam((0, 960, 540, 0.95), (C("Brazil, for example"), 500, 560, 1.1, 1.4), (C("Yet an industry study"), 1500, 540, 1.05, 1.4),
               (C("So a country with cheap power"), 960, 540, 0.9, 1.4), (C("And even if"), 960, 520, 0.95, 1.2)), "drift": 3,
    "items": [it("bubble", text="WHAT ABOUT CHEAP POWER?", x=1300, y=420, at=C("Then Theo's boss"), until=C("If robots make labor"), tail=[1500, 640], size=28),
              sign("BRAZIL: MOSTLY RENEWABLE ELECTRICITY (EPE)", 560, 270, C("gets most of its electricity"), color="#C8E6C9", size=28, until=C("Yet an industry study")),
              sign("+ A SALES-TAX OVERHAUL UNDER WAY", 1100, 270, C("overhauling its sales taxes"), color="#FFF59D", size=28, until=C("So a country with cheap power")),
              words("CHEAP POWER + COMPETITIVE COSTS TO PRODUCE?", 960, 270, C("So a country with cheap power"), size=44, color="#FFFFFF", until=C("And even if")),
              sign("THE TECH PROFIT CAN STILL COME HOME TO EUROPE", 960, 270, C("And even if"), color="#E1D5FF", size=32),
              tag((0, "MECHANISM"), (C("Brazil, for example"), "FACT"), (C("So a country with cheap power"), "SCENARIO"))]},
    sources=["epe_ben26", "pwc_acende25", "br_reform"])

# ====================================================================== ACT 7: a magnet for capital
bumper("s37_b7", "a7_card", "7", "ACT SEVEN", "A MAGNET FOR CAPITAL", "What pulls money and talent in, and what it costs.", TEAL)
stage("s38_magnet", "a7_magnet", {
    **W1("magnet", pulls=[{"label": "STRONG COURTS", "icon": "hq", "at": C("Strong courts")}, {"label": "RESEARCH LABS", "icon": "lab", "at": C("research labs")},
                          {"label": "SINGLE MARKET", "icon": "cash", "at": C("a huge single market")}, {"label": "INDUSTRIAL CLUSTERS", "icon": "hq", "at": C("industrial clusters")},
                          {"label": "LIVABLE CITIES", "icon": "people", "at": C("and cities people")}]),
    "cam": cam((0, 960, 520, 0.95), (C("It has real pull"), 960, 560, 1.05, 1.2)), "drift": 3,
    "items": [words("CAN EUROPE PULL THEM IN?", 960, 120, 0.3, size=56, until=C("It has real pull")),
              THEO(1700, 0.2, face="happy", pose="point", scale=1.0), tag((0, "MECHANISM"))]})
stage("s39_kinds", "a7_kinds", {
    **W1("magnet", pulls=[{"label": "WEALTHY RESIDENTS", "icon": "people", "at": C("Wealthy residents")}, {"label": "INVESTMENT", "icon": "cash", "at": C("productive investment")},
                          {"label": "HEAD OFFICE", "icon": "hq", "at": C("A head office")}, {"label": "RESEARCH LAB", "icon": "lab", "at": C("is not a research lab")}]),
    "cam": cam((0, 960, 540, 0.95)), "drift": 3,
    "items": [sign("RESIDENTS ≠ INVESTMENT", 960, 110, C("are not the same"), color="#FFE0B2", size=34, until=C("A head office")),
              sign("HEAD OFFICE ≠ RESEARCH LAB", 960, 110, C("A head office"), color="#FFE0B2", size=34, until=C("Only real activity")),
              words("ONLY REAL ACTIVITY BUILDS REAL GROWTH", 960, 120, C("Only real activity"), size=48, color="#FFFFFF"),
              NORA(1700, 0.2, face="worry", pose="point", scale=1.0), tag((0, "MECHANISM"))]})
stage("s40_risks", "a7_risks", {
    **W1("magnet", pulls=[{"label": "NEWCOMERS", "icon": "people", "at": 0.1}, {"label": "CAPITAL", "icon": "cash", "at": 0.2}],
         risks=[{"label": "PRICIER HOUSING", "at": C("Pricier housing"), "x": 330, "y": 170}, {"label": "WIDER INEQUALITY", "at": C("Wider inequality"), "x": 760, "y": 170},
                {"label": "SKILL SHORTAGES", "at": C("Shortages of skilled"), "x": 1180, "y": 170}, {"label": "BUDGETS: NOT AUTOMATIC", "at": C("Rich arrivals"), "x": 1600, "y": 170}]),
    "cam": cam((0, 960, 520, 0.95), (C("That depends on"), 960, 520, 1.05, 1.2)), "drift": 3,
    "items": [sign("DEPENDS ON WHAT THEY DO AND HOW THEY'RE TAXED", 960, 390, C("That depends on"), color="#FFFFFF", size=30),
              THEO(1700, 0.3, face="worry", pose="shrug"), tag((0, "MECHANISM"))]})

# ====================================================================== ACT 8: could Europe come back?
bumper("s41_b8", "a8_card", "8", "ACT EIGHT", "COULD EUROPE COME BACK?", "The verdict, and the fine print.", GOLD)
add("p42_conditions", "a8_conditions", "engine_draw", {
    "title": "What a comeback would take", "board": BOARD, "draw_start": C("Let me list it"), "speed": 1600, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        *[{"d": rect(620, y, 60, 60), "color": "accent3", "width": 5, "kind": "box", "start": C(cue)} for y, cue in
          ((400, "Let companies grow"), (480, "Make money easier"), (560, "Bring down energy"), (640, "Actually use AI"), (720, "And compete hard"))],
        *[{"d": f"M {632} {y + 30} L {646} {y + 46} L {670} {y + 14}", "color": "accent3", "width": 6, "start": C(cue, 0.4), "label": lbl(t_, 710, y + 42, 26, "ink", "start")} for y, cue, t_ in
          ((400, "Let companies grow", "SCALE UP WITHOUT LEAVING"), (480, "Make money easier", "EASIER CAPITAL"), (560, "Bring down energy", "CHEAPER ENERGY"),
           (640, "Actually use AI", "USE AI IN EVERYDAY WORK"), (720, "And compete hard", "WIN THE TALENT RACE"))],
        {"d": arrow((1250, 560), (1430, 560), 0.0), "color": "risk", "width": 6, "kind": "arrow", "start": C("Miss these"), "label": lbl("OR PROFITS FLOW ELSEWHERE", 1340, 520, 20, "risk")},
        {"d": dot(1030, 860), "color": "muted", "width": 1, "start": C("Let me list it"), "label": lbl("CONDITIONS, NOT PREDICTIONS · THEMES OF THE DRAGHI REPORT (2024)", 1030, 860, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Miss these", 0.2), "dur": 1.4, "target": [1340, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["draghi_a"])
stage("s43_verdict", "a8_verdict", {
    "zones": [Z("smartfab", x0=-1600, x1=1600, arms=3, armX=-300, armGap=420, scanX=900, maintX=-600, carts=1, techs=1, techX=200),
              Z("eurocity", x0=1600, x1=5000, era=1.0, smoke=0.0)], "worldW": 3400,
    "cam": cam((0, 600, 540, 1.0), (C("That race is China's"), 600, 520, 1.05, 1.2), (C("But as the owner"), 2600, 520, 0.95, 1.8), (C("Europe has the assets"), 1700, 520, 0.75, 1.6)), "drift": 2,
    "items": [words("COULD AI BRING EUROPE BACK TO POWER?", 600, 150, 0.3, size=44, until=C("Not by building")),
              words("NOT BY OUT-BUILDING CHINA", 600, 150, C("Not by building"), size=50, until=C("But as the owner")),
              sign("NOT BY COPYING SILICON VALLEY", 600, 240, C("And not by copying"), color="#FFCDD2", size=30, until=C("But as the owner")),
              words("OWNER · DEVELOPER · FINANCIER · LICENSOR", 2600, 150, C("But as the owner"), size=46, color="#FFFFFF", until=C("Europe has the assets")),
              sign("A PLAUSIBLE PATH, NOT A PROMISE", 2600, 240, C("It's a plausible path"), color="#E1D5FF", size=32, until=C("Europe has the assets")),
              words("THE ASSETS: YES · THE CHOICES: NOT YET MADE", 1700, 150, C("Europe has the assets"), size=46, color="#FFFFFF"),
              NORA(2400, 0.3, face="happy", pose="point"), THEO(2800, 0.3, face="happy", pose="stand"),
              tag((0, "VERDICT · HYPOTHESIS"), (C("Europe has the assets"), "FACT + SCENARIO"))]})
stage("s44_close", "a8_close", {
    **W1("eurocity", era=[[0, 0.0], [C("In a world run"), 0.0], [C("who owns the technology"), 1.0]], smoke=[[0, 1.0], [C("who owns the technology"), 0.2]],
         hyp=True, hypAt=C("And for Theo's old factory town"), hypText="SCENARIO · A POSSIBLE PATH, NOT A FORECAST"),
    "cam": cam((0, 300, 560, 1.15), (C("In a world run"), 960, 520, 0.95, 1.6), (C("who owns the technology"), 1500, 520, 1.05, 1.4), (C("And for Theo's old factory town"), 960, 520, 0.82, 1.6)), "drift": 2,
    "items": [words("FACTORIES + WORKERS = POWER", 300, 150, 0.3, size=50, until=C("In a world run")),
              words("WHO OWNS THE TECHNOLOGY, THE MACHINES, THE IDEAS?", 1300, 150, C("who owns the technology"), size=42, color="#FFFFFF", until=C("And for Theo's old factory town")),
              NORA([[C("And for Theo's old factory town"), -200], [C("And for Theo's old factory town", 1.2), 700]], C("And for Theo's old factory town", -0.2), face="happy", pose="cheer"),
              THEO([[C("And for Theo's old factory town"), 2200], [C("And for Theo's old factory town", 1.2), 1250]], C("And for Theo's old factory town", -0.2), face="happy", pose="wave"),
              tag((0, "SCENARIO"))]})
add("s45_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s46_button", "button", {
    **W1("eurocity", era=1.0, smoke=0.0),
    "cam": cam((0, 1300, 560, 1.15), (3.0, 1300, 560, 1.3, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [THEO(1150, 0.0, face="grin", pose="cheer", hops=[1.2], scale=1.1),
              it("bubble", text="SO... DO I STILL HAVE A JOB?", x=1150, y=250, at=0.8, until=2.8, tail=[1150, 520], size=30),
              NORA(1500, 0.6, face="happy", pose="point", scale=1.1),
              it("bubble", text="YES. NOW YOU RUN THE ROBOTS.", x=1500, y=330, at=2.9, tail=[1500, 560], size=30),
              pen(1300, 760, 3.6, drawAt=3.8, len=500, scale=0.8)]},
    sfx=[{"kind": "hit", "at": 3.0, "gain": 0.3}])

write(OUT, "# GENERATED by tools/gen_europeai_storyboard.py; edit the generator, not this file.\n"
           "# Episode 63 storyboard (Could AI Bring Europe Back to Power?): story-over-stats cut following THEO; bespoke worlds in CartoonStage/europe.tsx.\n")
