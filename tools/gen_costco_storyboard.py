"""Generates projects/how-costco-makes-money-selling-things-cheap/deliverables/documentary/storyboard.yaml (Episode 32,
US batch #04: How Costco Makes Money Selling Things Cheap).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: typography + a generic membership card at the door (no real logos or card designs; names in text only).
- Part 1 (the thin margin): the warehouse aisles (new `warehouse` set) + a register and full-screen margin charts.
- Part 2 (the membership machine): members queueing at the door at night, the card, calendars of renewals.
- Part 3 (the short shopping list): a crowded supermarket vs the warehouse racks, a cart of bulk packs (new `cart` item).
- Part 4 (selling before paying): pallets (new `pallet` item) arriving at the loading dock and selling out, a calendar
  of the supplier bill, the balance-sheet chart.
- Part 5 (the loyalty loop): an evidence board of the machine + charts.
Lint: tools/lint_storyboard.py.  Run: python tools/gen_costco_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-costco-makes-money-selling-things-cheap/deliverables/documentary/storyboard.yaml"
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


def chart(bars, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars, at=at, **kw)


def mcard(x=960, y=420, **kw):
    kw.setdefault("color", "#C62828")
    kw.setdefault("text", "MEMBER")
    return it("creditcard", x=x, y=y, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.25}, {"at": 1.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("counter", x=960, y=250, at=0.05, prefix="$", suffix="BN", decimals=1, steps=[[0.05, 0], [1.5, 5.9]], text="COSTCO MEMBERSHIP FEES, ONE YEAR (FY2026, 10-K)", scale=1.6),
              mcard(960, 680, at=0.6, scale=0.85, rot=-6, tapAt=C("just for the right"))]},
    sources=["tenk"])
stage("s02_twist", "h_twist", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "OPERATING PROFIT", "value": 11.7, "color": "#2F6FD1", "at": 0.4, "display": "$11.7bn"},
                     {"label": "MEMBERSHIP FEES", "value": 5.9, "color": "#E89A00", "at": C("the membership fees alone"), "display": "$5.9bn"}],
                    at=0.2, max=13, title="COSTCO, FY2026 (10-K)", x=360, w=860),
              it("letters", x=1550, y=380, text="≈ HALF", at=C("equal about half"), size=96, color="risk"),
              it("letters", x=1550, y=500, text="(our calculation)", at=C("equal about half", 0.4), size=34, color="white")]},
    sources=["tenk"])
stage("s03_question", "h_question", {
    "zones": [Z("warehouse")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 0.8, "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("cart", x=[[0, 500], [8, 1500]], at=0.1, scale=0.9, load=3),
              it("letters", x=1100, y=150, text="SELLING ALMOST AT COST?", at=0.4, size=76, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THIN MARGIN", at=0.3, color="#BBDEFB", size=42),
              it("sign", x=750, y=380, text="2 · THE CARD", at=C("the membership"), color="#FFCDD2", size=42),
              it("sign", x=1170, y=380, text="3 · SHORT LIST", at=C("the short shopping list"), color="#FFE0B2", size=42),
              it("sign", x=1590, y=380, text="4 · PAY LATER", at=C("before it pays"), color="#C8E6C9", size=42),
              it("letters", x=960, y=700, text="THE COSTCO MACHINE", at=C("the four parts"), size=70, color="gold")]})

# ====================================================================== PART 1: the thin margin (warehouse + register + charts)
card("s05_c1", "m1_card", "The Thin Margin", "Almost three hundred billion in sales")
stage("s06_sales", "m1_sales", {
    "zones": [Z("warehouse")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It runs"), "x": 1400, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("counter", x=1000, y=230, at=0.3, prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "worth of goods", "offset": 0}, 297.2]], text="NET SALES, FY2026 (COSTCO)", scale=1.2),
              it("cart", x=[[0, 300], [14, 2200]], at=0.3, scale=0.7, load=2),
              it("letters", x=1650, y=230, text="+10.1% IN A YEAR", at=C("up ten point one percent"), size=52, color="green"),
              it("letters", x=1650, y=320, text="939 WAREHOUSES · 647 IN THE U.S.", at=C("It runs"), size=40, color="gold")]},
    sources=["results", "tenk"])
stage("s07_margin", "m1_margin", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=480, text="WHAT IT KEEPS", at=0.3, until=C("gross margin was about"), size=90, color="gold"),
              chart([{"label": "GROSS MARGIN", "value": 11.09, "color": "#E89A00", "at": C("gross margin was about"), "display": "11.1%"},
                     {"label": "AVG MARKUP OVER COST", "value": 12.5, "color": "#2F6FD1", "at": C("by our calculation"), "display": "≈12.5%", "sub": "our calculation"}],
                    at=0.2, max=15, title="COSTCO, FY2026 (10-K)", x=520, w=880),
              it("letters", x=960, y=990, text="\"SIGNIFICANTLY LOWER\" THAN MOST RETAILERS", at=C("Costco itself says"), size=40, color="risk")]},
    sources=["tenk"])
stage("s08_costs", "m1_costs", {
    "zones": [Z("warehouse", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Its net income"), "x": 1300, "y": 520, "zoom": 1.05, "dur": 1.5}], "drift": 2,
    "items": [it("terminal", x=700, y=F, at=0.2, text="$100.00", scale=0.85),
              it("sign", x=950, y=200, text="STORES · STAFF · TRUCKS · POWER", at=C("The warehouses"), color="#FFE0B2", size=34),
              it("counter", x=1450, y=260, at=C("by our calculation"), prefix="", suffix="¢", decimals=0, steps=[[0, 0], [{"cue": "less than four cents", "offset": 0}, 4]], text="OPERATING PROFIT PER $1 OF REVENUE (< 4¢, OUR CALCULATION)"),
              it("letters", x=1500, y=470, text="NET INCOME $9.2BN", at=C("Its net income"), size=54, color="gold")]},
    sources=["tenk"])
add("p09_hundred", "m1_draw", "engine_draw", {
    "title": "Where $100 at the register goes", "board": BOARD, "draw_start": C("Let me draw where"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("Let me draw where")},
        {"d": "M 640 860 L 640 380 L 820 380 L 820 860", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.25, "kind": "bar", "start": C("About eighty-nine dollars"), "label": lbl("SUPPLIER ≈ $89", 730, 360, 24, "accent2")},
        {"d": "M 940 860 L 940 800 L 1120 800 L 1120 860", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.25, "kind": "bar", "start": C("About eleven dollars is left"), "label": lbl("LEFT ≈ $11", 1030, 780, 24, "accent")},
        {"d": "M 1240 860 L 1240 835 L 1420 835 L 1420 860", "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("tiny sliver"), "label": lbl("PROFIT: A SLIVER", 1330, 810, 22, "risk")},
        {"d": arrow((1030, 760), (1300, 600), -0.2), "color": "ink", "width": 4, "start": C("Most of that pays"), "label": lbl("stores + staff", 1220, 590, 22, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("tiny sliver", 0.3), "dur": 1.4, "target": [1330, 840]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])
kinetic("s10_t1", "m1_transition", [("The goods barely make money", 58, "If the goods", None, True), ("…it starts at the door", 64, "It starts at the door", "gold", False)])

# ====================================================================== PART 2: the membership machine (night door queue + card)
card("s11_c2", "m2_card", "The Membership Machine", "A card you pay for every year")
stage("s12_members", "m2_members", {
    "zones": [Z("district", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("cardholders"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [*crowd([500 + 90 * k for k in range(9)], "walk", at=0.2, scale=0.55),
              mcard(1700, 480, at=0.3, scale=0.6, rot=6),
              it("counter", x=1000, y=200, at=0.4, prefix="", suffix="M", decimals=1, steps=[[0, 0], [{"cue": "paid members", "offset": 0}, 84.1]], text="PAID MEMBERS (FY2026, 10-K)"),
              it("letters", x=1500, y=330, text="150M+ CARDHOLDERS", at=C("cardholders"), size=50, color="gold")]},
    sources=["tenk"])
stage("s13_price", "m2_price", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Costco says the higher fee"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("calendar", x=650, y=320, at=0.2, pages=[[0, "SEP 1", "2024"]], scale=0.8),
              it("pricetag", x=1050, y=300, at=0.3, text="$60", pages=[[{"cue": "to sixty-five"}, "$65", True]], scale=1.0),
              it("pricetag", x=1450, y=300, at=C("The Executive membership"), text="$120", pages=[[{"cue": "to one hundred and thirty"}, "$130", True]], scale=1.0),
              it("letters", x=1250, y=620, text="≈ 30% OF 2026 FEE GROWTH CAME FROM THE PRICE RISE", at=C("Costco says the higher fee"), size=34, color="white")]},
    sources=["fee", "tenk"])
stage("s14_renew", "m2_renew", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "U.S. & CANADA", "value": 92.3, "color": "#23995A", "at": 0.5, "display": "92.3%"},
                     {"label": "WORLDWIDE", "value": 89.8, "color": "#4FC3F7", "at": C("Worldwide"), "display": "89.8%"}],
                    at=0.2, max=100, dark=True, title="MEMBERS WHO RENEW (COSTCO 10-K, FY2026)", x=420, w=860),
              it("letters", x=1560, y=420, text="9 IN 10", at=C("More than nine in ten"), size=90, color="gold"),
              it("letters", x=1560, y=530, text="PAY AGAIN", at=C("sign up again"), size=50, color="white")]},
    sources=["tenk"])
stage("s15_fees", "m2_fees", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But they arrive"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [mcard(650, 430, at=0.2, scale=0.55, rot=-8),
              it("coins", **{"from": [800, 430], "to": [1650, 330]}, at=0.6, rate=7),
              it("piggy", x=1700, y=520, at=0.3, scale=1.0),
              it("counter", x=1250, y=170, at=C("and you get"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in a single year", "offset": 0}, 5.9]], text="MEMBERSHIP FEES, FY2026"),
              it("letters", x=1250, y=640, text="NOT PURE PROFIT · ≈ HALF OF OPERATING PROFIT", at=C("Fees have their own costs"), size=34, color="gold")]},
    sources=["tenk"])
add("p16_halves", "m2_draw", "engine_draw", {
    "title": "Store + club", "board": BOARD, "draw_start": C("On one side, the store"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 400, 280, 140), "color": "accent2", "width": 6, "kind": "box", "start": C("On one side, the store"), "label": lbl("STORE · THIN MARGIN", 700, 478, 22, "accent2")},
        {"d": rect(1160, 400, 280, 140), "color": "accent", "width": 6, "kind": "box", "start": C("the club, collecting fees"), "label": lbl("CLUB · YEARLY FEES", 1300, 478, 22, "accent")},
        {"d": arrow((850, 440), (1150, 440), -0.2), "color": "accent3", "width": 5, "start": C("The low prices bring members in"), "label": lbl("low prices → members", 1000, 380, 20, "accent3")},
        {"d": arrow((1150, 520), (850, 520), -0.2), "color": "risk", "width": 5, "start": C("The fees pay for the low prices"), "label": lbl("fees → low prices", 1000, 600, 20, "risk")},
        {"d": "M 900 700 A 100 60 0 1 0 1100 700 A 100 60 0 1 0 900 700", "color": "ink", "width": 4, "start": C("they keep coming back"), "label": lbl("COME BACK", 1000, 790, 22, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("The fees pay for the low prices", 0.3), "dur": 1.4, "target": [1000, 520]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])
kinetic("s17_t2", "m2_transition", [("Low prices need more than fees", 56, "But low prices", None, True), ("…what Costco refuses to sell", 60, "refuses to sell", "gold", False)])

# ====================================================================== PART 3: the short shopping list (supermarket vs warehouse)
card("s18_c3", "m3_card", "The Short Shopping List", "Fewer products, giant volumes")
stage("s19_skus", "m3_skus", {
    "zones": [Z("shop", label="SUPERMARKET")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Instead of twenty brands"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("counter", x=800, y=200, at=0.3, prefix="< ", suffix="", steps=[[0, 0], [{"cue": "active products per warehouse", "offset": 0}, 4000]], text="ACTIVE PRODUCTS PER WAREHOUSE (COSTCO 10-K)", scale=1.1),
              *[it("pricetag", x=620 + 150 * k, y=450, at=C("Instead of twenty brands", 0.1 * k), text="SAUCE", scale=0.5) for k in range(7)],
              it("cart", x=1700, at=C("you might find two"), scale=0.6, load=2, text="2 BRANDS")]},
    sources=["tenk"])
stage("s20_world", "m3_world", {
    "zones": [Z("warehouse")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 460, "zoom": 1.15}, {"at": 2.5, "x": 1300, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("pallet", x=900, at=0.2, rows=3, scale=0.8),
              it("pallet", x=1300, at=0.4, rows=2, scale=0.8, color="#90CAF9"),
              it("letters", x=1300, y=170, text="CONCRETE · STEEL · PALLETS", at=C("Concrete floors"), size=52, color="gold"),
              it("letters", x=1300, y=270, text="NO DECORATION", at=C("no decoration"), size=44, color="risk")]},
    sources=["tenk"])
stage("s21_volume", "m3_volume", {
    "zones": [Z("port")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("enormous bargaining power"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("pallet", x=700, at=0.2, rows=3, scale=0.7, arriveAt=0.3),
              it("pallet", x=1050, at=0.2, rows=3, scale=0.7, arriveAt=1.0, color="#A5D6A7"),
              it("pallet", x=1400, at=0.2, rows=3, scale=0.7, arriveAt=1.7, color="#EF9A9A"),
              it("letters", x=1150, y=330, text="939 WAREHOUSES · SAME SHORT LIST", at=C("warehouses around the world"), size=44, color="white"),
              it("letters", x=1450, y=430, text="BARGAINING POWER", at=C("enormous bargaining power"), size=56, color="gold")]},
    sources=["tenk"])
stage("s22_kirkland", "m3_kirkland", {
    "zones": [Z("warehouse", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And according to its annual report"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("pallet", x=750, at=0.2, rows=3, scale=0.8, color="#ECEFF1", text="STORE BRAND", textSize=32),
              it("counter", x=1350, y=220, at=C("Kirkland brings in"), prefix="≈ $", suffix="BN", steps=[[0, 0], [{"cue": "a year worldwide", "offset": 0}, 90]], text="KIRKLAND SIGNATURE, ANNUAL REVENUE (COSTCO LETTER, 2025)"),
              it("letters", x=1400, y=420, text="15–20% CHEAPER THAN NATIONAL BRANDS", at=C("fifteen to twenty percent"), size=38, color="green"),
              it("letters", x=1400, y=510, text="HIGHER MARGINS FOR COSTCO", at=C("generally earn Costco higher"), size=44, color="gold")]},
    sources=["ars", "tenk"])
add("p23_list", "m3_draw", "engine_draw", {
    "title": "Long list vs short list (illustration)", "board": BOARD, "draw_start": C("Here is a typical supermarket"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 960 860 M 1060 860 L 1460 860", "color": "ink", "width": 4, "start": C("Here is a typical supermarket")},
        {"d": " ".join(f"M {580 + 30 * k} 860 L {580 + 30 * k} {800 - 15 * (k % 3)} L {600 + 30 * k} {800 - 15 * (k % 3)} L {600 + 30 * k} 860" for k in range(13)), "color": "accent2", "width": 4, "fill": "accent2", "fillOpacity": 0.2, "kind": "bar", "start": C("each selling a little"), "label": lbl("MANY ITEMS, SMALL SALES", 760, 740, 20, "accent2")},
        {"d": " ".join(f"M {1100 + 110 * k} 860 L {1100 + 110 * k} {480 + 40 * k} L {1180 + 110 * k} {480 + 40 * k} L {1180 + 110 * k} 860" for k in range(3)), "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is Costco"), "label": lbl("FEW ITEMS, HUGE SALES", 1260, 450, 22, "accent")},
        {"d": arrow((1260, 400), (1260, 330), 0.0), "color": "risk", "width": 5, "start": C("squeeze the price"), "label": lbl("SQUEEZE THE PRICE", 1260, 310, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("far fewer items", 0.2), "dur": 1.4, "target": [1260, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])
kinetic("s24_t3", "m3_transition", [("Speed unlocks the hidden part", 56, "And the speed", None, True), ("Paid before it pays", 74, "Costco often gets", "gold", False)])

# ====================================================================== PART 4: selling before paying (loading dock + calendar + balance chart)
card("s25_c4", "m4_card", "Selling Before Paying", "Using the suppliers' money")
stage("s26_quote", "m4_quote", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Read that again"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("docs", x=650, y=560, at=0.2, text="COSTCO 10-K", scale=0.7, stamp="IN ITS OWN WORDS", stampAt=C("Read that again")),
              it("letters", x=1300, y=150, text="\"WE OFTEN SELL INVENTORY", at=0.4, size=46, color="white"),
              it("letters", x=1300, y=230, text="BEFORE WE ARE REQUIRED TO PAY FOR IT\"", at=0.9, size=46, color="white"),
              it("letters", x=1300, y=330, text="+ EARLY-PAYMENT DISCOUNTS", at=C("while taking advantage"), size=40, color="gold")]},
    sources=["tenk"])
stage("s27_balance", "m4_balance", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "GOODS ON THE SHELVES", "value": 19.3, "color": "#2F6FD1", "at": 0.5, "display": "$19.3bn", "sub": "merchandise inventories"},
                     {"label": "OWED TO SUPPLIERS", "value": 22.6, "color": "#E53935", "at": C("it owed its suppliers"), "display": "$22.6bn", "sub": "accounts payable"}],
                    at=0.2, max=25, title="COSTCO BALANCE SHEET, AUG 30, 2026 (10-K)", x=520, w=880),
              it("letters", x=960, y=990, text="OWES MORE THAN IT HOLDS", at=C("It owed more than"), size=48, color="risk")]},
    sources=["tenk"])
stage("s28_turns", "m4_turns", {
    "zones": [Z("warehouse")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A slower store"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("pallet", x=800, at=0.2, rows=3, scale=0.8, arriveAt=0.3, goneAt=C("sells through"), goneDur=6),
              it("counter", x=1450, y=230, at=C("By our calculation"), prefix="≈ ", suffix="×", steps=[[0, 0], [{"cue": "fourteen times", "offset": 0}, 14]], text="INVENTORY TURNS A YEAR (OUR CALCULATION)"),
              it("calendar", x=1150, y=560, at=C("A typical item sits"), pages=[[0, "< 1", "MONTH"]], scale=0.7),
              it("letters", x=1700, y=440, text="CASH FIRST, BILL LATER", at=C("often arrives first"), size=44, color="gold")]},
    sources=["tenk"])
add("p29_cycle", "m4_draw", "engine_draw", {
    "title": "The cash cycle (illustration)", "board": BOARD, "draw_start": C("Day zero"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 640 L 1460 640", "color": "ink", "width": 5, "start": C("Let me draw the cash cycle"), "label": lbl("TIME →", 1420, 690, 22, "ink")},
        {"d": rect(570, 560, 120, 80), "color": "accent2", "width": 6, "kind": "box", "start": C("Day zero"), "label": lbl("GOODS ARRIVE", 630, 540, 20, "accent2")},
        {"d": rect(900, 560, 120, 80), "color": "accent3", "width": 6, "kind": "box", "start": C("members have bought it"), "label": lbl("CASH IN", 960, 540, 22, "accent3")},
        {"d": rect(1280, 560, 120, 80), "color": "risk", "width": 6, "kind": "box", "start": C("Only later does the bill"), "label": lbl("PAY SUPPLIER", 1340, 540, 20, "risk")},
        {"d": "M 1030 700 L 1030 740 L 1270 740 L 1270 700", "color": "accent", "width": 6, "start": C("In between"), "label": lbl("SUPPLIERS' MONEY, IN COSTCO'S HANDS", 1150, 790, 20, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("In between", 0.3), "dur": 1.4, "target": [1150, 740]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])
kinetic("s30_t4", "m4_transition", [("One more piece…", 64, "One more piece", None, False), ("The biggest spenders", 66, "spend the most", "gold", False)])

# ====================================================================== PART 5: the loyalty loop (evidence board + charts)
card("s31_c5", "m5_card", "The Loyalty Loop", "Pay more, spend more")
stage("s32_exec", "m5_exec", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [mcard(420, 330, at=0.2, scale=0.45, rot=-6, color="#263238", text="EXECUTIVE"),
              it("letters", x=420, y=520, text="FEE $130 · 2% BACK (CAPPED)", at=C("they get back about two percent"), size=30, color="gold"),
              chart([{"label": "2024", "value": 35.4, "color": "#90A4AE", "at": C("Two years earlier"), "display": "35.4M"},
                     {"label": "2026", "value": 42.3, "color": "#E89A00", "at": C("Costco had"), "display": "42.3M"}],
                    at=0.2, max=48, dark=True, title="EXECUTIVE MEMBERS (10-K)", x=820, y=200, w=760, h=520),
              it("letters", x=1200, y=860, text="≈ 75% OF ALL SALES", at=C("about seventy-five percent"), size=56, color="risk")]},
    sources=["tenk", "fee"])
stage("s33_why", "m5_why", {
    "zones": [Z("warehouse")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The fee makes you come back"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("cart", x=[[0, 400], [12, 1500]], at=0.2, scale=0.8, load=3, price="2% BACK"),
              it("letters", x=1300, y=180, text="SPEND MORE → GET MORE BACK", at=C("The more you spend"), size=50, color="gold"),
              it("letters", x=1300, y=280, text="FEE = COME BACK · REWARD = SPEND MORE", at=C("The fee makes you come back"), size=38, color="white")]},
    sources=["tenk"])
add("p34_machine", "m5_draw", "engine_draw", {
    "title": "The Costco machine", "board": BOARD, "draw_start": C("Low prices bring members in"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(880, 360, 240, 90), "color": "accent3", "width": 6, "kind": "box", "start": C("Low prices bring members in"), "label": lbl("LOW PRICES", 1000, 413, 24, "accent3")},
        {"d": rect(1220, 520, 240, 90), "color": "accent", "width": 6, "kind": "box", "start": C("Members pay fees"), "label": lbl("FEES ≈ ½ PROFIT", 1340, 573, 22, "accent")},
        {"d": rect(880, 680, 240, 90), "color": "accent2", "width": 6, "kind": "box", "start": C("A short list of products"), "label": lbl("SHORT LIST", 1000, 733, 24, "accent2")},
        {"d": rect(540, 520, 240, 90), "color": "risk", "width": 6, "kind": "box", "start": C("Fast sales let Costco"), "label": lbl("SUPPLIERS' CASH", 660, 573, 22, "risk")},
        {"d": arrow((1120, 420), (1260, 510), -0.1) + " " + arrow((1300, 620), (1120, 710), -0.1) + " " + arrow((880, 720), (720, 620), -0.1) + " " + arrow((700, 510), (880, 420), -0.1), "color": "ink", "width": 4, "start": C("Each part feeds the next")},
    ],
    "actions": [{"kind": "point", "at": C("Each part feeds the next", 0.3), "dur": 1.4, "target": [1000, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["tenk"])

# ====================================================================== PAYOFF
stage("s35_payoff", "payoff", {
    "zones": [Z("warehouse", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("The store is the bait"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [mcard(1000, 520, at=0.2, scale=0.9, rot=-4),
              it("letters", x=1000, y=150, text="IT SELLS ACCESS", at=C("It sells"), size=70, color="gold"),
              it("letters", x=560, y=250, text="THE STORE IS THE BAIT", at=C("The store is the bait"), size=40, color="white"),
              it("letters", x=1380, y=250, text="THE MEMBERSHIP IS THE BUSINESS", at=C("The membership is the business"), size=36, color="green")]},
    sources=["tenk"])
add("s36_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_costco_storyboard.py; edit the generator, not this file.\n"
           "# Episode 32 storyboard (the Costco business model): one visual language per part; tones from visual_direction.yaml.\n")
