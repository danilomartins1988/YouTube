"""Generates projects/will-ai-make-japan-rich-again/deliverables/documentary/storyboard.yaml
(Episode 66: Will AI Make Japan Rich Again?).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/japan.tsx (jtown, jshop, jplatform, jroad, jcare, jhist, jfactory, jdensity, jkonbini,
jdemo, jyen, jscale, jtitle, jbumper; items jtag, kobo). Story over statistics: one protagonist (HIRO, a workshop owner in the
fictional town of Hoshimachi), AOI (his granddaughter) and KOBO (their cobot); all fictional. No real person is drawn; companies are
named in narration and shown only as generic buildings with plain plaques; no logos.
Signature animations: 1 the shrinking workforce (p04 board + s05 platform crowd), 2 the robots go abroad (s15 crates), 3 arms vs
androids (s19 restocking cutaway + s20 retired/at-work/prototype), 4 Kobo's install and load cycle (s22), 5 per worker, not per
citizen (p31 board). Presenter boards: p04 workforce bars, p17 why a shortage sells robots, p23 arm/brain/user, p31 per worker.
Every number carries a jtag pill: FACT / PROJECTION / ESTIMATE / OUR CALC / COMPANY CLAIM / PLAN / FINDING / STORY.
Run: python tools/gen_japanai_storyboard.py   (it also checks that every cue phrase exists in its segment's narration)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

SLUG = "will-ai-make-japan-rich-again"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE, INDIGO = "#2F6FD1", "#F5B700", "#D9443A", "#3E9B5F", "#7357C9", "#1F8A8C", "#1B2A4A", "#F08A24", "#2E3F7F"
OX = 3400  # offset for a second zone


def toon(x, at=0.0, **kw):
    return it("toon", x=x, at=at, **kw)


def HIRO(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.25)
    return toon(x, at, who="shopper", v=3, skin=4, hair=6, hairStyle=2, color=INDIGO, glasses=True, **kw)


def AOI(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.2)
    return toon(x, at, who="shopper", v=8, skin=0, hair=1, hairStyle=4, color=TEAL, glasses=False, scarf=GOLD, **kw)


def MOM(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.05)
    return toon(x, at, who="shopper", v=11, skin=4, hair=6, hairStyle=3, color=PURPLE, glasses=True, scarf="#F48FB1", **kw)


def CARER(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.15)
    return toon(x, at, who="shopper", v=4, skin=1, hair=1, hairStyle=1, color=GREEN, glasses=False, scarf=None, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def words(text, x, y, at, **kw):
    kw.setdefault("size", 56)
    return it("toonwords", text=text, x=x, y=y, at=at, **kw)


def bub(text, x, y, at, until=None, tail=None, size=30):
    d = {"text": text, "x": x, "y": y, "at": at, "size": size}
    if until is not None:
        d["until"] = until
    if tail:
        d["tail"] = tail
    return it("bubble", **d)


def tag(*keys, at=0.0):
    return it("jtag", at=at, x=36, y=36, tags=[[k[0], k[1]] for k in keys])


def bumper(id_, seg, act, title, caption, color):
    stage(id_, seg, {**W1("jbumper", act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "trade",
                     "min_seconds": 4.2, "items": [it("kobo", x=[[0, 2300], [1.4, 1640]], y=1010, at=1.0, scale=0.8, wave=[2.0], face="happy")]},
          sfx=[{"kind": "whoosh", "at": 0.25, "gain": 0.25}, {"kind": "hit", "at": 1.0, "gain": 0.3}])


def board(id_, seg, title, start, strokes, actions, enter_left=True, sources=()):
    add(id_, seg, "engine_draw", {
        "title": title, "board": BOARD, "draw_start": C(start), "speed": 1500, "push": 0.003,
        "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3} if enter_left else {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
        "strokes": strokes, "actions": actions, "scale": 0.86, "floor": 1040}, sources=sources)


# ====================================================================== CHAPTER 1: the empty stool
stage("s01_hook", "co_hook", {
    "zones": [Z("jtown", x0=-1600, x1=3000, signAt=0.0, shutters=[[0, 0.2], [C("His whole country"), 0.2], [C("And yet"), 0.6]], train=[1.0]),
              Z("jfactory", x0=3000, x1=7200, ox=OX, share=0.6, plaque="ROBOT MAKER (GENERIC)")],
    "worldW": 2400,
    "cam": cam((0, 360, 600, 1.55), (C("For a long time now"), 520, 560, 1.7, 1.2), (C("Nobody calls"), 420, 600, 1.45, 0.8),
               (C("His whole country"), 900, 520, 0.85, 1.6), (C("And yet"), OX + 1100, 520, 0.95, WHIP), (C("industrial robots"), OX + 1500, 520, 1.05, 1.2),
               (C("So could"), OX + 1000, 500, 0.82, 1.6)), "drift": 3,
    "items": [HIRO([[0, -200], [1.6, 240]], 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("Help wanted"), "worry"], [C("Nobody calls"), "deadpan"]],
                   label="HIRO · WORKSHOP OWNER (FICTIONAL)", labelUntil=C("For a long time now")),
              bub("TINY PARTS. BIG MACHINES.", 330, 300, C("parts that end up"), until=C("For a long time now"), tail=[260, 520], size=28),
              bub("...ANYONE?", 560, 250, C("Nobody calls"), until=C("His whole country"), tail=[300, 520], size=34),
              words("A WHOLE COUNTRY SHORT OF WORKERS", 900, 150, C("His whole country"), size=50, until=C("And yet")),
              words("≈ 4 IN 10 OF THE WORLD'S ROBOTS", OX + 1300, 150, C("industrial robots"), size=58, until=C("So could")),
              words("PROBLEM → ADVANTAGE?", OX + 1000, 160, C("So could"), size=62),
              tag((0, "STORY · FICTIONAL TOWN"), (C("industrial robots"), "FACT · IFR (2024 PRODUCTION)"))]},
    sources=["ifr_japan25"], sfx=[{"kind": "whoosh", "cue": "And yet", "gain": 0.3}, {"kind": "hit", "cue": "industrial robots", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("jtitle"), "cam": STILL(), "drift": 0, "min_seconds": 5.6,
    "items": [it("kobo", x=[[0, -200], [2.2, 300]], y=1010, at=1.6, scale=0.8, wave=[3.2], face="happy")]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])
stage("s03_town", "c1_town", {
    "zones": [Z("jtown", x0=-1600, x1=3000, signAt=0.0, shutters=[[0, 0.2], [C("More shops keep"), 0.2], [C("Hiro's apprentice"), 0.8]], train=[C("The train comes")]),
              Z("jshop", x0=3000, x1=7200, ox=OX, run=0, stoolHi=[C("his stool"), C("The strange thing")])],
    "worldW": 2400,
    "cam": cam((0, 1500, 500, 0.85), (C("The train comes"), 1700, 460, 1.0, 1.4), (C("More shops keep"), 700, 520, 0.95, 1.4),
               (C("Hiro's apprentice"), OX + 900, 540, 0.95, WHIP), (C("his stool"), OX + 780, 640, 1.35, 1.2), (C("The strange thing"), OX + 1100, 540, 1.0, 1.2),
               (C("What's missing"), OX + 780, 660, 1.45, 1.4)), "drift": 3,
    "items": [words("HOSHIMACHI (FICTIONAL)", 1100, 150, 0.3, size=50, until=C("Hiro's apprentice")),
              words("THE EMPTY STOOL", OX + 780, 260, C("his stool"), size=58, until=C("The strange thing")),
              HIRO(OX + 1250, C("Hiro's apprentice"), face="worry", pose="stand", hold="phone", faces=[[0, "worry"], [C("They want more parts"), "shock"], [C("What's missing"), "worry"]]),
              bub("MORE ORDERS THAN EVER!", OX + 1300, 300, C("They want more parts"), until=C("What's missing"), tail=[OX + 1260, 520], size=28),
              words("WHAT'S MISSING: HANDS", OX + 800, 240, C("What's missing"), size=58),
              tag((0, "STORY · FICTIONAL TOWN AND CAST"))]})
board("p04_draw", "c1_draw", "The shrinking workforce (working-age population, ages 15-64)", "Let me draw what happened", [
    {"d": "M 640 860 L 1560 860", "color": "ink", "width": 5, "start": C("Let me draw what happened")},
    {"d": "M 720 860 L 720 330 L 940 330 L 940 860 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.6, "kind": "bar", "start": C("This bar is everyone"), "label": lbl("1995 PEAK · 87.3M", 830, 312, 26, "accent2")},
    {"d": "M 1080 860 L 1080 410 L 1300 410 L 1300 860 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.35, "kind": "bar", "start": C("This bar is today"), "label": lbl("2024 · 73.7M", 1190, 480, 26, "ink")},
    {"d": "M 1080 330 L 1300 330 L 1300 410 L 1080 410 Z", "color": "risk", "width": 5, "kind": "box", "start": C("Japan has lost"), "label": lbl("−13.5M", 1190, 380, 30, "risk")},
    {"d": rect(1360, 520, 260, 110), "color": "risk", "width": 6, "kind": "box", "start": C("all of Tokyo"), "label": lbl("≈ ALL OF TOKYO", 1490, 588, 28, "risk")},
    {"d": arrow((1400, 520), (1305, 380), 0.2), "color": "risk", "width": 5, "kind": "arrow", "start": C("all of Tokyo", 0.4)},
    {"d": dot(1100, 920), "color": "muted", "width": 1, "start": C("Let me draw what happened"), "label": lbl("IPSS (1995 CENSUS PEAK 87.26M) · STATISTICS BUREAU (OCT 2024: 73.73M) · DIFFERENCE = OUR CALC · TOKYO ≈ 14.3M (TMG)", 1100, 920, 15, "muted")},
], [{"kind": "point", "at": C("This bar is today", 0.4), "dur": 1.4, "target": [1190, 500]}, {"kind": "point", "at": C("Japan has lost", 0.6), "dur": 1.6, "target": [1190, 370]},
    {"kind": "react", "at": C("That's the size of the hole")}], sources=["ipss23", "stat_pop24", "tmg_pop"])
stage("s05_future", "c1_future", {
    **W1("jplatform", crowd=[[0, 1.0], [C("Japan will have"), 1.0], [C("the working-age people"), 0.52], [C("Think of a rush-hour"), 1.0], [C("Now take away"), 1.0], [C("every other person"), 0.5]],
         board=[[0, "1995 · THE PEAK"], [C("Japan will have"), "2070 · PROJECTION"], [C("Think of a rush-hour"), "RUSH HOUR"], [C("every other person"), "HALF"]], trainAt=C("Think of a rush-hour")),
    "cam": cam((0, 960, 560, 0.95), (C("Japan will have"), 960, 600, 1.08, 1.4), (C("Think of a rush-hour"), 900, 560, 0.9, 1.2), (C("Now take away"), 1000, 620, 1.1, 1.4)), "drift": 2,
    "items": [words("≈ HALF THE PEAK", 960, 300, C("the working-age people"), size=66, color=PURPLE, until=C("Think of a rush-hour")),
              words("...NOW TAKE AWAY EVERY OTHER PERSON", 960, 300, C("Now take away"), size=46),
              tag((0, "PROJECTION · IPSS (2070, MEDIUM VARIANT)"), (C("Think of a rush-hour"), "ILLUSTRATION"))]},
    sources=["ipss23"])
stage("s06_jobs", "c1_jobs", {
    **W1("jtown", signAt=0.0, shutters=0.6),
    "cam": cam((0, 400, 600, 1.2), (C("Month after month"), 700, 520, 0.95, 1.4), (C("the convenience store"), 1300, 540, 1.05, 1.2), (C("And they're all losing"), 900, 520, 0.85, 1.4)), "drift": 3,
    "items": [words("1.19 JOBS PER JOB SEEKER", 900, 150, C("more open jobs"), size=56, until=C("Hiro is competing")),
              sign("HELP WANTED · STORE", 1300, 470, C("the convenience store"), color="#FFFDF5", size=24),
              sign("HELP WANTED · CARE HOME", 1650, 420, C("the nursing home"), color="#FFFDF5", size=24),
              sign("HELP WANTED · DELIVERY", 1900, 560, C("the delivery company"), color="#FFFDF5", size=24),
              words("EVERYONE IS HIRING", 900, 150, C("And they're all losing"), size=56, color=RED),
              HIRO(260, 0.0, face="worry", pose="shrug", faces=[[0, "worry"], [C("And they're all losing"), "deadpan"]]),
              tag((0, "FACT · MHLW (SEPT 2026, SEASONALLY ADJUSTED)"))]},
    sources=["mhlw_jobs"])

# ====================================================================== CHAPTER 2: a country running out of hands
bumper("s07_b2", "c2_card", "CHAPTER TWO", "A COUNTRY RUNNING OUT OF HANDS", "Trucks, caregivers, and a granddaughter in Tokyo.", RED)
stage("s08_trucks", "c2_trucks", {
    **W1("jroad", trucks=[[0, 6], [C("But fewer drivers"), 6], [C("move fewer boxes"), 3], [C("short of trucks"), 2]], capAt=C("Japan capped"),
         left=[[0, 0.0], [C("move fewer boxes"), 0.0], [C("short of trucks"), 0.34]]),
    "cam": cam((0, 500, 560, 1.0), (C("Japan capped"), 1500, 420, 1.05, 1.4), (C("But fewer drivers"), 600, 600, 0.95, 1.4), (C("short of trucks"), 1500, 620, 1.0, 1.4)), "drift": 3,
    "items": [words("GOOD FOR THE DRIVERS", 1500, 150, C("Good for the drivers"), size=48, color=GREEN, until=C("But fewer drivers")),
              words("FEWER DRIVERS × FEWER HOURS", 700, 150, C("But fewer drivers"), size=48, until=C("The government warns")),
              words("≈ 1/3 OF CARGO WITHOUT A TRUCK", 1500, 150, C("short of trucks"), size=54, color=RED),
              sign("FY2030 · IF NOTHING CHANGES", 1500, 240, C("short of trucks", 0.6), color="#FFE0B2", size=24),
              tag((0, "FACT · OVERTIME CAP SINCE APRIL 2024"), (C("The government warns"), "ESTIMATE · MLIT WHITE PAPER 2024"))]},
    sources=["mlit_wp24"])
stage("s09_care", "c2_care", {
    **W1("jcare", sensors=0, lift=0, need="+≈570,000 BY 2040", needAt=C("The health ministry")),
    "cam": cam((0, 2000, 560, 1.15), (C("It needs more caregivers"), 1300, 520, 0.95, 1.6), (C("The health ministry"), 1700, 480, 1.0, 1.4)), "drift": 3,
    "items": [MOM(2050, 0.0, face="happy", pose="sit", label="HIRO'S MOTHER (FICTIONAL)", labelUntil=C("It needs more caregivers")),
              CARER([[0, 600], [C("It needs more caregivers"), 1500], [C("because more people"), 400], [C("fewer young people"), 1600]], 0.3, face="happy", pose="stand",
                    faces=[[0, "happy"], [C("fewer young people"), "panic"]]),
              words("MORE OLD, FEWER YOUNG", 1300, 160, C("because more people"), size=54, until=C("The health ministry")),
              words("HUNDREDS OF THOUSANDS MORE", 1700, 300, C("hundreds of thousands"), size=48, color=RED),
              tag((0, "STORY"), (C("The health ministry"), "ESTIMATE · MHLW (JUL 2024)"))]},
    sources=["mhlw_care"])
stage("s10_aoi", "c2_aoi", {
    **W1("jplatform", crowd=0.25, board=[[0, "LIMITED EXPRESS · TOKYO"]], trainAt=-2.0),
    "cam": cam((0, 900, 600, 1.15), (C("She writes software"), 1100, 560, 1.0, 1.4), (C("He still needs"), 700, 620, 1.25, 1.4)), "drift": 2,
    "items": [AOI([[0, 900], [C("She writes software"), 900], [C("Hiro is proud"), 1300]], 0.0, face="happy", pose="stand", hold="bag", label="AOI · SOFTWARE DEVELOPER (FICTIONAL)", labelUntil=C("She writes software"),
                  until=C("He still needs")),
              HIRO(560, 0.2, face="happy", pose="wave", faces=[[0, "happy"], [C("He still needs"), "worry"]]),
              bub("CALL YOUR GRANDPA!", 560, 320, C("Hiro is proud"), until=C("He still needs"), tail=[560, 540], size=28),
              words("...AND THE LATHE?", 700, 230, C("He still needs"), size=56),
              tag((0, "STORY · FICTIONAL CAST"))]})
stage("s11_turn", "c2_turn", {
    "zones": [Z("jtown", x0=-1600, x1=3000, signAt=0.0, shutters=0.85), Z("jfactory", x0=3000, x1=7200, ox=OX, share=0.6, plaque="ROBOT MAKER (GENERIC)")],
    "worldW": 2400,
    "cam": cam((0, 900, 520, 0.9), (C("Old, shrinking, stuck"), 700, 560, 1.1, 1.2), (C("But here's the twist"), OX + 1000, 520, 0.9, WHIP), (C("one of Japan's greatest"), OX + 1300, 500, 1.0, 1.4)), "drift": 3,
    "items": [words("OLD. SHRINKING. STUCK?", 800, 160, C("Old, shrinking, stuck"), size=60, until=C("But here's the twist")),
              words("THE TWIST", OX + 1000, 160, C("But here's the twist"), size=72, color=ORANGE, until=C("one of Japan's greatest")),
              words("SHORTAGE → AN INDUSTRY", OX + 1100, 160, C("one of Japan's greatest"), size=58),
              tag((0, "ANALYSIS"))]},
    sfx=[{"kind": "whoosh", "cue": "But here's the twist", "gain": 0.3}])

# ====================================================================== CHAPTER 3: the robot superpower
bumper("s12_b3", "c3_card", "CHAPTER THREE", "THE ROBOT SUPERPOWER", "Born from a labor shortage.", ORANGE)
stage("s13_birth", "c3_birth", {
    **W1("jhist", armAt=C("began building"), helpAt=C("couldn't hire"), year="1969"), "tone": "history",
    "cam": cam((0, 1750, 420, 1.3), (C("Japan's economy was booming"), 960, 540, 0.9, 1.6), (C("began building"), 1200, 500, 1.15, 1.4), (C("Carmakers hungry"), 960, 560, 0.9, 1.4)), "drift": 3,
    "items": [words("1969", 1750, 150, 0.2, size=84, until=C("Japan's economy was booming")),
              words("JAPAN'S FIRST HOME-BUILT INDUSTRIAL ROBOT", 1100, 150, C("began building"), size=46, until=C("Carmakers hungry")),
              sign("UNDER AN AMERICAN LICENSE", 1100, 230, C("under an American license"), color="#F3E9D4", size=24, until=C("Carmakers hungry")),
              words("FIRST BUYERS: CARMAKERS SHORT OF WORKERS", 960, 150, C("Carmakers hungry"), size=44),
              tag((0, "FACT · KAWASAKI ROBOT HISTORY"))]},
    sources=["kawasaki_hist"])
stage("s14_world", "c3_world", {
    **W1("jfactory", share=0.6, plaque="ROBOT MAKER (GENERIC)"),
    "cam": cam((0, 900, 520, 0.9), (C("FANUC, Yaskawa"), 600, 560, 1.1, 1.4), (C("These are industrial robots"), 900, 600, 1.15, 1.4), (C("They just work"), 1200, 540, 0.95, 1.2)), "drift": 3,
    "items": [words("THE WORLD'S LEADING ROBOT MAKER", 960, 150, C("calls Japan"), size=52, until=C("FANUC, Yaskawa")),
              sign("FANUC · YASKAWA · KAWASAKI · AND OTHERS", 600, 240, C("FANUC, Yaskawa"), color="#FFFFFF", size=28, until=C("These are industrial robots")),
              words("INDUSTRIAL ROBOTS = WORKHORSES", 900, 150, C("These are industrial robots"), size=52, until=C("They just work")),
              words("NO WALKING. NO CHATTING. JUST WORK.", 1200, 150, C("They just work"), size=46, color=ORANGE),
              it("kobo", x=[[0, -200], [C("They don't walk"), 400]], y=1000, at=C("They don't walk"), scale=0.8, face="happy", wave=[C("They just work")]),
              tag((0, "FACT · IFR (JUL 2025)"))]},
    sources=["ifr_japan25", "ifr_wr25"])
stage("s15_fanuc", "c3_fanuc", {
    **W1("jfactory", share=[[0, 0.5], [C("Look at where the robots go"), 0.5], [C("of FANUC's sales"), 0.9]], plaque="ROBOT MAKER (GENERIC)"),
    "cam": cam((0, 1000, 520, 0.9), (C("Look at where the robots go"), 2100, 520, 1.0, 1.4), (C("of FANUC's sales"), 2200, 500, 0.9, 1.4),
               (C("Its robot sales in China"), 2100, 540, 1.05, 1.2), (C("Japan builds the robots"), 1500, 520, 0.85, 1.4)), "drift": 2,
    "items": [words("WHERE DO THE ROBOTS GO?", 2100, 150, C("Look at where the robots go"), size=52, until=C("of FANUC's sales")),
              words("≈ 9 IN 10 YEN FROM ABROAD", 2200, 150, C("of FANUC's sales"), size=58, color=BLUE, until=C("Its robot sales in China")),
              sign("CHINA ↑", 2050, 250, C("Its robot sales in China"), color="#C8E6C9", size=34),
              sign("JAPAN ↓", 2620, 330, C("Its robot sales at home"), color="#FFCDD2", size=34),
              words("JAPAN BUILDS. THE WORLD BUYS.", 1500, 150, C("Japan builds the robots"), size=56),
              tag((0, "FACT · FANUC (FY TO MAR 2026)"), (C("of FANUC's sales"), "OUR CALC · FANUC SALES BY REGION"), (C("Its robot sales in China"), "FACT · FANUC ROBOT DIVISION"))]},
    sources=["fanuc_fy25"])
stage("s16_density", "c3_density", {
    **W1("jdensity", rows=[{"label": "S. KOREA", "n": 12.2, "at": C("South Korea has"), "color": BLUE}, {"label": "JAPAN", "n": 4.5, "at": C("Count robots"), "color": ORANGE}]),
    "cam": cam((0, 960, 540, 1.0), (C("South Korea has"), 960, 520, 0.98, 1.4), (C("The robot superpower"), 960, 540, 1.02, 1.4)), "drift": 1,
    "items": [words("≈ 3× AS MANY ROBOTS PER WORKER", 960, 120, C("as many as Japan"), size=48, color=BLUE, until=C("The robot superpower")),
              words("THE ROBOT MAKER ISN'T THE MOST ROBOTIC", 960, 120, C("The robot superpower"), size=44, color=ORANGE),
              tag((0, "FACT · IFR WORLD ROBOTICS 2025 (2024 DATA)"), (C("as many as Japan"), "OUR CALC · 1,220 vs 446 PER 10,000"))]},
    sources=["ifr_wr25"])
board("p17_draw", "c3_draw", "Why a shortage sells robots (mechanism)", "Let me draw it", [
    {"d": rect(620, 300, 260, 110), "color": "risk", "width": 6, "kind": "box", "start": C("Fewer workers"), "label": lbl("FEWER WORKERS", 750, 368, 26, "risk")},
    {"d": arrow((880, 355), (960, 355), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("so wages rise")},
    {"d": rect(970, 300, 240, 110), "color": "accent", "width": 6, "kind": "box", "start": C("so wages rise"), "label": lbl("WAGES UP", 1090, 368, 28, "accent")},
    {"d": arrow((1210, 355), (1290, 355), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("Higher wages")},
    {"d": rect(1300, 300, 300, 110), "color": "accent2", "width": 6, "kind": "box", "start": C("Higher wages"), "label": lbl("ROBOT LOOKS CHEAP", 1450, 368, 24, "accent2")},
    {"d": arrow((1450, 410), (1240, 560), 0.15), "color": "ink", "width": 5, "kind": "arrow", "start": C("So companies buy robots")},
    {"d": rect(860, 560, 420, 130), "color": "accent3", "width": 8, "kind": "box", "start": C("every remaining worker"), "label": lbl("MORE OUTPUT PER WORKER", 1070, 635, 30, "accent3")},
    {"d": rect(760, 750, 620, 90), "color": "ink", "width": 5, "kind": "box", "start": C("A country can shrink"), "label": lbl("SHRINK + RICHER PER PERSON", 1070, 808, 30, "ink")},
    {"d": dot(1100, 905), "color": "muted", "width": 1, "start": C("Let me draw it"), "label": lbl("MECHANISM · ILLUSTRATIVE · NO FIGURES", 1100, 905, 16, "muted")},
], [{"kind": "point", "at": C("Higher wages", 0.4), "dur": 1.4, "target": [1450, 355]}, {"kind": "point", "at": C("That last box", 0.2), "dur": 1.6, "target": [1070, 625]},
    {"kind": "react", "at": C("Output per worker")}], enter_left=False)

# ====================================================================== CHAPTER 4: robots on the front line
bumper("s18_b4", "c4_card", "CHAPTER FOUR", "ROBOTS ON THE FRONT LINE", "Arms at work. Androids in the lab.", GREEN)
stage("s19_konbini", "c4_konbini", {
    **W1("jkonbini", cut=[[0, 0.0], [C("you may find"), 0.0], [C("sliding cold bottles"), 1.0]], stock=[[0, 0.3], [C("sliding cold bottles"), 0.3], [C("When it fumbles"), 0.75], [C("finishes the job"), 0.75], [C("That's a deployment"), 0.95]],
         fumbleAt=C("When it fumbles"), vrAt=C("puts on a headset")),
    "cam": cam((0, 700, 560, 0.9), (C("you may find"), 1200, 480, 1.1, 1.4), (C("Its maker"), 1100, 500, 0.95, 1.2), (C("When it fumbles"), 1300, 520, 1.1, 1.0),
               (C("puts on a headset"), 1500, 420, 0.95, 1.2), (C("That's a deployment"), 1100, 540, 0.85, 1.4)), "drift": 2,
    "items": [words("≈ 1,000 DRINKS A DAY", 1200, 130, C("restock about"), size=58, color=ORANGE, until=C("When it fumbles")),
              words("OOPS.", 1500, 200, C("When it fumbles"), size=72, color=RED, until=C("puts on a headset")),
              words("NOT A DEMO: A DEPLOYMENT", 1100, 130, C("That's a deployment"), size=56, color=GREEN),
              tag((0, "FACT · DEPLOYED (FAMILYMART, 7-ELEVEN PILOTS)"), (C("restock about"), "COMPANY CLAIM · TELEXISTENCE"))]},
    sources=["tx_ghost"], sfx=[{"kind": "hit", "cue": "When it fumbles", "gain": 0.25}])
stage("s20_humanoid", "c4_humanoid", {
    **W1("jdemo", caseAt=C("Japan's most famous"), workAt=C("the robots doing the work"), protoAt=C("developing a humanoid"), protoText="PROTOTYPE · TARGET 2029"),
    "cam": cam((0, 960, 520, 0.9), (C("Japan's most famous"), 300, 520, 1.15, 1.4), (C("developing a humanoid"), 1640, 520, 1.15, WHIP), (C("That's a plan"), 1640, 500, 1.05, 1.0),
               (C("the robots doing the work"), 960, 520, 0.85, 1.4)), "drift": 2,
    "items": [words("THE HEADLINE ROBOTS", 960, 130, 0.3, size=56, until=C("Japan's most famous")),
              words("CHARMED CROWDS. NEVER GOT A JOB.", 300, 130, C("charmed crowds"), size=40, until=C("developing a humanoid")),
              words("TARGET: 2029", 1640, 130, C("putting it in stores"), size=72, color=PURPLE, until=C("the robots doing the work")),
              words("ARMS, NOT ANDROIDS", 960, 130, C("the robots doing the work"), size=66, color=ORANGE),
              tag((0, "FACT · RETIRED 2022 (JAPAN TIMES)"), (C("developing a humanoid"), "PLAN · SEVEN-ELEVEN JAPAN / TELEXISTENCE"), (C("the robots doing the work"), "ANALYSIS"))]},
    sources=["asimo_jt", "tx_astra"])
stage("s21_care", "c4_care", {
    **W1("jcare", sensors=[[0, 0.0], [C("Sensors under"), 1.0]], lift=[[0, 0.0], [C("Machines that help"), 0.0], [C("out of bed"), 1.0]]),
    "cam": cam((0, 500, 560, 1.15), (C("Sensors under"), 560, 480, 1.1, 1.2), (C("Machines that help"), 1450, 520, 1.1, 1.4), (C("Economists who studied"), 1200, 520, 0.9, 1.4),
               (C("human touch"), 2100, 580, 1.2, 1.4)), "drift": 3,
    "items": [MOM(2050, 0.0, face="happy", pose="sit"),
              CARER([[0, 1700], [C("Homes that adopted"), 1700], [C("human touch"), 2250]], 0.2, face="happy", pose="stand", hold="coffee", faces=[[0, "happy"], [C("human touch"), "grin"]]),
              words("QUIET HELPERS", 800, 150, C("Sensors under"), size=56, until=C("Economists who studied")),
              words("MORE STAFF, NOT FEWER", 1200, 150, C("more staff, not fewer"), size=58, color=GREEN, until=C("human touch")),
              words("MORE TIME FOR HUMAN TOUCH", 2000, 150, C("human touch"), size=48),
              bub("TEA?", 2250, 330, C("human touch", 0.3), tail=[2250, 520], size=34),
              tag((0, "FACT · DEPLOYED IN JAPANESE CARE HOMES"), (C("Economists who studied"), "FINDING · LEE, IIZUKA & EGGLESTON (NBER)"))]},
    sources=["nh_robots"])
stage("s22_hiro", "c4_hiro", {
    **W1("jshop", arm=[[0, 0.0], [C("A small collaborative"), 0.0], [C("built to work safely"), 1.0]], codeAt=C("Aoi writes the program"),
         cycle=[[0, 0.0], [C("Kobo loads the lathe"), 0.0], [C("again and again"), 1.0]], run=[[0, 0.0], [C("again and again"), 1.0]],
         parts=[[0, ""], [C("while Hiro does"), "ON TIME"]], stoolHi=[0.0, C("Aoi comes home")]),
    "cam": cam((0, 760, 620, 1.2), (C("Aoi comes home"), 600, 560, 1.0, 1.4), (C("A small collaborative"), 1500, 520, 1.05, 1.4), (C("Aoi writes the program"), 560, 600, 1.2, 1.2),
               (C("Kobo loads the lathe"), 1300, 520, 0.95, 1.4), (C("checking every piece"), 900, 560, 1.05, 1.4)), "drift": 3,
    "items": [HIRO(1000, 0.0, face="worry", pose="stand", faces=[[0, "worry"], [C("Not a humanoid"), "shock"], [C("They name it Kobo"), "happy"], [C("checking every piece"), "grin"]],
                   poses=[[0, "stand"], [C("checking every piece"), "clipboard"]], takes=[C("Not a humanoid")]),
              AOI([[0, -300], [C("Aoi comes home", 1.2), 420]], C("Aoi comes home"), face="grin", pose="stand", poses=[[0, "stand"], [C("Aoi writes the program"), "type"], [C("Kobo loads the lathe"), "point"]]),
              bub("MEET YOUR NEW APPRENTICE.", 420, 280, C("with a plan"), until=C("A small collaborative"), tail=[420, 520], size=26),
              bub("A ROBOT?!", 1000, 300, C("Not a humanoid"), until=C("They name it Kobo"), tail=[1000, 520], size=34),
              words("KOBO (工房) = WORKSHOP", 1500, 150, C("They name it Kobo"), size=52, until=C("Aoi writes the program")),
              words("SAFE BESIDE PEOPLE", 1500, 150, C("built to work safely"), size=48, until=C("They name it Kobo")),
              words("ROBOT LOADS · HIRO CHECKS", 1100, 150, C("while Hiro does"), size=50, color=GREEN),
              tag((0, "STORY · COBOTS ARE A REAL CATEGORY (NO BRAND SHOWN)"))]})
board("p23_draw", "c4_draw", "Who gets paid for Kobo? (our framework)", "Let me draw it", [
    {"d": rect(620, 300, 300, 130), "color": "accent", "width": 7, "kind": "box", "start": C("First, the arm"), "label": lbl("THE ARM", 770, 375, 32, "accent")},
    {"d": dot(770, 455), "color": "accent", "width": 1, "start": C("Japan is superb"), "label": lbl("JAPAN: SUPERB", 770, 462, 22, "accent")},
    {"d": rect(980, 300, 300, 130), "color": "risk", "width": 7, "kind": "box", "start": C("Second, the brain"), "label": lbl("THE BRAIN (AI)", 1130, 375, 30, "risk")},
    {"d": dot(1130, 455), "color": "risk", "width": 1, "start": C("Much of that is written"), "label": lbl("MUCH OF IT: US + CHINA", 1130, 462, 20, "risk")},
    {"d": rect(1340, 300, 300, 130), "color": "accent3", "width": 7, "kind": "box", "start": C("And finally, the user"), "label": lbl("THE USER", 1490, 375, 32, "accent3")},
    {"d": dot(1490, 455), "color": "accent3", "width": 1, "start": C("the small business"), "label": lbl("SMALL FIRMS", 1490, 462, 22, "accent3")},
    {"d": rect(1360, 640, 280, 110), "color": "ink", "width": 6, "kind": "box", "start": C("more and more of the money"), "label": lbl("$ VALUE", 1500, 708, 32, "ink")},
    {"d": arrow((1420, 640), (1180, 480), 0.1), "color": "accent3", "width": 6, "kind": "arrow", "start": C("flows to the brain")},
    {"d": arrow((1520, 640), (1500, 480), -0.1), "color": "accent3", "width": 6, "kind": "arrow", "start": C("and to the user")},
    {"d": rect(560, 780, 420, 80), "color": "accent", "width": 5, "kind": "box", "start": C("Japan owns the arm"), "label": lbl("JAPAN OWNS THE ARM", 770, 832, 28, "accent")},
    {"d": dot(1300, 905), "color": "muted", "width": 1, "start": C("Let me draw it"), "label": lbl("FRAMEWORK · OUR ANALYSIS · NO FIGURES", 1300, 905, 16, "muted")},
], [{"kind": "point", "at": C("Second, the brain", 0.4), "dur": 1.4, "target": [1130, 365]}, {"kind": "point", "at": C("flows to the brain", 0.2), "dur": 1.6, "target": [1500, 695]},
    {"kind": "react", "at": C("Japan owns the arm")}], enter_left=True)

# ====================================================================== CHAPTER 5: the catch
bumper("s24_b5", "c5_card", "CHAPTER FIVE", "THE CATCH", "A weak yen, slow software, a mountain of debt.", PURPLE)
stage("s25_yen", "c5_yen", {
    **W1("jyen", shrink=[[0, 0.0], [C("it has lost"), 0.0], [C("of its value"), 1.0]], outAt=C("cheap for foreign buyers"), inAt=C("every imported chip")),
    "cam": cam((0, 960, 520, 0.95), (C("it has lost"), 760, 480, 1.08, 1.4), (C("cheap for foreign buyers"), 1300, 600, 0.95, 1.4), (C("every imported chip"), 900, 620, 0.95, 1.4)), "drift": 2,
    "items": [words("YEN ≈ −29% VS THE DOLLAR (2020 → 2025)", 960, 120, C("of its value"), size=46, color=RED, until=C("cheap for foreign buyers")),
              words("GOOD FOR FANUC", 1300, 120, C("which helps FANUC"), size=56, color=GREEN, until=C("every imported chip")),
              words("PRICIER FOR HIRO", 900, 120, C("more expensive for Hiro"), size=56, color=RED),
              HIRO(1750, C("every imported chip"), face="worry", pose="shrug", scale=1.0, takes=[C("more expensive for Hiro")]),
              tag((0, "OUR CALC · FED G.5A ANNUAL AVERAGES"))]},
    sources=["fed_g5a"])
stage("s26_software", "c5_software", {
    **W1("jscale", tilt=[[0, 0.0], [C("Second, software"), 0.0], [C("hasn't kept up"), 0.35]], weights=[{"label": "WEAK YEN", "at": 0.2, "color": "#8D6E63"}, {"label": "SLOW SOFTWARE", "at": C("Second, software"), "color": BLUE}]),
    "cam": cam((0, 960, 540, 0.95), (C("Measured by output"), 1300, 520, 1.05, 1.4), (C("And remember FANUC's"), 960, 540, 0.92, 1.4)), "drift": 1,
    "items": [words("OUTPUT PER HOUR: 28TH OF 38", 960, 120, C("the bottom third"), size=52, color=RED, until=C("And remember FANUC's")),
              sign("FANUC ROBOT SALES IN JAPAN: DOWN", 960, 210, C("They fell"), color="#FFCDD2", size=28),
              words("MADE HERE. NOT SPREADING HERE.", 960, 120, C("The robots are being made here"), size=48),
              tag((0, "FACT · JAPAN PRODUCTIVITY CENTER (OECD DATA, 2024)"), (C("And remember FANUC's"), "FACT · FANUC"))]},
    sources=["jpc_prod25", "fanuc_fy25"])
stage("s27_debt", "c5_debt", {
    **W1("jscale", tilt=[[0, 0.35], [C("owes about"), 0.35], [C("the highest of any"), 0.95], [C("the net picture"), 0.65], [C("But as more people retire"), 0.8]],
         weights=[{"label": "WEAK YEN", "at": 0.0, "color": "#8D6E63"}, {"label": "SLOW SOFTWARE", "at": 0.0, "color": BLUE}, {"label": "DEBT", "at": C("owes about"), "color": RED, "big": True}]),
    "cam": cam((0, 960, 540, 0.95), (C("owes about"), 1350, 560, 1.05, 1.2), (C("The government also owns"), 960, 540, 0.95, 1.4), (C("But as more people retire"), 1250, 560, 1.02, 1.4)), "drift": 1,
    "items": [words("GROSS DEBT ≈ 2× THE ECONOMY", 960, 120, C("owes about"), size=54, color=RED, until=C("The government also owns")),
              sign("NET OF ITS ASSETS: LOWER", 960, 120, C("the net picture"), color="#C8E6C9", size=32, until=C("But as more people retire")),
              words("PENSIONS + HEALTH CARE ↑", 960, 120, C("But as more people retire"), size=52),
              tag((0, "FACT · IMF (F&D, SEPT 2026)"))]},
    sources=["imf_fd"])
stage("s28_slow", "c5_slow", {
    **W1("jtown", signAt=0.0, shutters=0.85),
    "cam": cam((0, 900, 520, 0.85), (C("Last year"), 1200, 520, 1.0, 1.4), (C("And yet"), 400, 600, 1.3, 1.2)), "drift": 3,
    "items": [bub("JAPAN: COLLAPSE?", 700, 260, C("so many videos"), until=C("Last year"), size=34),
              bub("THE LOST DECADES!", 1300, 330, C("a slow-motion collapse"), until=C("Last year"), size=30),
              words("2025 GROWTH: +1.2%", 1200, 150, C("its whole economy grew"), size=60, until=C("And yet")),
              it("kobo", x=[[C("And yet"), -200], [C("And yet", 1.4), 300]], y=1000, at=C("And yet"), scale=0.9, face="think"),
              words("...THE WRONG THING?", 400, 200, C("measuring the wrong thing"), size=58, color=ORANGE),
              tag((0, "ANALYSIS"), (C("its whole economy grew"), "FACT · CABINET OFFICE (REAL GDP)"))]},
    sources=["cao_gdp"])

# ====================================================================== CHAPTER 6: will AI make Japan rich again?
bumper("s29_b6", "c6_card", "CHAPTER SIX", "WILL AI MAKE JAPAN RICH AGAIN?", "Count the hands, not the heads.", BLUE)
stage("s30_twist", "c6_twist", {
    **W1("jplatform", crowd=0.55, board=[[0, "PER CITIZEN?"], [C("but per working-age adult"), "PER WORKER"], [C("Their answer"), "JAPAN ≥ USA"]], trainAt=-5),
    "cam": cam((0, 960, 540, 0.95), (C("but per working-age adult"), 960, 360, 1.25, 1.4), (C("Their answer"), 960, 520, 0.9, 1.4)), "drift": 2,
    "items": [words("A DIFFERENT QUESTION", 960, 140, C("asked a different question"), size=56, until=C("Their answer")),
              words("SLIGHTLY FASTER THAN AMERICA", 960, 140, C("slightly faster than America"), size=56, color=GREEN),
              sign("PER WORKING-AGE ADULT · 1998-2019", 960, 230, C("slightly faster than America", 0.4), color="#FFFFFF", size=26),
              tag((0, "FINDING · FERNÁNDEZ-VILLAVERDE, VENTURA & YAO (NBER)"))]},
    sources=["fv_wealth"])
board("p31_draw", "c6_draw", "Per citizen vs per worker (illustrative shape of the NBER finding)", "Let me draw it", [
    {"d": "M 640 840 L 1580 840 M 640 840 L 640 320", "color": "ink", "width": 5, "start": C("Let me draw it")},
    {"d": "M 660 640 Q 900 630 1100 625 T 1540 615", "color": "muted", "width": 7, "start": C("Japan's total economy looks flat"), "label": lbl("JAPAN: TOTAL ECONOMY", 1280, 590, 22, "muted")},
    {"d": "M 660 800 Q 1000 680 1200 560 T 1540 400", "color": "accent2", "width": 6, "start": C("right alongside America's"), "label": lbl("USA", 1560, 380, 24, "accent2")},
    {"d": "M 660 800 Q 1000 670 1200 545 T 1540 380", "color": "accent3", "width": 9, "start": C("the line climbs"), "label": lbl("JAPAN: PER WORKER", 1380, 350, 26, "accent3")},
    {"d": rect(700, 300, 400, 90), "color": "risk", "width": 5, "kind": "box", "start": C("It was fewer of them"), "label": lbl("NOT LAZY. FEWER.", 900, 358, 30, "risk")},
    {"d": rect(1130, 700, 420, 90), "color": "accent", "width": 6, "kind": "box", "start": C("exactly the problem robots"), "label": lbl("ROBOTS = MORE PER HAND", 1340, 758, 28, "accent")},
    {"d": dot(1100, 905), "color": "muted", "width": 1, "start": C("Let me draw it"), "label": lbl("ILLUSTRATIVE SHAPE · NBER w31914: 1998-2019 GDP PER WORKING-AGE ADULT JAPAN +31.9%, US +29.5%", 1100, 905, 15, "muted")},
], [{"kind": "point", "at": C("the line climbs", 0.4), "dur": 1.6, "target": [1380, 420]}, {"kind": "react", "at": C("It was fewer of them")}], enter_left=False, sources=["fv_wealth"])
stage("s32_verdict", "c6_verdict", {
    **W1("jscale", tilt=[[0, 0.6], [C("would be built on output"), 0.6], [C("keep getting richer"), -0.2], [C("But only if"), 0.1]],
         weights=[{"label": "WEAK YEN", "at": 0.0, "color": "#8D6E63"}, {"label": "SLOW SOFTWARE", "at": 0.0, "color": BLUE}, {"label": "DEBT", "at": 0.0, "color": RED, "big": True}],
         leftText="OUTPUT PER HAND"),
    "cam": cam((0, 960, 520, 0.92), (C("That boom was built"), 960, 540, 1.0, 1.2), (C("keep getting richer"), 600, 560, 1.05, 1.4), (C("But only if"), 960, 520, 0.9, 1.4)), "drift": 1,
    "items": [words("NOT A NEW BUBBLE", 960, 120, C("Not the way it was"), size=60, until=C("would be built on output")),
              sign("WATCH: WHEN TOKYO'S LAND WAS WORTH MORE THAN ENTIRE COUNTRIES", 960, 210, C("in the bubble"), color="#FFFFFF", size=24, until=C("would be built on output")),
              words("OUTPUT PER PAIR OF HANDS", 960, 120, C("would be built on output"), size=56, color=GREEN, until=C("But only if")),
              words("IF: SMALL FIRMS ADOPT", 960, 110, C("small firms like Hiro's"), size=46, until=C("Japan writes more")),
              words("IF: JAPAN WRITES THE BRAINS", 960, 110, C("Japan writes more"), size=46, until=C("the debt doesn't")),
              words("IF: DEBT DOESN'T CROWD IT OUT", 960, 110, C("the debt doesn't"), size=46),
              tag((0, "VERDICT · OUR ANALYSIS"))]},
    sources=["fv_wealth", "imf_fd", "fanuc_fy25"])
stage("s33_hiro", "c6_hiro", {
    "zones": [Z("jtown", x0=-1600, x1=3000, signAt=0.0, shutters=0.6, kobo=1.0, truckX=[[0, -600], [C("But now the parts"), -600], [C("ship on time"), 900]]),
              Z("jshop", x0=3000, x1=7200, ox=OX, arm=1.0, cycle=1.0, run=1.0, parts=[[0, "ON TIME"]])],
    "worldW": 2400,
    "cam": cam((0, 480, 580, 1.6), (C("Hiro still wants"), 400, 600, 1.3, 1.2), (C("But now the parts"), 600, 600, 0.95, 1.4), (C("and Aoi comes home"), OX + 900, 560, 1.0, WHIP),
               (C("Japan's biggest problem"), OX + 1100, 540, 0.9, 1.4), (C("What's changing"), OX + 1300, 560, 1.05, 1.4)), "drift": 2,
    "items": [HIRO(260, 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("Hiro still wants"), "smug"]]),
              bub("STILL HIRING, BY THE WAY.", 300, 300, C("Hiro still wants"), until=C("But now the parts"), tail=[260, 520], size=26),
              AOI(OX + 500, C("and Aoi comes home"), face="happy", pose="point"),
              HIRO(OX + 900, C("and Aoi comes home"), face="grin", pose="clipboard"),
              words("A WORKSHOP WITH TOO FEW HANDS...", OX + 1100, 150, C("Japan's biggest problem"), size=48, until=C("What's changing")),
              words("...CAN DO MORE", OX + 1300, 150, C("What's changing"), size=64, color=GREEN),
              tag((0, "STORY"))]})
add("s34_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s35_button", "button", {
    **W1("jshop", arm=1.0, cycle=1.0, run=1.0, parts=[[0, "ON TIME"]]),
    "cam": cam((0, 900, 600, 1.15), (3.0, 1100, 600, 1.3, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [HIRO(900, 0.0, face="grin", pose="stand", scale=1.15),
              bub("DOES KOBO WANT TEA?", 900, 280, 0.5, until=2.8, tail=[900, 520], size=30),
              AOI(560, 0.3, face="happy", pose="point", scale=1.1),
              bub("IT ONLY DRINKS ELECTRICITY.", 640, 420, 2.9, tail=[560, 560], size=28),
              it("kobo", x=[[0, 2300], [2.0, 1300]], y=1010, at=1.4, scale=0.7, face="happy", wave=[3.4, 4.6])]},
    sfx=[{"kind": "hit", "at": 3.0, "gain": 0.3}])

TIGHT = {"jdensity", "jscale", "jyen", "jkonbini", "jdemo"}
for _sc in cartoon_kit.scenes:
    _z = _sc["params"].get("zones") or []
    if _sc["type"] == "engine_cartoon" and len(_z) == 1 and _z[0]["set"] in TIGHT:
        for _k in _sc["params"].get("cam", []):
            _k["zoom"] = max(0.85, min(_k["zoom"], 1.15))
            _k["y"] = max(480, min(600, _k["y"]))
        _sc["params"]["drift"] = min(_sc["params"].get("drift", 3), 2)

TAGCOL = {"FACT": "green", "ESTIMATE": "gold", "PROJECTION": "gold", "OUR": "gold", "COMPANY": "gold", "PLAN": "gold", "FINDING": "green"}
for _sc in cartoon_kit.scenes:
    if _sc["type"] != "engine_cartoon":
        continue
    P = _sc["params"]
    for _k in P.get("cam", []):
        _k["zoom"] = min(_k["zoom"], 1.25)
        _k["y"] = max(470, min(570, _k["y"]))
    keep, calls = [], P.setdefault("callouts", [])
    for _it in P.get("items", []):
        if _it.get("kind") == "jtag":
            tl = _it["tags"]
            for j, (t0, txt) in enumerate(tl):
                c = {"text": txt, "x": 40 + (len(txt) * 20 * 0.6 + 60) / 2, "y": 50, "at": t0, "size": 20, "screen": True, "color": TAGCOL.get(txt.split(" ")[0], "white")}
                if j + 1 < len(tl):
                    c["until"] = tl[j + 1][0]
                calls.append(c)
            continue
        if _it.get("kind") in ("toonwords", "sign", "bubble") and isinstance(_it.get("y"), (int, float)) and _it["y"] < 200:
            _it["y"] = 200
        keep.append(_it)
    P["items"] = keep

write(OUT, "# GENERATED by tools/gen_japanai_storyboard.py; edit the generator, not this file.\n"
           "# Episode 66 storyboard (Will AI Make Japan Rich Again?): bespoke worlds in CartoonStage/japan.tsx.\n")

# ---- cue check: every {cue: ...} must occur in its segment's rendered narration
from hiddeneco.config import ProjectPaths  # noqa: E402
from hiddeneco.research.dossier import build_dossier  # noqa: E402
from hiddeneco.script import load_script, render_text  # noqa: E402
import re  # noqa: E402

paths = ProjectPaths(SLUG, ROOT)
dos = build_dossier(paths)
scr = load_script(OUT.parent)
nar = {s.id: re.sub(r"[^\w% ]", "", render_text(s.narration, dos).lower()) for s in scr.segments}
bad = []


def walk(o, seg):
    if isinstance(o, dict):
        if "cue" in o and isinstance(o["cue"], str):
            c = re.sub(r"[^\w% ]", "", o["cue"].lower())
            if " ".join(c.split()) not in " ".join(nar.get(seg, "").split()):
                bad.append((seg, o["cue"]))
        for v in o.values():
            walk(v, seg)
    elif isinstance(o, list):
        for v in o:
            walk(v, seg)


for sc in cartoon_kit.scenes:
    walk(sc, sc["segment"])
print("cue problems:", bad if bad else "none")
