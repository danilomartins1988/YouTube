# Cartoon scenes for Episode 09 (exec'd by tools/gen_cables_storyboard.py, which provides `scenes`, `C`, `INTER`).
# Each entry REPLACES the scene with the same id (or is inserted); ids listed in DROP are removed.
# Coordinates are in the CartoonOcean world (sea surface y=380, seabed y≈930, view 1920x1080 at zoom 1).

def cart(id_, seg, params, sources=(), sfx=None):
    s = {"id": id_, "segment": seg, "type": "engine_cartoon", "params": params}
    if sfx:
        s["sfx"] = sfx
    if sources:
        s["sources"] = list(sources)
    s["assets"] = list(INTER)
    return s


CART = [
    # ---------------------------------------------------------------- hook: from the sky down to the seabed
    cart("s01_seabed", "h_question", {
        "worldW": 3840, "coasts": {"left": True, "right": True}, "fish": 5,
        "cam": [{"at": 0, "x": 1500, "y": -260, "zoom": 1.0}, {"at": C("but at the bottom", -0.4), "x": 1700, "y": 640, "zoom": 1.1, "dur": 2.6}],
        "drift": 10,
        "cables": [{"lightAt": 0.0}],
        "actors": [{"kind": "satellite", "x": 1450, "y": -420, "beamAt": C("in the sky")}, {"kind": "whale", "x": [[0, 2400], [12, 1500]], "y": 720, "flip": True},
                   {"kind": "cargo", "x": [[0, 900], [12, 1400]], "scale": 0.8}],
        "callouts": [{"text": "In the sky?", "x": 1700, "y": -480, "at": C("in the sky"), "tail": [1520, -420], "color": "gold"},
                     {"text": "No: down here!", "sub": "the internet's cables", "x": 1950, "y": 780, "at": C("bottom of the ocean"), "tail": [1880, 905], "color": "green"}]},
        sfx=[{"kind": "hit", "cue": "bottom of the ocean", "gain": 0.3}]),
    # ---------------------------------------------------------------- part 1
    cart("s05_m1q", "m1_question", {
        "worldW": 1920, "coasts": {"left": True, "right": True}, "fish": 3, "sea": 420,
        "cam": [{"at": 0, "x": 960, "y": 380, "zoom": 1.0}, {"at": C("It mostly"), "x": 960, "y": 560, "zoom": 1.05, "dur": 2.0}],
        "cables": [{"lightAt": 0.3}],
        "actors": [{"kind": "satellite", "x": 960, "y": 130, "beamAt": C("satellites")}, {"kind": "fishing", "x": [[0, 700], [10, 1100]], "scale": 0.8}],
        "callouts": [{"text": "Satellites?", "x": 1300, "y": 120, "at": C("satellites"), "tail": [1060, 130], "color": "gold"},
                     {"text": "Mostly not!", "x": 960, "y": 820, "at": C("mostly doesn't"), "tail": [960, 920], "color": "green", "size": 44}]}),
    cart("s06_sat", "m1_satellite", {
        "worldW": 1920, "coasts": {"left": True, "right": True}, "fish": 3,
        "cam": [{"at": 0, "x": 960, "y": 330, "zoom": 1.1}, {"at": C("TeleGeography"), "x": 960, "y": 640, "zoom": 1.1, "dur": 2.4}],
        "cables": [{"lightAt": 0.0}, {"lightAt": 0.4, "dy": 26}],
        "actors": [{"kind": "satellite", "x": 960, "y": 140, "beamAt": C("Satellites carry")}],
        "callouts": [{"text": "{{satellite.display}}", "sub": "satellites' share of U.S. international capacity (FCC)", "x": 1320, "y": 160, "at": C("government"), "tail": [1060, 140], "color": "gold", "size": 52},
                     {"text": "{{tg_check.display}}", "sub": "of traffic between continents: by cable (TeleGeography)", "x": 960, "y": 760, "at": C("between continents"), "tail": [960, 905], "color": "green", "size": 52}]},
        sources=["tg_faq", "tg_myth_2023"]),
    cart("s09_size", "m1_discovery", {
        "worldW": 2600, "coasts": {"left": True}, "fish": 3,
        "cam": [{"at": 0, "x": 1700, "y": 760, "zoom": 1.5}, {"at": C("Near the shore", -0.3), "x": 620, "y": 520, "zoom": 1.3, "dur": 2.6},
                {"at": C("built to last"), "x": 1200, "y": 560, "zoom": 1.0, "dur": 2.4}],
        "cables": [{"lightAt": 0.0, "color": "#2B3A5C"}],
        "actors": [{"kind": "fishing", "x": [[0, 900], [20, 600]], "scale": 0.8, "flip": True}, {"kind": "cargo", "x": [[0, 160], [20, 260]], "scale": 0.6, "anchorAt": C("anchors are")}],
        "callouts": [{"text": "≈ a garden hose", "sub": "for most of the journey", "x": 1700, "y": 760, "at": C("as wide as"), "until": C("Near the shore", -0.5), "tail": [1700, 910], "color": "white"},
                     {"text": "glass + plastic + steel wire", "x": 1700, "y": 630, "at": C("thin glass"), "until": C("Near the shore", -0.5), "color": "white", "size": 26},
                     {"text": "Extra armor", "sub": "near the shore: fishing boats and anchors", "x": 760, "y": 470, "at": C("extra armor"), "tail": [640, 560], "color": "gold"},
                     {"text": "Built to last {{design_life.display}}+", "x": 1300, "y": 220, "at": C("built to last"), "color": "green", "screen": True, "size": 44}]},
        sources=["tg_faq"]),
    # ---------------------------------------------------------------- part 2
    cart("s12_m2q", "m2_question", {
        "zones": [{"set": "beach", "x0": -1600, "x1": 1300}, {"set": "datacenter", "x0": 1300, "x1": 5000}], "worldW": 2600,
        "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.1}, {"at": C("whoever owns"), "x": 1300, "y": 520, "zoom": 0.9, "dur": 2.4}], "drift": 0,
        "items": [{"kind": "sign", "x": 420, "y": 640, "text": "CABLE LANDS HERE", "post": True, "color": "#FFF59D", "size": 28, "at": 0.2},
                  {"kind": "arrow", "from": [300, 940], "to": [1700, 940], "at": 0.4, "color": "cyan"},
                  {"kind": "letters", "x": 900, "y": 300, "text": "OWNER?", "size": 90, "color": "gold", "at": C("Who owns")},
                  {"kind": "device", "type": "server", "x": 1800, "y": 860, "at": 0.5, "text": "DATA CENTER"},
                  {"kind": "sign", "x": 1300, "y": 420, "text": "WHO CAN USE IT?", "sub": "and how much it costs", "at": C("whoever owns"), "color": "#FFCDD2", "size": 34, "hang": True, "swing": True}],
        "callouts": [{"text": "Whose cable is this?", "x": 960, "y": 150, "at": C("Who owns"), "color": "gold", "size": 44, "screen": True, "until": C("whoever owns", -0.3)},
                     {"text": "The owner decides: who uses it + what it costs", "x": 960, "y": 150, "at": C("whoever owns"), "color": "white", "screen": True, "size": 38}]}),
    # ---------------------------------------------------------------- part 3
    cart("s20_m3q", "m3_question", {
        "worldW": 3000, "coasts": {"left": True}, "fish": 3,
        "cam": [{"at": 0, "x": 1000, "y": 560, "zoom": 1.0}],
        "drift": 40,
        "cables": [{"follow": 0, "lightAt": 0.5}],
        "actors": [{"kind": "layer", "x": [[0, 1100], [14, 2000]], "name": "Cable ship"}],
        "callouts": [{"text": "Laying a cable", "sub": "spooled out from the ship onto the seabed", "x": 1100, "y": 230, "at": C("who builds"), "color": "gold", "screen": True},
                     {"text": "Very few companies can do it", "x": 960, "y": 1000, "at": C("Very few"), "color": "white", "screen": True, "size": 36}]}),
    cart("s23_repair", "m3_repair", {
        "worldW": 2800, "coasts": {"left": True}, "fish": 3,
        "cam": [{"at": 0, "x": 1400, "y": 640, "zoom": 1.0}, {"at": C("find the damaged"), "x": 1350, "y": 640, "zoom": 1.15, "dur": 2.0},
                {"at": C("bring it up"), "x": 1350, "y": 470, "zoom": 1.25, "dur": 2.2}, {"at": C("stationed around"), "x": 1300, "y": 560, "zoom": 1.0, "dur": 2.4}],
        "cables": [{"lightAt": 0.0, "breakAt": 0.0, "breakX": 1350, "repairAt": C("repair it at sea", 2.2)}],
        "actors": [{"kind": "repair", "x": [[0, 2700], [{"cue": "to the spot"}, 1230]], "name": "Repair ship",
                    "grapple": {"at": C("find the damaged"), "lift": C("bring it up"), "splice": C("repair it at sea"), "lower": C("stationed around")}}],
        "callouts": [{"text": "Broken!", "x": 1350, "y": 800, "at": 0.4, "until": C("has to sail"), "tail": [1350, 905], "color": "risk"},
                     {"text": "Fixed at sea", "x": 1650, "y": 300, "at": C("repair it at sea", 1.0), "until": C("stationed around"), "tail": [1400, 400], "color": "green"},
                     {"text": "Baltic Sea, Nov 2024", "sub": "two cables damaged · both repaired {{repair_ships.display}}", "x": 960, "y": 230, "at": C("Baltic Sea"), "color": "gold", "screen": True}]},
        sources=["icpc_media"]),
    # ---------------------------------------------------------------- part 4
    cart("s26_m4q", "m4_question", {
        "worldW": 1920, "coasts": {"left": True, "right": True}, "fish": 3,
        "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.0}, {"at": C("switch off"), "x": 1400, "y": 420, "zoom": 1.15, "dur": 2.0}],
        "cables": [{"lightAt": 0.0, "breakAt": C("One cut"), "breakX": 900}],
        "coasts_dark": True,
        "actors": [{"kind": "fishing", "x": [[0, 1300], [8, 760]], "flip": True, "netAt": 0.6}],
        "callouts": [{"text": "Snap!", "x": 900, "y": 790, "at": C("One cut"), "until": C("switch off"), "tail": [900, 905], "color": "risk", "size": 44},
                     {"text": "Lights out", "x": 1590, "y": 160, "at": C("switch off", 0.3), "tail": [1590, 290], "color": "risk"}]}),
    cart("s27_faults", "m4_faults", {
        "worldW": 2400, "coasts": {"left": True}, "fish": 3,
        "cam": [{"at": 0, "x": 1300, "y": 560, "zoom": 1.0}],
        "drift": 14,
        "cables": [{"lightAt": 0.0, "breakAt": C("Just everyday", 0.6), "breakX": 1500}],
        "actors": [{"kind": "fishing", "x": [[0, 900], [20, 1300]], "netAt": C("fishing gear")},
                   {"kind": "cargo", "x": [[0, 1750], [{"cue": "Just everyday"}, 1750], [{"cue": "Just everyday", "offset": 3}, 1560]], "scale": 0.8, "anchorAt": C("ships' anchors")}],
        "callouts": [{"text": "{{faults.display}} faults a year", "sub": "worldwide (ICPC)", "x": 960, "y": 220, "at": C("cable faults"), "color": "gold", "screen": True, "size": 44},
                     {"text": "{{faults.human_display}}: accidents", "sub": "mostly fishing gear and ships' anchors", "x": 960, "y": 1000, "at": C("accidents"), "color": "white", "screen": True},
                     {"text": "Sabotage? Rare.", "x": 1560, "y": 380, "at": C("Not sabotage"), "until": C("Just everyday", 2.0), "color": "green", "screen": True}]},
        sources=["icpc_media"]),
    cart("s28_redsea", "m4_redsea", {
        "worldW": 2400, "fish": 2, "banner": {"text": "Red Sea, February 2024", "sub": "a cargo ship's dragging anchor"},
        "cam": [{"at": 0, "x": 1100, "y": 420, "zoom": 1.0}, {"at": C("dragging anchor"), "x": 1250, "y": 640, "zoom": 1.05, "dur": 2.4}],
        "cables": [{"lightAt": 0.0, "breakAt": C("cut three", 0.0), "breakX": 1250, "color": "#2B3A5C"},
                   {"lightAt": 0.2, "dy": -30, "breakAt": C("Seacom"), "breakX": 1290},
                   {"lightAt": 0.4, "dy": -60, "breakAt": C("E I G"), "breakX": 1330, "color": "#3A2B5C"},
                   {"lightAt": 0.1, "dy": 40, "color": "#1E4A44"}],
        "actors": [{"kind": "cargo", "name": "Rubymar", "x": [[0, 900], [{"cue": "dragging anchor"}, 1080], [{"cue": "E I G", "offset": 1}, 1420]],
                    "smokeAt": C("missile attack"), "anchorAt": C("later sank", -1.5), "sinkAt": C("later sank")}],
        "callouts": [{"text": "Seacom · AAE-1 · EIG", "x": 1290, "y": 1000, "at": C("Seacom"), "color": "risk"},
                     {"text": "{{redsea.display}} of the region's traffic", "sub": "estimate by internet provider HGC", "x": 1300, "y": 240, "at": C("estimated"), "color": "gold", "screen": True}]},
        sources=["redsea_2024"], sfx=[{"kind": "hit", "cue": "cut three", "gain": 0.3}]),
    cart("s30_tonga", "m4_tonga", {
        "worldW": 2400, "fish": 2, "banner": {"text": "Tonga, January 2022", "sub": "an eruption tore its cable apart"},
        "cam": [{"at": 0, "x": 1300, "y": 420, "zoom": 1.0}, {"at": C("tore"), "x": 1150, "y": 640, "zoom": 1.05, "dur": 2.0},
                {"at": C("was gone"), "x": 1400, "y": 380, "zoom": 1.1, "dur": 2.0}, {"at": C("It took"), "x": 1300, "y": 520, "zoom": 0.95, "dur": 2.0}],
        "shake": [{"at": C("erupted"), "dur": 2.0, "amp": 16}],
        "cables": [{"from": 1480, "to": 2700, "lightAt": 0.0, "breakAt": C("tore"), "breakX": 1900, "shred": True, "repairAt": C("new cable")}],
        "actors": [{"kind": "island", "x": 1400, "w": 380, "darkAt": C("was gone"), "lightAt": C("new cable")},
                   {"kind": "volcano", "x": 700, "eruptAt": C("erupted"), "scale": 1.1},
                   {"kind": "repair", "at": C("It took"), "x": [[0, 2600], [{"cue": "It took", "offset": 4}, 1950]], "flip": True}],
        "callouts": [{"text": "{{tonga.display}} of cable torn", "x": 1950, "y": 780, "at": C("tore", 0.6), "until": C("It took"), "tail": [1950, 900], "color": "risk"},
                     {"text": "Offline {{tonga.weeks_display}}", "x": 1400, "y": 150, "at": C("It took"), "color": "gold"},
                     {"text": "{{tonga.replaced_display}} of new cable", "x": 1950, "y": 780, "at": C("new cable"), "tail": [1950, 900], "color": "green"}]},
        sources=["tonga_techxplore", "tonga_aljazeera"], sfx=[{"kind": "hit", "cue": "erupted", "gain": 0.4}]),
    # ---------------------------------------------------------------- payoff: one long journey of light
    cart("s39_payoff", "payoff", {
        "worldW": 5200, "coasts": {"left": True, "right": True}, "fish": 7,
        "cam": [{"at": 0, "x": 300, "y": 230, "zoom": 1.2}, {"at": C("glass, plastic"), "x": 900, "y": 760, "zoom": 1.25, "dur": 2.6},
                {"at": C("built by a few"), "x": 1800, "y": 600, "zoom": 1.0, "dur": 3.0}, {"at": C("repaired by"), "x": 2900, "y": 520, "zoom": 1.0, "dur": 3.0},
                {"at": C("Every time"), "x": 4100, "y": 600, "zoom": 1.0, "dur": 3.0}, {"at": C("as pulses"), "x": 4850, "y": 260, "zoom": 1.2, "dur": 3.0}],
        "drift": 0,
        "cables": [{"lightAt": 0.0}],
        "actors": [{"kind": "layer", "x": [[0, 1700], [40, 2200]], "scale": 0.8}, {"kind": "repair", "x": [[0, 3200], [40, 2700]], "flip": True, "scale": 0.8},
                   {"kind": "whale", "x": [[0, 3900], [40, 3300]], "y": 700, "flip": True}, {"kind": "cargo", "x": [[0, 4200], [40, 4600]], "scale": 0.7}],
        "callouts": [{"text": "Not a cloud", "x": 300, "y": 120, "at": C("not a cloud"), "until": C("glass, plastic", 0.5), "color": "white"},
                     {"text": "glass · plastic · steel", "x": 900, "y": 790, "at": C("glass, plastic", 0.5), "until": C("built by a few", 0.5), "tail": [900, 880], "color": "white"},
                     {"text": "Built by a few companies", "x": 1900, "y": 230, "at": C("built by a few", 0.8), "until": C("repaired by", 0.4), "color": "gold"},
                     {"text": "Paid for by tech giants", "x": 1900, "y": 330, "at": C("paid for"), "until": C("repaired by", 0.4), "color": "gold"},
                     {"text": "Fixed by a small fleet", "x": 2900, "y": 200, "at": C("repaired by", 0.8), "until": C("Every time"), "color": "green"},
                     {"text": "Argued over by governments", "x": 2900, "y": 300, "at": C("argued over"), "until": C("Every time"), "color": "risk"},
                     {"text": "Your message, as light", "x": 960, "y": 230, "at": C("as pulses"), "color": "green", "size": 44, "screen": True}]},
        sources=["itu_2025", "tg_faq"]),
]

DROP = {"s03_missions"}
# the question card of part 5 becomes a plain line (no "THE QUESTION / WHY IT MATTERS" labels)
Q5 = {"id": "s34_m5q", "segment": "m5_question", "type": "kinetic_text", "params": {"align": "center", "lines": [
    {"text": "Why governments now fight", "size": 56, "style": "body", "cue": "Which is why"},
    {"text": "over the seabed", "size": 84, "color": "accent", "cue": "over the seabed"},
    {"text": "your data passes through, and lands in, other countries", "size": 38, "style": "body", "color": "muted", "cue": "passes through"}]},
    "assets": list(INTER)}
by_id = {c["id"]: c for c in CART + [Q5]}
scenes[:] = [by_id.get(s["id"], s) for s in scenes if s["id"] not in DROP]
for s in scenes:
    if s["params"].pop("coasts_dark", None):
        s["params"]["coasts"]["darkAt"] = C("switch off", 0.3)
