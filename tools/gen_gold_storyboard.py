"""Generates projects/americas-trillion-dollar-gold-booked-at-11-billion/deliverables/documentary/storyboard.yaml
(Episode 43, new topics N3: America's $1 Trillion of Gold Is Booked at $11 Billion).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the bullion depository at night (new `depository` set) with a giant counter; the vault with gold bars (new `bars` item).
- Part 1 (the pile): numbers, a location chart, deep storage, the New York vault, the Fed's bank hall.
- Part 2 (the price tag): calendars and price tags in Congress, the depository by day.
- Part 3 (the paper gold): the bank hall, an office with documents, numbers.
- Part 4 (who checks): the depository with inspectors, the vault, a plane under an eclipse sky, Congress.
- Part 5 (rewriting the price): book vs market chart, Congress at night, a printing press, a world comparison chart.
No real seals, no logos, no real people drawn (names in text only). Lint: tools/lint_storyboard.py.
Run: python tools/gen_gold_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/americas-trillion-dollar-gold-booked-at-11-billion/deliverables/documentary/storyboard.yaml"
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


def chart(bars_, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("depository", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1000, y=170, at=0.05, prefix="$", suffix="BN", decimals=2, steps=[[0.05, 0], [1.5, 11.04]], text="U.S. GOLD, OFFICIAL BOOK VALUE (TREASURY, OCT 2026)", scale=1.3)]},
    sources=["fiscal"])
stage("s02_twist", "h_twist", {
    "zones": [Z("vault")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.1}, {"at": 0.8, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 0,
    "items": [it("bars", x=960, y=800, at=0.3, rows=4, scale=1.0),
              it("letters", x=960, y=180, text="AT MARKET PRICE (SEPT 30, 2025)", at=0.3, size=48, color="white"),
              it("counter", x=960, y=330, at=C("the very same gold was worth"), prefix="≈ $", suffix="TN", decimals=1, steps=[[0, 0], [{"cue": "about one trillion"}, 1.0]], text="OUR CALCULATION, TREASURY OIG PRICE", scale=1.2),
              it("letters", x=960, y=520, text="≈ 90× MORE", at=C("Nearly a hundred times"), size=70, color="gold")]},
    sources=["oig"])
stage("s03_question", "h_question", {
    "zones": [Z("depository")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=130, text="WHY A 1973 PRICE?", at=0.3, size=80, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · WHERE IT SITS", at=C("where that gold really sits"), color="#BBDEFB", size=34),
              it("sign", x=750, y=380, text="2 · THE OLD PRICE", at=C("price from the seventies"), color="#FFE0B2", size=34),
              it("sign", x=1170, y=380, text="3 · WHO CHECKS", at=C("who checks"), color="#C8E6C9", size=34),
              it("sign", x=1590, y=380, text="4 · A NEW PRICE?", at=C("rewrote the price"), color="#FFCDD2", size=34),
              it("letters", x=960, y=700, text="THE $11 BILLION TRILLION", at=0.4, size=68, color="gold")]})

# ====================================================================== PART 1: the pile
card("s05_c1", "m1_card", "The Pile", "How much gold, and where")
stage("s06_total", "m1_total", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("counter", x=960, y=270, at=0.3, prefix="", suffix="M OZ", steps=[[0, 0], [{"cue": "of gold"}, 261.5]], decimals=1, text="FINE TROY OUNCES OWNED BY THE U.S. (TREASURY)", scale=1.3),
              it("letters", x=960, y=560, text="≈ 8,100 TONNES (OUR CALCULATION)", at=C("By our calculation"), size=56, color="gold"),
              it("letters", x=960, y=670, text="SAME AMOUNT IN 2010 (GAO)", at=C("in twenty ten"), size=44, color="white")]},
    sources=["fiscal", "gao"])
stage("s07_where", "m1_where", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "FORT KNOX", "value": 56.3, "color": "#E8A200", "at": C("Fort Knox, in Kentucky"), "display": "56%"},
                     {"label": "WEST POINT", "value": 20.7, "color": "#FFC94D", "at": C("West Point"), "display": "21%"},
                     {"label": "DENVER", "value": 16.8, "color": "#FFD97A", "at": C("in Denver"), "display": "17%"},
                     {"label": "NEW YORK FED", "value": 5.1, "color": "#B0BEC5", "at": C("Federal Reserve Bank of New York"), "display": "5%"}],
                    at=0.2, max=65, title="WHERE U.S. GOLD SITS, OCT 2026 (TREASURY; OUR SHARES)", x=360, w=1200)]},
    sources=["fiscal"])
stage("s08_deep", "m1_deep", {
    "zones": [Z("depository")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The gold is not inventory"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=650, y=130, text="DEEP STORAGE", at=0.3, size=70, color="gold"),
              it("sign", x=650, y=260, text="NOT USED FOR COINS (FY2024–25, OIG)", at=C("did not use any"), color="#FFE0B2", size=34),
              it("letters", x=650, y=380, text="A RESERVE, NOT INVENTORY", at=C("The gold is not inventory"), size=44, color="white")]},
    sources=["oig"])
stage("s09_ny", "m1_ny", {
    "zones": [Z("vault")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("bars", x=700, y=820, at=0.3, rows=3, scale=0.8),
              it("letters", x=960, y=150, text="NEW YORK VAULT: ≈ 13.5M OZ", at=0.3, size=54, color="white"),
              it("counter", x=1350, y=380, at=C("that slice alone was worth"), prefix="≈ $", suffix="BN", steps=[[0, 0], [{"cue": "fifty-one billion"}, 51]], text="MARKET VALUE, SEPT 30, 2025 (OIG)"),
              it("letters", x=1350, y=600, text="> 4× ALL U.S. GOLD ON THE BOOKS", at=C("more than four times"), size=36, color="gold")]},
    sources=["oig", "fiscal"])
stage("s10_owner", "m1_owner", {
    "zones": [Z("bankhall", label="THE CENTRAL BANK")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("The owner is the Treasury"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=200, text="WHO OWNS IT?", at=0.3, until=C("does not own gold"), size=64, color="gold"),
              it("letters", x=1000, y=330, text="'THE FEDERAL RESERVE DOES NOT OWN GOLD'", at=C("does not own gold"), size=44, color="risk"),
              it("sign", x=1500, y=470, text="OWNER: THE TREASURY", at=C("The owner is the Treasury"), color="#C8E6C9", size=40)]},
    sources=["h41"])
add("p11_stack", "m1_draw", "engine_draw", {
    "title": "Where the gold sits (Treasury, Oct 2026)", "board": BOARD, "draw_start": C("Here is the whole stack"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1440 860", "color": "ink", "width": 4, "start": C("Let me draw where")},
        {"d": "M 600 860 L 600 400 L 760 400 L 760 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.35, "kind": "bar", "start": C("Fort Knox takes"), "label": lbl("FORT KNOX 56%", 680, 380, 20, "accent")},
        {"d": "M 820 860 L 820 690 L 980 690 L 980 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.25, "kind": "bar", "start": C("Then West Point"), "label": lbl("WEST POINT 21%", 900, 670, 20, "accent")},
        {"d": "M 1040 860 L 1040 720 L 1200 720 L 1200 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.2, "kind": "bar", "start": C("Then Denver"), "label": lbl("DENVER 17%", 1120, 700, 20, "accent")},
        {"d": "M 1260 860 L 1260 818 L 1420 818 L 1420 860", "color": "muted", "width": 5, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("a thin slice in New York"), "label": lbl("NY FED 5%", 1340, 800, 20, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("More than half", 0.1), "dur": 1.4, "target": [680, 500]}],
    "scale": 0.86, "floor": 1040}, sources=["fiscal"])
kinetic("s12_t1", "m1_transition", [("The gold is real, and enormous…", 62, "The gold is real", None, False),
                                    ("…the strange part is the price", 62, "The strange part", "gold", False)])

# ====================================================================== PART 2: the price tag
card("s13_c2", "m2_card", "The Price Tag", "From $20.67 to $42.22")
stage("s14_history", "m2_history", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In nineteen thirty-four"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("calendar", x=600, y=520, at=0.3, pages=[[0, "1900", "$20.67 / OZ"], [{"cue": "In nineteen thirty-four"}, "1934", "$35 / OZ"]], scale=0.8),
              it("letters", x=1300, y=200, text="THE DOLLAR, DEFINED IN GOLD", at=0.3, size=48, color="gold"),
              it("letters", x=1350, y=330, text="DOLLAR CUT TO 59% OF ITS GOLD VALUE (FED HISTORY)", at=C("cut the gold value"), size=30, color="white")]},
    sources=["fedhist"])
stage("s15_law", "m2_law", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And in September"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("pricetag", x=900, y=330, at=C("In March nineteen seventy-two"), text="$38 / OZ (1972)", pages=[[{"cue": "And in September"}, "$42.22 / OZ (1973)", True]], scale=1.0),
              it("letters", x=1000, y=150, text="TWO LAWS, TWO YEARS", at=0.3, size=56, color="gold"),
              it("letters", x=1500, y=470, text="+ START OF THE END OF THE GOLD OWNERSHIP BAN", at=C("The same law also"), size=30, color="white")]},
    sources=["usc"])
stage("s16_frozen", "m2_frozen", {
    "zones": [Z("depository")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Every ounce"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="FROZEN SINCE 1973", at=0.3, size=70, color="risk"),
              it("bars", x=1500, y=840, at=C("Every ounce"), rows=3, scale=0.7, tag="$42.22 / OZ")]},
    sources=["usc", "fiscal"])
add("p17_prices", "m2_draw", "engine_draw", {
    "title": "Official price vs market price (illustration)", "board": BOARD, "draw_start": C("The official price climbs"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1440 860 M 560 860 L 560 330", "color": "ink", "width": 4, "start": C("Let me draw two prices")},
        {"d": "M 580 840 L 700 840 L 700 820 L 820 820 L 820 816 L 900 816 L 900 812 L 1420 812", "color": "accent2", "width": 6, "start": C("The official price climbs"), "label": lbl("OFFICIAL $42.22", 1250, 790, 22, "accent2")},
        {"d": "M 900 812 Q 1000 760 1080 700 Q 1200 600 1300 480 Q 1360 420 1420 360", "color": "accent", "width": 7, "start": C("The market price leaves it"), "label": lbl("MARKET ≈ $3,825 (SEPT 2025)", 1250, 340, 22, "accent")},
        {"d": "M 1400 360 L 1400 812", "color": "risk", "width": 5, "kind": "bar", "start": C("By our calculation"), "label": lbl("≈ 90×", 1460, 600, 30, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("By our calculation", 0.3), "dur": 1.4, "target": [1400, 580]}],
    "scale": 0.86, "floor": 1040}, sources=["usc", "oig"])
kinetic("s18_t2", "m2_transition", [("Why keep such an old number?", 64, "Why would anyone", None, False),
                                    ("…it is tied to real money", 64, "tied to real money", "gold", False)])

# ====================================================================== PART 3: the paper gold
card("s19_c3", "m3_card", "The Paper Gold", "Certificates at the central bank")
stage("s20_1934", "m3_1934", {
    "zones": [Z("bankhall", label="1934")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("In return"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("docs", x=700, y=560, at=0.3, text="GOLD RESERVE ACT (1934)", scale=0.7, stamp="GOLD → TREASURY", stampAt=C("hand all its gold")),
              it("sign", x=1400, y=330, text="GOLD CERTIFICATES (IN DOLLARS)", at=C("In return"), color="#FFE0B2", size=38),
              it("letters", x=1400, y=470, text="NOT SWAPPABLE FOR GOLD", at=C("cannot be swapped"), size=44, color="risk")]},
    sources=["h41", "fedhist"])
stage("s21_how", "m3_how", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But there is a limit"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="THE TRICK", at=0.3, until=C("monetized the gold"), size=70, color="gold"),
              it("letters", x=1000, y=150, text="'MONETIZED THE GOLD' (CRS)", at=C("monetized the gold"), size=54, color="gold"),
              it("sign", x=900, y=300, text="CERTIFICATES → FED", at=C("issuing those certificates"), color="#BBDEFB", size=36),
              it("sign", x=1450, y=300, text="DOLLARS → TREASURY ACCOUNT", at=C("put the money into"), color="#C8E6C9", size=34),
              it("letters", x=1250, y=460, text="LIMIT: THE OFFICIAL VALUE", at=C("But there is a limit"), size=46, color="risk")]},
    sources=["crs"])
stage("s22_numbers", "m3_numbers", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=140, text="THE FED'S WEEKLY BALANCE SHEET (H.4.1)", at=0.3, size=48, color="white"),
              it("counter", x=560, y=380, at=C("a gold stock of"), prefix="$", suffix="BN", decimals=2, steps=[[0, 0], [{"cue": "eleven billion dollars"}, 11.04]], text="GOLD STOCK"),
              it("counter", x=1360, y=380, at=C("gold certificate account"), prefix="$", suffix="BN", decimals=3, steps=[[0, 0], [{"cue": "gold certificate account", "offset": 1.0}, 11.037]], text="GOLD CERTIFICATE ACCOUNT"),
              it("letters", x=960, y=660, text="ALREADY MONEY, AT THE 1973 PRICE", at=C("already been turned into money"), size=50, color="gold")]},
    sources=["h41"])
add("p23_loop", "m3_draw", "engine_draw", {
    "title": "The certificate loop", "board": BOARD, "draw_start": C("Here is the Treasury"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 500, 260, 120), "color": "accent", "width": 6, "kind": "box", "start": C("Here is the Treasury"), "label": lbl("TREASURY + GOLD", 690, 568, 22, "accent")},
        {"d": rect(1180, 500, 260, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the Federal Reserve"), "label": lbl("FEDERAL RESERVE", 1310, 568, 22, "accent2")},
        {"d": arrow((830, 520), (1170, 520), 0.15), "color": "accent", "width": 5, "kind": "arrow", "start": C("sends certificates"), "label": lbl("CERTIFICATES", 1000, 470, 20, "accent")},
        {"d": arrow((1170, 600), (830, 600), 0.15), "color": "accent3", "width": 5, "kind": "arrow", "start": C("sends dollars back"), "label": lbl("DOLLARS", 1000, 680, 20, "accent3")},
        {"d": "M 640 640 L 640 720 L 740 720 L 740 640", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.4, "kind": "bar", "start": C("The gold itself never moves"), "label": lbl("GOLD STAYS", 690, 760, 20, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("Only the paper", 0.1), "dur": 1.4, "target": [1000, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["crs", "h41"])
kinetic("s24_t3", "m3_transition", [("It only works if the gold is there…", 60, "only works if", None, False),
                                    ("…so who checks?", 72, "So who checks", "gold", False)])

# ====================================================================== PART 4: who checks
card("s25_c4", "m4_card", "Who Checks the Vault", "Audits since 1974")
stage("s26_1974", "m4_1974", {
    "zones": [Z("depository")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The next year"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [*crowd([800, 900, 1000, 1100], "walk", at=0.3, scale=0.55),
              it("letters", x=700, y=130, text="1974 AUDIT (GAO)", at=0.3, size=64, color="gold"),
              it("docs", x=500, y=560, at=C("Auditors checked"), text="3 OF 13 COMPARTMENTS", scale=0.65, stamp="NO DIFFERENCES", stampAt=C("found no differences")),
              it("letters", x=700, y=250, text="1975: PERMANENT AUDIT COMMITTEE", at=C("The next year"), size=36, color="white")]},
    sources=["gao"])
stage("s27_today", "m4_today", {
    "zones": [Z("vault")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("bars", x=500, y=820, at=0.3, rows=3, scale=0.7),
              it("letters", x=1200, y=170, text="1986: ≈ 92% AUDITED", at=0.3, size=54, color="gold"),
              it("letters", x=1200, y=280, text="EVERY YEAR SINCE 1995 (OIG)", at=C("since nineteen ninety-five"), size=48, color="white"),
              it("letters", x=1200, y=420, text="42 SEALED COMPARTMENTS", at=C("forty-two"), size=50, color="white"),
              it("letters", x=1200, y=560, text="LATEST: CLEAN OPINION", at=C("clean opinion"), size=48, color="gold")]},
    sources=["gao", "oig"])
stage("s28_visit", "m4_visit", {
    "zones": [Z("depository", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The plane cost"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("plane", x=[[0, 200], [9, 1700]], y=[[0, 380], [9, 180]], at=0.2, text="", tilt=-6, scale=0.6),
              it("letters", x=1000, y=130, text="AUGUST 21, 2017", at=0.3, size=60, color="gold"),
              it("letters", x=1000, y=230, text="SECRETARY MNUCHIN + SENATOR McCONNELL", at=C("Steven Mnuchin"), size=34, color="white"),
              it("sign", x=1450, y=380, text="ECLIPSE? 'NO INDICATION' (OIG)", at=C("found no indication"), color="#FFE0B2", size=34),
              it("letters", x=1450, y=500, text="PLANE ≈ $26,900", at=C("The plane cost"), size=44, color="gold")]},
    sources=["oig"])
stage("s29_bill", "m4_bill", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It is a proposal"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="H.R. 3795 (2025): AUDIT EVERY 5 YEARS", scale=0.7, stamp="PROPOSAL", stampAt=C("It is a proposal")),
              it("letters", x=1300, y=200, text="NOT LAW (AS FAR AS WE COULD CHECK)", at=C("has not become law"), size=40, color="risk")]},
    sources=["bills", "crs"])
add("p30_vault", "m4_draw", "engine_draw", {
    "title": "The vault routine (illustration)", "board": BOARD, "draw_start": C("Forty-two compartments"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 880, 440), "color": "ink", "width": 6, "kind": "box", "start": C("Let me draw the vault"), "label": lbl("42 COMPARTMENTS", 1000, 340, 26, "ink")},
        {"d": " ".join(f"M {560 + k * 126} 360 L {560 + k * 126} 800" for k in range(1, 7)) + " M 560 580 L 1440 580", "color": "muted", "width": 3, "start": C("each one sealed")},
        {"d": " ".join(f"M {610 + k * 126} 470 m -12 0 a 12 12 0 1 0 24 0 a 12 12 0 1 0 -24 0" for k in range(7)), "color": "risk", "width": 4, "start": C("inspectors check the seals"), "label": lbl("SEALS CHECKED YEARLY", 1000, 840, 20, "risk")},
        {"d": "M 1206 600 L 1206 780 L 1300 780 L 1300 600", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.4, "kind": "bar", "start": C("a compartment is opened"), "label": lbl("OPENED + COUNTED", 1253, 640, 16, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("one door at a time", 0.1), "dur": 1.4, "target": [1253, 690]}],
    "scale": 0.86, "floor": 1040}, sources=["gao", "oig"])
kinetic("s31_t4", "m4_transition", [("The most tempting idea of all…", 62, "most tempting idea", None, False),
                                    ("…update the price?", 72, "simply updated the price", "gold", False)])

# ====================================================================== PART 5: rewriting the price
card("s32_c5", "m5_card", "Rewriting the Price", "Proposals, not law")
stage("s33_idea", "m5_idea", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "BOOK VALUE", "value": 11, "color": "#90A4AE", "at": C("would jump from"), "display": "$11BN"},
                     {"label": "AT SEPT 2025 MARKET", "value": 1000, "color": "#E8A200", "at": C("to about one trillion"), "display": "≈ $1,000BN"}],
                    at=0.2, max=1100, title="U.S. GOLD: BOOK VS MARKET (OUR CALCULATION)", x=300, w=800),
              it("letters", x=1520, y=420, text="'MONETIZE' (CRS)", at=C("monetize or demonetize"), size=50, color="gold")]},
    sources=["crs", "oig"])
stage("s34_bitcoin", "m5_bitcoin", {
    "zones": [Z("parliament", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Again, a proposal"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="S. 954 BITCOIN ACT (2025)", scale=0.7, stamp="PROPOSAL", stampAt=C("Again, a proposal")),
              it("letters", x=1300, y=200, text="NEW CERTIFICATES AT FAIR MARKET VALUE", at=C("at fair market value"), size=36, color="gold"),
              it("letters", x=1300, y=310, text="→ HELP FUND A BITCOIN RESERVE", at=C("national bitcoin reserve"), size=40, color="white")]},
    sources=["bills"])
stage("s35_catch", "m5_catch", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Supporters see"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="NOT ONE NEW OUNCE", at=0.3, size=70, color="risk"),
              it("sign", x=900, y=320, text="SUPPORTERS: A HIDDEN ASSET", at=C("Supporters see"), color="#C8E6C9", size=36),
              it("sign", x=1500, y=320, text="CRITICS: PRINTING MONEY", at=C("Critics see"), color="#FFCDD2", size=36)]},
    sources=["crs"])
stage("s36_world", "m5_world", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "UNITED STATES", "value": 8133, "color": "#E8A200", "at": C("By our calculation"), "display": "≈ 8,133t"},
                     {"label": "CHINA", "value": 2387, "color": "#EF5350", "at": C("China holds"), "display": "≈ 2,387t"},
                     {"label": "RUSSIA", "value": 2271, "color": "#90A4AE", "at": C("and Russia"), "display": "2,271t"}],
                    at=0.2, max=9000, dark=True, title="OFFICIAL GOLD, TONNES (WGC/IMF; U.S. OUR CALCULATION)", x=360, w=1200)]},
    sources=["wgc", "fiscal"])
stage("s37_buyers", "m5_buyers", {
    "zones": [Z("bankhall", night=True, label="CENTRAL BANKS")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("America's own total"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=200, text="OTHERS KEEP BUYING", at=0.3, size=60, color="gold"),
              it("counter", x=1000, y=330, at=C("central banks around the world"), prefix="≈ ", suffix="T", steps=[[0, 0], [{"cue": "one hundred and seventy tonnes"}, 170]], text="BOUGHT JAN–AUG 2026 (WGC)"),
              it("letters", x=1000, y=520, text="POLAND: +98 TONNES", at=C("Poland alone"), size=50, color="gold"),
              it("letters", x=1500, y=640, text="U.S.: SAME PILE SINCE 2010", at=C("America's own total"), size=40, color="white")]},
    sources=["wgc", "gao"])
add("p38_sheets", "m5_draw", "engine_draw", {
    "title": "Same gold, two price tags (our calculation)", "board": BOARD, "draw_start": C("On the left, the gold"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1440 860", "color": "ink", "width": 4, "start": C("Let me draw the two balance sheets")},
        {"d": "M 660 860 L 660 845 L 860 845 L 860 860", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.4, "kind": "bar", "start": C("On the left, the gold"), "label": lbl("$42.22 → $11BN", 760, 820, 22, "accent2")},
        {"d": "M 1140 860 L 1140 340 L 1340 340 L 1340 860", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.35, "kind": "bar", "start": C("On the right"), "label": lbl("MARKET → ≈ $1TN", 1240, 320, 22, "accent")},
        {"d": arrow((880, 830), (1120, 420), 0.2), "color": "risk", "width": 5, "kind": "arrow", "start": C("Only the price tag changed"), "label": lbl("SAME BARS", 1000, 560, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("The bars are identical", 0.1), "dur": 1.4, "target": [1000, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["oig", "fiscal"])

# ====================================================================== PAYOFF
stage("s39_payoff", "payoff", {
    "zones": [Z("depository", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("The gold is real"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=130, text="WHY $11 BILLION?", at=0.3, until=C("The gold is real"), size=64, color="gold"),
              it("letters", x=1000, y=130, text="REAL GOLD · OLD PRICE TAG", at=C("The gold is real"), size=58, color="gold"),
              it("letters", x=1000, y=230, text="WHOEVER REWRITES IT CREATES MONEY", at=C("whoever gets to rewrite it"), size=44, color="white")]},
    sources=["fiscal", "crs"])
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_gold_storyboard.py; edit the generator, not this file.\n"
           "# Episode 43 storyboard (U.S. gold reserve): one visual language per part; tones from visual_direction.yaml.\n")
