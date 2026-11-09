"""Generates projects/the-bank-that-accidentally-sent-900-million/deliverables/documentary/storyboard.yaml (Episode 21, Citibank / Revlon).

Bespoke worlds (tones from visual_direction.yaml: thriller -> crisis -> strategy -> reflective): a late-evening operations
floor, the new `wireform` item (a redrawn, generic loan-payment form with the three wash-account checkboxes FRONT / FUND /
PRINCIPAL, the maker-checker-approver row and the "Funds will be sent out of the bank. Continue?" dialog) as the
through-line, a vault whose door swings open, a river of coins to the lenders, a split pile (returned vs kept), and two
courtrooms (2021 ruling, 2022 reversal).
Presenter: the agent plumbing (boxes + arrows), the size of the mistake (bars), the discharge-for-value test (boxes + arrows).
No Citi, Revlon or Flexcube logos or real UI; real people named in text only, as they appear in the court opinion.
Run: python tools/gen_citibank_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-bank-that-accidentally-sent-900-million/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}


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
    "zones": [Z("vault", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.15}, {"at": C("and the people who receive it"), "x": 1400, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 2,
    "items": [it("vaultdoor", x=900, at=0.2, openAt=C("sends almost a billion dollars"), scale=0.9),
              it("coins", **{"from": [900, 500], "to": [2300, 420]}, at=C("sends almost a billion dollars", 0.5), rate=9),
              *crowd([2050, 2200, 2350], "cheer", at=C("and the people who receive it"), scale=0.7),
              it("letters", x=2200, y=220, text="THANK YOU, WE'RE KEEPING IT", at=C("we are keeping it"), size=48, color="gold")],
    "callouts": [co("One of the world's biggest banks…", 960, 960, C("What happens"), "white", screen=True, size=40, until=C("and the people who receive it", -0.3)),
                 co("…sends almost $1 billion to the wrong place", 960, 960, C("and the people who receive it"), "risk", screen=True, size=40)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("office", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": C("A federal judge"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=380, y=300, at=0.2, pages=[[0, "AUG 11", "2020"]], scale=0.8),
              it("wireform", x=1000, y=470, at=0.3, scale=0.75, checks=[None, None, 0.6], approvals=[0.8, 1.0, 1.2], warnAt=C("Instead", -1.2), yesAt=C("Instead"), total=894),
              it("paper", x=1800, y=380, at=C("A federal judge"), text="'one of the biggest blunders in banking history'", name="S.D.N.Y. OPINION", scale=0.75),
              it("gavel", x=2300, y=420, hits=[C("And then he ruled", 0.6)])],
    "callouts": [co("Meant to pay: {{wired.interest_display}} of interest", 960, 960, C("Citibank meant to pay"), "white", screen=True, size=40, sub="S.D.N.Y. opinion", until=C("Instead", -0.3)),
                 co("Sent: {{wired.display}} of its own money", 960, 960, C("Instead"), "risk", screen=True, size=42, until=C("A federal judge", -0.3)),
                 co("'One of the biggest blunders in banking history'", 960, 960, C("A federal judge"), "gold", screen=True, size=36, until=C("And then he ruled", -0.3)),
                 co("…and much of it did not have to come back", 960, 960, C("And then he ruled"), "risk", screen=True, size=38)]},
    sources=["furman"])

# ====================================================================== PART 1: the middleman
card("s03_c1", "m1_card", "The Middleman", "Revlon's $1.8 billion loan")
stage("s04_q1", "m1_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("building", x=700, at=0.2, text="BANK", scale=0.8),
              it("arrow", **{"from": [900, 450], "to": [1250, 450]}, at=1.0),
              it("pricetag", x=1400, y=320, at=1.4, pages=[[0, "REVLON'S BILLS"]], sub="paid by the bank?")],
    "callouts": [co("Why was a bank paying Revlon's bills?", 960, 150, C("Why was Citibank"), "gold", screen=True, size=42)]})
stage("s05_loan", "m1_loan", {
    "zones": [Z("exchange")], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("Someone has to sit"), "x": 1500, "y": 520, "zoom": 0.9, "dur": 2.4},
            {"at": C("And Revlon's agent"), "x": 1600, "y": 500, "zoom": 1.05, "dur": 2.2}], "drift": 3,
    "items": [it("counter", x=700, y=220, at=C("Revlon borrowed"), prefix="$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "Revlon borrowed", "offset": 1.5}, 1.8]], text="2016 TERM LOAN · 7 YEARS"),
              it("stack", x=700, h=[[0, 40], [{"cue": "syndicated loan", "offset": 1}, 260]], at=C("syndicated loan"), text="LOAN", sub="many lenders"),
              *crowd([1900, 2020, 2140, 2260, 2380], "stand", at=C("from dozens of lenders"), scale=0.6),
              it("desk", x=1500, at=C("Someone has to sit"), scale=0.9, pile=True),
              it("sign", x=1500, y=300, text="ADMINISTRATIVE AGENT", sub="collects and passes on payments", at=C("That job is called"), color="#BBDEFB", size=32),
              it("letters", x=1500, y=180, text="= CITIBANK", at=C("And Revlon's agent"), size=60, color="gold")],
    "callouts": [co("2016: a $1.8bn syndicated loan to Revlon", 960, 960, C("Revlon borrowed"), "white", screen=True, size=38, sub="S.D.N.Y. opinion", until=C("Someone has to sit", -0.3)),
                 co("The middleman: the administrative agent", 960, 960, C("Someone has to sit"), "gold", screen=True, size=40)]},
    sources=["furman"])
add("p06_plumbing", "m1_draw", "engine_draw", {
    "title": "The plumbing", "board": BOARD, "draw_start": C("Here is Revlon"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(580, 440, 220, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is Revlon"), "label": lbl("REVLON", 690, 510, 26, "accent2")},
        {"d": rect(930, 440, 240, 120), "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.2, "kind": "box", "start": C("Here is Citibank"), "label": lbl("CITIBANK (AGENT)", 1050, 510, 22, "accent")},
        {"d": rect(1300, 330, 200, 80) + " " + rect(1300, 460, 200, 80) + " " + rect(1300, 590, 200, 80), "color": "accent3", "width": 5, "kind": "box", "start": C("here are the lenders"), "label": lbl("LENDERS", 1400, 310, 24, "accent3")},
        {"d": arrow((810, 500), (920, 500), 0.1), "color": "ink", "width": 4, "start": C("Revlon sends the money")},
        {"d": arrow((1180, 480), (1290, 370), 0.1) + " " + arrow((1180, 500), (1290, 500), 0.0) + " " + arrow((1180, 520), (1290, 630), -0.1), "color": "ink", "width": 4, "kind": "arrow", "start": C("splits it")},
        {"d": rect(560, 700, 220, 110), "color": "risk", "width": 5, "kind": "box", "start": C("connected to the bank's own vault"), "label": lbl("CITI'S OWN VAULT", 670, 760, 22, "risk")},
        {"d": "M 1000 570 L 780 720", "color": "risk", "width": 4, "start": C("connected to the bank's own vault", 0.4)},
        {"d": "M 790 760 Q 1050 800 1290 660", "color": "risk", "width": 5, "start": C("If the agent sends too much"), "label": lbl("too much: Citi's money", 1060, 840, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("out of Citibank's own pocket", 0.2), "dur": 1.4, "target": [670, 760]}],
    "scale": 0.86, "floor": 1040}, sources=["furman"])
stage("s07_trouble", "m1_trouble", {
    "zones": [Z("exchange")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("On the market"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("storm", x=800, y=220, at=C("Revlon was in deep trouble"), scale=0.7),
              it("contract", x=800, y=450, at=C("In May"), text="MAY 2020 DEAL", sub="$800M+ new financing", scale=0.6),
              *crowd([1150, 1270, 1390], "worry", at=C("Many lenders were furious"), scale=0.7),
              it("chart", x=1800, y=420, w=500, h=300, at=C("On the market"), dur=2.5, text="OLD LOAN PRICE (¢ PER $1)", pts=[0.9, 0.7, 0.5, 0.35, 0.28], color="risk"),
              it("letters", x=1800, y=170, text="< 30¢", at=C("trading for"), size=90, color="risk")],
    "callouts": [co("May 2020: $800M+ raised, old lenders' collateral moved", 960, 960, C("In May"), "white", screen=True, size=34, sub="S.D.N.Y. opinion", until=C("On the market", -0.3)),
                 co("Old loan: under 30 cents on the dollar", 960, 960, C("On the market"), "risk", screen=True, size=40, sub="Kelley Drye")]},
    sources=["furman", "kelleydrye"])
kinetic("s08_t1", "m1_transition", [("Then Citibank paid them back in full", 54, "Citibank paid them back", None, True), ("By accident.", 84, "By accident", "risk", False)])

# ====================================================================== PART 2: three checkboxes
card("s09_c2", "m2_card", "Three Checkboxes", "August 11, 2020")
stage("s10_q2", "m2_question", {
    "zones": [Z("office", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("wireform", x=960, y=470, at=0.2, scale=0.8, checks=[None, None, 2.5])],
    "callouts": [co("How do you send $900 million by mistake?", 960, 120, C("How do you send"), "gold", screen=True, size=42)]})
stage("s11_task", "m2_task", {
    "zones": [Z("office", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Citibank's payment software"), "x": 1500, "y": 500, "zoom": 1.05, "dur": 2.4},
            {"at": C("and then redirect"), "x": 2000, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("docs", x=800, y=560, at=C("As part of a deal"), text="PAY INTEREST EARLY · ALL OLD LENDERS", scale=0.6),
              it("device", type="laptop", x=1450, y=F, at=C("Citibank's payment software"), scale=1.1, text="PAYMENT SOFTWARE"),
              it("pricetag", x=1450, y=300, at=C("as if Revlon were paying off"), pages=[[0, "FULL PAYOFF?"]], sub="entered as a payoff"),
              it("vaultdoor", x=2200, at=C("an internal account"), scale=0.6),
              it("sign", x=2200, y=200, text="WASH ACCOUNT", sub="internal · money stays in", at=C("called a wash account"), color="#C8E6C9", size=34)],
    "callouts": [co("Pay interest to all old lenders, early", 960, 960, C("As part of a deal"), "white", screen=True, size=38, sub="S.D.N.Y. opinion", until=C("Citibank's payment software", -0.3)),
                 co("The quirk: enter a full payoff…", 960, 960, C("The easiest way"), "gold", screen=True, size=40, until=C("and then redirect", -0.3)),
                 co("…and park the principal in a 'wash account'", 960, 960, C("and then redirect"), "green", screen=True, size=38)]},
    sources=["furman"])
stage("s12_boxes", "m2_boxes", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True, "min_seconds": 18,
    "cam": [{"at": 0, "x": 1100, "y": 500, "zoom": 1.15}, {"at": C("The employee who built"), "x": 1200, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 1,
    "items": [it("wireform", x=1000, y=470, at=0.2, scale=0.9, checks=[None, None, C("ticked only one", 1.0)]),
              it("letters", x=1000, y=130, text="ALL THREE REQUIRED", at=C("three fields on the screen"), size=48, color="gold"),
              it("person", x=1650, pose="read", at=C("The employee who built"), scale=0.8, hair=3, skin=2),
              it("sign", x=1700, y=300, text="OUTSOURCED TEAM · INDIA", sub="working for Citibank via Wipro", at=C("part of a team in India"), color="#FFE082", size=26)],
    "callouts": [co("The manual: FRONT, FUND and PRINCIPAL", 960, 960, C("They were called front"), "white", screen=True, size=40, sub="S.D.N.Y. opinion", until=C("The employee who built", -0.3)),
                 co("Ticked: only PRINCIPAL", 960, 960, C("ticked only one"), "risk", screen=True, size=44)]},
    sources=["furman", "reg_2021"])
stage("s13_six", "m2_six", {
    "zones": [Z("office", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("All three believed"), "x": 1300, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 2,
    "items": [it("wireform", x=950, y=470, at=0.2, scale=0.85, checks=[None, None, 0.1], approvals=[C("Three people must review"), C("The second person checked", 1), C("The third", 4)]),
              *[it("person", x=1700 + 200 * k, pose="read", at=C("Three people must review", 0.4 * k), scale=0.7, hair=k + 1, skin=k) for k in range(3)],
              it("letters", x=1900, y=200, text="3 PEOPLE · 6 EYES", at=C("called six eyes"), size=56, color="gold"),
              it("paper", x=1900, y=420, at=C("replied"), text="'Looks good, please proceed.'", name="EMAIL", scale=0.6)],
    "callouts": [co("'Six eyes': maker, checker, approver", 960, 960, C("called six eyes"), "white", screen=True, size=40, sub="S.D.N.Y. opinion", until=C("The third", -0.3)),
                 co("'Principal is going to wash.' It was not.", 960, 960, C("The third"), "gold", screen=True, size=38, until=C("All three believed", -0.3)),
                 co("All three misread the same screen", 960, 960, C("All three believed"), "risk", screen=True, size=40)]},
    sources=["furman"])
stage("s14_stop", "m2_stop", {
    "zones": [Z("office", night=True), Z("vault", 1700, 6000, night=True)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": C("And Citibank's money went out"), "x": 1800, "y": 520, "zoom": 0.85, "dur": 2.6}], "drift": 2,
    "items": [it("wireform", x=1000, y=470, at=0.2, scale=0.9, checks=[None, None, 0.1], approvals=[0.1, 0.1, 0.1], warnAt=C("A box popped up"), yesAt=C("The approver clicked yes", 0.4), total=894),
              it("vaultdoor", x=2300, at=C("The approver clicked yes"), openAt=C("And Citibank's money went out"), scale=0.7),
              it("coins", **{"from": [2300, 500], "to": [3300, 400]}, at=C("And Citibank's money went out", 0.4), rate=10),
              it("letters", x=2300, y=160, text="TO THE PENNY", at=C("to the penny"), size=60, color="risk")],
    "callouts": [co("'Funds will be sent out of the bank. Continue?'", 960, 120, C("A box popped up"), "white", screen=True, size=36, sub="S.D.N.Y. opinion", until=C("But it did not say", -0.3)),
                 co("No amount shown", 960, 120, C("But it did not say"), "gold", screen=True, size=44, until=C("The approver clicked yes", -0.3)),
                 co("YES → the whole loan, paid off to the penny", 960, 120, C("The approver clicked yes"), "risk", screen=True, size=38)]},
    sources=["furman"])
stage("s15_missed", "m2_missed", {
    "zones": [Z("office", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Under amount paid"), "x": 1500, "y": 500, "zoom": 1.15, "dur": 2.4}], "drift": 2,
    "items": [it("clock", x=500, y=300, at=C("That evening"), period=3.0),
              it("docs", x=900, y=560, at=C("sent his manager the paperwork"), text="BACK-UP + SCREENSHOTS", scale=0.6),
              it("board", x=1500, y=380, at=C("Under amount paid"), text="AMOUNT PAID", rows=[{"name": "INTEREST  $7.8M"}, {"name": "PRINCIPAL  $894M", "color": "risk"}]),
              it("magnifier", x=[[0, 1300], [6, 1600]], y=[[0, 520], [6, 470]], at=C("in principal"), scale=0.8),
              it("person", x=2150, pose="stand", at=C("He did not see anything wrong"), scale=0.75, hair=4, skin=1)],
    "callouts": [co("The screenshots showed $894M in principal…", 960, 960, C("Under amount paid"), "risk", screen=True, size=38, sub="S.D.N.Y. opinion", until=C("He did not see", -0.3)),
                 co("…read as 'paid' to the internal account", 960, 960, C("He did not see"), "white", screen=True, size=38)]},
    sources=["furman"])
add("p16_size", "m2_draw", "engine_draw", {
    "title": "The size of the mistake", "board": BOARD, "draw_start": C("Here is what Citibank meant to send"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 820 L 1400 820 M 600 820 L 600 330", "color": "ink", "width": 4, "start": C("Here is what Citibank meant to send")},
        {"d": "M 700 820 L 700 816 L 860 816 L 860 820", "color": "accent3", "width": 6, "kind": "bar", "start": C("Here is what Citibank meant to send", 0.6), "label": lbl("MEANT: $7.8M", 780, 860, 24, "accent3")},
        {"d": "M 1000 820 L 1000 360 L 1200 360 L 1200 820", "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("what actually left the bank"), "label": lbl("SENT: $894M + $7.8M", 1100, 330, 24, "risk")},
        {"d": "M 780 800 Q 880 700 990 600", "color": "ink", "width": 4, "start": C("barely a line"), "label": lbl("> 100× smaller", 820, 660, 26, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("More than a hundred times smaller", 0.2), "dur": 1.4, "target": [780, 815]}],
    "scale": 0.86, "floor": 1040}, sources=["furman"])
kinetic("s17_t2", "m2_transition", [("Nobody noticed that evening", 58, "Nobody noticed", None, False), ("The next morning, somebody did", 58, "somebody did", "risk", False)])

# ====================================================================== PART 3: the morning after
card("s18_c3", "m3_card", "The Morning After", "August 12, 2020")
stage("s19_q3", "m3_question", {
    "zones": [Z("office")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("docs", x=800, y=560, at=0.2, text="PLEASE RETURN", scale=0.7, stamp="SENT IN ERROR", stampAt=2.0),
              it("arrow", **{"from": [1050, 450], "to": [1500, 450]}, at=1.2)],
    "callouts": [co("Can you just ask for it back?", 960, 150, C("Can you just ask"), "gold", screen=True, size=44)]})
stage("s20_bad", "m3_bad", {
    "zones": [Z("office")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("By the afternoon"), "x": 1800, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=0.2, pages=[[0, "AUG 12", "9:00 AM"]], scale=0.8),
              it("device", type="laptop", x=900, y=F, at=C("a team manager"), redAt=C("found a"), scale=1.0, text="CASH BREAKS"),
              it("paper", x=1150, y=360, at=C("In a chat message"), text="'bad news… went out the door'", name="CHAT", scale=0.6),
              *[it("docs", x=1650 + 180 * k, y=560, at=C("By the afternoon", 0.3 * k), text="RECALL NOTICE", scale=0.45, stamp="IN ERROR", stampAt=C("sent in error", 0.2 * k)) for k in range(4)]],
    "callouts": [co("Next morning: the discrepancy surfaces", 960, 960, C("Around nine"), "white", screen=True, size=38, sub="S.D.N.Y. opinion", until=C("By the afternoon", -0.3)),
                 co("Recall notices to every lender", 960, 960, C("By the afternoon"), "gold", screen=True, size=40)]},
    sources=["furman"])
stage("s21_split", "m3_split", {
    "zones": [Z("vault")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("refused"), "x": 1700, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("stack", x=800, h=[[0, 40], [{"cue": "came home", "offset": 1.2}, 300]], at=C("Many lenders sent it back"), text="$385M", sub="returned"),
              it("coins", **{"from": [1700, 400], "to": [800, 500]}, at=C("Many lenders sent it back"), rate=5, until=C("came home", 2)),
              it("stack", x=1700, h=[[0, 40], [{"cue": "refused", "offset": 1.2}, 400]], at=C("investment firms"), text="$504M", sub="kept by 10 firms", color="#C62828"),
              it("letters", x=1700, y=170, text="REFUSED", at=C("refused"), size=70, color="risk"),
              it("paper", x=2300, y=400, at=C("One of them replied"), text="'not at all clear… paid in error'", name="REPLY", scale=0.6)],
    "callouts": [co("About {{split.display}}", 960, 960, C("Many lenders sent it back"), "green", screen=True, size=40, sub="Banking Dive", until=C("refused", -0.3)),
                 co("10 firms refused: ≈ {{split.kept_display}} at stake", 960, 960, C("refused"), "risk", screen=True, size=38, sub="S.D.N.Y. opinion")]},
    sources=["bankingdive", "furman"])
stage("s22_hold", "m3_hold", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("One firm said"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("arrow", **{"from": [1000, 400], "to": [500, 400]}, at=C("straight back")),
              it("barrier", x=900, at=C("Others told their banks to wait"), closeAt=C("to wait"), scale=0.9),
              it("paper", x=1600, y=380, at=C("One firm said"), text="'please hold off until you hear from us'", name="TO THE TRUSTEE", scale=0.65),
              it("clock", x=2200, y=330, at=C("The longer they held on"), period=2.0)],
    "callouts": [co("Some sent it straight back; others said 'wait'", 960, 960, C("Some sent the money"), "white", screen=True, size=36, sub="S.D.N.Y. opinion", until=C("The longer they held on", -0.3)),
                 co("A delay that became a decision", 960, 960, C("The longer they held on"), "gold", screen=True, size=40)]},
    sources=["furman"])
stage("s23_why", "m3_why", {
    "zones": [Z("exchange")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("And they were already in a fight"), "x": 1800, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("pricetag", x=700, y=300, at=C("They held a loan"), pages=[[0, "< 30¢"], [{"cue": "every cent"}, "100¢ IN CASH"]], sub="per $1 of loan"),
              *crowd([1100, 1220], "cheer", at=C("every cent"), scale=0.7),
              it("gavel", x=1900, y=420, hits=[C("sued Revlon and Citibank", 0.5)]),
              it("docs", x=2000, y=600, at=C("The very next day"), text="LENDERS v. REVLON & CITIBANK", scale=0.55),
              it("letters", x=1900, y=170, text="'WHAT WE WERE OWED'", at=C("It was what they were owed"), size=54, color="gold")],
    "callouts": [co("A loan worth < 30¢ suddenly paid at 100¢", 960, 960, C("They held a loan"), "gold", screen=True, size=38, sub="Kelley Drye", until=C("And they were already in a fight", -0.3)),
                 co("Aug 12: lenders sue Revlon and Citibank (UMB Bank)", 960, 960, C("And they were already in a fight"), "white", screen=True, size=36, sub="S.D.N.Y. opinion")]},
    sources=["kelleydrye", "furman"])
kinetic("s24_t3", "m3_transition", [("So Citibank went to court", 60, "went to court", None, False), ("sure the law was on its side", 56, "on its side", "gold", False)])

# ====================================================================== PART 4: finders keepers
card("s25_c4", "m4_card", "Finders Keepers?", "The 2021 ruling")
stage("s26_q4", "m4_question", {
    "zones": [Z("court")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("gavel", x=960, y=420, hits=[3.0]), it("coins", **{"from": [400, 300], "to": [1500, 500]}, at=0.6, rate=4)],
    "callouts": [co("Paid by mistake: must you give it back?", 960, 150, C("If someone pays you"), "gold", screen=True, size=40)]})
stage("s27_rule", "m4_rule", {
    "zones": [Z("court")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("But there is an old exception"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("docs", x=800, y=560, at=C("Under New York law"), text="MISTAKEN PAYMENT → RETURN IT", scale=0.6),
              it("sign", x=1600, y=300, text="DISCHARGE FOR VALUE", sub="the exception", at=C("called discharge for value"), color="#FFE082", size=36),
              it("paper", x=2200, y=400, at=C("As New York's highest court"), text="'a final and complete transaction'", name="BANQUE WORMS, 1991", scale=0.65)],
    "callouts": [co("The rule: mistaken payments go back", 960, 960, C("Usually, yes"), "white", screen=True, size=40, sub="S.D.N.Y. opinion", until=C("But there is an old exception", -0.3)),
                 co("The exception: 'discharge for value'", 960, 960, C("But there is an old exception"), "gold", screen=True, size=40)]},
    sources=["furman"])
add("p28_test", "m4_draw", "engine_draw", {
    "title": "The test", "board": BOARD, "draw_start": C("First box"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 360, 300, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("First box"), "label": lbl("OWED THE MONEY?", 690, 422, 20, "accent2")},
        {"d": rect(880, 360, 300, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("Second box"), "label": lbl("DIDN'T MISLEAD?", 1030, 422, 20, "accent2")},
        {"d": rect(1220, 360, 300, 110), "color": "accent", "width": 7, "fill": "accent", "fillOpacity": 0.2, "kind": "box", "start": C("Third box"), "label": lbl("NO NOTICE OF MISTAKE?", 1370, 422, 18, "accent")},
        {"d": arrow((1010, 480), (760, 680), 0.1), "color": "accent3", "width": 5, "start": C("the arrow leads to keeping it"), "label": lbl("ALL YES → KEEP IT", 720, 720, 24, "accent3")},
        {"d": arrow((1010, 480), (1300, 680), -0.1), "color": "risk", "width": 5, "start": C("If any answer is no"), "label": lbl("ANY NO → GIVE IT BACK", 1320, 720, 24, "risk")},
        {"d": "M 1210 350 L 1530 350 L 1530 480 L 1210 480 Z", "color": "risk", "width": 4, "kind": "box", "start": C("came down to that third box")},
    ],
    "actions": [{"kind": "point", "at": C("that third box", 0.2), "dur": 1.4, "target": [1370, 420]}],
    "scale": 0.86, "floor": 1040}, sources=["furman", "kelleydrye"])
stage("s29_ruling", "m4_ruling", {
    "zones": [Z("court")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("The amounts matched"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("His conclusion was blunt"), "x": 2000, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=0.2, pages=[[0, "FEB 16", "2021"]], scale=0.8),
              it("gavel", x=900, y=420, hits=[C("ruled in February", 0.3)]),
              it("letters", x=1450, y=200, text="TO THE PENNY", at=C("The amounts matched"), size=54, color="gold"),
              it("sign", x=1500, y=420, text="BACKER OWNED ≈ 85%", sub="Ronald Perelman's company", at=C("Ronald Perelman"), color="#E1BEE7", size=30),
              it("paper", x=2050, y=380, at=C("His conclusion was blunt"), text="'not entitled to its money back'", name="S.D.N.Y. OPINION", scale=0.7),
              it("stack", x=2500, h=[[0, 40], [{"cue": "The lenders could keep", "offset": 1.2}, 400]], at=C("The lenders could keep"), text="$504M", sub="kept (for now)", color="#C62828")],
    "callouts": [co("Feb 2021: 'Defendants' clients are entitled to keep the money'", 960, 960, C("After a trial"), "white", screen=True, size=32, sub="S.D.N.Y. opinion", until=C("His conclusion was blunt", -0.3)),
                 co("Citibank 'is not entitled to its money back'", 960, 960, C("His conclusion was blunt"), "risk", screen=True, size=38)]},
    sources=["furman", "bankingdive"])
stage("s30_fine", "m4_fine", {
    "zones": [Z("parliament")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Citibank said it would appeal"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.2}], "drift": 3,
    "items": [it("magnifier", x=[[0, 700], [6, 1000]], y=[[0, 520], [6, 480]], at=C("raised questions about its controls"), scale=0.8),
              it("docs", x=1100, y=560, at=C("may have contributed"), text="OCC · OCT 2020", scale=0.6, stamp="$400M FINE", stampAt=C("fine")),
              it("sign", x=1800, y=300, text="APPEAL", sub="Second Circuit", at=C("Citibank said it would appeal"), color="#BBDEFB", size=40)],
    "callouts": [co("Oct 2020: OCC fine of {{occ.display}} (link 'potential', per Banking Dive)", 960, 960, C("as the trade publication"), "white", screen=True, size=32, sub="Banking Dive", until=C("Citibank said it would appeal", -0.3)),
                 co("Citibank appeals", 960, 960, C("Citibank said it would appeal"), "gold", screen=True, size=42)]},
    sources=["bankingdive"])
kinetic("s31_t4", "m4_transition", [("The appeal took", 60, "The appeal took", None, False), ("another year and a half", 66, "year and a half", "gold", False)])

# ====================================================================== PART 5: the appeal
card("s32_c5", "m5_card", "The Appeal", "September 2022")
stage("s33_q5", "m5_question", {
    "zones": [Z("court")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("device", type="phone", x=960, y=700, at=0.2, scale=1.4), it("letters", x=960, y=220, text="?", at=1.0, size=120, color="gold")],
    "callouts": [co("Should the lenders have known?", 960, 150, C("Should the lenders"), "gold", screen=True, size=44)]})
stage("s34_reverse", "m5_reverse", {
    "zones": [Z("court")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("First, the loan"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=400, y=300, at=0.2, pages=[[0, "SEP 8", "2022"]], scale=0.8),
              it("gavel", x=1000, y=420, hits=[C("reversed the ruling", 0.2)]),
              it("calendar", x=1700, y=320, at=C("First, the loan"), pages=[[0, "DUE", "2023"]], scale=0.8),
              it("letters", x=1700, y=620, text="NOT YET OWED", at=C("not owed that money yet"), size=60, color="risk")],
    "callouts": [co("Sep 8, 2022: the Second Circuit reverses", 960, 960, C("the federal appeals court"), "gold", screen=True, size=40, sub="Torys / Kelley Drye", until=C("First, the loan", -0.3)),
                 co("The loan wasn't due until 2023: no 'value' defense", 960, 960, C("First, the loan"), "white", screen=True, size=36)]},
    sources=["torys", "kelleydrye"])
stage("s35_flags", "m5_flags", {
    "zones": [Z("exchange")], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 0.95}, {"at": C("It could have bought"), "x": 1800, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 4,
    "items": [*[it("sign", x=600 + 520 * k, y=300, text=f"RED FLAG {k + 1}", sub=s, at=C(c), color="#FFCDD2", size=30) for k, (s, c) in enumerate([
                  ("no prepayment notice", "Revlon had not sent the notice"), ("3 years early, while struggling", "A struggling company"),
                  ("debt cost < 30¢ on the market", "It could have bought"), ("a deal to stop early repayment", "And days earlier")])],
              it("device", type="phone", x=1500, y=F, at=C("pick up the phone"), scale=1.2)],
    "callouts": [co("Red flags a careful investor should have checked", 960, 960, C("Second, the court listed"), "white", screen=True, size=36, sub="Kelley Drye", until=C("It could have bought", -0.3)),
                 co("Why repay at 100¢ what you could buy for 30¢?", 960, 960, C("It could have bought"), "gold", screen=True, size=38)]},
    sources=["kelleydrye"])
stage("s36_after", "m5_after", {
    "zones": [Z("vault")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("By then, the industry"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("And Revlon itself"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("vaultdoor", x=900, at=0.2, openAt=0.5, scale=0.7),
              it("coins", **{"from": [2000, 400], "to": [900, 500]}, at=C("The money had to go back"), rate=6, until=C("By then, the industry", 3)),
              it("contract", x=1600, y=430, at=C("By then, the industry"), text="ERRONEOUS-PAYMENT CLAUSE", sub="'paid in error = return it'", scale=0.6),
              it("docs", x=2250, y=560, at=C("And Revlon itself"), text="REVLON", scale=0.6, stamp="CHAPTER 11", stampAt=C("filed for bankruptcy"))],
    "callouts": [co("The money had to go back", 960, 960, C("The money had to go back"), "green", screen=True, size=42, sub="Torys", until=C("By then, the industry", -0.3)),
                 co("New loan clauses: errors must be returned", 960, 960, C("By then, the industry"), "white", screen=True, size=38, until=C("And Revlon itself", -0.3)),
                 co("Revlon later filed for chapter 11", 960, 960, C("And Revlon itself"), "risk", screen=True, size=40, sub="Kelley Drye")]},
    sources=["torys", "kelleydrye"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("office", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("Six eyes are only safe"), "x": 1400, "y": 520, "zoom": 0.95, "dur": 2.6},
            {"at": C("And when money arrives"), "x": 1900, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 2,
    "items": [it("wireform", x=1000, y=470, at=0.2, scale=0.8, checks=[C("Six eyes are only safe", 0.5), C("Six eyes are only safe", 1.0), 0.1], approvals=[C("each pair is really looking"), C("each pair is really looking", 0.4), C("each pair is really looking", 0.8)]),
              it("device", type="phone", x=2000, y=F, at=C("And when money arrives"), scale=1.2),
              it("letters", x=2000, y=200, text="WHY DIDN'T YOU CALL?", at=C("Why didn't you call"), size=56, color="gold")],
    "callouts": [co("Billions still pass through a few people and a screen", 960, 120, C("That the biggest transfers"), "white", screen=True, size=36, until=C("Six eyes are only safe", -0.3)),
                 co("Six eyes only work if every pair looks", 960, 120, C("Six eyes are only safe"), "gold", screen=True, size=40, until=C("And when money arrives", -0.3)),
                 co("Too good to be true? Pick up the phone.", 960, 120, C("And when money arrives"), "risk", screen=True, size=40)]},
    sources=["furman", "kelleydrye"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_citibank_storyboard.py; edit the generator, not this file.\n"
           "# Episode 21 storyboard (Citibank / Revlon): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
