"""Generates projects/nvidia-ceo-crisis-second-report/deliverables/documentary/storyboard.yaml
(Episode 53: follow-up to Ep 52 — Nvidia's CEO crisis after a second report).

Same world as Ep 52 (owner direction): very animated retro-future cartoon, genre-level inspiration only, original designs;
many anonymous people (`folk`), >= 40% daytime scenes, few charts (one bar board).
Real people: Jensen Huang as a respectful caricature (`caricature who=huang`); the first woman only as a faceless silhouette;
the SECOND PERSON IS NEVER DRAWN OR NAMED; Colette Kress and lawmakers appear in text only.

LIVE STORY — before rendering:
  1. Update CUM_BN / LATEST / ASOF below AND claim "cum" in sources.yaml (same numbers; defaults = Nov 12 premarket).
  2. Set `ending:` in project.yaml (pending | stays | out). For stays/out, first replace every [TO UPDATE ...] in endings.yaml
     with sourced facts. This generator copies the chosen ending into script.yaml (segment m_end) and refuses unfinished text.
  3. Run: python tools/gen_nvceo_storyboard.py, then lint + strictcue.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

ROOT = Path(__file__).resolve().parents[1]
PROJ = ROOT / "projects/nvidia-ceo-crisis-second-report"
OUT = PROJ / "deliverables/documentary/storyboard.yaml"

# ---------------------------------------------------------------- TO UPDATE before rendering (keep in sync with sources.yaml "cum")
CUM_BN = 649            # our estimate, $bn lost vs the Nov 6 close ($186.64) x 24.1bn shares
LATEST = 159.70         # price used for CUM_BN
ASOF = "PREMARKET, NOV 12, 8:11 A.M. ET"   # label shown on screen next to the latest price
# ---------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------- ending selection -> script.yaml m_end
ENDING = (yaml.safe_load((PROJ / "project.yaml").read_text()) or {}).get("ending", "pending")
_end = yaml.safe_load((PROJ / "endings.yaml").read_text())
if ENDING not in _end:
    raise SystemExit(f"project.yaml ending: {ENDING!r} not in endings.yaml")
_txt = " ".join(str(_end[ENDING]).split())
if "[TO UPDATE" in _txt:
    raise SystemExit(f"endings.yaml '{ENDING}' still contains [TO UPDATE ...]; fill it with sourced facts first")
_sp = PROJ / "deliverables/documentary/script.yaml"
_s = _sp.read_text()
_new = "- id: m_end\n  chapter: What to watch\n  narration: '" + _txt.replace("'", "''") + "'\n  claims:"
_s2, n = re.subn(r"- id: m_end\n  chapter: What to watch\n  narration: .*?\n  claims:", lambda m: _new, _s, flags=re.S)
if n != 1:
    raise SystemExit("could not locate segment m_end in script.yaml")
if _s2 != _s:
    _sp.write_text(_s2)

Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
FLOORS = ["$4.50TN", "$4.19TN", "$3.86TN"]


def buddy(x, y=860, **kw):
    return it("chipbuddy", x=x, y=y, **kw)


_SHIRTS = ["#4FB3F6", "#FF8A65", "#7BD389", "#B39DDB", "#FFC93C", "#F06292", "#4DD0E1", "#A1887F"]
_N = [0]


def folk(x, pose="stand", y=860, at=0.3, scale=0.95, **kw):
    """A generic, anonymous cartoon person (archetype only, never a real individual)."""
    k = _N[0]; _N[0] += 1
    d = {"x": x, "y": y, "pose": pose, "at": at, "scale": scale, "hair": (k * 3) % 5, "skin": (k * 7) % 4,
         "color": _SHIRTS[k % len(_SHIRTS)], **kw}
    return it("person", **d)


def bar(x, price, label, color, start):
    h = max(12, (price - 140) * 7.2)
    return {"d": f"M {x} 700 L {x} {700 - h:.0f} L {x + 150} {700 - h:.0f} L {x + 150} 700 Z", "color": color, "width": 4,
            "fill": color, "fillOpacity": 0.35, "kind": "bar", "start": start,
            "label": lbl(label, x + 75, 700 - h - 22, 20, color)}


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("chipcity", day=True)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.15}, {"at": 1.2, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=640, y=200, at=0.05, prefix="≈ -$", suffix="BN", steps=[[0.05, 0], [{"cue": "By our own estimate"}, CUM_BN]], text="NVIDIA MARKET VALUE SINCE NOV 6 (OUR ESTIMATE)", scale=1.3),
              it("sign", x=600, y=470, text=ASOF, at=C("measured at"), color="#FFE0B2", size=26),
              it("stockelevator", x=1560, y=110, at=0.3, scale=0.78, floors=FLOORS, stops=[C("By our own estimate"), C("measured at")], text="NVIDIA SHARES × 24.1BN"),
              buddy(520, 860, at=0.5, mood="worry", moods=[[C("By our own estimate"), "shock"]], label="GPU", hop=24),
              folk(300, "phone", at=0.3, poses=[[C("By our own estimate"), "shock"]]),
              folk(820, "phone", at=0.45, flip=True, poses=[[C("measured at"), "worry"]]),
              folk(1060, "stand", at=0.6, glasses=True, poses=[[C("measured at"), "shock"]])]},
    sources=["px", "sec"])
stage("s02_twist", "h_twist", {
    "zones": [Z("chipcity", day=True, signs=["SECOND HEADLINE INBOUND", "BOARD MEETING: DO NOT DISTURB", "CEO PARKING ONLY?", "STAY CHILL"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("Then came a second"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=600, y=240, text="EP 52: ≈ -$428BN IN TWO DAYS", at=C("In our last video"), color="#BBDEFB", size=32),
              it("paper", x=1050, y=430, at=C("Then came a second"), text="A SECOND REPORT", sub="THE NEW YORK TIMES · NOV 11", size=40),
              it("sign", x=1550, y=260, text="+ A BOARD MEETING", at=C("and a board meeting"), color="#FFCDD2", size=34),
              it("emptychair", x=1650, y=860, at=C("and a board meeting"), scale=0.8, text="CEO SEAT"),
              folk(360, "read", at=0.3), folk(760, "mic", at=C("Then came a second")), folk(1320, "camera", at=C("Then came a second", 0.3), flip=True)]},
    sources=["px", "nyt", "board"])
stage("s03_question", "h_question", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=150, text="LOSE THE FOUNDER? WHAT'S THE PRICE SAYING?", at=0.4, size=52, color="gold"),
              it("caricature", who="huang", x=760, y=860, at=0.3, scale=1.0, pose="worry"),
              it("emptychair", x=1400, y=860, at=0.6, scale=0.85, text="?"),
              folk(300, "phone", at=0.5), folk(1820, "shrug", at=0.7, flip=True)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("chipcity", day=True, signs=["REPORTED ≠ CONFIRMED", "BOARD ROOM →", "WHO'S NEXT?", "MARK YOUR CALENDAR"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("and the dates to watch"), "x": 1150, "y": 520, "zoom": 1.0, "dur": 2}], "drift": 3,
    "items": [it("sign", x=420, y=330, text="1 · REPORTED VS CONFIRMED", at=C("what was reported"), color="#BBDEFB", size=28),
              it("sign", x=900, y=330, text="2 · REMOVING A FOUNDER", at=C("what removing a founder"), color="#FFE0B2", size=28),
              it("sign", x=1380, y=330, text="3 · WHO COULD STEP IN", at=C("who could step in"), color="#C8E6C9", size=28),
              it("sign", x=1820, y=330, text="4 · DATES TO WATCH", at=C("and the dates to watch"), color="#F8BBD0", size=28),
              buddy(1000, 860, at=0.3, mood="happy", label="YOU?", hop=24),
              folk(560, "point", at=0.5), folk(1450, "clipboard", at=0.7, flip=True, glasses=True)]})

# ====================================================================== PART 1: the story so far
card("s05_c1", "m1_card", "The Story So Far", "Ep 52 in one minute")
stage("s06_recap", "m1_recap", {
    "zones": [Z("chipcity", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.1}, {"at": C("The New York Times and the Financial Times"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.2}], "drift": 2,
    "items": [it("caricature", who="huang", x=780, y=860, at=0.2, scale=1.1, poses=[[0, "stand"], [C("sent an email"), "memo"], [C("The same day"), "stand"]], label="JENSEN HUANG · FOUNDER AND CEO"),
              it("sign", x=780, y=200, text="'I WAS UNFAITHFUL TO MY WIFE.' (NOV 8 EMAIL)", at=C("I was unfaithful"), color="#FFF8E1", size=28),
              it("sign", x=1500, y=250, text="BOARD: INDEPENDENT INVESTIGATION", at=C("The same day"), color="#BBDEFB", size=28),
              it("caricature", who="silhouette", x=1800, y=860, at=C("The New York Times and the Financial Times"), scale=0.9, label="UNNAMED · PER PRESS REPORTS"),
              it("sign", x=1650, y=380, text="ALLEGED · DENIED BY CHINA · NO CHARGES", at=C("China called that"), color="#FFCDD2", size=26),
              folk(300, "read", at=C("sent an email")), folk(2200, "phone", at=0.6, flip=True)]},
    sources=["nvidia", "press"])
stage("s07_market", "m1_market", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Over two trading days"), "x": 1100, "y": 520, "zoom": 1.02, "dur": 1.6}], "drift": 1,
    "items": [it("sign", x=1000, y=170, text="BOARD: 'NO REASON TO BELIEVE … SECRETS WERE COMPROMISED'", at=C("no reason to believe"), color="#C8E6C9", size=24),
              buddy(480, 860, at=C("the broad market"), mood="happy", label="S&P 500", color="#3A86FF", hop=30),
              buddy(820, 860, at=C("Nvidia's rivals rose"), mood="happy", label="AMD", color="#E71D73", hop=60, hopRate=4.5),
              buddy(1160, 860, at=C("Nvidia's rivals rose", 0.3), mood="happy", label="AVGO", color="#FF9F1C", hop=50, hopRate=4),
              it("stockelevator", x=1720, y=120, at=0.3, scale=0.7, floors=FLOORS, stops=[C("while Nvidia fell", 0.5)], text="NOV 6 → NOV 10"),
              it("counter", x=1000, y=330, at=C("Over two trading days"), prefix="≈ -$", suffix="BN", steps=[[0, 0], [{"cue": "disappeared"}, 428]], text="TWO DAYS (OUR ESTIMATE, EP 52)"),
              folk(300, "type", y=900, at=0.3, tie=True, poses=[[C("while Nvidia fell"), "shock"]]),
              folk(2000, "cheer", y=900, at=C("Nvidia's rivals rose"), flip=True)]},
    sources=["nvidia", "px", "sec"])
add("p08_prices", "m1_draw", "engine_draw", {
    "title": "NVDA share price, four checkpoints", "board": BOARD, "draw_start": C("Let me draw the share price"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 700 700 L 1560 700", "color": "ink", "width": 4, "start": C("Let me draw the share price"), "label": lbl("CLOSES + LATEST (VENDOR DATA)", 1130, 750, 18, "ink")},
        bar(720, 186.64, "NOV 6 · $186.64", "accent2", C("Friday, November sixth")),
        bar(920, 168.89, "NOV 10 · $168.89", "accent2", C("Tuesday,")),
        bar(1120, 173.73, "NOV 11 · $173.73", "accent3", C("Then Wednesday's close")),
        bar(1320, LATEST, f"${LATEST:.2f}", "risk", C("And here is the latest")),
        {"d": arrow((1200, 330), (1380, 470), 0.2), "color": "risk", "width": 6, "kind": "arrow", "start": C("Look at what happened"), "label": lbl("THE SECOND STORY", 1240, 300, 18, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("between those last two bars", 0.1), "dur": 1.4, "target": [1300, 480]}],
    "scale": 0.86, "floor": 1040}, sources=["px"])
kinetic("s09_t1", "m1_transition", [("Wednesday started well…", 70, "Wednesday had started", None, False),
                                    ("…then the second story broke", 62, "the second story broke", "gold", False)])

# ====================================================================== PART 2: the second report
card("s10_c2", "m2_card", "The Second Report", "What the Times reported")
stage("s11_nyt", "m2_nyt", {
    "zones": [Z("newsroom")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The Times cited"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("calendar", x=520, y=330, at=0.2, pages=[[0, "NOV 11", "WEDNESDAY"]]),
              it("paper", x=1050, y=430, at=C("the New York Times reported"), text="A SECOND RELATIONSHIP", sub="REPORTED BY THE NEW YORK TIMES", size=38),
              it("sign", x=1500, y=250, text="SOURCES: 5 FORMER NVIDIA STAFF (NYT)", at=C("The Times cited"), color="#BBDEFB", size=28),
              it("sign", x=1050, y=760, text="REPORTED · NOT CONFIRMED", at=C("According to the report"), color="#FFCDD2", size=30),
              folk(300, "type", at=0.3), folk(1750, "phone", at=C("The Times cited"), flip=True), folk(1980, "type", at=0.6, flip=True, glasses=True)]},
    sources=["nyt"])
stage("s12_unconfirmed", "m2_unconfirmed", {
    "zones": [Z("chipcity", day=True, signs=["NO COMMENT ZONE", "PRESS: BEHIND THE LINE", "GPU PARKING ONLY", "MORE CORES"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("When the Times reached"), "x": 1050, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("sign", x=520, y=220, text="HUANG: NOT CONFIRMED", at=C("Huang has not confirmed"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=220, text="NVIDIA: NO COMMENT", at=C("Nvidia has not commented"), color="#FFE0B2", size=28),
              it("sign", x=1480, y=220, text="NBC: 'HAS NOT CONFIRMED'", at=C("NBC News said"), color="#FFE0B2", size=28),
              it("caricature", who="huang", x=1000, y=860, at=C("When the Times reached"), scale=1.05, poses=[[0, "stand"], [C("I don't think"), "talk"]]),
              it("sign", x=1000, y=380, text="'I DON'T THINK YOU SHOULD BE TALKING TO ME DIRECTLY.'", at=C("I don't think"), color="#FFF8E1", size=24),
              it("sign", x=1000, y=480, text="WE DON'T NAME HER · SHE IS NOT ACCUSED OF ANYTHING", at=C("We are not naming"), color="#C8E6C9", size=24),
              folk(380, "mic", at=0.4), folk(620, "camera", at=0.5), folk(1450, "mic", at=0.6, flip=True), folk(1720, "camera", at=0.7, flip=True)]},
    sources=["nyt"])
stage("s13_why", "m2_why", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It is a governance question"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="WHY INVESTORS CARE", at=0.3, size=66, color="gold"),
              it("sign", x=820, y=280, text="CEO", at=C("Because of the reporting line"), color="#FFE0B2", size=44),
              it("sign", x=820, y=420, text="↓ REPORTS TO HIM", at=C("who reports to him is not"), color="#BBDEFB", size=30),
              it("sign", x=1450, y=300, text="NOT GOSSIP: GOVERNANCE", at=C("It is a governance question"), color="#C8E6C9", size=32),
              it("sign", x=1450, y=420, text="CONFLICTS? WHO KNEW WHAT?", at=C("about conflicts of interest"), color="#FFCDD2", size=28),
              folk(350, "clipboard", at=0.4, tie=True, glasses=True), folk(1150, "read", at=0.6, tie=True),
              folk(1850, "point", at=C("That is the lens"), flip=True, tie=True, old=True)]},
    sources=["nyt"])
stage("s14_afterhours", "m2_afterhours", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In trading after the close"), "x": 1150, "y": 530, "zoom": 1.02, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=120, text="WEDNESDAY, NOV 11", at=0.2, size=58, color="gold"),
              it("sign", x=650, y=250, text="CLOSE: +2.86% → $173.73", at=C("closed up"), color="#C8E6C9", size=30),
              it("stockelevator", x=1720, y=120, at=C("In trading after the close"), scale=0.72, floors=["$4.19TN", "$3.96TN", "$3.76TN"], stops=[C("they slid"), C("the price had touched")], text="AFTER HOURS · LOW $156.20 (5:25 P.M. ET)"),
              it("sign", x=650, y=380, text="≈ -10% VS THE CLOSE (AFTER HOURS)", at=C("roughly ten percent"), color="#FFCDD2", size=28),
              it("sign", x=650, y=500, text="THU PREMARKET: AMD +3.9% · AVGO +3% (CNBC)", at=C("rivals AMD and Broadcom"), color="#BBDEFB", size=24),
              folk(300, "cheer", y=900, at=0.3, tie=True, poses=[[C("they slid"), "shock"]]),
              folk(1050, "type", y=900, at=0.5, poses=[[C("the price had touched"), "worry"]]),
              folk(1350, "phone", y=900, at=0.6, flip=True, poses=[[C("they slid", 0.3), "shock"]])]},
    sources=["px", "nyt"])
kinetic("s15_t2", "m2_transition", [("Meanwhile…", 76, "And while the price", None, False),
                                    ("…the board was meeting", 64, "the board was meeting", "gold", False)])

# ====================================================================== PART 3: the board meeting
card("s16_c3", "m3_card", "The Board Meeting", "Reported, not decided")
stage("s17_reports", "m3_reports", {
    "zones": [Z("secretroom", spinAt=0.5)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("CNBC confirmed"), "x": 1000, "y": 470, "zoom": 1.08, "dur": 2.0}], "drift": 1,
    "items": [it("sign", x=1000, y=150, text="WSJ: BOARD 'PREPARING TO OUST' HUANG (REPORTED)", at=C("The Wall Street Journal reported"), color="#FFE0B2", size=26),
              it("sign", x=1000, y=260, text="SEMAFOR: 'THE FULL BOARD HAS YET TO MAKE A DECISION'", at=C("Semafor reported the same"), color="#BBDEFB", size=24),
              it("sign", x=1000, y=370, text="CNBC: THE BOARD MET WEDNESDAY", at=C("CNBC confirmed"), color="#C8E6C9", size=28),
              it("sign", x=1000, y=480, text="THURSDAY MORNING: 'NO OUTCOME … ANNOUNCED'", at=C("no outcome had been announced"), color="#FFCDD2", size=26),
              it("emptychair", x=1000, y=900, at=0.4, scale=0.7, text="CEO SEAT"),
              folk(500, "read", at=0.4, tie=True), folk(740, "clipboard", at=0.5, tie=True, old=True),
              folk(1260, "worry", at=0.6, flip=True, tie=True), folk(1500, "read", at=0.7, flip=True, tie=True, glasses=True)]},
    sources=["board"])
stage("s17b_confidence", "m3_confidence", {
    "zones": [Z("newsroom")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("As of Thursday morning"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("calendar", x=520, y=330, at=0.2, pages=[[0, "NOV 8", "SUNDAY"], [C("As of Thursday morning"), "NOV 12", "THURSDAY"]]),
              it("paper", x=1050, y=430, at=C("On Sunday"), until=C("As of Thursday morning"), text="'CONFIDENCE IN JENSEN'", sub="NVIDIA BOARD STATEMENT · NOV 8", size=38),
              it("sign", x=1100, y=250, text="WITHDRAWN? NOT PUBLICLY (AS OF NOV 12, A.M.)", at=C("As of Thursday morning"), color="#FFE0B2", size=26),
              it("sign", x=1100, y=370, text="NEW STATEMENT: NONE · NEW SEC FILING: NONE", at=C("There was no new statement"), color="#BBDEFB", size=26),
              it("sign", x=1100, y=490, text="SOURCE OF THE OUSTER TALK: REPORTING", at=C("Everything about a possible"), color="#FFCDD2", size=28),
              folk(300, "type", at=0.3), folk(1750, "phone", at=C("As of Thursday morning"), flip=True), folk(1980, "read", at=0.6, flip=True, glasses=True)]},
    sources=["nvidia", "sec", "board"])
stage("s18_interim", "m3_interim", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Semafor reported that some"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("detective", x=[[0, -200], [C("an outside search firm"), 600]], y=860, at=0.2, scale=0.85, searchAt=C("chief executive candidates"), text="OUTSIDE SEARCH FIRM (BLOOMBERG · REPORTED)"),
              it("sign", x=1300, y=230, text="INTERIM LEADER WEIGHED (BLOOMBERG · REPORTED)", at=C("an interim leader first"), color="#BBDEFB", size=26),
              it("sign", x=1300, y=350, text="SEMAFOR: SOME DIRECTORS FAVOR CFO COLETTE KRESS", at=C("Semafor reported that some"), color="#FFE0B2", size=24),
              it("sign", x=1300, y=470, text="CONFIRMED BY NVIDIA: NO NAME", at=C("No name has been confirmed"), color="#FFCDD2", size=30),
              it("emptychair", x=1750, y=860, at=0.4, scale=0.8, text="INTERIM?"),
              folk(1050, "clipboard", at=0.5, glasses=True)]},
    sources=["board"])
stage("s19_control", "m3_control", {
    "zones": [Z("chipcity", day=True, signs=["SHAREHOLDERS ENTRANCE", "BOARD PARKING · 11 SPACES", "FOUNDER'S WALK", "NOW HIRING: CEO?"])], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("serves at the pleasure"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("counter", x=860, y=210, at=C("Huang owns about"), prefix="≈ ", suffix="%", decimals=1, steps=[[0, 0], [{"cue": "of the company's shares"}, 3.6]], text="HUANG'S SHARE OF NVIDIA (PROXY)"),
              it("sign", x=860, y=420, text="A FORTUNE, NOT A MAJORITY", at=C("far from a majority"), color="#FFE0B2", size=32),
              it("sign", x=1560, y=520, text="11 DIRECTORS · LEAD DIRECTOR, NO CHAIR (CNBC)", at=C("eleven directors"), color="#BBDEFB", size=26),
              it("sign", x=1560, y=640, text="OUT AS CEO ≠ OFF THE BOARD", at=C("would not, by itself"), color="#C8E6C9", size=30),
              it("caricature", who="huang", x=1180, y=860, at=0.3, scale=1.0, poses=[[0, "stand"], [C("serves at the pleasure"), "worry"]]),
              folk(1700, "read", at=C("eleven directors"), tie=True, flip=True), folk(1950, "clipboard", at=C("eleven directors", 0.3), tie=True, old=True, flip=True),
              folk(380, "phone", at=0.5)]},
    sources=["sec", "board"])
add("p20_decision", "m3_draw", "engine_draw", {
    "title": "Who sits in the CEO seat", "board": BOARD, "draw_start": C("Here is the board"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(640, 430, 260, 180), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the board"), "label": lbl("THE BOARD", 770, 528, 24, "accent2")},
        {"d": rect(1180, 430, 260, 180), "color": "accent", "width": 6, "kind": "box", "start": C("chief executive's seat"), "label": lbl("CEO SEAT", 1310, 528, 24, "accent")},
        {"d": arrow((905, 520), (1175, 520)), "color": "ink", "width": 6, "kind": "arrow", "start": C("The board appoints"), "label": lbl("APPOINTS", 1040, 490, 18, "ink")},
        {"d": rect(1180, 680, 260, 120), "color": "risk", "width": 5, "kind": "box", "start": C("an interim leader"), "label": lbl("INTERIM? (REPORTED)", 1310, 748, 18, "risk")},
        {"d": arrow((1310, 615), (1310, 675)), "color": "risk", "width": 5, "kind": "arrow", "start": C("the arrow moves"), "label": lbl("IF IT CHANGES", 1460, 650, 16, "risk")},
        {"d": "M 640 820 L 1440 820", "color": "accent3", "width": 4, "start": C("by law"), "label": lbl("8-K FILING, NORMALLY WITHIN 4 BUSINESS DAYS", 1040, 860, 18, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("that arrow points at the founder", 0.1), "dur": 1.4, "target": [1040, 520]}],
    "scale": 0.86, "floor": 1040}, sources=["board", "sec"])
kinetic("s21_t3", "m3_transition", [("Meanwhile, in Washington…", 70, "Meanwhile, in Washington", None, False),
                                    ("…louder", 80, "getting louder", "gold", False)])

# ====================================================================== PART 4: Washington
card("s22_c4", "m4_card", "Washington", "Calls to resign")
stage("s23_calls", "m4_calls", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Representative Suhas"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("sign", x=1000, y=170, text="SEN. KEVIN CRAMER (R-N.D.): 'HE'S GOT TO GO' (POLITICO VIA REUTERS)", at=C("Senator Kevin Cramer"), color="#FFE0B2", size=24),
              it("sign", x=1000, y=290, text="REP. SUHAS SUBRAMANYAM (D-VA.): 'SHOULD RESIGN' (CNBC)", at=C("Representative Suhas"), color="#BBDEFB", size=24),
              it("sign", x=1000, y=410, text="OPINIONS · NO REGULATOR FINDING", at=C("Those are their opinions"), color="#C8E6C9", size=30),
              folk(420, "point", at=C("Senator Kevin Cramer"), tie=True, old=True), folk(1580, "mic", at=C("Representative Suhas"), flip=True, tie=True),
              folk(1850, "camera", at=0.6, flip=True), folk(700, "camera", at=0.8)]},
    sources=["hill"])
stage("s24_chairs", "m4_chairs", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Asked whether subpoenas"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=700, y=250, text="DEADLINE: END OF WEDNESDAY", at=C("gave him until"), color="#FFE0B2", size=30),
              it("sign", x=700, y=370, text="REPS. MAST AND MOOLENAAR: NO REPLY YET", at=C("had not heard from Huang"), color="#BBDEFB", size=26),
              it("letters", x=1300, y=240, text="SUBPOENAS? 'YES.'", at=C("Mast said, yes"), size=64, color="gold"),
              folk(1050, "mic", at=0.4, tie=True), folk(1300, "camera", at=0.5, flip=True), folk(1550, "point", at=C("Asked whether subpoenas"), flip=True, tie=True, old=True)]},
    sources=["hill"])
stage("s25_letter", "m4_letter", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Democrats take control"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("docs", x=700, y=860, at=C("Elizabeth Warren and Chris Coons"), stampAt=C("preserve its records"), text="LETTER TO COMMERCE", stamp="KEEP"),
              it("sign", x=760, y=280, text="SENS. WARREN + COONS: PRESERVE EXPORT RECORDS", at=C("preserve its records"), color="#BBDEFB", size=26),
              it("sign", x=1450, y=280, text="'SIGNIFICANT CONCERNS' ON EXPORT CONTROLS", at=C("raises significant concerns"), color="#FFE0B2", size=26),
              it("calendar", x=1450, y=520, at=C("Democrats take control"), pages=[[0, "JAN", "NEW CONGRESS"]]),
              folk(380, "read", at=0.4, tie=True, glasses=True), folk(1850, "clipboard", at=C("Democrats take control"), flip=True, tie=True)]},
    sources=["hill"])
kinetic("s26_t4", "m4_transition", [("So what is the market", 70, "So what is the market", None, False),
                                    ("actually pricing?", 76, "actually pricing", "gold", False)])

# ====================================================================== PART 5: what the price says
card("s27_c5", "m5_card", "What the Price Says", "One seat, hundreds of billions")
stage("s28_keyperson", "m5_keyperson", {
    "zones": [Z("chipcity", day=True)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Jensen is Nvidia"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="KEY-PERSON RISK", at=0.3, size=66, color="gold"),
              it("sign", x=1000, y=230, text="10-K: 'HIGHLY DEPENDENT ON … OUR LONGSTANDING EXECUTIVE TEAM'", at=C("highly dependent"), color="#FFE0B2", size=24),
              it("letters", x=1000, y=360, text="'JENSEN IS NVIDIA. NVIDIA IS JENSEN.'", at=C("Jensen is Nvidia"), size=46, color="gold"),
              it("sign", x=1000, y=450, text="STACY RASGON, ANALYST (CNBC)", at=C("Jensen is Nvidia"), color="#BBDEFB", size=26),
              it("caricature", who="huang", x=760, y=860, at=0.3, scale=1.0, pose="stand"),
              buddy(1300, 860, at=0.5, mood="worry", label="GPU", hop=14),
              folk(380, "phone", at=0.5), folk(1700, "read", at=0.7, flip=True, glasses=True)]},
    sources=["sec", "press"])
stage("s29_ives", "m5_ives", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Bernstein downgraded"), "x": 1200, "y": 520, "zoom": 1.02, "dur": 1.6}], "drift": 1,
    "items": [it("sign", x=650, y=200, text="DAN IVES: -25% TO -30% IF REMOVED (OPINION)", at=C("Some analysts have put numbers"), color="#FFE0B2", size=26),
              it("sign", x=650, y=320, text="TARGET $300 IF HE STAYS · $225 IF OUSTED (IVES)", at=C("different price targets"), color="#BBDEFB", size=24),
              it("sign", x=1450, y=200, text="BERNSTEIN: DOWNGRADE · TARGET $400 → $200", at=C("Bernstein downgraded"), color="#FFE0B2", size=26),
              it("sign", x=1450, y=330, text="OPINIONS, NOT FACTS", at=C("Those are opinions"), color="#C8E6C9", size=32),
              it("emptychair", x=1000, y=900, at=C("a single seat"), scale=0.7, text="ONE SEAT"),
              folk(300, "type", y=900, at=0.3, tie=True), folk(1700, "phone", y=900, at=0.5, flip=True), folk(2000, "worry", y=900, at=C("a single seat"), flip=True)]},
    sources=["press", "nyt"])
stage("s30_peers", "m5_peers", {
    "zones": [Z("chipcity", day=True, signs=["AMD: OPEN LATE", "AVGO: SAME", "NVDA: PLEASE HOLD", "GPU PARKING ONLY"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Investors were not"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [buddy(560, 860, at=C("AMD and Broadcom rose"), mood="happy", label="AMD", color="#E71D73", hop=60, hopRate=4.5),
              buddy(900, 860, at=C("AMD and Broadcom rose", 0.3), mood="happy", label="AVGO", color="#FF9F1C", hop=50, hopRate=4),
              buddy(1400, 860, at=0.3, mood="sad", label="NVDA", color="#2EC4B6", hop=0),
              it("letters", x=1000, y=170, text="NOT SELLING CHIPS: SELLING UNCERTAINTY", at=C("Investors were not"), size=46, color="gold"),
              folk(300, "cheer", at=C("AMD and Broadcom rose")), folk(1750, "worry", at=0.5, flip=True), folk(2000, "phone", at=C("buying its rivals"), flip=True)]},
    sources=["px", "nyt"])
kinetic("s31_t5", "m5_transition", [("Three things to watch", 80, "Which leaves three", "gold", False)])

# ====================================================================== PART 6: what to watch
card("s32_c6", "m6_card", "What to Watch", "Board · results · Congress")
add("p33_watch", "m6_draw", "engine_draw", {
    "title": "Three things to watch", "board": BOARD, "draw_start": C("Let me draw them"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(600, 360, 280, 130), "color": "accent2", "width": 6, "kind": "box", "start": C("First, the board"), "label": lbl("1 · BOARD / 8-K", 740, 432, 20, "accent2")},
        {"d": rect(600, 530, 280, 130), "color": "accent", "width": 6, "kind": "box", "start": C("the results"), "label": lbl("2 · RESULTS NOV 17", 740, 602, 20, "accent")},
        {"d": rect(600, 700, 280, 130), "color": "accent3", "width": 6, "kind": "box", "start": C("Third, Congress"), "label": lbl("3 · BRIEFING NOV 18?", 740, 772, 20, "accent3")},
        {"d": rect(1200, 520, 300, 160), "color": "risk", "width": 6, "kind": "box", "start": C("All three arrows"), "label": lbl("WHO RUNS NVIDIA?", 1350, 608, 22, "risk")},
        {"d": arrow((885, 425), (1195, 560)), "color": "ink", "width": 5, "kind": "arrow", "start": C("All three arrows")},
        {"d": arrow((885, 595), (1195, 600)), "color": "ink", "width": 5, "kind": "arrow", "start": C("All three arrows", 0.3)},
        {"d": arrow((885, 765), (1195, 640)), "color": "ink", "width": 5, "kind": "arrow", "start": C("All three arrows", 0.6)},
    ],
    "actions": [{"kind": "point", "at": C("who runs Nvidia", 0.05), "dur": 1.4, "target": [1350, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["nvidia", "sec", "press"])

# ending scene (matches project.yaml ending)
_END_ITEMS = {
    "pending": [it("letters", x=1000, y=130, text="DECISION: NOT ANNOUNCED", at=0.3, size=60, color="gold"),
                it("sign", x=1000, y=250, text=f"AS OF: {ASOF}", at=0.6, color="#FFE0B2", size=26),
                it("sign", x=1000, y=360, text="WATCH FOR: AN 8-K FILING (≈ 4 BUSINESS DAYS)", at=C("the first thing to look for"), color="#BBDEFB", size=26),
                it("emptychair", x=1450, y=860, at=0.4, scale=0.85, text="CEO SEAT"),
                it("caricature", who="huang", x=650, y=860, at=0.5, scale=0.95, pose="stand")],
    "stays": [it("letters", x=1000, y=130, text="UPDATE: HUANG STAYS (NVIDIA)", at=0.3, size=58, color="gold"),
              it("caricature", who="huang", x=1000, y=860, at=0.4, scale=1.1, poses=[[0, "stand"], [1.5, "wave"]])],
    "out": [it("letters", x=1000, y=130, text="UPDATE: HUANG STEPS DOWN AS CEO (NVIDIA)", at=0.3, size=52, color="gold"),
            it("emptychair", x=1000, y=860, at=0.4, scale=1.0, text="CEO SEAT"),
            it("caricature", who="huang", x=500, y=860, at=0.6, scale=0.9, pose="worry")],
}
stage("s34_end", "m_end", {
    "zones": [Z("chipcity", day=True)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.08}, {"at": 2.0, "x": 1050, "y": 520, "zoom": 1.0, "dur": 3}], "drift": 3,
    "items": [*_END_ITEMS[ENDING], folk(300, "phone", at=0.5), folk(1850, "mic", at=0.6, flip=True), folk(2080, "camera", at=0.7, flip=True)]},
    sources=["board", "sec"])

# ====================================================================== PAYOFF
stage("s35_payoff", "payoff", {
    "zones": [Z("chipcity", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("But markets"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=110, text="NOT THE CHIPS", at=0.3, size=62, color="gold"),
              it("sign", x=1000, y=250, text="'HIGHLY DEPENDENT' ON ITS LEADERS (10-K)", at=C("by its own admission"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=370, text="PROVEN IN COURT: NOTHING · CHARGES: NONE", at=C("Nothing in this story"), color="#C8E6C9", size=28),
              it("letters", x=1000, y=520, text="NOT A CHIP. A CHAIR.", at=C("It is a chair"), size=64, color="gold"),
              it("emptychair", x=1000, y=900, at=C("the biggest uncertainty"), scale=0.8, text=""),
              buddy(500, 860, at=0.4, mood="worry", label="GPU", hop=18), buddy(1500, 860, at=0.6, mood="worry", label="GPU", color="#FF9F1C", hop=18),
              folk(260, "phone", at=0.5), folk(1780, "read", at=0.7, flip=True)]},
    sources=["px", "sec"])
add("s36_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_nvceo_storyboard.py; edit the generator, not this file.\n"
           f"# Episode 53 storyboard (Nvidia CEO crisis). ending={ENDING}; CUM_BN={CUM_BN}; LATEST={LATEST}; ASOF={ASOF}.\n")
