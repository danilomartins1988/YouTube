"""Generates projects/why-americas-airports-make-money-before-you-fly/deliverables/documentary/storyboard.yaml (Episode 38,
US batch #12: Why America's Airports Make Money Before You Fly).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the airport parking garage (new `parkingdeck` set) with a giant counter.
- Part 1 (who owns the airport): city hall (parliament set) and the concourse (new `terminal` set).
- Part 2 (the ticket): a stacked ticket chart and departure-board style screens.
- Part 3 (the landlord): the concourse with jets at the gates; LAX revenue chart.
- Part 4 (the car): the garage, the rental lot (dealership set) and the curb with ride-hail cars.
- Part 5 (the terminal): shops and screens in the concourse at night; grants in Washington.
No airline/airport logos; names in text only. Lint: tools/lint_storyboard.py.  Run: python tools/gen_airports_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-americas-airports-make-money-before-you-fly/deliverables/documentary/storyboard.yaml"
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


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("parkingdeck")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 1.0, "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1100, y=210, at=0.05, prefix="$", suffix="BN", decimals=1, steps=[[0.05, 0], [1.5, 6.9]], text="U.S. AIRPORT PARKING & GROUND TRANSPORT REVENUE, FY2025 (FAA)", scale=1.3),
              it("sedan", x=[[0, -200], [3.0, 600]], at=0.2, scale=0.55, color="#E53935"),
              it("letters", x=1450, y=1000, text="> AIRLINE LANDING FEES ($5.5BN)", at=C("More than passenger airlines"), size=42, color="gold")]},
    sources=["cats"])
stage("s02_twist", "h_twist", {
    "zones": [Z("terminal")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In rent from the airline"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 3,
    "items": [it("letters", x=1000, y=640, text="PAID BEFORE TAKEOFF", at=0.2, size=70, color="risk"),
              it("sign", x=600, y=300, text="PARKING", at=C("your parking spot"), color="#BBDEFB", size=40),
              it("sign", x=950, y=300, text="TICKET CHARGE", at=C("hidden in your ticket"), color="#FFE0B2", size=40),
              it("sign", x=1350, y=300, text="AIRLINE RENT", at=C("In rent from the airline"), color="#C8E6C9", size=40),
              it("sign", x=1700, y=300, text="COFFEE", at=C("the coffee you bought"), color="#FFCDD2", size=40)]},
    sources=["cats", "pfc"])
stage("s03_question", "h_question", {
    "zones": [Z("terminal", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [*crowd([600, 700, 800, 1300, 1400], "walk", at=0.1, scale=0.6),
              it("letters", x=1000, y=130, text="WHO OWNS THE AIRPORT?", at=0.4, size=70, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE TICKET", at=0.3, color="#BBDEFB", size=40),
              it("sign", x=750, y=380, text="2 · THE AIRLINES", at=C("the airlines"), color="#FFE0B2", size=40),
              it("sign", x=1170, y=380, text="3 · YOUR CAR", at=C("car"), color="#C8E6C9", size=40),
              it("sign", x=1590, y=380, text="4 · THE TERMINAL", at=C("the terminal itself"), color="#FFCDD2", size=40),
              it("letters", x=960, y=700, text="FOUR WAYS TO GET PAID", at=C("the four ways"), size=68, color="gold")]})

# ====================================================================== PART 1: who owns the airport (city hall + concourse)
card("s05_c1", "m1_card", "Who Owns the Airport", "Public owners, run like a business")
stage("s06_owners", "m1_owners", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And when they take federal grants"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("sign", x=850, y=230, text="STATES · COUNTIES · CITIES · AUTHORITIES", at=C("owned by states"), color="#BBDEFB", size=32),
              it("letters", x=1000, y=110, text="NOT COMPANIES", at=0.3, size=60, color="gold"),
              it("docs", x=1500, y=560, at=C("And when they take federal grants"), text="FAA GRANT ASSURANCES", scale=0.65, stamp="SELF-SUSTAINING", stampAt=C("as self-sustaining"))]},
    sources=["gao", "assur"])
stage("s07_size", "m1_size", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("counter", x=520, y=280, at=0.3, prefix="$", suffix="BN+", decimals=1, steps=[[0, 0], [{"cue": "in operating revenue"}, 34.5]], text="AIRPORT OPERATING REVENUE, FY2025 (FAA CATS)", scale=1.1),
              it("counter", x=1400, y=280, at=C("They also carried"), prefix="$", suffix="BN", steps=[[0, 0], [{"cue": "of debt"}, 141]], text="DEBT AT YEAR END (FAA CATS)", scale=1.1),
              it("letters", x=960, y=600, text="≈ 996 MILLION BOARDINGS", at=C("nine hundred and ninety-six"), size=60, color="gold")]},
    sources=["cats"])
stage("s08_traffic", "m1_traffic", {
    "zones": [Z("terminal")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("On November thirtieth"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 3,
    "items": [*crowd([500 + 90 * k for k in range(12)], "walk", at=0.2, scale=0.55),
              it("letters", x=1000, y=150, text="≈ 1.1 BILLION PASSENGERS, 2025 (BTS)", at=C("Airlines carried"), size=44, color="white"),
              it("counter", x=1650, y=260, at=C("On November thirtieth"), prefix="", suffix="", steps=[[0, 0], [{"cue": "in a single day"}, 3134613]], text="TSA SCREENINGS, NOV 30, 2025 (RECORD)")]},
    sources=["bts", "tsa"])
add("p09_model", "m1_draw", "engine_draw", {
    "title": "How an airport is financed", "board": BOARD, "draw_start": C("Here is the city or authority"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 380, 240, 90), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the city or authority"), "label": lbl("PUBLIC OWNER", 680, 433, 22, "accent2")},
        {"d": rect(1180, 380, 240, 90), "color": "accent", "width": 6, "kind": "box", "start": C("It borrows money"), "label": lbl("BONDS", 1300, 433, 24, "accent")},
        {"d": arrow((1180, 425), (810, 425)), "color": "accent", "width": 4, "kind": "arrow", "start": C("It borrows money", 0.4)},
        {"d": rect(860, 600, 280, 100), "color": "ink", "width": 6, "kind": "box", "start": C("It builds a terminal"), "label": lbl("TERMINAL + RUNWAYS", 1000, 658, 22, "ink")},
        {"d": arrow((680, 480), (880, 600)), "color": "ink", "width": 4, "kind": "arrow", "start": C("It builds a terminal", 0.3)},
        {"d": arrow((1120, 600), (1290, 480)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("pay back the debt"), "label": lbl("FEES PAY THE DEBT", 1320, 560, 20, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("A public owner", 0.1), "dur": 1.4, "target": [1000, 650]}],
    "scale": 0.86, "floor": 1040}, sources=["gao", "cats"])
kinetic("s10_t1", "m1_transition", [("The first payment…", 64, "The first payment", None, False), ("…hidden in your ticket", 64, "hidden in the price", "gold", False)])

# ====================================================================== PART 2: the ticket (stacked chart + screens)
card("s11_c2", "m2_card", "The Ticket", "Facility charges, taxes and fees")
stage("s12_pfc", "m2_pfc", {
    "zones": [Z("terminal")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The cap was last raised"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("pricetag", x=700, y=320, at=0.3, text="$4.50 / SEGMENT", scale=1.0),
              it("letters", x=1300, y=180, text="MAX $18 PER ROUND TRIP", at=C("up to eighteen dollars"), size=50, color="gold"),
              it("letters", x=1300, y=280, text="KEPT BY THE AIRPORT", at=C("The airport keeps it"), size=44, color="white"),
              it("calendar", x=1700, y=480, at=C("The cap was last raised"), pages=[[0, "$3 → $4.50", "2000"]], scale=0.7)]},
    sources=["pfc"])
stage("s13_total", "m2_total", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2019", "value": 3.63, "color": "#90A4AE", "at": 0.4, "display": "$3.63bn"},
                     {"label": "2020", "value": 1.69, "color": "#B0BEC5", "at": 0.8, "display": "$1.69bn"},
                     {"label": "2025", "value": 3.85, "color": "#E89A00", "at": C("about three point eight five"), "display": "$3.85bn"}],
                    at=0.2, max=4.5, title="PASSENGER FACILITY CHARGES COLLECTED (FAA)", x=360, w=880),
              it("letters", x=1550, y=380, text="$79.4BN", at=C("Since the program began"), size=64, color="gold"),
              it("letters", x=1600, y=470, text="SINCE 1992", at=C("Since the program began", 0.3), size=40, color="white"),
              it("letters", x=1600, y=560, text="ALL LARGE AIRPORTS: MAX", at=C("Every large airport"), size=34, color="risk")]},
    sources=["pfc"])
stage("s14_taxes", "m2_taxes", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "TICKET TAX 7.5%", "value": 22.5, "color": "#4FC3F7", "at": C("a federal ticket tax"), "display": "$22.50"},
                     {"label": "SEGMENT FEES", "value": 21.2, "color": "#FFB300", "at": C("a segment fee"), "display": "$21.20"},
                     {"label": "FACILITY CHARGES", "value": 18.0, "color": "#43A047", "at": C("on a three hundred dollar"), "display": "$18.00", "sub": "→ the airport"},
                     {"label": "SECURITY FEE", "value": 11.2, "color": "#E53935", "at": C("a security fee"), "display": "$11.20"}],
                    at=0.2, max=26, dark=True, title="EXTRAS ON A $300 ROUND TRIP WITH CONNECTIONS (OUR CALCULATION)", x=300, w=1100),
              it("letters", x=1600, y=380, text="= $72.90", at=C("all of these add up"), size=64, color="gold"),
              it("letters", x=1650, y=480, text="NONSTOP ≈ $53", at=C("Even on a nonstop"), size=44, color="white")]},
    sources=["excise", "tsa", "pfc"])
stage("s15_fight", "m2_fight", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The same group estimates"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("pricetag", x=700, y=320, at=0.3, text="$4.50", pages=[[{"cue": "it should rise to twelve"}, "$12?", True]], scale=1.1),
              it("letters", x=1300, y=170, text="AIRPORT INDUSTRY ASKS FOR $12 (ACI-NA)", at=C("Their industry group"), size=40, color="gold"),
              it("counter", x=1350, y=330, at=C("The same group estimates"), prefix="$", suffix="BN", steps=[[0, 0], [{"cue": "of new investment"}, 174]], text="NEEDS OVER 5 YEARS (AIRPORTS' OWN ESTIMATE)")]},
    sources=["acina"])
add("p16_ticket", "m2_draw", "engine_draw", {
    "title": "Your ticket, stacked (illustration)", "board": BOARD, "draw_start": C("Here is the fare"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 800 860 L 1200 860", "color": "ink", "width": 4, "start": C("Let me draw your ticket")},
        {"d": "M 860 860 L 860 560 L 1140 560 L 1140 860", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.2, "kind": "bar", "start": C("Here is the fare"), "label": lbl("FARE", 1000, 720, 26, "accent2")},
        {"d": "M 860 560 L 860 500 L 1140 500 L 1140 560", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("the ticket tax"), "label": lbl("TICKET TAX", 1250, 535, 18, "accent")},
        {"d": "M 860 500 L 860 444 L 1140 444 L 1140 500", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("Then the segment fees"), "label": lbl("SEGMENT FEES", 1260, 478, 18, "risk")},
        {"d": "M 860 444 L 860 414 L 1140 414 L 1140 444", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.4, "kind": "bar", "start": C("Then the security fee"), "label": lbl("SECURITY", 1240, 432, 18, "accent2")},
        {"d": "M 860 414 L 860 366 L 1140 366 L 1140 414", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.4, "kind": "bar", "start": C("a thin slice"), "label": lbl("→ AIRPORT", 1240, 393, 20, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("a thin slice", 0.3), "dur": 1.4, "target": [1000, 390]}],
    "scale": 0.86, "floor": 1040}, sources=["excise", "tsa", "pfc"])
kinetic("s17_t2", "m2_transition", [("The second payment…", 64, "The second payment", None, False), ("…the biggest of all", 66, "the biggest of all", "gold", False)])

# ====================================================================== PART 3: the landlord (concourse + LAX chart)
card("s18_c3", "m3_card", "The Landlord", "Airlines pay rent and landing fees")
stage("s19_aero", "m3_aero", {
    "zones": [Z("terminal")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Terminal rents"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 3,
    "items": [it("letters", x=1000, y=380, text="THE AIRPORT IS A LANDLORD", at=0.3, until=C("landing fees from passenger"), size=64, color="gold"),
              it("counter", x=1100, y=190, at=C("landing fees from passenger"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "brought in about"}, 5.5]], text="PASSENGER AIRLINE LANDING FEES, FY2025 (FAA)"),
              it("letters", x=1650, y=420, text="+ TERMINAL RENTS ≈ $8.9BN", at=C("Terminal rents"), size=44, color="gold"),
              it("letters", x=1650, y=560, text="AVIATION TOTAL ≈ $19.3BN (56%)", at=C("All the aviation charges"), size=38, color="white")]},
    sources=["cats"])
stage("s20_cpe", "m3_cpe", {
    "zones": [Z("terminal", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}], "drift": 2,
    "items": [*crowd([700, 790, 880], "walk", at=0.2, scale=0.55),
              it("pricetag", x=1300, y=300, at=C("cost per enplaned"), text="$15.76", scale=1.1),
              it("letters", x=1300, y=150, text="AIRLINE COST PER BOARDING PASSENGER (FAA, FY2025)", at=0.4, size=34, color="white"),
              it("letters", x=1300, y=560, text="→ BUILT INTO YOUR FARE", at=C("ends up in the price"), size=44, color="gold")]},
    sources=["cats"])
stage("s21_lax", "m3_lax", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "TERMINAL RENTALS", "value": 935, "color": "#2F6FD1", "at": C("Its biggest source"), "display": "$935M"},
                     {"label": "LANDING FEES", "value": 369, "color": "#4FC3F7", "at": C("Second came landing fees"), "display": "$369M"},
                     {"label": "AUTO PARKING", "value": 161, "color": "#E89A00", "at": C("about three quarters"), "display": "$161M"}],
                    at=0.2, max=1000, title="LAX TOP REVENUE SOURCES, FY2025 (LAWA)", x=360, w=1000),
              it("letters", x=960, y=470, text="LOS ANGELES INTERNATIONAL", at=0.3, until=C("Its biggest source"), size=72, color="gold"),
              it("letters", x=1550, y=420, text="AVIATION ≈ 3/4", at=C("about three quarters"), size=50, color="white")]},
    sources=["lax"])
add("p22_lease", "m3_draw", "engine_draw", {
    "title": "The lease (illustration)", "board": BOARD, "draw_start": C("The airport builds the terminal"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 380, 260, 100), "color": "ink", "width": 6, "kind": "box", "start": C("The airport builds the terminal"), "label": lbl("AIRPORT", 690, 438, 26, "ink")},
        {"d": rect(1180, 380, 260, 100), "color": "accent2", "width": 6, "kind": "box", "start": C("The airline rents the gate"), "label": lbl("AIRLINE", 1310, 438, 26, "accent2")},
        {"d": arrow((1180, 410), (830, 410)), "color": "accent", "width": 5, "kind": "arrow", "start": C("The airline rents the gate", 0.4), "label": lbl("RENT", 1000, 390, 22, "accent")},
        {"d": arrow((1180, 460), (830, 460)), "color": "risk", "width": 5, "kind": "arrow", "start": C("Every landing pays a fee"), "label": lbl("LANDING FEES", 1000, 500, 20, "risk")},
        {"d": rect(860, 620, 280, 90), "color": "accent3", "width": 6, "kind": "box", "start": C("lenders know the rent"), "label": lbl("LENDERS", 1000, 673, 24, "accent3")},
        {"d": arrow((1000, 610), (720, 490)), "color": "accent3", "width": 4, "kind": "arrow", "start": C("help the airport borrow")},
    ],
    "actions": [{"kind": "point", "at": C("will keep coming", 0.1), "dur": 1.4, "target": [1000, 660]}],
    "scale": 0.86, "floor": 1040}, sources=["cats"])
kinetic("s23_t3", "m3_transition", [("Nothing to do with planes…", 60, "nothing to do with planes", None, True), ("…your car", 84, "It comes from your car", "gold", False)])

# ====================================================================== PART 4: the car (garage, rental lot, curb)
card("s24_c4", "m4_card", "The Car", "Parking, rentals and ride apps")
stage("s25_parking", "m4_parking", {
    "zones": [Z("parkingdeck")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("And it is growing"), "x": 1350, "y": 500, "zoom": 1.0, "dur": 1.5}], "drift": 3,
    "items": [it("counter", x=1000, y=110, at=0.3, prefix="$", suffix="BN", decimals=2, steps=[[0, 0], [{"cue": "in twenty twenty-five"}, 6.89]], text="PARKING & GROUND TRANSPORTATION, FY2025 (FAA CATS)", scale=1.1),
              it("letters", x=1550, y=300, text="≈ 1 IN 5 REVENUE DOLLARS", at=C("one in every five"), size=44, color="gold"),
              it("letters", x=1700, y=350, text="2024: $6.55BN", at=C("A year earlier"), size=40, color="white")]},
    sources=["cats"])
stage("s26_rental", "m4_rental", {
    "zones": [Z("dealership")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("At Los Angeles"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [*[it("sedan", x=500 + 260 * k, at=0.2 + 0.1 * k, scale=0.4, color=["#90A4AE", "#ECEFF1", "#1E88E5", "#E53935"][k % 4], sticker="RENT") for k in range(4)],
              it("letters", x=1000, y=160, text="RENTAL CARS ≈ $2.5BN TO AIRPORTS (FAA)", at=C("Rental companies paid"), size=44, color="gold"),
              it("sign", x=1700, y=300, text="LAX: PARKING = #3 SOURCE ($161M)", at=C("At Los Angeles"), color="#FFE0B2", size=34)]},
    sources=["cats", "lax"])
stage("s27_rides", "m4_rides", {
    "zones": [Z("terminal")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 3,
    "items": [it("sedan", x=[[0, 2400], [6, 600]], at=0.2, scale=0.45, color="#263238", sticker="RIDE"),
              it("sedan", x=[[0, 2800], [8, 1200]], at=0.5, scale=0.45, color="#6D4C41", sticker="RIDE"),
              it("counter", x=1000, y=150, at=C("Los Angeles lists"), prefix="$", suffix="M", steps=[[0, 0], [{"cue": "a year"}, 36]], text="LAX: RIDE-HAIL APPS, FY2025 (TOP-10 SOURCE)"),
              it("letters", x=1000, y=380, text="DRIVE · RENT · DROP-OFF → AIRPORT COLLECTS", at=C("Whether you drive"), size=38, color="gold")]},
    sources=["lax"])
add("p28_curb", "m4_draw", "engine_draw", {
    "title": "Three ways to arrive", "board": BOARD, "draw_start": C("Here is the garage"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 400, 220, 100), "color": "accent", "width": 6, "kind": "box", "start": C("Here is the garage"), "label": lbl("GARAGE · $/HOUR", 670, 458, 20, "accent")},
        {"d": rect(890, 400, 220, 100), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the rental car center"), "label": lbl("RENTAL CARS", 1000, 458, 20, "accent2")},
        {"d": rect(1220, 400, 220, 100), "color": "risk", "width": 6, "kind": "box", "start": C("Here is the pickup lane"), "label": lbl("RIDE APPS", 1330, 458, 20, "risk")},
        {"d": rect(860, 660, 280, 90), "color": "ink", "width": 6, "kind": "box", "start": C("Three ways to arrive"), "label": lbl("AIRPORT", 1000, 713, 26, "ink")},
        {"d": arrow((670, 510), (880, 660)) + " " + arrow((1000, 510), (1000, 650)) + " " + arrow((1330, 510), (1120, 660)), "color": "ink", "width": 4, "kind": "arrow", "start": C("three ways to pay")},
    ],
    "actions": [{"kind": "point", "at": C("three ways to pay", 0.2), "dur": 1.4, "target": [1000, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["cats", "lax"])
kinetic("s29_t4", "m4_transition", [("Once you're inside…", 64, "once you are inside", None, False), ("…the terminal earns", 68, "starts earning", "gold", False)])

# ====================================================================== PART 5: the terminal (shops + screens + grants)
card("s30_c5", "m5_card", "The Terminal", "Shops, screens and grants")
stage("s31_shops", "m5_shops", {
    "zones": [Z("terminal", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("At Los Angeles"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("restaurant", x=700, at=0.2, scale=0.7, text="CAFE"),
              it("letters", x=1300, y=150, text="FOOD & DRINK ≈ $1.26BN · RETAIL ≈ $1BN (FAA)", at=C("brought America's airports"), size=36, color="gold"),
              it("letters", x=1400, y=260, text="LAX CONCESSIONS ≈ $511M (≈ 25%)", at=C("At Los Angeles"), size=40, color="white")]},
    sources=["cats", "lax"])
stage("s32_ads", "m5_ads", {
    "zones": [Z("terminal")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Some airports even run hotels"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("bigphone", x=800, y=420, at=0.2, scale=0.7, rot=90, len=6),
              it("letters", x=800, y=200, text="LAX ADVERTISING ≈ $39M", at=C("from advertising"), size=44, color="gold"),
              it("sign", x=1550, y=300, text="AIRPORT HOTELS ≈ $407M (FAA)", at=C("Some airports even run hotels"), color="#BBDEFB", size=36)]},
    sources=["lax", "cats"])
stage("s33_grants", "m5_grants", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By our calculation"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.2, text="INFRASTRUCTURE LAW (2021)", scale=0.7, stamp="$14.5BN / 5 YRS", stampAt=C("over five years")),
              it("letters", x=1350, y=180, text="FINAL INSTALLMENT ≈ $2.89BN", at=C("fifth and final"), size=44, color="white"),
              it("counter", x=1400, y=340, at=C("By our calculation"), prefix="≈ $", suffix="BN", steps=[[0, 0], [{"cue": "about nine billion"}, 9]], text="FEDERAL AIRPORT GRANTS, FY2025 (OUR SUM OF FAA FILES)")]},
    sources=["grants"])
add("p34_streams", "m5_draw", "engine_draw", {
    "title": "Five streams, one owner", "board": BOARD, "draw_start": C("Your ticket carries"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 600, 280, 100), "color": "ink", "width": 6, "kind": "box", "start": C("Let me put the whole airport"), "label": lbl("PUBLIC OWNER", 1000, 658, 24, "ink")},
        {"d": rect(540, 360, 180, 70), "color": "accent3", "width": 5, "kind": "box", "start": C("Your ticket carries"), "label": lbl("TICKET", 630, 403, 20, "accent3")},
        {"d": rect(760, 360, 180, 70), "color": "accent2", "width": 5, "kind": "box", "start": C("The airlines pay rent"), "label": lbl("AIRLINES", 850, 403, 20, "accent2")},
        {"d": rect(980, 360, 180, 70), "color": "accent", "width": 5, "kind": "box", "start": C("Your car pays"), "label": lbl("CAR", 1070, 403, 20, "accent")},
        {"d": rect(1200, 360, 180, 70), "color": "risk", "width": 5, "kind": "box", "start": C("The terminal collects"), "label": lbl("TERMINAL", 1290, 403, 20, "risk")},
        {"d": rect(1240, 760, 180, 70), "color": "ink", "width": 4, "kind": "box", "start": C("federal grants fill in"), "label": lbl("GRANTS", 1330, 803, 20, "ink")},
        {"d": arrow((630, 440), (900, 600)) + " " + arrow((850, 440), (960, 600)) + " " + arrow((1070, 440), (1040, 600)) + " " + arrow((1290, 440), (1100, 600)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Five streams")},
    ],
    "actions": [{"kind": "point", "at": C("all flowing into one", 0.1), "dur": 1.4, "target": [1000, 650]}],
    "scale": 0.86, "floor": 1040}, sources=["pfc", "cats", "grants"])

# ====================================================================== PAYOFF
stage("s35_payoff", "payoff", {
    "zones": [Z("terminal", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("And every one of those"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("plane", x=[[0, 300], [12, 1700]], y=[[0, 450], [12, 200]], at=0.2, text="", tilt=-8),
              it("letters", x=1000, y=130, text="LANDLORD · PARKING · MALL · TOLL", at=C("It is a landlord"), size=50, color="gold"),
              it("letters", x=1000, y=230, text="PAID BEFORE WHEELS UP", at=C("And every one of those"), size=50, color="white")]},
    sources=["cats"])
add("s36_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_airports_storyboard.py; edit the generator, not this file.\n"
           "# Episode 38 storyboard (US airports): one visual language per part; tones from visual_direction.yaml.\n")
