"""Generates projects/how-google-actually-makes-money/deliverables/documentary/storyboard.yaml
(Episode 54: How Google Actually Makes Money).

Bespoke worlds (new in CartoonStage for this episode): `auctionhall` (a daylit auction room with a search screen),
`tollroad` (query-cars through a toll plaza into a search city; coins paid back to the booths), `livingroom` (a family
TV with a skippable ad), `serverfarm` (a daytime data-centre campus with a crane building new halls), `reservoir`
(a dam whose lake is the cash pile). New items: `searchbar`, `barrace`, `jars`, `cashfalls`; person poses `paddle`
(auction bidders) and `sit`; caricature preset `pichai` (only where the narration names him).
Signature animations: the second-price auction with paddles (s08-s10), the toll road paying back (s16), the segment
bar race (s32), Cloud's margin jars (s30), the 2025 vs 2026 cash falls (s39/s41).
No logos or brand marks: the search box, phone, TV and data centres are generic. Lint: tools/lint_storyboard.py.
Run: python tools/gen_alphabet_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-google-actually-makes-money/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
CAM = lambda cue, x1=1250, y1=520, z1=1.0, x0=1000, y0=520, z0=1.0: [{"at": 0, "x": x0, "y": y0, "zoom": z0}, {"at": cue, "x": x1, "y": y1, "zoom": z1, "dur": 1.8}]
HALL = lambda night=False, **kw: {"zones": [Z("auctionhall", night=night, podiumX=0.44, **kw)], "worldW": 2400, **({"night": True} if night else {})}
ROAD = lambda **kw: {"zones": [Z("tollroad", **{"cityX": 0.58, **kw})], "worldW": 2400}
BIDS = [("$2.00", "#4FB3F6", 0), ("$1.50", "#FF8A65", 1), ("$1.20", "#7BD389", 2)]


def bidders(at=0.3, x0=520, gap=260, p2=None, p2at=None, win=None, winat=None, poses=None):
    out = []
    for k, (bid, colr, hair) in enumerate(BIDS):
        kw = {}
        if p2:
            kw.update(paddle2=p2[k], paddle2At=p2at)
        if win is not None and win == k:
            kw.update(winAt=winat)
        if poses:
            kw["poses"] = poses[k]
        out.append(it("person", x=x0 + k * gap, at=(dict(at, offset=at.get("offset", 0) + 0.15 * k) if isinstance(at, dict) else at + 0.15 * k), pose="paddle", paddle=bid, color=colr, hair=hair, skin=k, **kw))
    return out


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.2}, {"at": C("For a setting"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.6},
            {"at": C("That number comes"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=240, at=0.05, prefix="≈ $", suffix=" BILLION", steps=[[0.05, 0], [1.8, 20]], text="GOOGLE → APPLE, 2022 (COURT ESTIMATE)", scale=1.35),
              it("letters", x=700, y=420, text="NOT A FACTORY", at=C("Not for a factory"), until=C("For a setting"), size=52, color="white"),
              it("letters", x=1300, y=420, text="NOT A COMPANY", at=C("Not for a company"), until=C("For a setting"), size=52, color="white"),
              it("letters", x=1000, y=400, text="FOR A SETTING:", at=C("For a setting"), until=C("That number comes"), size=60, color="gold"),
              it("searchbar", x=1000, y=520, w=900, at=C("The search box"), typeAt=C("The search box", 0.6), query="the default search box", scale=0.9, until=C("That number comes")),
              it("docs", x=640, y=700, at=C("That number comes"), text="US v. GOOGLE · D.D.C. 2024", scale=0.7, stamp="FINDING 299", stampAt=C("federal judge's ruling")),
              it("gavel", x=1500, y=640, hits=[C("federal judge's ruling", 0.2)], scale=1.0)]},
    sources=["mehta"])
stage("s02_twist", "h_twist", {
    **HALL(), "cam": [{"at": 0, "x": 1050, "y": 470, "zoom": 1.15}, {"at": C("Last year"), "x": 1150, "y": 520, "zoom": 0.95, "dur": 2.0}], "drift": 2,
    "items": [it("searchbar", x=1056, y=150, w=980, at=0.1, typeAt=0.4, query="running shoes", rows=[{"text": "Shoe shop A · fast delivery", "ad": True, "at": C("behind every search")}, {"text": "Shoe shop B · sale today", "ad": True, "at": C("behind every search", 0.4)}], scale=0.85),
              *bidders(at=C("runs an auction"), x0=380),
              it("person", x=1056, at=C("runs an auction"), pose="talk", tie=True, color="#28407A", skin=2, hair=4),
              it("counter", x=1700, y=520, at=C("took in"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "Alphabet, Google's parent"}, 0], [{"cue": "By our calculation"}, 402.8]], text="ALPHABET REVENUE, 2025 (10-K)", scale=0.85),
              it("sign", x=1700, y=720, text="≈ $1.1BN A DAY (OUR CALC.)", at=C("a day"), color="#FFE0B2", size=30)]},
    sources=["tenk", "mehta"])
stage("s03_question", "h_question", {
    **ROAD(booths=["PHONES", "BROWSERS", "WEBSITES"]), "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.1}, {"at": C("Who gets paid"), "x": 1300, "y": 470, "zoom": 0.95, "dur": 2.2}], "drift": 3,
    "items": [it("letters", x=1000, y=120, text="HOW DOES GOOGLE MAKE MONEY?", at=0.2, size=58, color="gold"),
              it("sign", x=800, y=250, text="WHO GETS PAID?", at=C("Who gets paid"), color="#BBDEFB", size=36),
              it("sign", x=1500, y=250, text="WHERE DOES THE CASH GO?", at=C("And where does"), color="#C8E6C9", size=36)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("serverfarm", buildAt=C("why Google now spends"), buildX=0.5)], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 470, "zoom": 1.0}, {"at": C("why Google now spends"), "x": 1100, "y": 470, "zoom": 0.95, "dur": 2.4}], "drift": 2,
    "items": [it("letters", x=1000, y=90, text="BY THE END OF THIS VIDEO", at=0.05, size=50, color="gold"),
              it("sign", x=560, y=170, text="1 · HOW A CLICK IS PRICED", at=C("how the auction"), color="#BBDEFB", size=30),
              it("sign", x=1000, y=300, text="2 · WHO COLLECTS THE TOLLS", at=C("who collects the tolls"), color="#FFE0B2", size=30),
              it("sign", x=1460, y=170, text="3 · SPENDING MORE THAN IT BRINGS IN", at=C("why Google now spends"), color="#FFCDD2", size=30)]},
    sources=["tenq3"])

# ====================================================================== PART 1: the auction
card("s05_c1", "m1_card", "The Auction", "Behind every search")
stage("s06_map", "m1_map", {
    "zones": [Z("campus")], "worldW": 2400,
    "cam": CAM(C("And the Other Bets"), x1=1150, y1=500, z1=0.95, y0=440, z0=1.05), "drift": 2,
    "items": [it("tower", x=560, h=520, w=260, color="#2E6FD8", text="SERVICES", growAt=C("Google Services")),
              it("sign", x=560, y=170, text="GOOGLE SERVICES · $342.7BN", at=C("Google Services", 0.4), color="#BBDEFB", size=28),
              it("tower", x=1120, h=110, w=220, color="#22A06B", text="CLOUD", growAt=C("Google Cloud")),
              it("sign", x=1120, y=560, text="GOOGLE CLOUD · $58.7BN", at=C("Google Cloud", 0.4), color="#C8E6C9", size=28),
              it("tower", x=1600, h=14, w=160, color="#F2A900", text="BETS", growAt=C("And the Other Bets")),
              it("sign", x=1640, y=640, text="OTHER BETS · $1.5BN", at=C("And the Other Bets", 0.4), color="#FFE0B2", size=28),
              it("letters", x=1100, y=90, text="REVENUE 2025 (10-K)", at=0.2, size=50, color="gold")]},
    sources=["tenk"])
stage("s07_ads", "m1_ads", {
    "zones": [Z("office")], "worldW": 2400, "cam": CAM(C("And the biggest piece"), x1=1100, y1=440, z1=1.05, y0=500, z0=0.95), "drift": 2,
    "items": [it("searchbar", x=1056, y=140, w=960, at=0.1, typeAt=0.3, query="running shoes", scale=0.85,
                 rows=[{"text": "Shoe shop A · fast delivery", "ad": True, "at": C("from the little ads", -0.2), "hi": C("from the little ads", 0.3)},
                       {"text": "Shoe shop B · sale today", "ad": True, "at": C("from the little ads")},
                       {"text": "Ten best running shoes, tested", "at": C("from the little ads", 0.4)}]),
              it("sign", x=420, y=200, text="> 70% OF REVENUE = ADS (10-K)", at=C("More than seventy percent"), color="#FFE0B2", size=28),
              it("counter", x=1700, y=300, at=C("And the biggest piece"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "is Search"}, 0], [{"cue": "More than half"}, 224.5]], text="SEARCH & OTHER, 2025", scale=0.85),
              it("letters", x=1700, y=520, text="≈ 56% OF ALL REVENUE", at=C("More than half"), size=40, color="gold"),
              it("person", x=420, at=0.3, pose="phone", color="#4FB3F6", skin=1, hair=2)]},
    sources=["tenk"])
stage("s08_bids", "m1_bids", {
    **HALL(), "cam": [{"at": 0, "x": 1056, "y": 380, "zoom": 1.15}, {"at": C("Advertisers have already bid"), "x": 980, "y": 520, "zoom": 0.95, "dur": 2.0}], "drift": 2,
    "items": [it("searchbar", x=1056, y=140, w=960, at=0.05, typeAt=C("You type"), query="running shoes", scale=0.85),
              *bidders(at=C("Advertisers have already bid"), x0=360, poses=[[[0, "paddle"]], [[0, "paddle"]], [[0, "paddle"]]]),
              it("person", x=1056, at=C("Google runs an auction"), pose="talk", tie=True, color="#28407A", skin=2, hair=4),
              it("sign", x=1650, y=420, text="ILLUSTRATIVE BIDS, PER CLICK", at=C("Advertisers have already bid", 0.8), color="#FFFFFF", size=24),
              it("sign", x=1650, y=300, text="AUCTION: A FRACTION OF A SECOND", at=C("in a fraction of a second"), color="#BBDEFB", size=28),
              it("letters", x=1056, y=470, text="HIGHEST BID ≠ WINNER", at=C("does not automatically win"), size=56, color="gold")]},
    sources=["mehta"])
stage("s09_quality", "m1_quality", {
    **HALL(), "cam": [{"at": 0, "x": 980, "y": 520, "zoom": 0.95}, {"at": C("So a cheaper ad"), "x": 760, "y": 560, "zoom": 1.1, "dur": 2.0}], "drift": 1,
    "items": [it("letters", x=1056, y=150, text="SCORE = BID × CHANCE OF A CLICK", at=0.3, size=50, color="gold"),
              it("sign", x=1056, y=250, text="CHANCE: A SCORE FROM 0 TO 1 (COURT FINDINGS)", at=C("a score between zero and one"), color="#BBDEFB", size=26),
              *bidders(at=0.0, x0=250, gap=300, p2=["$2.00 × 0.05", "$1.50 × 0.20", "$1.20 × 0.10"], p2at=C("multiplies each bid"), win=1, winat=C("So a cheaper ad")),
              it("person", x=1056, at=0.0, pose="talk", tie=True, color="#28407A", skin=2, hair=4),
              it("sign", x=1056, y=340, text="SCORES 0.10 · 0.30 · 0.12 (ILLUSTRATIVE)", at=C("the predicted chance"), color="#FFFFFF", size=24),
              it("sign", x=660, y=440, text="CHEAPER BID WINS", at=C("can beat an expensive ad"), color="#C8E6C9", size=30)]},
    sources=["mehta"])
stage("s10_second", "m1_second", {
    "zones": [Z("district")], "worldW": 2400, "cam": CAM(C("The winner pays"), x1=1056, y1=430, z1=1.1, y0=520, z0=0.95), "drift": 1,
    "items": [it("searchbar", x=1056, y=140, w=960, at=0.05, typeAt=0.1, query="running shoes", scale=0.85,
                 rows=[{"text": "Winner · bid $1.50", "ad": True, "at": 0.4, "hi": C("The winner pays"), "tag": "PAYS $1.21", "tagAt": C("one cent above")},
                       {"text": "Runner-up · score worth $1.20", "ad": True, "at": 0.8}]),
              it("letters", x=1056, y=560, text="SECOND-PRICE AUCTION", at=C("a classic second-price"), size=54, color="gold"),
              it("sign", x=1056, y=660, text="PAY 1¢ ABOVE THE RUNNER-UP (ILLUSTRATIVE $)", at=C("one cent above"), color="#FFE0B2", size=26),
              it("person", x=360, at=0.2, pose="paddle", paddle="$1.50", color="#FF8A65", hair=1, skin=1, winAt=0.4),
              it("sign", x=1700, y=480, text="COURT FINDINGS, US v. GOOGLE", at=C("the judge wrote"), color="#FFFFFF", size=24)]},
    sources=["mehta"])
stage("s11_knobs", "m1_knobs", {
    **HALL(night=True), "cam": CAM(C("Google's own studies"), x1=1200, y1=500, z1=1.05, x0=900, y0=540), "drift": 2,
    "items": [it("docs", x=640, y=640, at=0.3, text="COURT FINDINGS 243-252", scale=0.7, stamp="PRICING KNOBS", stampAt=C("pricing knobs")),
              it("letters", x=1100, y=130, text="PRICING KNOBS", at=C("pricing knobs"), size=60, color="gold"),
              it("sign", x=1300, y=260, text="'SQUASHING' RAISES WHAT WINNERS PAY", at=C("names like squashing"), color="#FFE0B2", size=28),
              it("sign", x=1300, y=370, text="PRICES UP · ADVERTISERS STAYED", at=C("without losing advertisers"), color="#FFCDD2", size=30),
              it("sign", x=1300, y=470, text="(GOOGLE STUDIES CITED BY THE COURT)", at=C("cited by the court"), color="#FFFFFF", size=22),
              it("person", x=1650, at=C("Google's own studies"), pose="read", tie=True, color="#28407A", skin=0, hair=1)]},
    sources=["mehta"])
stage("s12_volume", "m1_volume", {
    **ROAD(booths=["PHONES", "BROWSERS", "WEBSITES"]), "cam": CAM(C("In the latest quarter"), x1=1250, y1=470, z1=1.0, x0=900, y0=470), "drift": 2,
    "items": [it("letters", x=1000, y=110, text="TWO DIALS", at=0.3, size=60, color="gold"),
              it("counter", x=650, y=280, at=C("How many ads get clicked"), prefix="+", suffix="%", steps=[[0, 0], [{"cue": "Last year, paid clicks"}, 0], [{"cue": "and the average cost"}, 6], [{"cue": "clicks rose eight"}, 8]], text="PAID CLICKS"),
              it("counter", x=1350, y=280, at=C("the price of each click"), prefix="+", suffix="%", steps=[[0, 0], [{"cue": "and the average cost"}, 0], [{"cue": "In the latest quarter"}, 7], [{"cue": "and price four"}, 4]], text="COST PER CLICK"),
              it("sign", x=1000, y=440, text="2025 (10-K)", at=C("Last year"), until=C("In the latest quarter"), color="#FFFFFF", size=28),
              it("sign", x=1000, y=440, text="Q3 2026, YEAR OVER YEAR (10-Q)", at=C("In the latest quarter"), color="#FFE0B2", size=28)]},
    sources=["tenk", "tenq3"])
add("p13_auction", "m1_draw", "engine_draw", {
    "title": "The auction behind a search", "board": BOARD, "draw_start": C("Here is your search"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 380, 240, 120), "color": "ink", "width": 6, "kind": "box", "start": C("Here is your search"), "label": lbl("YOUR SEARCH", 680, 450, 24, "ink")},
        {"d": rect(940, 300, 250, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("Here are the bidders"), "label": lbl("BID A × CHANCE", 1065, 355, 20, "accent2")},
        {"d": rect(940, 420, 250, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("Here are the bidders", 0.4), "label": lbl("BID B × CHANCE", 1065, 475, 20, "accent2")},
        {"d": rect(940, 540, 250, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("Here are the bidders", 0.8), "label": lbl("BID C × CHANCE", 1065, 595, 20, "accent2")},
        {"d": arrow((805, 440), (935, 465)), "color": "muted", "width": 4, "kind": "arrow", "start": C("Each bid is multiplied")},
        {"d": rect(1330, 400, 250, 130), "color": "accent3", "width": 6, "kind": "box", "start": C("The top score wins"), "label": lbl("TOP SCORE WINS", 1455, 470, 22, "accent3")},
        {"d": arrow((1195, 465), (1325, 465)), "color": "accent", "width": 5, "kind": "arrow", "start": C("The top score wins", 0.5)},
        {"d": dot(1455, 600), "color": "accent", "width": 1, "start": C("and pays just enough"), "label": lbl("PAYS ≈ RUNNER-UP + 1¢", 1455, 590, 20, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("and pays just enough", 0.1), "dur": 1.4, "target": [1455, 470]}],
    "scale": 0.86, "floor": 1040}, sources=["mehta"])
kinetic("s14_t1", "m1_transition", [("An auction needs searchers…", 66, "But an auction needs", None, False),
                                    ("…so Google pays tolls", 72, "Google pays tolls", "gold", False)])

# ====================================================================== PART 2: the toll booths
card("s15_c2", "m2_card", "The Toll Booths", "Paying for the searchers")
stage("s16_tac", "m2_tac", {
    **ROAD(booths=["BROWSERS", "PHONE MAKERS", "CARRIERS", "WEBSITES"], plazaX=0.4, payAt=C("Payments to whoever")),
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.0}, {"at": C("Last year they came"), "x": 1200, "y": 450, "zoom": 0.92, "dur": 2.0}], "drift": 3,
    "items": [it("letters", x=1000, y=90, text="TRAFFIC ACQUISITION COSTS", at=0.3, size=54, color="gold"),
              it("counter", x=1750, y=250, at=C("Last year they came"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "About twenty cents"}, 59.9]], text="TAC, 2025 (10-K)", scale=0.85),
              it("sign", x=1750, y=440, text="≈ 20¢ OF EVERY AD $1 (TAC RATE 20.3%)", at=C("About twenty cents"), color="#FFE0B2", size=26)]},
    sources=["tenk"])
stage("s17_apple", "m2_apple", {
    **ROAD(booths=["iPHONE · SAFARI"], plazaX=0.36, plazaLabel="THE BIGGEST TOLL BOOTH", payAt=C("in exchange for being the default")),
    "cam": [{"at": 0, "x": 860, "y": 470, "zoom": 1.15}, {"at": C("In twenty twenty-two"), "x": 1150, "y": 480, "zoom": 0.95, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=860, y=110, text="THE iPHONE TOLL", at=0.05, size=56, color="gold"),
              it("sign", x=1500, y=150, text="A SHARE OF SAFARI SEARCH AD REVENUE", at=C("a share of the ad revenue"), color="#BBDEFB", size=28),
              it("bigcheck", x=1450, y=420, at=C("In twenty twenty-two"), scale=0.7, amount="≈ $20,000,000,000", payee="APPLE", memo="REVENUE SHARE 2022 (COURT ESTIMATE)", date="2022"),
              it("sign", x=1450, y=690, text="> ALL OTHER REVENUE-SHARE PAYMENTS COMBINED", at=C("More than all"), color="#FFE0B2", size=26)]},
    sources=["mehta"])
stage("s18_total", "m2_total", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": CAM(C("The judge ruled"), x1=1250, y1=500, z1=1.05), "drift": 2,
    "items": [it("counter", x=800, y=200, at=0.3, prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in revenue share"}, 26.3]], text="REVENUE SHARE PAID, 2021 (COURT)", scale=1.1),
              it("sign", x=800, y=420, text="APPLE · MOZILLA · ANDROID MAKERS · CARRIERS", at=C("Add Mozilla"), color="#BBDEFB", size=26),
              it("letters", x=1350, y=140, text="'GOOGLE IS A MONOPOLIST'", at=C("Google is a monopolist"), size=52, color="gold"),
              it("sign", x=1500, y=300, text="EXCLUSIVE DEALS HELPED KEEP IT ONE", at=C("these exclusive deals"), color="#FFCDD2", size=28),
              it("gavel", x=1500, y=640, hits=[C("Google is a monopolist", 0.2)], scale=1.0),
              it("person", x=420, at=0.4, pose="clipboard", tie=True, color="#455A64", skin=1, hair=0, poses=[[C("Google is a monopolist"), "shock"], [C("these exclusive deals"), "clipboard"]])]},
    sources=["mehta"])
stage("s19_remedy", "m2_remedy", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": CAM(C("But it did not ban"), x1=1300, y1=500, z1=1.0, x0=950), "drift": 2,
    "items": [it("docs", x=600, y=640, at=0.3, text="REMEDIES DECISION · SEPT 2025", scale=0.7, stamp="NO EXCLUSIVES", stampAt=C("barred exclusive contracts")),
              it("sign", x=1350, y=150, text="✗ NO EXCLUSIVE CONTRACTS", at=C("barred exclusive contracts"), color="#C8E6C9", size=30),
              it("sign", x=1350, y=250, text="SHARE SOME SEARCH DATA WITH RIVALS", at=C("share some search data"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=350, text="✓ PAYMENTS FOR PLACEMENT STILL ALLOWED", at=C("But it did not ban"), color="#FFE0B2", size=28),
              it("sign", x=1350, y=450, text="'CRIPPLING' HARM TO PARTNERS IF CUT", at=C("could cripple"), color="#FFFFFF", size=26),
              it("person", x=980, at=0.4, pose="read", tie=True, color="#455A64", skin=2, hair=1),
              it("person", x=1850, at=C("Both sides have appealed"), pose="clipboard", tie=True, color="#6D4C41", skin=0, hair=4, flip=True),
              it("sign", x=1350, y=550, text="BOTH SIDES APPEALED", at=C("Both sides have appealed"), color="#FFCDD2", size=30)]},
    sources=["remedy", "tenk"])
stage("s20_network", "m2_network", {
    "zones": [Z("web")], "worldW": 2400,
    "cam": CAM(C("That network brought in"), x1=1250, y1=500, z1=1.0), "drift": 2,
    "items": [it("browser", x=600, y=380, at=0.3, page="site", url="recipes-blog.example", typeAt=0.5, scale=0.75),
              it("browser", x=1150, y=330, at=C("other people's websites"), page="site", url="news-site.example", typeAt=C("other people's websites", 0.3), scale=0.6),
              it("coins", **{"from": [800, 300], "to": [600, 760]}, at=C("hands most of that money"), rate=5, until=C("That network brought in", 2.0)),
              it("person", x=560, at=C("hands most of that money"), pose="cheer", color="#FFC93C", skin=3, hair=0),
              it("counter", x=1650, y=250, at=C("That network brought in"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "less than the year before"}, 29.8]], text="GOOGLE NETWORK, 2025 (10-K)", scale=0.85),
              it("sign", x=1650, y=440, text="DOWN $567M FROM 2024", at=C("less than the year before"), color="#FFCDD2", size=30)]},
    sources=["tenk"])
add("p21_toll", "m2_draw", "engine_draw", {
    "title": "Where an ad dollar goes", "board": BOARD, "draw_start": C("Here is an advertiser's dollar"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 470, 230, 150), "color": "ink", "width": 6, "kind": "box", "start": C("Here is an advertiser's dollar"), "label": lbl("ADVERTISER $1", 675, 553, 24, "ink")},
        {"d": arrow((795, 545), (895, 545)), "color": "accent", "width": 5, "kind": "arrow", "start": C("It goes into")},
        {"d": rect(900, 470, 260, 150), "color": "accent2", "width": 6, "kind": "box", "start": C("It goes into", 0.4), "label": lbl("GOOGLE AUCTION", 1030, 553, 24, "accent2")},
        {"d": arrow((1165, 500), (1290, 390)), "color": "risk", "width": 5, "kind": "arrow", "start": C("Out of that box")},
        {"d": rect(1295, 290, 250, 110), "color": "risk", "width": 6, "kind": "box", "start": C("goes to the partners"), "label": lbl("PARTNERS ≈ 20¢", 1420, 353, 22, "risk")},
        {"d": arrow((1165, 590), (1290, 690)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("Google keeps the rest")},
        {"d": rect(1295, 650, 250, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("Google keeps the rest", 0.3), "label": lbl("GOOGLE ≈ 80¢", 1420, 713, 22, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("goes to the partners", 0.3), "dur": 1.4, "target": [1420, 330]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])
kinetic("s22_t2", "m2_transition", [("Search pays the bills…", 70, "Search pays the bills", None, False),
                                    ("…but the second audience is watching", 62, "It is watching", "gold", False)])

# ====================================================================== PART 3: the second screen
card("s23_c3", "m3_card", "The Second Screen", "YouTube and subscriptions")
stage("s24_yt", "m3_yt", {
    "zones": [Z("livingroom", tvX=0.468, adAt=C("before and during videos"), adUntil=C("Those ads brought in", 2.5))], "worldW": 2400,
    "cam": [{"at": 0, "x": 1300, "y": 450, "zoom": 1.1}, {"at": C("Those ads brought in"), "x": 1150, "y": 500, "zoom": 0.95, "dur": 2.0}], "drift": 2,
    "items": [it("person", x=290, y=810, at=0.2, pose="sit", color="#FF8A65", skin=0, hair=3),
              it("person", x=420, y=810, at=0.35, pose="sit", color="#7BD389", skin=2, hair=1, scale=0.75),
              it("counter", x=600, y=200, at=C("Those ads brought in"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "Add subscriptions"}, 40.4]], text="YOUTUBE ADS, 2025 (10-K)", scale=0.85),
              it("sign", x=600, y=380, text="> $60BN WITH SUBSCRIPTIONS (COMPANY)", at=C("Add subscriptions"), color="#FFE0B2", size=26)]},
    sources=["tenk", "q4rel"])
stage("s25_tv", "m3_tv", {
    "zones": [Z("livingroom", tvX=0.468, adAt=C("made up over one-third"), adUntil=C("made up over one-third", 5.0))], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 0.95}, {"at": C("the living room"), "x": 1400, "y": 470, "zoom": 1.12, "dur": 2.2}], "drift": 1,
    "items": [it("person", x=290, y=810, at=0.0, pose="sit", color="#FF8A65", skin=0, hair=3),
              it("person", x=420, y=810, at=0.0, pose="sit", color="#7BD389", skin=2, hair=1, scale=0.75),
              it("person", x=700, at=C("people watching on a television"), pose="carry", box="POPCORN", color="#B39DDB", skin=1, hair=4),
              it("letters", x=1490, y=110, text="> 1/3 OF YOUTUBE AD REVENUE", at=C("made up over one-third"), size=48, color="gold"),
              it("sign", x=1490, y=210, text="WATCHED ON A TV · Q3 2026 (EARNINGS CALL)", at=C("in the quarter"), color="#FFFFFF", size=24)]},
    sources=["call"])
stage("s26_creators", "m3_creators", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": CAM(C("and the annual report"), x1=1000, y1=520, z1=1.05, x0=960, y0=540), "drift": 1,
    "items": [it("person", x=520, at=0.2, pose="camera", color="#F06292", skin=1, hair=3),
              it("person", x=760, at=0.4, pose="mic", color="#4FB3F6", skin=3, hair=0),
              it("coins", **{"from": [1500, 300], "to": [640, 700]}, at=C("It shares money with creators"), rate=5, until=C("and the annual report", 1.0)),
              it("sign", x=1400, y=200, text="SHARES MONEY WITH CREATORS", at=C("It shares money"), color="#C8E6C9", size=28),
              it("sign", x=1400, y=300, text="PAYS MEDIA COMPANIES", at=C("and pays media companies"), color="#BBDEFB", size=28),
              it("docs", x=1400, y=700, at=C("and the annual report"), text="10-K 2025", scale=0.6, stamp="CONTENT COSTS ↑", stampAt=C("a main reason"))]},
    sources=["tenk"])
stage("s27_subs", "m3_subs", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": CAM(C("Together"), x1=1250, y1=500, z1=1.0, x0=900), "drift": 2,
    "items": [it("home", x=420, at=0.2, scale=0.7), it("home", x=900, at=0.35, scale=0.7, color="#E1F5FE"),
              it("clock", x=660, y=260, at=C("Subscriptions, platforms"), period=2.5, scale=0.8, text="RENEWS"),
              it("sign", x=1400, y=130, text="PREMIUM · YOUTUBE TV · SUNDAY TICKET", at=C("YouTube Premium and TV"), color="#BBDEFB", size=24),
              it("sign", x=1400, y=220, text="GOOGLE ONE · PLAY APPS · OWN PHONES", at=C("Google One storage"), color="#C8E6C9", size=24),
              it("counter", x=1400, y=380, at=C("Together"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "last year"}, 48.0]], text="SUBSCRIPTIONS, PLATFORMS & DEVICES, 2025", scale=0.85),
              it("sign", x=1400, y=560, text="> 325M PAID SUBSCRIPTIONS (COMPANY)", at=C("paid subscriptions"), color="#FFE0B2", size=26)]},
    sources=["tenk", "q4rel"])
kinetic("s28_t3", "m3_transition", [("Consumer money…", 72, "Ads and subscriptions", None, False),
                                    ("…and the business that sells to companies", 58, "The fastest-growing business", "gold", False)])

# ====================================================================== PART 4: the cloud turns
card("s29_c4", "m4_card", "The Cloud Turns", "From cost to second engine")
stage("s30_cloud", "m4_cloud", {
    "zones": [Z("serverfarm")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 460, "zoom": 1.05}, {"at": C("In twenty twenty-three"), "x": 1000, "y": 470, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=90, text="GOOGLE CLOUD: RENTING COMPUTERS", at=0.2, until=C("In twenty twenty-three"), size=50, color="gold"),
              it("jars", x=1000, y=780, panel=True, at=C("In twenty twenty-three"), gap=400, title="CLOUD: OPERATING PROFIT PER $1 OF SALES",
                 items=[{"label": "2023", "value": 5.2, "color": "#2E6FD8", "at": C("it kept about five cents"), "display": "≈ 5¢"},
                        {"label": "2025", "value": 23.7, "color": "#2E6FD8", "at": C("In twenty twenty-five"), "display": "≈ 24¢"},
                        {"label": "Q3 2026", "value": 36.2, "color": "#22A06B", "at": C("In the latest quarter"), "display": "≈ 36¢"}],
                 note="OUR CALCULATION FROM ALPHABET'S SEGMENT RESULTS (10-K, Q3 2026 RELEASE)")]},
    sources=["tenk", "q3rel"])
stage("s31_q3", "m4_q3", {
    "zones": [Z("serverfarm", buildAt=0.4, buildX=0.48)], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 470, "zoom": 1.0}, {"at": C("The company says"), "x": 1250, "y": 440, "zoom": 0.92, "dur": 2.2}], "drift": 2,
    "items": [it("counter", x=640, y=180, at=0.3, prefix="$", suffix="BN", decimals=1, steps=[[0, 15.2], [{"cue": "Cloud revenue rose"}, 15.2], [{"cue": "The company says"}, 30.7]], text="CLOUD REVENUE · Q3 2025 → Q3 2026", scale=1.0),
              it("letters", x=640, y=400, text="+103%", at=C("one hundred and three percent"), size=80, color="gold"),
              it("sign", x=1500, y=150, text="TPU SYSTEMS: 'A MEANINGFUL CONTRIBUTOR'", at=C("called TPUs"), color="#C8E6C9", size=26),
              it("van", x=[[0, -200], [9, 1300]], at=C("sales of its own AI chips"), scale=0.6, text="TPU RACKS")]},
    sources=["q3rel"])
stage("s32_race", "m4_race", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("barrace", x=260, y=200, w=1400, rowH=118, at=0.2, max=260, decimals=1, title="REVENUE BY BUSINESS ($BN)",
                 series=[{"key": "s", "label": "SEARCH", "color": "#2E6FD8"}, {"key": "y", "label": "YOUTUBE ADS", "color": "#E5483B"},
                         {"key": "n", "label": "NETWORK", "color": "#8C8FA3"}, {"key": "p", "label": "SUBSCRIPTIONS & DEVICES", "color": "#F2A900"},
                         {"key": "c", "label": "CLOUD", "color": "#22A06B"}],
                 periods=[{"label": "2023", "at": 0.2, "values": {"s": 175.0, "y": 31.5, "n": 31.3, "p": 34.7, "c": 33.1}},
                          {"label": "2024", "at": C("bunched behind it"), "values": {"s": 198.1, "y": 36.1, "n": 30.4, "p": 40.3, "c": 43.2}},
                          {"label": "2025", "at": C("Over the last four"), "values": {"s": 224.5, "y": 40.4, "n": 29.8, "p": 48.0, "c": 58.7}},
                          {"label": "LAST 4 QTRS", "at": C("Cloud reached"), "values": {"s": 250.1, "y": 43.5, "n": 29.6, "p": 53.2, "c": 93.2}}],
                 highlight="c", highlightAt=C("Second only to Search"),
                 note="10-K; quarterly releases. LAST 4 QTRS = Q4 2025 TO Q3 2026, OUR SUM")]},
    sources=["tenk", "q4rel", "q1rel", "q2rel", "q3rel"])
stage("s33_pichai", "m4_pichai", {
    "zones": [Z("campus")], "worldW": 2400,
    "cam": CAM(C("That is the company's"), x1=1150, y1=480, z1=1.05, y0=500, z0=1.0), "drift": 2,
    "items": [it("caricature", x=700, y=820, at=0.2, who="pichai", pose="talk", label="SUNDAR PICHAI · CEO", labelUntil=C("That is the company's", 1.5), scale=1.3),
              it("letters", x=1350, y=140, text="'HALF-TRILLION-DOLLAR RUN RATE'", at=C("half-trillion-dollar"), size=46, color="gold"),
              it("counter", x=1350, y=320, at=C("half-trillion-dollar", 0.5), prefix="≈ $", suffix="BN", steps=[[0, 0], [{"cue": "That is the company's"}, 510]], text="Q3 2026 REVENUE × 4 (OUR CALC.)", scale=0.85),
              it("sign", x=1350, y=500, text="THE COMPANY'S OWN DESCRIPTION", at=C("own description"), color="#FFFFFF", size=26)]},
    sources=["q3rel"])
add("p34_margins", "m4_draw", "engine_draw", {
    "title": "What each business keeps (Q3 2026)", "board": BOARD, "draw_start": C("Google Services keeps"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 700 L 1500 700", "color": "ink", "width": 5, "start": C("Let me draw")},
        {"d": "M 680 700 L 680 454 L 880 454 L 880 700 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Google Services keeps"), "label": lbl("SERVICES ≈ 41¢", 780, 434, 22, "accent2")},
        {"d": "M 950 700 L 950 483 L 1150 483 L 1150 700 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("Cloud, about"), "label": lbl("CLOUD ≈ 36¢", 1050, 463, 22, "accent3")},
        {"d": "M 1220 700 L 1220 820 L 1420 820 L 1420 700 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("And the Other Bets lost"), "label": lbl("OTHER BETS: −$2.0BN ON $372M", 1320, 860, 18, "risk")},
        {"d": dot(1060, 920), "color": "muted", "width": 1, "start": C("of revenue"), "label": lbl("OPERATING PROFIT PER $1 OF SALES · OUR CALC.", 1060, 925, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("And the Other Bets lost", 0.4), "dur": 1.4, "target": [1320, 780]}],
    "scale": 0.86, "floor": 1040}, sources=["q3rel"])
stage("s35_bets", "m4_bets", {
    "zones": [Z("highway")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 500, "zoom": 1.05}, {"at": C("But all the Other Bets"), "x": 1250, "y": 500, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("sedan", x=[[0, -300], [12, 2200]], at=0.1, scale=0.6, color="#ECEFF1", sticker="NO DRIVER"),
              it("counter", x=900, y=180, at=C("Alphabet says"), prefix="", suffix="M+", steps=[[0, 0], [{"cue": "fully autonomous"}, 300]], text="AUTONOMOUS MILES (COMPANY)"),
              it("sign", x=900, y=380, text="15 MAJOR US CITIES (COMPANY)", at=C("major American cities"), color="#BBDEFB", size=28),
              it("counter", x=1600, y=180, at=C("But all the Other Bets"), prefix="−$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "lost seven"}, 7.5]], text="OTHER BETS OPERATING LOSS, 2025 (10-K)")]},
    sources=["call", "tenk"])
kinetic("s36_t4", "m4_transition", [("Enormous profits…", 74, "enormous profits", None, False),
                                    ("…where does the money go?", 70, "Where does that money go", "gold", False)])

# ====================================================================== PART 5: where the cash goes
card("s37_c5", "m5_card", "Where the Cash Goes", "Following the money out")
stage("s38_2025", "m5_2025", {
    "zones": [Z("reservoir", damX=0.55)], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.0}], "drift": 1,
    "items": [it("cashfalls", x=160, y=220, w=1300, h=470, at=0.1, max=180, title="CASH, 2025 ($BN, 10-K)",
                 steps=[{"label": "FROM OPERATIONS", "value": 164.7, "kind": "total", "at": C("Operations brought in"), "display": "$164.7BN", "color": "#2E6FD8"},
                        {"label": "CAPEX", "sub": "data centers, servers", "value": 91.4, "kind": "out", "at": C("went into capital spending"), "display": "−$91.4BN"},
                        {"label": "BUYBACKS", "value": 45.7, "kind": "out", "at": C("bought back shares"), "display": "−$45.7BN", "color": "#F2A900"},
                        {"label": "DIVIDENDS", "value": 10.0, "kind": "out", "at": C("paid dividends"), "display": "−$10.0BN", "color": "#F2A900"}])]},
    sources=["tenk"])
stage("s39_fcf", "m5_fcf", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": CAM(C("roughly three quarters"), x1=1100, y1=500, z1=1.05, x0=1000), "drift": 2,
    "items": [it("letters", x=1000, y=90, text="WHAT IS LEFT?", at=0.05, size=56, color="gold"),
              it("counter", x=760, y=230, at=C("free cash flow"), prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "By our calculation"}, 73.3]], text="FREE CASH FLOW 2025 (OUR CALC.)", scale=1.1),
              it("coins", **{"from": [1300, 360], "to": [520, 780]}, at=C("roughly three quarters"), rate=6),
              *[it("person", x=380 + 120 * k, at=C("went straight back", round(0.15 * k, 2)), pose="cheer", color=["#4FB3F6", "#FF8A65", "#7BD389"][k], skin=k, hair=k + 1, scale=0.8) for k in range(3)],
              it("sign", x=760, y=420, text="≈ 3/4 BACK TO SHAREHOLDERS (OUR CALC.)", at=C("roughly three quarters"), color="#FFE0B2", size=28)]},
    sources=["tenk"])
stage("s40_2026", "m5_2026", {
    "zones": [Z("reservoir", damX=0.55, dryAt=C("More than the"))], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.0}], "drift": 1,
    "items": [it("cashfalls", x=200, y=220, w=900, h=470, at=0.1, max=180, min=-20, title="CASH, JAN–SEP 2026 ($BN, 10-Q)",
                 steps=[{"label": "FROM OPERATIONS", "value": 127.1, "kind": "total", "at": C("In the first nine months"), "display": "$127.1BN", "color": "#2E6FD8"},
                        {"label": "CAPEX", "value": 132.0, "kind": "out", "at": C("on capital expenditure"), "display": "−$132.0BN"},
                        {"label": "BUYBACKS", "value": 0.0, "kind": "out", "at": C("It bought back no shares"), "display": "$0"}]),
              it("letters", x=1500, y=160, text="NO BUYBACKS", at=C("It bought back no shares"), size=60, color="gold"),
              it("sign", x=1500, y=300, text="FULL-YEAR 2026 CAPEX GUIDE: $195–205BN", at=C("For the full year"), color="#FFE0B2", size=26),
              it("sign", x=1500, y=390, text="(Q3 2026 EARNINGS CALL)", at=C("it expects to spend"), color="#FFFFFF", size=22)]},
    sources=["tenq3", "call"])
stage("s41_raise", "m5_raise", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": CAM(C("In nine months"), x1=1060, y1=500, z1=1.0, x0=1060, y0=540, z0=1.05), "drift": 1,
    "items": [it("letters", x=1000, y=110, text="FROM HANDING CASH BACK… TO RAISING IT", at=0.3, size=46, color="gold"),
              it("sign", x=560, y=260, text="+ $42.9BN NEW SHARES", at=C("of new shares"), color="#C8E6C9", size=32),
              it("sign", x=1060, y=260, text="+ $19.0BN PREFERRED", at=C("of preferred stock"), color="#BBDEFB", size=32),
              it("sign", x=1560, y=260, text="+ $85.2BN DEBT ISSUED", at=C("of new debt"), color="#FFE0B2", size=32),
              it("sign", x=1060, y=400, text="JAN–SEP 2026 (10-Q)", at=C("of new debt", 0.5), color="#FFFFFF", size=24)]},
    sources=["tenq3"])
add("p42_cash", "m5_draw", "engine_draw", {
    "title": "Cash in vs data centers", "board": BOARD, "draw_start": C("Twenty twenty-five"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 760 L 1500 760", "color": "ink", "width": 5, "start": C("Let me draw")},
        {"d": "M 640 760 L 640 430 L 800 430 L 800 760 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Cash flows in"), "label": lbl("2025 CASH IN $165BN", 720, 410, 18, "accent2")},
        {"d": "M 830 760 L 830 577 L 990 577 L 990 760 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("data centers take a big share"), "label": lbl("CAPEX $91BN", 910, 557, 18, "risk")},
        {"d": "M 1110 760 L 1110 506 L 1270 506 L 1270 760 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Twenty twenty-six"), "label": lbl("9M 2026 IN $127BN", 1190, 486, 18, "accent2")},
        {"d": "M 1300 760 L 1300 496 L 1460 496 L 1460 760 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("Data centers take more"), "label": lbl("CAPEX $132BN", 1380, 476, 18, "risk")},
        {"d": arrow((1560, 380), (1470, 470)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("new money comes in"), "label": lbl("+ OUTSIDE MONEY", 1600, 360, 18, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("new money comes in", 0.3), "dur": 1.4, "target": [1600, 360]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk", "tenq3"])
kinetic("s43_t5", "m5_transition", [("A giant bet on AI…", 72, "It is a giant bet", None, False),
                                    ("…which brings us to the threat", 66, "Which brings us", "gold", False)])

# ====================================================================== PART 6: the threat
card("s44_c6", "m6_card", "The Threat", "When the answer replaces the links")
stage("s45_ai", "m6_ai", {
    **HALL(night=True), "cam": CAM(C("On the latest call"), x1=1150, y1=520, z1=1.0, x0=1056, y0=440, z0=1.1), "drift": 2,
    "items": [it("searchbar", x=1056, y=140, w=960, at=0.05, typeAt=0.2, query="which running shoes for flat feet?", scale=0.85,
                 rows=[{"text": "AI ANSWER: here are three good options…", "at": C("simply answers your question"), "hi": C("simply answers your question", 0.5)}]),
              *bidders(at=0.2, x0=360, poses=[[[0, "paddle"], [C("there may be no page"), "worry"]], [[0, "paddle"], [C("there may be no page", 0.2), "worry"]], [[0, "paddle"], [C("there may be no page", 0.4), "worry"]]]),
              it("sign", x=1650, y=380, text="'LOWER MONETIZATION' IN AI MODE", at=C("lower monetization"), color="#FFCDD2", size=28),
              it("sign", x=1650, y=480, text="(CHIEF BUSINESS OFFICER, Q3 CALL)", at=C("lower monetization", 0.4), color="#FFFFFF", size=22),
              it("sign", x=1650, y=600, text="NOW: SCALING ADS INSIDE AI ANSWERS", at=C("Google is now scaling"), color="#C8E6C9", size=26)]},
    sources=["call"])
stage("s46_queries", "m6_queries", {
    **ROAD(booths=["PHONES", "BROWSERS", "AI APPS"]), "cam": CAM(C("and Search revenue"), x1=1250, y1=470, z1=0.95, x0=900, y0=480), "drift": 4,
    "items": [it("letters", x=900, y=60, text="SO FAR…", at=0.05, until=C("Google says query growth"), size=56, color="gold"),
              it("sign", x=900, y=140, text="QUERY GROWTH: HIGHEST IN 5 YEARS (COMPANY)", at=C("Google says query growth"), color="#BBDEFB", size=28),
              it("counter", x=1500, y=280, at=C("and Search revenue"), prefix="$", suffix="BN", decimals=1, steps=[[0, 56.6], [{"cue": "in the quarter"}, 56.6], [{"cue": "sixty-three"}, 63.4]], text="SEARCH & OTHER · Q3 2026 (+12%)", scale=0.9)]},
    sources=["q3rel"])
stage("s47_courts", "m6_courts", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": CAM(C("In September"), x1=1250, y1=500, z1=1.0), "drift": 2,
    "items": [it("docs", x=600, y=640, at=0.3, text="AD TECH CASE · E.D. VA.", scale=0.7, stamp="APPEAL PLANNED", stampAt=C("Google plans to appeal")),
              it("sign", x=1350, y=150, text="PUBLISHER TOOLS 'UNFAIRLY EXCLUDED RIVALS' (2025)", at=C("unfairly excluded rivals"), color="#FFCDD2", size=24),
              it("sign", x=1350, y=260, text="SEPT 2026: NO BREAKUP", at=C("declined to order a breakup"), color="#C8E6C9", size=30),
              it("sign", x=1350, y=360, text="CONDUCT REMEDIES INSTEAD", at=C("required changes in conduct"), color="#BBDEFB", size=28),
              it("gavel", x=1650, y=640, hits=[C("declined to order a breakup", 0.3)], scale=0.9)]},
    sources=["tenk", "tenq3"])
add("p48_risk", "m6_draw", "engine_draw", {
    "title": "The old path and the new", "board": BOARD, "draw_start": C("The old path"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 200, 110), "color": "ink", "width": 5, "kind": "box", "start": C("The old path"), "label": lbl("QUESTION", 660, 422, 22, "ink")},
        {"d": arrow((765, 415), (895, 415)), "color": "muted", "width": 4, "kind": "arrow", "start": C("a page of links")},
        {"d": rect(900, 340, 300, 150), "color": "accent2", "width": 5, "kind": "box", "start": C("a page of links", 0.3), "label": lbl("LINKS + ADS ON TOP", 1050, 422, 20, "accent2")},
        {"d": rect(560, 620, 200, 110), "color": "ink", "width": 5, "kind": "box", "start": C("The new path"), "label": lbl("QUESTION", 660, 682, 22, "ink")},
        {"d": arrow((765, 675), (895, 675)), "color": "muted", "width": 4, "kind": "arrow", "start": C("and one AI answer")},
        {"d": rect(900, 600, 300, 150), "color": "accent3", "width": 5, "kind": "box", "start": C("and one AI answer", 0.3), "label": lbl("ONE AI ANSWER", 1050, 682, 22, "accent3")},
        {"d": dot(1380, 680), "color": "risk", "width": 1, "start": C("whether ads fit"), "label": lbl("ADS INSIDE?", 1390, 685, 30, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("whether ads fit", 0.2), "dur": 1.6, "target": [1050, 675]}],
    "scale": 0.86, "floor": 1040}, sources=["call"])

# ====================================================================== PAYOFF
stage("s49_payoff", "payoff", {
    "zones": [Z("auctionhall", x0=-1600, x1=1200, podiumX=0.62), Z("tollroad", x0=1200, x1=3200, booths=["PHONES", "BROWSERS"], payAt=0.5),
              Z("livingroom", x0=3200, x1=5200, tvX=0.55, adAt=C("YouTube adds"), adUntil=C("YouTube adds", 5)), Z("serverfarm", x0=5200, x1=8200, buildAt=C("Cloud has turned"), buildX=0.3)],
    "worldW": 8000,
    "cam": [{"at": 0, "x": 160, "y": 500, "zoom": 1.0}, {"at": C("and paying tolls"), "x": 2200, "y": 480, "zoom": 1.0, "dur": 2.4},
            {"at": C("YouTube adds"), "x": 4200, "y": 480, "zoom": 1.0, "dur": 2.4}, {"at": C("Cloud has turned"), "x": 6300, "y": 470, "zoom": 1.0, "dur": 2.4},
            {"at": C("The lesson"), "x": 6300, "y": 470, "zoom": 0.92, "dur": 1.6}], "drift": 2,
    "items": [it("searchbar", x=120, y=140, w=900, at=0.05, typeAt=0.3, query="how does google make money?", scale=0.85, rows=[{"text": "Your click · sold at auction", "ad": True, "at": C("one click at a time")}]),
              *bidders(at=0.3, x0=-520, gap=200),
              it("sign", x=2200, y=150, text="TOLLS TO WHOEVER OWNS THE BOX", at=C("and paying tolls"), color="#FFE0B2", size=30),
              it("sign", x=4200, y=120, text="A SECOND SCREEN + A STEADY DRIP", at=C("YouTube adds"), color="#BBDEFB", size=30),
              it("letters", x=6300, y=120, text="CLOUD: A SECOND ENGINE", at=C("Cloud has turned"), until=C("The lesson"), size=50, color="gold"),
              it("letters", x=6300, y=120, text="THE REAL PRODUCT: A DEFAULT", at=C("It is a default"), size=56, color="gold"),
              it("sign", x=6300, y=240, text="2026 CAPEX GUIDE > 2× 2025", at=C("more than twice"), color="#FFCDD2", size=32),
              it("searchbar", x=6300, y=380, w=900, at=C("the next default"), typeAt=C("the next default", 0.3), query="ask anything…", scale=0.8)]},
    sources=["tenk", "call"])
add("s50_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_alphabet_storyboard.py; edit the generator, not this file.\n"
           "# Episode 54 storyboard (Alphabet/Google): bespoke worlds per part; tones from visual_direction.yaml.\n")
