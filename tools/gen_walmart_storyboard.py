"""Generates projects/how-one-family-still-controls-walmart/deliverables/documentary/storyboard.yaml
(Episode 55: How One Family Still Controls Walmart).

Bespoke worlds (new in CartoonStage for this episode): `fivedime` (a sunny 1950s small-town square with a variety
store, rounded cars, a domed county building; a 1960s discount store rises behind it), `trustroom` (the family vault:
a daylit wood-panelled room, banker's lamps, a giant round vault door opening onto shelves of share bundles that thin
out as the trust sells), `dccity` (a distribution-centre city at midday: warehouses with working docks, a conveyor
bridge, generic semi-trucks, a generic big-box store and car park). New items: `pie` (the 1953 partnership split),
`ballots` (votes flying through the proxy), `sapling` (the 1953 gift growing into a giant tree); caricature presets
`sam` (cap), `rob`, `penner`, `steuart`, `furner` (named public figures only, respectful, name tags).
Signature animations: the 1953 pie split (s08), the gift-to-giant presenter board (p09), the proxy ballots into
Walton Enterprises (s21 + p23), the 4.2-cent coin (s28), the vault shelves thinning as the trust sells (s37).
No logos or brand marks; private individuals never drawn (silhouettes / documents). Lint: tools/lint_storyboard.py.
Run: python tools/gen_walmart_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-one-family-still-controls-walmart/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
CAM = lambda cue, x1=1250, y1=520, z1=1.0, x0=1000, y0=520, z0=1.0: [{"at": 0, "x": x0, "y": y0, "zoom": z0}, {"at": cue, "x": x1, "y": y1, "zoom": z1, "dur": 1.8}]
SQ = lambda **kw: {"zones": [Z("fivedime", **{"storeX": 0.4, **kw})], "worldW": 2400}
VAULT = lambda **kw: {"zones": [Z("trustroom", **{"vaultX": 0.43, **kw})], "worldW": 2400}
DC = lambda **kw: {"zones": [Z("dccity", **{"storeX": 0.66, **kw})], "worldW": 2400}
cari = lambda who, x, at, label=None, **kw: it("caricature", who=who, x=x, at=at, **({"label": label} if label else {}), **kw)
sil = lambda x, at, **kw: it("caricature", who="silhouette", x=x, at=at, **kw)


def chart(bars_, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("dccity", x0=-1200, storeX=0.66)], "worldW": 2400, "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.15}, {"at": C("Amazon passed it"), "x": 1150, "y": 500, "zoom": 1.0, "dur": 1.6},
                    {"at": C("But Walmart still holds"), "x": 1000, "y": 430, "zoom": 1.1, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1100, y=110, text="NO. 1 FOR 13 YEARS…", at=0.05, until=C("Amazon passed it"), size=60, color="gold"),
              it("tower", x=760, h=[[0, 120], [{"cue": "Amazon passed it"}, 520]], w=240, color="#5B6577", text="AMAZON", at=0.3),
              it("tower", x=1180, h=[[0, 120], [{"cue": "Amazon passed it"}, 505]], w=240, color="#1E5AA8", text="WALMART", at=0.3),
              it("sign", x=1000, y=110, text="FORTUNE 500, 2026: AMAZON NO. 1 · WALMART NO. 2", at=C("Amazon passed it", 0.4), until=C("But Walmart still holds"), color="#FFFFFF", size=30),
              it("sign", x=1650, y=300, text="GAP < $4BN (OUR CALC.)", sub="AMAZON 2025 vs WALMART FY ENDED JAN 2026", at=C("by less than"), until=C("But Walmart still holds"), color="#FFE0B2", size=30),
              it("letters", x=1000, y=170, text="…BUT ANOTHER TITLE?", at=C("But Walmart still holds"), size=64, color="gold")]},
    sources=["fortune", "amzn", "tenk"])
stage("s02_twist", "h_twist", {
    **VAULT(openAt=0.2, vaultX=0.51), "cam": [{"at": 0, "x": 1030, "y": 420, "zoom": 1.15}, {"at": C("Walmart is number one"), "x": 960, "y": 470, "zoom": 1.0, "dur": 1.8}], "drift": 0,
    "items": [chart([{"label": "WALMART", "value": 648.13, "color": "#1E5AA8", "at": C("Walmart is number one"), "display": "$648BN"},
                     {"label": "VOLKSWAGEN", "value": 356.71, "color": "#90A4AE", "at": C("Number two"), "display": "$357BN"},
                     {"label": "SCHWARZ", "value": 179.09, "color": "#B0BEC5", "at": C("Number two", 0.8), "display": "$179BN"},
                     {"label": "CARGILL", "value": 177.0, "color": "#B0BEC5", "at": C("Number two", 1.2), "display": "$177BN"}],
                    at=0.1, max=700, title="FAMILY BUSINESSES BY REVENUE (EY / ST. GALLEN 2025)", x=200, y=190, w=900, h=480),
              it("letters", x=1420, y=50, text="NO. 1 FAMILY BUSINESS", at=C("Walmart is number one", 0.3), size=56, color="gold"),
              it("sign", x=1580, y=880, text="≈ 1.8× NO. 2", sub="OUR CALCULATION", at=C("almost twice as big"), color="#FFE0B2", size=34)]},
    sources=["ey"])
stage("s03_question", "h_question", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("So how did the Waltons"), "x": 1100, "y": 470, "zoom": 1.12, "dur": 2.0}], "drift": 3,
    "items": [it("letters", x=1000, y=120, text="ON THE STOCK MARKET SINCE 1970", at=0.2, size=52, color="gold"),
              it("person", x=520, at=C("anyone can buy"), pose="phone", color="#4FB3F6", skin=1, hair=2),
              it("person", x=760, at=C("anyone can buy", 0.3), pose="read", color="#FF8A65", skin=2, hair=1),
              it("person", x=1480, at=C("anyone can buy", 0.6), pose="phone", color="#7BD389", skin=0, hair=3, flip=True),
              it("sign", x=1000, y=280, text="FOUNDERS USUALLY LOSE CONTROL", at=C("Founding families"), color="#FFCDD2", size=34),
              it("letters", x=1100, y=430, text="HOW DID THE WALTONS KEEP IT?", at=C("So how did the Waltons"), size=60, color="gold"),
              it("person", x=1000, at=C("So how did the Waltons", 0.3), pose="shrug", color="#B39DDB", skin=3, hair=4)]},
    sources=["hist"])
stage("s04_promise", "h_promise", {
    **SQ(), "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.08}, {"at": C("how much of Walmart"), "x": 1050, "y": 480, "zoom": 1.0, "dur": 2.2}], "drift": 2,
    "items": [it("letters", x=1000, y=90, text="BY THE END OF THIS VIDEO", at=0.05, size=48, color="gold"),
              it("sign", x=560, y=200, text="1 · THE 1953 MOVE", at=C("nineteen fifty-three move"), color="#FFE0B2", size=32),
              it("sign", x=1000, y=320, text="2 · WHAT THE FAMILY HOLDS", at=C("how much of Walmart"), color="#BBDEFB", size=32),
              it("sign", x=1460, y=200, text="3 · THE CASH THAT FLOWS BACK", at=C("how much cash flows"), color="#C8E6C9", size=32),
              cari("sam", 960, 0.3, "SAM WALTON", pose="wave", labelUntil=C("how much of Walmart"), scale=0.85)]},
    sources=["hist"])

# ====================================================================== PART 1: one store in Bentonville
card("s05_c1", "m1_card", "One Store in Bentonville", "1950-1962")
stage("s06_store", "m1_store", {
    **SQ(), "cam": [{"at": 0, "x": 1700, "y": 380, "zoom": 1.05}, {"at": C("In nineteen fifty"), "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.6},
                    {"at": C("where Sam opened"), "x": 960, "y": 560, "zoom": 1.15, "dur": 2.0}], "drift": 2,
    "items": [it("sign", x=1650, y=260, text="BENTONVILLE, ARKANSAS · 1950", until=C("where Sam opened"), at=0.2, color="#FFF8E1", size=34),
              cari("sam", [[0, 1500], [{"cue": "where Sam opened"}, 1180]], C("Sam Walton and his wife"), "SAM WALTON", pose="talk", scale=0.8),
              it("person", x=[[0, 400], [{"cue": "variety store"}, 760]], at=C("variety store"), pose="walk", color="#F06292", skin=0, hair=3),
              it("person", x=[[0, 300], [{"cue": "variety store", "offset": 0.6}, 640]], at=C("variety store", 0.6), pose="walk", color="#4FB3F6", skin=2, hair=1, scale=0.8),
              it("sign", x=960, y=200, text="WALTON'S 5 & 10 (PER WALMART)", at=C("Walton's five and dime"), color="#FFE0B2", size=30)]},
    sources=["hist"])
stage("s07_estate", "m1_partner", {
    **SQ(night=False), "cam": CAM(C("But Sam was already"), x1=1150, y1=500, z1=1.08, x0=960, y0=540), "drift": 2,
    "items": [it("calendar", text="YEAR", x=520, y=300, at=0.1, pages=[[0.1, "1950"], [{"cue": "Three years later"}, "1953"]], scale=0.9),
              it("sign", x=1550, y=170, text="OLDEST CHILD: 9", at=C("his oldest child"), color="#FFF8E1", size=34),
              cari("sam", 1000, 0.0, pose="memo", scale=0.8, poses=[[0, "memo"], [{"cue": "But Sam was already"}, "worry"]]),
              it("docs", x=1500, y=700, at=C("the estate tax"), text="ESTATE TAX", scale=0.7, stamp="NEXT GENERATION", stampAt=C("passes to the next")),
              it("coins", **{"from": [1500, 500], "to": [1900, 300]}, at=C("the tax the government takes"), rate=3, until=C("passes to the next"))]},
    sources=["bbg"])
stage("s08_split", "m1_split", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("His reasoning"), "x": 1150, "y": 470, "zoom": 1.0, "dur": 1.8}], "drift": 1,
    "items": [it("letters", x=1000, y=100, text="1953: A FAMILY PARTNERSHIP", at=0.2, until=C("His reasoning"), size=54, color="gold"),
              it("pie", x=760, y=500, r=240, at=0.3, total=100, popAt=[4, C("Sam and Helen kept", 0.4)], title="WHO OWNED THE BUSINESS",
                 slices=[{"v": 20, "label": "CHILD 1\n20%", "color": "#1E5AA8", "at": C("each of his four children")},
                         {"v": 20, "label": "CHILD 2\n20%", "color": "#2E9E5B", "at": C("each of his four children", 0.4)},
                         {"v": 20, "label": "CHILD 3\n20%", "color": "#E67E22", "at": C("each of his four children", 0.8)},
                         {"v": 20, "label": "CHILD 4\n20%", "color": "#8E44AD", "at": C("each of his four children", 1.2)},
                         {"v": 20, "label": "SAM &\nHELEN\n20%", "color": "#C0392B", "at": C("Sam and Helen kept")}]),
              it("sign", x=1500, y=230, text="AS REPORTED BY BLOOMBERG (2013)", sub="CITING SAM WALTON'S AUTOBIOGRAPHY", at=C("According to his autobiography"), color="#FFFFFF", size=28),
              it("sign", x=1500, y=470, text="“GIVE YOUR ASSETS AWAY", at=C("The best way"), color="#FFF8E1", size=34),
              it("sign", x=1500, y=580, text="BEFORE THEY APPRECIATE”", at=C("before they appreciate", -0.4), color="#FFF8E1", size=34),
              cari("sam", 1500, C("His reasoning"), pose="talk", scale=0.6)]},
    sources=["bbg"])
add("p09_gift", "m1_draw", "engine_draw", {
    "title": "Why an early gift works (simplified)", "board": BOARD, "draw_start": C("Here is the gift"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(600, 560, 260, 170), "color": "ink", "width": 6, "kind": "box", "start": C("Here is the gift"), "label": lbl("1953 GIFT", 730, 630, 26, "ink")},
        {"d": dot(730, 680), "color": "muted", "width": 1, "start": C("worth very little"), "label": lbl("SMALL VALUE", 730, 690, 22, "muted")},
        {"d": rect(1180, 360, 360, 370), "color": "accent3", "width": 7, "kind": "box", "start": C("And here is the same stake"), "label": lbl("SAME STAKE, TODAY", 1360, 520, 26, "accent3")},
        {"d": dot(1360, 580), "color": "accent3", "width": 1, "start": C("grown into a giant"), "label": lbl("GIANT", 1360, 600, 40, "accent3")},
        {"d": arrow((870, 640), (1170, 560), 0.15), "color": "accent", "width": 7, "kind": "arrow", "start": C("The arrow between them"), "label": lbl("ALL GROWTH", 1010, 520, 24, "accent")},
        {"d": dot(1010, 800), "color": "accent2", "width": 1, "start": C("inside the children's shares"), "label": lbl("→ INSIDE THE CHILDREN'S SHARES", 1010, 800, 24, "accent2")},
        {"d": dot(1010, 850), "color": "risk", "width": 1, "start": C("not inside Sam's estate"), "label": lbl("NOT IN SAM'S ESTATE", 1010, 850, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("The arrow between them", 0.4), "dur": 1.4, "target": [1010, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["bbg"])
stage("s10_rogers", "m1_rogers", {
    **SQ(discount=C("Sam opened the first")), "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("Sam opened the first"), "x": 960, "y": 420, "zoom": 0.92, "dur": 2.4}], "drift": 2,
    "items": [it("calendar", text="YEAR", x=1700, y=230, at=0.1, pages=[[0.1, "1953"], [{"cue": "In nineteen sixty-two"}, "1962"]], scale=0.8),
              it("sign", x=960, y=-40, text="FIRST WALMART · ROGERS, ARKANSAS (1962)", at=C("Rogers, Arkansas"), color="#FFF8E1", size=32),
              it("sapling", x=330, at=0.2, growAt=C("according to Bloomberg"), dur=3.2, scale=0.75, tagSmall="THE 1953 STAKE", tagBig="STILL IN THE PARTNERSHIP", bigAt=C("partnership structure")),
              cari("sam", 1500, 0.2, pose="wave", scale=0.75)]},
    sources=["hist", "bbg"])
kinetic("s11_t1", "m1_transition", [("A chain needs money to grow…", 64, "But a chain", None, False),
                                    ("…and raising it risks control", 64, "puts control at risk", "gold", False)])

# ====================================================================== PART 2: going public
card("s12_c2", "m2_card", "Going Public", "1970-1992")
stage("s13_ipo", "m2_ipo", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": CAM(C("Sam's eldest son"), x1=1250, y1=500, z1=1.05), "drift": 2,
    "items": [it("letters", x=1000, y=100, text="1970: SHARES FOR THE PUBLIC", at=0.2, size=56, color="gold"),
              it("counter", x=760, y=290, at=C("for the first time"), prefix="$", suffix="", decimals=2, steps=[[0, 0], [{"cue": "each. The money"}, 16.5]], text="FIRST SHARES SOLD AT (WALMART)"),
              it("coins", **{"from": [760, 420], "to": [1500, 700]}, at=C("The money financed"), rate=4, until=C("Sam's eldest son")),
              it("sign", x=1500, y=260, text="→ FINANCED A STEADY EXPANSION", at=C("The money financed"), color="#C8E6C9", size=28),
              cari("rob", 1500, C("Sam's eldest son"), "ROB WALTON", traits={"hairColor": "#6B4E33"}, pose="memo", scale=0.75),
              it("sign", x=1250, y=560, text="“MOST OF THE WORK TO TAKE US PUBLIC” – SAM WALTON (VIA WALMART)", at=C("most of the work"), color="#FFF8E1", size=26)]},
    sources=["hist", "proxy24"])
stage("s14_keep", "m2_keep", {
    **VAULT(openAt=C("kept their shares together")), "cam": CAM(C("Walmart has no special"), x1=1150, y1=480, z1=1.05, x0=1030, y0=470, z0=1.12), "drift": 2,
    "items": [it("sign", x=1000, y=90, text="GOING PUBLIC = SELLING A SLICE", at=0.2, until=C("Walmart has no special"), color="#FFFFFF", size=34),
              it("letters", x=1030, y=150, text="ONE FAMILY BLOCK", at=C("one family block"), until=C("Walmart has no special"), size=58, color="gold"),
              it("sign", x=1600, y=200, text="NO SUPER-VOTING SHARES", at=C("Walmart has no special"), color="#FFCDD2", size=32),
              it("sign", x=1600, y=320, text="1 SHARE = 1 VOTE", at=C("Every share gets one vote"), color="#C8E6C9", size=36),
              it("ballots", **{"from": [300, 300], "to": [1000, 420]}, at=C("Every share gets one vote"), rate=5, until=C("in one place"), color="green"),
              it("letters", x=1030, y=120, text="ENOUGH SHARES, ONE PLACE", at=C("The family simply kept"), size=50, color="gold")]},
    sources=["meet", "proxy"])
stage("s15_growth", "m2_growth", {
    **DC(), "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("Under Rob"), "x": 1300, "y": 450, "zoom": 0.95, "dur": 2.2}], "drift": 3,
    "items": [it("calendar", text="YEAR", x=620, y=230, at=0.1, pages=[[0.1, "1970"], [{"cue": "Sam Walton died"}, "1992"], [{"cue": "grew from about"}, "2015"]], scale=0.8),
              cari("rob", 1000, C("Rob became chairman"), "ROB WALTON · CHAIRMAN 1992-2015", pose="talk", scale=0.8),
              it("counter", x=1500, y=220, at=C("Under Rob"), prefix="$", suffix="BN", steps=[[0, 44], [{"cue": "grew from about"}, 44], [{"cue": "to four hundred"}, 482]], text="ANNUAL SALES UNDER ROB (WALMART)"),
              it("sign", x=1500, y=420, text="AS CHAIRMAN, PER 2024 PROXY", at=C("according to Walmart"), color="#FFFFFF", size=26)]},
    sources=["proxy24", "hist"])
stage("s16_estate", "m2_estate", {
    **VAULT(openAt=0.1), "cam": CAM(C("Most of the stake"), x1=1200, y1=480, z1=1.05, x0=1000, y0=480), "drift": 2,
    "items": [it("docs", x=1560, y=760, at=0.2, text="1992", scale=0.7, stamp="NO FIRE SALE", stampAt=C("no fire sale")),
              it("letters", x=1000, y=110, text="NO GIANT SALE TO PAY TAX", at=C("to pay a giant tax bill"), size=52, color="gold"),
              it("calendar", text="YEAR", x=1880, y=300, at=C("Most of the stake"), pages=[[0, "1953"], [{"cue": "for almost forty years"}, "1992"]], scale=0.75),
              it("sign", x=1050, y=240, text="ALREADY THE CHILDREN'S FOR ~39 YEARS", at=C("for almost forty years"), color="#C8E6C9", size=30)]},
    sources=["bbg"])
kinetic("s17_t2", "m2_transition", [("50+ years after going public…", 64, "more than fifty years", None, False),
                                    ("…how much does the family hold?", 68, "how much does the family", "gold", False)])

# ====================================================================== PART 3: the family vault
card("s18_c3", "m3_card", "The Family Vault", "Who holds what today")
stage("s19_two", "m3_two", {
    **VAULT(openAt=0.3), "cam": [{"at": 0, "x": 1030, "y": 430, "zoom": 1.25}, {"at": C("Walton Enterprises, a family"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 2.0}], "drift": 1,
    "items": [it("letters", x=1030, y=90, text="TWO PLACES", at=0.3, size=60, color="gold"),
              it("sign", x=1650, y=220, text="WALTON ENTERPRISES, LLC", sub="≈ 3.00BN SHARES", at=C("Walton Enterprises, a family"), color="#FFE0B2", size=32),
              it("sign", x=1650, y=380, text="AFTER A 3-FOR-1 SPLIT (FEB 2024)", at=C("split in twenty twenty-four"), color="#FFFFFF", size=24),
              it("sign", x=1650, y=520, text="WALTON FAMILY HOLDINGS TRUST", sub="≈ 514M SHARES (APR 2026)", at=C("The Walton Family Holdings Trust"), color="#BBDEFB", size=30)]},
    sources=["proxy", "split"])
stage("s20_pct", "m3_pct", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": CAM(C("At the closing price"), x1=1250, y1=500, z1=1.0, x0=900, y0=500, z0=1.05), "drift": 2,
    "items": [it("shares", x=790, y=430, at=0.1, scale=0.95, groups=[{"n": 38, "color": "#F2B200", "label": "WALTON ENT.", "at": C("Together")},
                                                                    {"n": 6, "color": "#FF8A65", "label": "TRUST", "at": C("Together", 0.8)},
                                                                    {"n": 56, "color": "#90CAF9", "label": "EVERYONE ELSE", "at": C("of the whole company")}]),
              it("counter", x=1500, y=170, at=C("Together"), prefix="", suffix="%", decimals=2, steps=[[0, 0], [{"cue": "of the whole company"}, 44.11]], text="FAMILY ENTITIES' STAKE (PROXY, APR 2026)"),
              it("sign", x=1500, y=400, text="≈ $442BN AT $126.19", sub="NOV 12, 2026 CLOSE · OUR CALCULATION", at=C("they were worth"), color="#C8E6C9", size=32),
              it("sign", x=1500, y=560, text="WALMART ≈ $1.0 TRILLION", sub="OUR CALCULATION", at=C("in a company valued"), color="#FFFFFF", size=30)]},
    sources=["proxy", "price", "tenq"])
stage("s21_proxy", "m3_proxy", {
    **VAULT(), "cam": CAM(C("so one entity"), x1=1100, y1=480, z1=1.08, x0=1000, y0=480), "drift": 2,
    "items": [it("docs", x=420, y=700, at=0.1, text="FAMILY TRUST", scale=0.75, stamp="IRREVOCABLE PROXY", stampAt=C("irrevocable proxy")),
              it("ballots", **{"from": [420, 420], "to": [1620, 380]}, at=C("irrevocable proxy", 0.4), rate=5, arc=220),
              it("sign", x=1620, y=200, text="WALTON ENTERPRISES VOTES IT ALL", at=C("so one entity"), color="#FFE0B2", size=30),
              it("sign", x=1620, y=560, text="DECISIONS: MAJORITY OF MANAGING MEMBERS", at=C("by majority vote"), color="#FFFFFF", size=26)]},
    sources=["proxy", "d13"])
stage("s22_handover", "m3_handover", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": CAM(C("Rob, Jim and Alice"), x1=1200, y1=520, z1=1.0, x0=1000, y0=480, z0=1.08), "drift": 2,
    "items": [it("calendar", text="MONTH", x=420, y=230, at=0.1, pages=[[0.1, "DEC 2024"]], scale=0.8),
              it("letters", x=1100, y=100, text="REWIRED FOR THE NEXT GENERATION", at=C("rewired that machine"), size=48, color="gold"),
              it("sign", x=1100, y=230, text="ROB · JIM · ALICE → 4 FAMILY TRUSTS", at=C("Rob, Jim and Alice"), color="#FFE0B2", size=32),
              *[sil(700 + 150 * k, C("younger family members", 0.15 * k), scale=0.5) for k in range(8)],
              it("sign", x=1225, y=420, text="+8 YOUNGER TRUSTEES (SCHEDULE 13D)", at=C("became trustees"), color="#BBDEFB", size=28)]},
    sources=["d13"])
add("p23_control", "m3_draw", "engine_draw", {
    "title": "One voice", "board": BOARD, "draw_start": C("A box for the family trust"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 380, 280, 150), "color": "accent2", "width": 6, "kind": "box", "start": C("A box for the family trust"), "label": lbl("FAMILY TRUST", 700, 465, 24, "accent2")},
        {"d": rect(560, 660, 280, 150), "color": "accent", "width": 6, "kind": "box", "start": C("A box for Walton Enterprises"), "label": lbl("WALTON ENT.", 700, 745, 24, "accent")},
        {"d": arrow((700, 535), (700, 655)), "color": "accent2", "width": 5, "kind": "arrow", "start": C("An arrow for the proxy"), "label": lbl("PROXY: VOTES", 820, 600, 20, "accent2")},
        {"d": rect(1060, 480, 300, 240), "color": "ink", "width": 7, "kind": "box", "start": C("And Walmart"), "label": lbl("WALMART", 1210, 610, 30, "ink")},
        {"d": arrow((845, 735), (1055, 640), 0.1), "color": "accent", "width": 12, "kind": "arrow", "start": C("one thick arrow"), "label": lbl("≈ 44% OF SHARES", 1000, 850, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("Two entities, one voice", 0.1), "dur": 1.4, "target": [950, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["proxy", "d13"])
stage("s24_turnout", "m3_turnout", {
    "zones": [Z("office", night=False)], "worldW": 2400,
    "cam": CAM(C("By our calculation"), x1=1200, y1=480, z1=1.05, x0=1000, y0=500), "drift": 2,
    "items": [it("sign", x=1000, y=110, text="NOT EVERYONE VOTES", at=C("not everyone votes"), color="#FFCDD2", size=40),
              it("counter", x=700, y=300, at=C("At the twenty twenty-six"), prefix="", suffix="BN", decimals=2, steps=[[0, 0], [{"cue": "shares were represented"}, 7.16]], text="SHARES REPRESENTED, JUNE 2026 (8-K)"),
              it("counter", x=1500, y=300, at=C("By our calculation"), prefix="≈ ", suffix="%", decimals=0, steps=[[0, 0], [{"cue": "of them"}, 49]], text="FAMILY BLOCK'S SHARE (OUR CALC.)", scale=1.1),
              it("person", x=520, at=0.2, pose="type", color="#4FB3F6", skin=1, hair=2),
              it("person", x=1650, at=0.4, pose="read", color="#FF8A65", skin=0, hair=4, flip=True)]},
    sources=["meet", "proxy"])
kinetic("s25_t3", "m3_transition", [("Control is one thing…", 66, "Control is one thing", None, False),
                                    ("…a stake is worth what the business earns", 58, "only worth what", "gold", False)])

# ====================================================================== PART 4: the money machine
card("s26_c4", "m4_card", "The Money Machine", "Fiscal 2026")
stage("s27_scale", "m4_scale", {
    **DC(), "cam": [{"at": 0, "x": 900, "y": 420, "zoom": 1.1}, {"at": C("Walmart had revenue"), "x": 1200, "y": 480, "zoom": 0.92, "dur": 3.0}], "drift": 4,
    "items": [it("sign", x=1000, y=90, text="FISCAL YEAR ENDED JAN 31, 2026 (10-K)", at=0.3, color="#FFFFFF", size=30),
              it("counter", x=700, y=250, at=C("Walmart had revenue"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "stores and clubs"}, 713.2]], text="REVENUE", scale=1.1),
              it("counter", x=1450, y=250, at=C("stores and clubs"), prefix="", suffix="", steps=[[0, 0], [{"cue": "associates"}, 10955]], text="STORES & CLUBS"),
              it("sign", x=1100, y=460, text="≈ 2.1 MILLION ASSOCIATES", at=C("associates"), color="#C8E6C9", size=34)]},
    sources=["tenk"])
stage("s28_margin", "m4_margin", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}, {"at": C("Thin margins"), "x": 960, "y": 520, "zoom": 1.12, "dur": 2.0}], "drift": 1,
    "items": [it("bigcoin", x=620, y=480, at=0.2, metal="silver", value="$1", tag="KEEPS ≈ 4.2¢", spin=True, scale=1.0),
              it("cart", x=[[0, -300], [{"cue": "Thin margins"}, 2300]], at=0.1, load=3, scale=0.8),
              it("coins", **{"from": [620, 480], "to": [1350, 260]}, at=C("Operating income was"), rate=2, until=C("of every dollar")),
              it("counter", x=1350, y=260, at=C("Operating income was"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "of every dollar"}, 29.8]], text="OPERATING INCOME, FY2026"),
              it("letters", x=1350, y=470, text="≈ 4.2¢ PER $1 OF SALES", at=C("of every dollar"), size=50, color="gold"),
              it("sign", x=1350, y=640, text="EVERYDAY LOW PRICES: THIN MARGIN × HUGE VOLUME", at=C("everyday low price"), color="#FFE0B2", size=26)]},
    sources=["tenk"])
stage("s29_supply", "m4_supply", {
    **DC(), "cam": [{"at": 0, "x": 700, "y": 500, "zoom": 1.15}, {"at": C("In the U.S. alone"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 4.0}], "drift": 5,
    "items": [it("counter", x=1100, y=150, at=C("In the U.S. alone"), prefix="", suffix="", steps=[[0, 0], [{"cue": "distribution facilities"}, 192]], text="U.S. DISTRIBUTION FACILITIES (10-K)"),
              it("pallet", x=520, at=0.2, arriveAt=0.3, rows=3, text="CASES", scale=0.7),
              it("sign", x=1700, y=400, text="OWN TRUCK FLEET + OUTSIDE CARRIERS", at=C("private truck fleet"), color="#BBDEFB", size=28)]},
    sources=["tenk"])
add("p30_segments", "m4_draw", "engine_draw", {
    "title": "Net sales by business, fiscal 2026 (10-K)", "board": BOARD, "draw_start": C("Walmart U.S."), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 800 L 1480 800", "color": "ink", "width": 5, "start": C("Let me build")},
        {"d": "M 680 800 L 680 380 L 880 380 L 880 800 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Walmart U.S."), "label": lbl("WALMART U.S. $483.0BN", 780, 360, 20, "accent2")},
        {"d": "M 950 800 L 950 687 L 1150 687 L 1150 800 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("Walmart International"), "label": lbl("INTERNATIONAL $130.4BN", 1050, 667, 20, "accent3")},
        {"d": "M 1220 800 L 1220 719 L 1420 719 L 1420 800 Z", "color": "accent", "width": 3, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("And Sam's Club"), "label": lbl("SAM'S CLUB U.S. $93.0BN", 1320, 699, 20, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("The American stores", 0.1), "dur": 1.4, "target": [780, 480]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])
stage("s31_new", "m4_new", {
    **DC(), "cam": CAM(C("Add membership fees"), x1=1300, y1=480, z1=1.0, x0=1000, y0=500, z0=1.08), "drift": 3,
    "items": [it("letters", x=1000, y=90, text="NEWER, FASTER-GROWING BUSINESSES", at=0.2, until=C("Advertising, sold"), size=48, color="gold"),
              it("counter", x=1000, y=230, at=C("Advertising, sold"), prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "including the TV maker"}, 6.4]], text="ADVERTISING, FY2026 (+46%, INCL. VIZIO)"),
              it("sign", x=1500, y=200, text="LATEST QUARTER: ADS +38% (Q2 FY27)", at=C("In the latest quarter"), color="#C8E6C9", size=28),
              it("sign", x=1500, y=330, text="MEMBERSHIPS: SAM'S CLUB · WALMART+", at=C("Add membership fees"), color="#FFE0B2", size=28),
              it("sign", x=1500, y=460, text="MARKETPLACE FOR OUTSIDE SELLERS", at=C("an online marketplace"), color="#BBDEFB", size=28),
              it("van", x=[[0, 200], [{"cue": "an online marketplace"}, 200], [{"cue": "outside sellers", "offset": 2}, 1200]], at=C("an online marketplace"), text="DELIVERY", scale=0.8)]},
    sources=["q4rel", "q2rel", "tenk"])
stage("s32_cash", "m4_cash", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": CAM(C("of free cash flow"), x1=1100, y1=500, z1=1.03, x0=1000, y0=500, z0=1.06), "drift": 2,
    "items": [chart([{"label": "OPERATING CASH", "value": 41.6, "color": "#2E9E5B", "at": C("Operations brought in"), "display": "$41.6BN"},
                     {"label": "CAPEX", "value": 26.6, "color": "#E67E22", "at": C("Walmart spent"), "display": "−$26.6BN"},
                     {"label": "FREE CASH FLOW", "value": 14.9, "color": "#1E5AA8", "at": C("and still had"), "display": "$14.9BN"}],
                    at=0.1, max=45, title="CASH, FISCAL 2026 (10-K; FREE CASH FLOW IS NON-GAAP)", highlight=2)]},
    sources=["tenk"])
stage("s33_dividend", "m4_dividend", {
    **VAULT(openAt=0.1, vaultX=0.4), "cam": CAM(C("by our calculation"), x1=1180, y1=470, z1=1.05, x0=1000, y0=480, z0=1.0), "drift": 2,
    "items": [it("counter", x=1700, y=160, scale=0.9, at=0.2, prefix="$", suffix=" / SHARE", decimals=2, steps=[[0, 0], [{"cue": "a share"}, 0.99]], text="FISCAL 2027 DIVIDEND (10-Q)"),
              it("sign", x=1720, y=330, text="× ≈ 3.5BN FAMILY-ENTITY SHARES", at=C("Multiply that"), color="#FFE0B2", size=28),
              it("counter", x=1700, y=500, at=C("by our calculation"), prefix="≈ $", suffix="BN / YEAR", decimals=2, steps=[[0, 0], [{"cue": "a year"}, 3.47]], text="OUR CALCULATION, BEFORE TAXES", scale=0.85),
              it("sign", x=1720, y=680, text="≈ $290M A MONTH", at=C("a month"), color="#C8E6C9", size=30),
              it("coins", **{"from": [200, 120], "to": [880, 430]}, at=C("by our calculation"), rate=6)]},
    sources=["tenq", "proxy", "form4"])
stage("s34_buyback", "m4_buyback", {
    "zones": [Z("exchange", night=False)], "worldW": 2400,
    "cam": CAM(C("and every share"), x1=1150, y1=480, z1=1.05, x0=1000, y0=500), "drift": 2,
    "items": [it("counter", x=1500, y=180, at=C("Walmart bought back"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "of its own stock"}, 8.1]], text="BUYBACKS, FISCAL 2026 (10-K)"),
              it("shares", x=780, y=400, at=0.1, scale=0.85, groups=[{"n": 44, "color": "#F2B200", "label": "FAMILY ENTITIES", "at": 0.1}, {"n": 56, "color": "#90CAF9", "label": "OTHERS", "at": 0.3}]),
              it("docs", x=1500, y=760, at=C("every share it retires"), text="RETIRED SHARES", scale=0.6, stamp="CANCELLED", stampAt=C("every share it retires", 0.6)),
              it("letters", x=1500, y=420, text="SAME SHARES → BIGGER SLICE", at=C("a little bigger"), size=46, color="gold")]},
    sources=["tenk"])
kinetic("s35_t4", "m4_transition", [("The machine keeps paying…", 66, "So the machine keeps paying", None, False),
                                    ("…can the family keep the block?", 64, "keep the block together", "gold", False)])

# ====================================================================== PART 5: the next generation
card("s36_c5", "m5_card", "The Next Generation", "Sales, trusts and scrutiny")
stage("s37_sales", "m5_sales", {
    **VAULT(thinAt=C("report sales of"), openAt=0.1), "cam": [{"at": 0, "x": 1030, "y": 430, "zoom": 1.25}, {"at": C("By our tally"), "x": 1150, "y": 480, "zoom": 1.0, "dur": 2.0}], "drift": 1,
    "items": [it("sign", x=1030, y=90, text="DEC 2024 → JUN 2026 (FORMS 4)", at=0.3, color="#FFFFFF", size=30),
              it("counter", x=1650, y=200, at=C("report sales of"), prefix="≈ ", suffix="M SHARES", steps=[[0, 0], [{"cue": "By our tally"}, 69]], text="SOLD BY THE HOLDINGS TRUST"),
              it("sign", x=1650, y=380, text="≈ $7.1BN", sub="OUR TALLY OF REPORTED PRICES", at=C("By our tally"), color="#FFE0B2", size=36),
              it("sign", x=1650, y=540, text="+ ≈ 35M GIVEN TO BENEFICIARIES", at=C("It also handed"), color="#BBDEFB", size=28),
              it("coins", shape="note", **{"from": [1030, 430], "to": [1900, 700]}, at=C("report sales of"), rate=4, until=C("It also handed"))]},
    sources=["form4"])
stage("s38_why", "m5_why", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": CAM(C("The trust went from"), x1=1200, y1=500, z1=1.0, x0=1000, y0=480, z0=1.06), "drift": 2,
    "items": [it("docs", x=650, y=720, at=0.1, text="SCHEDULE 13D", scale=0.7, stamp="STATED PURPOSE", stampAt=C("investment, personal")),
              it("sign", x=650, y=330, text="INVESTMENT · PERSONAL · CHARITABLE", at=C("investment, personal", 0.4), color="#FFF8E1", size=26),
              it("counter", x=1350, y=200, at=0.4, prefix="≈ ", suffix="M", steps=[[0, 604], [{"cue": "shares to about"}, 604], [{"cue": "Walton Enterprises' own"}, 500]], text="HOLDINGS TRUST'S SHARES"),
              it("sign", x=1350, y=430, text="WALTON ENTERPRISES: ≈ 3.00BN, UNCHANGED", at=C("Walton Enterprises' own"), color="#C8E6C9", size=30)]},
    sources=["d13", "form4", "proxy"])
stage("s39_grat", "m5_grat", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": CAM(C("The IRS challenged"), x1=1200, y1=500, z1=1.05, x0=950, y0=480, z0=1.05), "drift": 2,
    "items": [it("sign", x=1000, y=100, text="LEGAL ESTATE-PLANNING TOOLS", at=0.2, color="#FFFFFF", size=34),
              it("sign", x=1000, y=220, text="GRAT = GRANTOR RETAINED ANNUITY TRUST", at=C("grantor retained annuity"), color="#FFE0B2", size=30),
              it("sign", x=1500, y=360, text="1993: ≈ $200M OF STOCK, TWO SHORT GRATs (BLOOMBERG)", at=C("put about"), color="#BBDEFB", size=24),
              it("docs", x=600, y=720, at=C("The IRS challenged"), text="WALTON v. COMM'R · 115 T.C. 589", scale=0.75, stamp="TAX COURT 2000", stampAt=C("Tax Court sided")),
              it("gavel", x=1500, y=640, hits=[C("Tax Court sided", 0.2)], scale=1.0),
              it("letters", x=1300, y=480, text="TAXPAYER WON THE VALUATION", at=C("sided with her"), size=40, color="gold")]},
    sources=["court", "bbg"])
stage("s40_clat", "m5_clat", {
    **VAULT(), "cam": CAM(C("And in twenty twenty-six"), x1=1250, y1=480, z1=1.0, x0=1000, y0=480, z0=1.05), "drift": 2,
    "items": [it("sign", x=1000, y=90, text="CHARITABLE LEAD TRUST", at=0.2, color="#FFE0B2", size=36),
              it("coins", **{"from": [1030, 420], "to": [400, 260]}, at=C("pays a charity"), rate=4, until=C("passes what's left")),
              it("sign", x=400, y=200, text="CHARITY, EVERY YEAR", at=C("pays a charity"), color="#C8E6C9", size=26),
              it("coins", **{"from": [1030, 420], "to": [1700, 260]}, at=C("passes what's left"), rate=4, until=C("Bloomberg reported")),
              it("sign", x=1700, y=200, text="THEN HEIRS", at=C("passes what's left"), color="#BBDEFB", size=26),
              it("counter", x=1100, y=650, at=C("Bloomberg reported"), prefix="> $", suffix="BN", steps=[[0, 0], [{"cue": "into such trusts"}, 9]], text="INTO SUCH TRUSTS SINCE 2003 (BLOOMBERG, 2013)", until=C("And in twenty twenty-six")),
              it("docs", x=1650, y=760, at=C("And in twenty twenty-six"), text="FORM 144 · 2026", scale=0.6, stamp="'2024 WMT GRAT'", stampAt=C("filed notice"))]},
    sources=["bbg", "f144"])
stage("s41_board", "m5_board", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("His son-in-law"), "x": 1100, "y": 520, "zoom": 1.05, "dur": 1.8},
            {"at": C("And the chief executive"), "x": 1350, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 1,
    "items": [cari("rob", [[0, 600], [{"cue": "His son-in-law"}, 600], [{"cue": "His son-in-law", "offset": 2.5}, -300]], 0.1, "ROB WALTON · RETIRED FROM BOARD 2024", pose="wave", scale=0.75, labelUntil=C("His son-in-law")),
              cari("penner", 900, C("Greg Penner"), "GREG PENNER · CHAIRMAN", pose="talk", scale=0.8, labelUntil=C("And the chief executive")),
              cari("steuart", 1200, C("Steuart Walton"), "STEUART WALTON · DIRECTOR", pose="stand", scale=0.8, labelUntil=C("And the chief executive")),
              it("sign", x=1050, y=120, text="2 OF 11 DIRECTORS FROM THE FAMILY (PROXY)", at=C("family members out of"), color="#FFE0B2", size=30),
              cari("furner", 1600, C("And the chief executive"), "JOHN FURNER · CEO SINCE FEB 2026", pose="talk", scale=0.8),
              it("sign", x=1600, y=240, text="STARTED AS AN HOURLY ASSOCIATE (1993)", at=C("hourly associate"), color="#C8E6C9", size=26)]},
    sources=["proxy", "proxy24", "ceo", "d13"])
add("p42_trust", "m5_draw", "engine_draw", {
    "title": "Holdings trust shares (filings)", "board": BOARD, "draw_start": C("December twenty twenty-four"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 800 L 1480 800", "color": "ink", "width": 5, "start": C("Let me chart")},
        {"d": "M 680 800 L 680 440 L 880 440 L 880 800 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("December twenty twenty-four"), "label": lbl("DEC 2024 · 604M", 780, 420, 20, "accent2")},
        {"d": "M 950 800 L 950 490 L 1150 490 L 1150 800 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("March twenty twenty-six"), "label": lbl("MAR 2026 · 521M", 1050, 470, 20, "accent2")},
        {"d": "M 1220 800 L 1220 502 L 1420 502 L 1420 800 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("June, about"), "label": lbl("JUN 2026 · 500M", 1320, 482, 20, "risk")},
        {"d": dot(1050, 860), "color": "muted", "width": 1, "start": C("still huge"), "label": lbl("13D · 13D/A · FORM 4", 1050, 860, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("it isn't frozen", 0.1), "dur": 1.4, "target": [1320, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["d13", "d13a", "form4"])
stage("s43_scrutiny", "m5_scrutiny", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": CAM(C("It got about"), x1=1150, y1=500, z1=1.03, x0=1000, y0=500, z0=1.06), "drift": 2,
    "items": [chart([{"label": "FOR", "value": 0.122, "color": "#2E9E5B", "at": C("votes for"), "display": "0.12BN"},
                     {"label": "AGAINST", "value": 6.39, "color": "#C0392B", "at": C("against", -0.4), "display": "6.39BN"}],
                    at=0.3, max=7, title="2026 PROPOSAL: CUMULATIVE VOTING · VOTES CAST (8-K)", x=420, y=170, w=1100, h=380),
              it("person", x=380, at=0.4, pose="mic", color="#4FB3F6", skin=1, hair=2),
              it("person", x=1650, at=0.6, pose="clipboard", color="#FF8A65", skin=0, hair=4, flip=True),
              it("sign", x=1600, y=420, text="'LIMITS OTHER INVESTORS' SAY'", sub="PROPOSAL TEXT (PROXY 2026)", at=C("concentrated family control"), color="#FFF8E1", size=26),
              it("docs", x=380, y=640, at=C("a shareholder proposal"), text="SHAREHOLDER PROPOSAL", scale=0.55, stamp="REJECTED", stampAt=C("against", 0.2))]},
    sources=["meet", "proxy"])

# ====================================================================== PAYOFF
stage("s44_payoff", "payoff", {
    **SQ(discount=0.0), "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.1}, {"at": C("With timing"), "x": 960, "y": 380, "zoom": 0.9, "dur": 3.0},
                                {"at": C("The test now"), "x": 1100, "y": 420, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("sapling", x=1700, at=0.1, growAt=C("With timing"), dur=4.0, scale=0.6),
              it("letters", x=960, y=110, text="NOT SPECIAL SHARES. TIMING.", at=C("Not with special shares"), until=C("The test now"), size=52, color="gold"),
              it("sign", x=640, y=240, text="GIFT EARLY", at=C("gave the company"), until=C("The test now"), color="#FFE0B2", size=32),
              it("sign", x=1000, y=240, text="ONE BLOCK", at=C("kept the shares in one block"), until=C("The test now"), color="#BBDEFB", size=32),
              it("sign", x=1500, y=240, text="THIN MARGIN × HUGE VOLUME", at=C("thin-margin"), until=C("The test now"), color="#C8E6C9", size=30),
              it("letters", x=1100, y=110, text="WILL THE BLOCK HOLD?", at=C("The test now"), size=60, color="gold"),
              cari("sam", 600, 0.2, pose="wave", scale=0.7)]},
    sources=["bbg", "proxy", "form4"])
add("s45_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_walmart_storyboard.py; edit the generator, not this file.\n"
           "# Episode 55 storyboard (Walmart / Walton family): bespoke worlds fivedime, trustroom, dccity; tones from visual_direction.yaml.\n")
