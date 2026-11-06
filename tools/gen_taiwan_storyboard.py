"""Generates projects/why-taiwan-matters/deliverables/documentary/storyboard.yaml (Episode 07).

Kept as a script because several presenter drawings (wafer grid, map coordinates) are computed.
Run: python tools/gen_taiwan_storyboard.py
"""
from __future__ import annotations

import math
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parents[1] / "projects/why-taiwan-matters/deliverables/documentary/storyboard.yaml"
INTER = ["font:inter"]
GEO = ["geo:remotion_world", "font:inter"]
BOARD = {"x": 470, "y": 230, "w": 1370, "h": 800}


def wafer(cx: float, cy: float, r: float, step: float) -> tuple[str, list[tuple[float, float]]]:
    """Grid of die lines clipped to a circle, and the die centres that fit inside it."""
    d = []
    k = -math.floor(r / step)
    while k * step <= r:
        o = k * step
        if abs(o) < r - 4:
            h = math.sqrt(r * r - o * o)
            d.append(f"M {cx - h:.0f} {cy + o:.0f} L {cx + h:.0f} {cy + o:.0f}")
            d.append(f"M {cx + o:.0f} {cy - h:.0f} L {cx + o:.0f} {cy + h:.0f}")
        k += 1
    dies = []
    n = math.ceil(r / step)
    for i in range(-n, n):
        for j in range(-n, n):
            x, y = cx + (i + 0.5) * step, cy + (j + 0.5) * step
            if math.hypot(abs(x - cx) + step / 2, abs(y - cy) + step / 2) < r:
                dies.append((x, y))
    return " ".join(d), dies


def circle(cx: float, cy: float, r: float) -> str:
    return f"M {cx - r:.0f} {cy:.0f} A {r:.0f} {r:.0f} 0 1 0 {cx + r:.0f} {cy:.0f} A {r:.0f} {r:.0f} 0 1 0 {cx - r:.0f} {cy:.0f}"


def cross(x: float, y: float, s: float = 13) -> str:
    return f"M {x - s:.0f} {y - s:.0f} L {x + s:.0f} {y + s:.0f} M {x + s:.0f} {y - s:.0f} L {x - s:.0f} {y + s:.0f}"


scenes: list[dict] = []


def add(id_, segment, type_, params, sources=(), assets=INTER, sfx=None):
    s = {"id": id_, "segment": segment, "type": type_, "params": params}
    if sfx:
        s["sfx"] = sfx
    if sources:
        s["sources"] = list(sources)
    s["assets"] = list(assets)
    scenes.append(s)


def card(id_, segment, number, title, subtitle):
    add(id_, segment, "act_title", {"number": number, "title": title, "subtitle": subtitle, "min_seconds": 3.0},
        sfx=[{"kind": "hit", "at": 0.1, "gain": 0.25}])


def question(id_, segment, chapter, q, why, q_cue, why_cue):
    add(id_, segment, "kinetic_text", {"align": "center", "chapter": chapter, "lines": [
        {"text": "THE QUESTION", "size": 34, "style": "body", "color": "muted", "cue": q_cue},
        {"text": q, "size": 66, "color": "accent", "cue": q_cue, "offset": 0.4},
        {"text": "WHY IT MATTERS", "size": 34, "style": "body", "color": "muted", "cue": why_cue},
        {"text": why, "size": 50, "style": "body", "cue": why_cue, "offset": 0.4},
    ]})


# ====================================================================== HOOK
add("s01_island", "h_question", "map", {
    "no_chrome": True, "geo": "world",
    "views": [{"lon": 62, "lat": 36, "span": 175}, {"lon": 64, "lat": 34, "span": 150, "cue": "smaller than"}],
    "move": 4.0,
    "highlights": {"TWN": {"colour": "accent", "cue": "an island"}, "CHE": {"colour": "accent2", "cue": "Switzerland"}},
    "markers": [
        {"lon": 121.0, "lat": 23.7, "label": "Taiwan", "sublabel": "{{taiwan_area.display}}", "cue": "an island", "size": 36, "anchor": "end"},
        {"lon": 8.2, "lat": 46.8, "label": "Switzerland", "sublabel": "{{taiwan_area.ch_display}}", "cue": "Switzerland", "size": 36},
    ]}, sources=["cia_taiwan", "cia_switzerland", "natural_earth"], assets=GEO,
    sfx=[{"kind": "hit", "at": 0.0, "gain": 0.3}])

add("s02_stakes", "h_stakes", "map", {
    "chapter": "The island", "geo": "world",
    "views": [{"lon": 121.0, "lat": 23.7, "span": 36}, {"lon": 121.0, "lat": 23.7, "span": 9, "cue": "most of the world"}],
    "move": 3.0,
    "highlights": {"TWN": {"colour": "accent", "cue": "Taiwan covers"}},
    "markers": [{"lon": 121.0, "lat": 23.7, "label": "Taiwan", "sublabel": "{{lt10_capacity.display}} of advanced logic capacity (2022)",
                 "cue": "most advanced chips", "size": 40}],
    }, sources=["cia_taiwan", "sia_bcg_2024", "natural_earth"], assets=GEO)

add("s03_missions", "h_missions", "kinetic_text", {"align": "center", "chapter": "Five missions", "lines": [
    {"text": "Today: five missions", "size": 64, "color": "accent", "cue": "five missions"},
    {"text": "1 · How Taiwan became essential", "size": 42, "style": "body", "cue": "how Taiwan became"},
    {"text": "2 · Why nobody can simply copy it", "size": 42, "style": "body", "cue": "simply copy"},
    {"text": "3 · Who depends on it", "size": 42, "style": "body", "cue": "who depends"},
    {"text": "4 · What a disruption could cost", "size": 42, "style": "body", "color": "risk", "cue": "what a disruption"},
    {"text": "5 · Can the world spread the risk?", "size": 42, "style": "body", "color": "accent2", "cue": "spread the risk"},
]})

# ====================================================================== MISSION 1
card("s04_m1", "m1_card", "Mission 1", "How Taiwan Became Essential", "From one idea to the center of chipmaking")
question("s05_m1q", "m1_question", "Mission 1 · How Taiwan became essential",
         "How did a small island become the center of chipmaking?", "Almost everything now runs on chips",
         "How did", "It matters")
add("s06_oldrule", "m1_conflict", "compare", {"chapter": "Mission 1 · The conflict", "title": "The old rule of the chip business", "sides": [
    {"kicker": "If you designed chips…", "value": "Own fab", "label": "you built your own factory", "cue": "one rule"},
    {"kicker": "…and fabs were", "value": "Brutally expensive", "label": "so only giants could play", "cue": "brutally expensive"},
]})
add("s07_timeline_network", "m1_tsmc", "timeline_network", {
    "title": "One idea: a chipmaker that designs nothing", "title_cue": "with backing", "subtitle": "The foundry model",
    "start_year": 1980, "end_year": 2000, "tick_every": 5, "axis_cue": "with backing",
    "items": [
        {"year": "{{tsmc_1987.value}}", "label": "TSMC: first dedicated foundry", "place": "TSMC · Hsinchu", "role": "manufactures for others",
         "lon": 120.99, "lat": 24.78, "colour": "accent", "cue": "a new company"},
        {"year": "{{tsmc_1987.value}}", "label": "Backed by Taiwan's government + Philips", "place": "Philips", "role": "early backer · Netherlands",
         "lon": 5.47, "lat": 51.44, "colour": "accent3", "cue": "Dutch company Philips"},
        {"year": "{{nvda_1993.value}}", "label": "NVIDIA founded: a designer, no fab", "place": "NVIDIA", "role": "designs · California",
         "lon": -121.96, "lat": 37.37, "colour": "accent2", "cue": "Nvidia, founded", "label_dy": -44},
        {"place": "Apple · AMD", "role": "design · California", "lon": -121.9, "lat": 37.3, "colour": "accent2", "cue": "so did Apple", "label_dy": 92},
    ],
    "links": [[2, 0], [3, 0], [1, 0]],
    "morph_cue": "They focus on design", "view": {"lon": 0, "lat": 30, "span": 320},
    "highlight": {"TWN": "accent"}, "network_title": "Design anywhere, manufacture in Taiwan",
}, sources=["tsmc_about", "tsmc_history", "nvda_10k_fy2026", "apple_arizona", "natural_earth"], assets=GEO,
    sfx=[{"kind": "pop", "cue": "They focus on design", "offset": 0.4}])
add("s08_share", "m1_discovery", "compare", {"chapter": "Mission 1 · The discovery", "title": "TSMC today", "sides": [
    {"kicker": "Foundry revenue share · {{foundry_share.period_display}}", "value": "{{foundry_share.display}}", "label": "of the top-10 contract chipmakers", "cue": "TSMC takes"},
    {"kicker": "Revenue · 2025", "value": "{{tsmc_revenue_2025.display}}", "label": "in US dollars", "cue": "it brought in"},
    {"kicker": "Advanced nodes · Q4 2025", "value": "{{advanced_q4.display}}", "label": "of wafer revenue at 7 nm or smaller", "cue": "most advanced processes"},
]}, sources=["trendforce_2q26", "tsmc_4q25_call", "tsmc_4q25"], sfx=[{"kind": "pop", "cue": "TSMC takes", "offset": 1.2}])
add("s09_m1t", "m1_transition", "kinetic_text", {"align": "center", "lines": [
    {"text": "If the idea was that simple…", "size": 60, "style": "body", "cue": "But if"},
    {"text": "why didn't everyone copy it?", "size": 76, "color": "accent", "cue": "why didn't"},
    {"text": "Mission 2 →", "size": 44, "color": "muted", "cue": "mission two"},
]})

# ====================================================================== MISSION 2
card("s10_m2", "m2_card", "Mission 2", "Why Chips Are So Hard to Make", "Design, wafers, lithography, packaging, yield, money")
question("s11_m2q", "m2_question", "Mission 2 · Why chips are so hard to make",
         "Why can't every country build its own fabs?", "If they could, Taiwan would not be special",
         "Why can't", "It matters")

# ---- PRESENTER A: the character draws the manufacturing process (signature animation 2)
add("p12_process", "m2_process", "presenter", {
    "title": "How a chip is made", "title_cue": "what it takes",
    "enter": {"from": "left", "cue": "Let's draw"},
    "items": [
        {"box": [540, 380, 250, 130], "label": "DESIGN", "colour": "accent2", "cue": "engineers design"},
        {"stroke": "M 575 640 L 625 640 L 625 690 L 685 690 L 685 650 L 750 650 M 585 725 L 665 725 L 665 690 M 705 725 L 755 725",
         "colour": "accent2", "w": 5, "speed": 900, "cue": "tiny switches"},
        {"text": "BILLIONS OF SWITCHES", "x": 515, "y": 820, "size": 24, "colour": "muted", "cue": "tiny switches", "offset": 0.6},
        {"arrow": [[800, 445], [865, 445]], "bend": 0.0, "colour": "ink", "cue": "Then a fab"},
        {"box": [870, 380, 250, 130], "label": "WAFER FAB", "colour": "accent", "cue": "Then a fab"},
        {"stroke": circle(995, 685, 62), "colour": "accent", "w": 5, "cue": "silicon wafer"},
        {"stroke": "M 950 655 L 1040 655 M 935 685 L 1055 685 M 950 715 L 1040 715 M 965 630 L 965 740 M 995 625 L 995 745 M 1025 630 L 1025 740",
         "colour": "accent", "w": 3, "speed": 1600, "cue": "layer after layer"},
        {"text": "PRINTED WITH LIGHT", "x": 870, "y": 820, "size": 24, "colour": "muted", "cue": "using light"},
        {"arrow": [[1130, 445], [1195, 445]], "bend": 0.0, "colour": "ink", "cue": "cut into chips"},
        {"box": [1200, 380, 270, 130], "label": "PACKAGE", "colour": "accent3", "cue": "cut into chips"},
        {"stroke": "M 1255 645 L 1325 645 L 1325 725 L 1255 725 Z M 1340 645 L 1390 645 L 1390 680 L 1340 680 Z M 1340 690 L 1390 690 L 1390 725 L 1340 725 Z M 1235 745 L 1410 745",
         "colour": "accent3", "w": 4, "speed": 1300, "cue": "packaged together"},
        {"text": "CHIP + MEMORY", "x": 1245, "y": 820, "size": 24, "colour": "muted", "cue": "with memory"},
        {"arrow": [[1480, 445], [1545, 445]], "bend": 0.0, "colour": "ink", "cue": "and tested"},
        {"box": [1550, 380, 230, 130], "label": "TEST", "colour": "accent2", "cue": "and tested"},
        {"stroke": "M 1615 690 L 1655 730 L 1730 645", "colour": "accent", "w": 8, "cue": "and tested", "offset": 0.4},
        {"text": "EVERY STEP: CLOSE TO PERFECT", "x": 790, "y": 930, "size": 40, "colour": "accent", "cue": "and tested", "offset": 1.2},
        {"point": [1180, 915], "label": "no step can fail", "colour": "accent", "hold": 1.6, "laser": True, "cue": "every single step"},
    ],
    "scale": 0.86, "floor": 1040, "board": BOARD, "speed": 1500,
}, sources=["sia_bcg_2024"])

add("s13_euv", "m2_euv", "map", {
    "chapter": "Mission 2 · Obstacle 1: lithography", "geo": "world",
    "views": [{"lon": 30, "lat": 35, "span": 200}, {"lon": 6, "lat": 50, "span": 30, "cue": "Dutch firm"}],
    "move": 3.0,
    "highlights": {"NLD": {"colour": "accent2", "cue": "Dutch firm"}},
    "markers": [{"lon": 5.4, "lat": 51.4, "label": "ASML", "sublabel": "the only maker of EUV machines · {{asml_only.display}}",
                 "cue": "Only one company", "size": 40}],
}, sources=["asml_euv", "asml_2025", "natural_earth"], assets=GEO)

wgrid, dies = wafer(960, 580, 250, 62)
bad = [dies[i] for i in (3, 9, 17, 22, 30)] if len(dies) > 30 else dies[:4]
add("s14_yield", "m2_yield", "whiteboard", {
    "speed": 1400, "caption": "Yield: the share of chips on a wafer that actually work", "caption_cue": "The real secret",
    "caption_y": 1030,
    "strokes": [
        {"d": circle(960, 580, 250), "w": 7, "cue": "owning the machines"},
        {"d": wgrid, "w": 3, "cue": "owning the machines", "offset": 0.8, "speed": 3600},
        {"text": "ONE WAFER", "x": 1250, "y": 400, "size": 40, "cue": "owning the machines", "offset": 1.4},
        {"d": " ".join(cross(x, y) for x, y in bad), "w": 6, "colour": "risk", "cue": "actually work"},
        {"text": "✗ = DEFECTIVE CHIP", "x": 1250, "y": 470, "size": 32, "colour": "risk", "cue": "actually work", "offset": 0.4},
        {"text": "YEARS OF PRACTICE", "x": 1250, "y": 620, "size": 34, "cue": "years of practice"},
        {"text": "THOUSANDS OF ENGINEERS", "x": 1250, "y": 680, "size": 34, "cue": "thousands of engineers"},
        {"text": "LEARNING FROM MISTAKES", "x": 1250, "y": 740, "size": 34, "colour": "accent", "cue": "endless learning"},
    ]})

add("s15_capex", "m2_capex", "compare", {"chapter": "Mission 2 · Obstacle 3: money", "title": "The cost of staying at the top", "sides": [
    {"kicker": "TSMC capital spending · 2026 guidance", "value": "{{capex_2026.display}}", "label": "in a single year", "bar": 54, "cue": "TSMC planned"},
    {"kicker": "Industry fab investment · 2024-2032", "value": "{{fab_investment.display}}", "label": "SIA/BCG projection", "bar": 2300, "cue": "Across the industry"},
]}, sources=["tsmc_4q25_call", "sia_bcg_2024"])

add("s16_capacity", "m2_discovery", "bar_chart", {
    "chapter": "Mission 2 · The discovery", "title": "Logic chips below 10 nm: share of global capacity, 2022",
    "subtitle": "Total capacity, all chip types: Taiwan {{total_capacity.display}} (China is larger) · SIA/BCG",
    "data": "{{lt10_capacity.value}}", "highlight": "TWN", "value_suffix": "%", "value_decimals": 0,
    "axis_step": 20, "axis_suffix": "%", "axis_prefix": "", "axis_divisor": 1,
    "callout": "Most advanced logic: Taiwan {{lt10_capacity.display}}", "callout_cue": {"cue": "below ten nanometers"},
}, sources=["sia_bcg_2024"])

add("s17_layers", "m2_layers", "compare", {"chapter": "Mission 2 · Not one market", "title": "Four different chip markets", "sides": [
    {"kicker": "Leading-edge logic", "value": "{{lt10_capacity.display}}", "label": "Taiwan · <10 nm", "cue": "not one market"},
    {"kicker": "All chipmaking", "value": "{{total_capacity.display}}", "label": "Taiwan · all chips", "cue": "not one market", "offset": 0.6},
    {"kicker": "DRAM memory", "value": "{{total_capacity.dram_kor_display}}", "label": "South Korea · DRAM", "cue": "led by South Korea"},
    {"kicker": "Advanced packaging", "value": "Bottleneck", "label": "chips + memory", "cue": "Advanced packaging"},
]}, sources=["sia_bcg_2024"])
add("s18_m2t", "m2_transition", "kinetic_text", {"align": "center", "lines": [
    {"text": "A narrow edge, at the very top", "size": 60, "style": "body", "cue": "Which raises"},
    {"text": "Who depends on that top?", "size": 76, "color": "accent", "cue": "Who depends"},
]})

# ====================================================================== MISSION 3
card("s19_m3", "m3_card", "Mission 3", "Who Depends on Taiwan", "Designers, makers, and everyone downstream")
question("s20_m3q", "m3_question", "Mission 3 · Who depends on Taiwan",
         "Who actually depends on Taiwan?", "Dependence = economic power, and economic risk",
         "Who actually", "It matters")

# ---- PRESENTER B: draws a world map linking Taiwan to tech companies
add("p21_map", "m3_map", "presenter", {
    "title": "Designed in California, made in Taiwan", "title_cue": "Let me draw",
    "enter": {"from": "right", "cue": "Let me draw"},
    "items": [
        {"map": {"lon": 5, "lat": 28, "span": 300}, "rect": [520, 330, 1280, 600], "countries": ["TWN", "USA"],
         "highlight": {"TWN": "accent", "USA": "accent2"}, "country_cues": {"USA": "across the Pacific"}, "points": 110, "speed": 2200, "cue": "Here is Taiwan"},
        {"pin": [-122.0, 37.4], "ll": True, "label": "NVIDIA · APPLE · AMD", "colour": "accent2", "r": 16, "side": "right", "cue": "home to Nvidia"},
        {"pin": [121.0, 23.7], "ll": True, "label": "TSMC", "colour": "accent", "r": 16, "cue": "TSMC does"},
        {"arrow": [[-118.0, 40.0], [118.0, 27.0]], "ll": True, "bend": -0.16, "colour": "accent2", "cue": "So the lines"},
        {"text": "DESIGNS →", "x": 1020, "y": 420, "size": 32, "colour": "accent2", "cue": "So the lines"},
        {"arrow": [[118.0, 21.0], [-110.0, 31.0]], "ll": True, "bend": -0.12, "colour": "accent", "cue": "from California to Taiwan", "offset": 0.6},
        {"text": "← FINISHED CHIPS", "x": 960, "y": 840, "size": 32, "colour": "accent", "cue": "and back again"},
    ],
    "scale": 0.86, "floor": 1040, "board": BOARD, "speed": 1500,
}, sources=["nvda_10k_fy2026", "apple_arizona", "natural_earth"], assets=GEO)

add("s22_customers", "m3_customers", "compare", {"chapter": "Mission 3 · Concentration", "title": "TSMC's two largest customers, 2025", "sides": [
    {"kicker": "Largest customer", "value": "{{tsmc_customers.first_display}}", "label": "of TSMC revenue · said to be NVIDIA", "bar": 19, "cue": "largest customer alone"},
    {"kicker": "Second largest", "value": "{{tsmc_customers.second_display}}", "label": "of TSMC revenue · reported to be Apple", "bar": 17, "cue": "second largest"},
]}, sources=["tsmc_customers_2025"])

add("s23_dependency", "m3_network", "supply_chain", {
    "title": "Global dependency network", "subtitle": "Illustrative: where chips made in Taiwan end up",
    "title_cue": "follow the chips",
    "views": [{"lon": 121, "lat": 24, "span": 60}, {"lon": 10, "lat": 25, "span": 320, "cue": "Cloud companies"}],
    "anchor_y": 0.46,
    "nodes": [
        {"id": "tw", "label": "Taiwan", "role": "leading-edge chips", "lon": 121.0, "lat": 23.7, "colour": "accent", "country": "TWN", "cue": "follow the chips", "dx": 26, "dy": 30},
        {"id": "us", "label": "Clouds · US", "role": "AI data centers", "lon": -78.5, "lat": 38.9, "colour": "accent2", "country": "USA", "cue": "United States", "dx": 26},
        {"id": "eu", "label": "Clouds · Europe", "role": "AI data centers", "lon": 8.7, "lat": 50.1, "colour": "accent2", "cue": "Europe", "dx": 26},
        {"id": "as", "label": "Clouds · Asia", "role": "AI data centers", "lon": 103.8, "lat": 1.35, "colour": "accent2", "cue": "and Asia", "dx": 26},
        {"id": "ph", "label": "Phone & PC makers", "role": "devices", "lon": 114.1, "lat": 22.5, "colour": "accent3", "cue": "Phone makers", "dx": -26, "dy": 40},
        {"id": "car", "label": "Carmakers", "role": "Germany · Japan · US", "lon": 9.2, "lat": 48.8, "colour": "accent3", "cue": "carmakers", "dx": -26, "dy": 46},
        {"id": "car2", "label": "Carmakers", "role": "Detroit", "lon": -83.0, "lat": 42.3, "colour": "accent3", "cue": "carmakers", "offset": 0.3, "dx": -26, "dy": -30},
    ],
    "links": [
        {"from": "tw", "to": "us", "lift": 0.25}, {"from": "tw", "to": "eu", "lift": 0.2}, {"from": "tw", "to": "as", "lift": 0.3},
        {"from": "tw", "to": "ph", "lift": 0.4}, {"from": "tw", "to": "car", "lift": 0.22}, {"from": "tw", "to": "car2", "lift": 0.18},
    ],
    "steps": [
        {"label": "Chips made in Taiwan", "colour": "accent", "cue": "follow the chips"},
        {"label": "Cloud data centers", "colour": "accent2", "cue": "Cloud companies"},
        {"label": "Phones · PCs · cars", "colour": "accent3", "cue": "Phone makers"},
        {"label": "Exports {{exports_2025.display}} (2025)", "colour": "accent", "cue": "exports hit"},
    ],
}, sources=["taiwan_exports_2025", "natural_earth"], assets=GEO)

add("s24_designers", "m3_designers", "compare", {"chapter": "Mission 3 · The key distinction", "title": "Everyone depends on someone", "sides": [
    {"kicker": "Chip designers", "value": "NVIDIA · Apple · AMD", "label": "depend on the makers", "cue": "Companies that design"},
    {"kicker": "Chip makers", "value": "TSMC", "label": "depend on suppliers", "cue": "the makers depend"},
    {"kicker": "Their suppliers", "value": "NL · JP · US", "label": "machines · materials · software", "cue": "Dutch machines"},
]}, sources=["asml_euv", "sia_bcg_2024"])

add("s25_unequal", "m3_unequal", "compare", {"chapter": "Mission 3 · Not equal", "title": "How exposed is each product?", "sides": [
    {"kicker": "AI chips · phone processors", "value": "High", "label": "need leading-edge fabs (Taiwan {{lt10_capacity.display}})", "bar": 69, "cue": "cutting-edge AI chip"},
    {"kicker": "Cars · washing machines", "value": "Lower", "label": "mostly older chips, made in many countries", "bar": 18, "cue": "washing machine"},
]}, sources=["sia_bcg_2024"])
add("s26_m3t", "m3_transition", "kinetic_text", {"align": "center", "lines": [
    {"text": "What if the flow of chips", "size": 60, "style": "body", "cue": "So what would"},
    {"text": "were suddenly interrupted?", "size": 76, "color": "risk", "cue": "suddenly interrupted"},
    {"text": "Mission 4 →", "size": 44, "color": "muted", "cue": "Mission four"},
]})

# ====================================================================== MISSION 4 (hypothetical)
card("s27_m4", "m4_card", "Mission 4", "A Hypothetical Disruption", "A thought experiment, not a prediction")
add("s28_m4q", "m4_question", "kinetic_text", {"align": "center", "chapter": "Mission 4 · Hypothetical scenario", "lines": [
    {"text": "HYPOTHETICAL SCENARIO", "size": 36, "style": "body", "color": "risk", "cue": "thought experiment"},
    {"text": "What if chip shipments from Taiwan were seriously disrupted?", "size": 60, "color": "accent", "cue": "What if"},
    {"text": "Not a prediction", "size": 48, "style": "body", "cue": "not a prediction"},
]})
add("s29_precedent", "m4_precedent", "compare", {"chapter": "Mission 4 · A real clue: 2021", "title": "The 2021 chip shortage (pandemic, not Taiwan)", "sides": [
    {"kicker": "Lost auto revenue · forecast", "value": "{{auto_2021.display}}", "label": "global auto industry, 2021", "cue": "lost"},
    {"kicker": "Vehicles not built · forecast", "value": "{{auto_2021.cars_display}}", "label": "AlixPartners", "cue": "never built"},
]}, sources=["alix_2021"])

# ---- Signature animation 4: domino-effect disruption
add("s30_domino", "m4_domino", "domino", {
    "title": "If the source stops", "title_cue": "Now imagine", "banner": "Hypothetical scenario",
    "source": "src", "shock_cue": "supply stops", "step": 1.6,
    "nodes": [
        {"id": "src", "label": "Advanced chips", "x": 330, "y": 560, "w": 280, "colour": "accent", "cue": "Now imagine", "tag": "supply stops"},
        {"id": "ph", "label": "Phones & PCs", "x": 780, "y": 320, "colour": "accent3", "cue": "Now imagine", "offset": 0.4, "tag": "launches slip"},
        {"id": "cl", "label": "Cloud & AI", "x": 780, "y": 560, "colour": "accent2", "cue": "Now imagine", "offset": 0.7, "tag": "no new servers"},
        {"id": "car", "label": "Carmakers", "x": 780, "y": 800, "colour": "accent3", "cue": "Now imagine", "offset": 1.0, "tag": "lines idle"},
        {"id": "pr", "label": "Prices", "x": 1230, "y": 440, "colour": "accent", "cue": "Now imagine", "offset": 1.3, "tag": "rise"},
        {"id": "jobs", "label": "Consumers", "x": 1230, "y": 700, "colour": "accent3", "cue": "Now imagine", "offset": 1.6, "tag": "pay more, wait longer"},
        {"id": "oth", "label": "Other industries", "x": 1640, "y": 300, "w": 300, "colour": "accent2", "cue": "Now imagine", "offset": 1.9, "tag": "spillover"},
    ],
    "edges": [["src", "ph"], ["src", "cl"], ["src", "car"], ["ph", "pr"], ["cl", "pr"], ["car", "pr"], ["car", "jobs"], ["pr", "jobs"], ["pr", "oth"]],
    "precedent": {"title": "Real precedent · 2021", "value": "{{auto_2021.display}}", "label": "auto revenue lost (forecast)", "cue": "industries that never"},
}, sources=["alix_2021"], sfx=[{"kind": "hit", "cue": "supply stops", "gain": 0.3}])

# ---- PRESENTER C: draws a supply chain and shows the disruption propagating
add("p31_chain", "m4_chain", "presenter", {
    "title": "Break one link", "title_cue": "draw that chain",
    "enter": {"from": "left", "cue": "Let's draw"},
    "items": [
        {"text": "HYPOTHETICAL SCENARIO", "x": 540, "y": 340, "size": 26, "colour": "risk", "cue": "Let's draw"},
        {"box": [540, 400, 300, 120], "label": "TAIWAN FABS", "colour": "accent", "cue": "Taiwan's fabs"},
        {"arrow": [[845, 460], [915, 460]], "bend": 0.0, "colour": "ink", "cue": "Then packaging"},
        {"box": [920, 400, 300, 120], "label": "PACKAGING", "colour": "accent3", "cue": "Then packaging"},
        {"arrow": [[1225, 460], [1295, 460]], "bend": 0.0, "colour": "ink", "cue": "device makers"},
        {"box": [1300, 400, 330, 120], "label": "DEVICE MAKERS", "colour": "accent2", "cue": "device makers"},
        {"arrow": [[1400, 525], [1290, 640]], "bend": 0.0, "colour": "ink", "cue": "the stores"},
        {"box": [1060, 645, 280, 120], "label": "STORES", "colour": "accent3", "cue": "the stores"},
        {"arrow": [[1540, 525], [1600, 640]], "bend": 0.0, "colour": "ink", "cue": "data centers"},
        {"box": [1420, 645, 340, 120], "label": "DATA CENTERS", "colour": "accent2", "cue": "data centers"},
        {"stroke": "M 862 425 L 898 495 M 898 425 L 862 495", "colour": "risk", "w": 9, "cue": "break the very first"},
        {"shock": [[700, 460], [1070, 460], [1465, 460], [1200, 705]], "speed": 750, "cue": "watch the shock"},
        {"shock": [[1465, 460], [1590, 705]], "speed": 750, "cue": "down the line"},
        {"text": "EVERY BOX AFTER THE BREAK TURNS RED", "x": 600, "y": 900, "size": 36, "colour": "risk", "cue": "down the line"},
    ],
    "scale": 0.86, "floor": 1040, "board": BOARD, "speed": 1500,
})

add("s32_estimate", "m4_estimate", "compare", {"chapter": "Mission 4 · Bloomberg Economics scenarios (2024)", "title": "Estimated hit to world GDP in year one", "sides": [
    {"kicker": "Scenario: war over Taiwan", "value": "{{bloomberg_scenarios.display}}", "label": "{{bloomberg_scenarios.pct_display}} · estimate", "bar": 10, "cue": "a war over Taiwan"},
    {"kicker": "Scenario: blockade", "value": "{{bloomberg_scenarios.blockade_short}}", "label": "of world GDP · estimate", "bar": 5, "cue": "Even a"},
]}, sources=["bloomberg_2024"])
add("s33_m4t", "m4_transition", "kinetic_text", {"align": "center", "lines": [
    {"text": "Numbers like that explain", "size": 56, "style": "body", "cue": "Numbers like"},
    {"text": "the race to make chips at home", "size": 72, "color": "accent2", "cue": "racing"},
    {"text": "Mission 5 →", "size": 44, "color": "muted", "cue": "Mission five"},
]})

# ====================================================================== MISSION 5
card("s34_m5", "m5_card", "Mission 5", "The Race to Diversify", "Can the world spread the risk?")
question("s35_m5q", "m5_question", "Mission 5 · The race to diversify",
         "Can the world spread the risk?", "Diversification is expensive, and slow",
         "Can the world", "It matters")

# ---- PRESENTER D: interacts with an animated map of investment (signature animation 5, part 1)
add("p36_race", "m5_race", "presenter", {
    "title": "The race to build fabs outside Taiwan", "title_cue": "map the race",
    "enter": {"from": "left", "cue": "Let's map"},
    "items": [
        {"map": {"lon": 5, "lat": 28, "span": 300}, "rect": [520, 330, 1280, 600], "countries": ["USA", "TWN"],
         "highlight": {"USA": "accent2", "TWN": "accent"}, "points": 150, "cue": "map the race"},
        {"text": "CHIPS ACT: {{chips_act_figs.display}}", "x": 540, "y": 370, "size": 30, "colour": "accent2", "cue": "CHIPS Act"},
        {"text": "{{chips_act_figs.mfg_display}} FOR FACTORIES", "x": 540, "y": 410, "size": 24, "colour": "muted", "cue": "for manufacturing"},
        {"bubble": [-112.0, 33.4], "ll": True, "value": 165, "max_value": 165, "max_r": 78, "label": "TSMC ARIZONA",
         "display": "{{tsmc_us_165.display}}", "colour": "accent", "hold": 1.6, "side": "right", "cue": "in Arizona"},
        {"map": {"lon": 5, "lat": 28, "span": 300}, "rect": [520, 330, 1280, 600], "countries": ["JPN"],
         "highlight": {"JPN": "accent2"}, "points": 120, "cue": "In Japan"},
        {"bubble": [130.7, 32.8], "ll": True, "value": 20, "max_value": 165, "max_r": 78, "label": "KUMAMOTO",
         "display": "{{japan_jasm.display}}", "colour": "accent", "hold": 1.4, "cue": "Kumamoto venture"},
        {"map": {"lon": 5, "lat": 28, "span": 300}, "rect": [520, 330, 1280, 600], "countries": ["DEU"],
         "highlight": {"DEU": "accent2"}, "points": 100, "cue": "In Germany"},
        {"pin": [13.7, 51.05], "ll": True, "label": "ESMC DRESDEN", "display": "end-2027 target", "colour": "accent", "r": 16, "cue": "rising in"},
    ],
    "scale": 0.86, "floor": 1040, "board": BOARD, "speed": 1500,
}, sources=["chips_act", "tsmc_165bn", "jasm", "esmc", "natural_earth"], assets=GEO)

# ---- Race-to-diversify map (signature animation 5, part 2)
add("s37_race_map", "m5_europe", "map", {
    "chapter": "Mission 5 · The race to diversify", "geo": "world",
    "views": [{"lon": 10, "lat": 48, "span": 60}, {"lon": 124, "lat": 30, "span": 48, "cue": "South Korea"}],
    "move": 3.0,
    "highlights": {
        "DEU": {"colour": "accent2", "cue": "Europe wants"}, "FRA": {"colour": "accent2", "cue": "Europe wants", "offset": 0.2},
        "ITA": {"colour": "accent2", "cue": "Europe wants", "offset": 0.3}, "NLD": {"colour": "accent2", "cue": "Europe wants", "offset": 0.4},
        "IRL": {"colour": "accent2", "cue": "Europe wants", "offset": 0.5},
        "KOR": {"colour": "accent3", "cue": "South Korea"}, "TWN": {"colour": "accent", "cue": "Taiwan keeps"},
    },
    "markers": [
        {"lon": 10.0, "lat": 50.0, "label": "EU target", "sublabel": "{{eu_target.display}} of global production", "cue": "Europe wants", "size": 40},
        {"lon": 127.5, "lat": 36.5, "label": "South Korea", "sublabel": "memory + its own foundries", "cue": "South Korea", "size": 34},
        {"lon": 121.0, "lat": 23.7, "label": "Taiwan", "sublabel": "newest fabs stay at home", "cue": "Taiwan keeps", "size": 34, "anchor": "end"},
    ],
}, sources=["oecd_chips", "tsmc_4q25_call", "natural_earth"], assets=GEO)

add("s38_limits", "m5_limits", "compare", {"chapter": "Mission 5 · The limit", "title": "Logic below 10 nm: share of global capacity (SIA/BCG)", "sides": [
    {"kicker": "Taiwan", "value": "{{lt10_capacity.display}} → {{lt10_capacity.tw32_display}}", "label": "2022 → 2032 forecast", "bar": 47, "cue": "still has Taiwan"},
    {"kicker": "United States", "value": "{{lt10_capacity.us22_display}} → {{lt10_capacity.us32_display}}", "label": "2022 → 2032 forecast", "bar": 28, "cue": "United States at"},
]}, sources=["sia_bcg_2024"])
add("s39_why", "m5_why", "kinetic_text", {"align": "center", "chapter": "Mission 5 · Why so slow", "lines": [
    {"text": "The hard part isn't the building", "size": 60, "color": "accent", "cue": "Why so slow"},
    {"text": "Engineers", "size": 48, "style": "body", "cue": "the engineers"},
    {"text": "Suppliers", "size": 48, "style": "body", "cue": "the suppliers"},
    {"text": "Years of yield learning", "size": 48, "style": "body", "cue": "yield learning"},
    {"text": "Taiwan: decades of it", "size": 56, "color": "accent", "cue": "spent decades"},
]})

# ====================================================================== PAYOFF
add("s40_payoff", "payoff", "map", {
    "chapter": "Mission complete", "geo": "world",
    "views": [{"lon": 20, "lat": 25, "span": 330}, {"lon": 121.0, "lat": 23.7, "span": 14, "cue": "smaller than Switzerland"}],
    "move": 4.0,
    "highlights": {"TWN": {"colour": "accent", "cue": "mission complete"}},
    "markers": [{"lon": 121.0, "lat": 23.7, "label": "Not every chip", "sublabel": "the hardest ones, at unmatched scale",
                 "cue": "hardest", "size": 40}],
}, sources=["sia_bcg_2024", "natural_earth"], assets=GEO)
add("s41_end", "teaser", "end_card", {
    "words": ["Next time:", "another hidden link"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description",
    "brand_cue": {"cue": "This is The Hidden Economics"}})

OUT.write_text("# GENERATED by tools/gen_taiwan_storyboard.py; edit the generator, not this file.\n"
               "# Mission-based storyboard for Episode 07. The channel intro is inserted automatically after the hook.\n"
               + yaml.safe_dump({"scenes": scenes}, sort_keys=False, allow_unicode=True, width=200))
print(f"{len(scenes)} scenes -> {OUT}")
