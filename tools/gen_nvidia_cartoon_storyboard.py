"""Generates projects/how-nvidia-took-over-the-ai-economy/deliverables/documentary_presenter/storyboard.yaml (Ep06, cartoon).

Bespoke CartoonStage worlds for the Nvidia story: a gamer's bedroom (the GPU's origin), a cartoon web where a chatbot
answers, data centers full of racks, the stock-exchange floor for the $5 trillion moment, a research lab, a chip fab in
Arizona, construction sites for AI data centers, an export barrier for China. The signature animations of the earlier
cut (CPU vs GPU, the CUDA stack, revenue mix columns, margin line, supply chain, chip landscape) and the four presenter
sequences are kept from tools/data/nvidia_presenter_storyboard_v2.yaml. No real person is drawn.
Run: python tools/gen_nvidia_cartoon_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "projects/how-nvidia-took-over-the-ai-economy/deliverables/documentary_presenter/storyboard.yaml"
BASE = {s["id"]: s for s in yaml.safe_load((ROOT / "tools/data/nvidia_presenter_storyboard_v2.yaml").read_text())["scenes"]}
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}


def keep(*ids):
    for i in ids:
        cartoon_kit.scenes.append(BASE[i])


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 1, "skin": k, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


GPU = lambda x, y=640, **kw: it("device", type="chip", x=x, y=y, color="#76B900", **kw)

# ====================================================================== OPENING
stage("s01_network", "open_network", {
    "zones": [Z("web", -1600, 1500), Z("datacenter", 1500, 3200), Z("fab", 3200, 7000)], "worldW": 4400,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.1}, {"at": C("Behind the labs"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.6},
            {"at": C("one supplier"), "x": 3700, "y": 520, "zoom": 1.05, "dur": 2.6}], "drift": 0,
    "items": [it("browser", x=760, y=440, at=0.2, url="ask-the-chatbot.ai", page="chat", w=700),
              it("coins", **{"from": [1000, 500], "to": [2300, 500]}, at=C("does the math"), rate=4, shape="chip"),
              it("sign", x=1150, y=780, text="AI LABS", at=C("AI labs"), color="#E1BEE7", size=30),
              it("device", type="server", x=2300, y=F, at=C("cloud companies"), text="CLOUD + DATA CENTERS"),
              GPU(3700, 620, at=C("one supplier"), text="ONE SUPPLIER", scale=1.6)],
    "callouts": [co("A machine somewhere does the math", 960, 150, C("does the math"), "white", screen=True, until=C("Behind the labs", -0.3)),
                 co("Behind them all: one supplier", 960, 150, C("one supplier"), "gold", screen=True, size=44)]})
stage("s02_value", "open_value", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 420, "zoom": 1.15}, {"at": C("first company"), "x": 960, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [
              it("counter", x=960, y=300, at=0.3, steps=[[0, 0], [0.6, 0], [3.2, 5]], prefix="$", suffix=" trillion", text="market value, October 2025 (AP)"),
              it("burst", x=960, y=300, at=3.3),
              *crowd([380, 520, 1400, 1540], "cheer", at=C("first company"), tie=True)],
    "callouts": [co("The first company ever worth $5 trillion", 960, 960, C("first company"), "gold", screen=True, size=42)]},
    sources=["ap_5tn"])
stage("s03_revenue", "open_revenue", {
    "zones": [Z("datacenter")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.0}], "drift": 4,
    "items": [it("stack", x=560, at=0.3, h=60, text="{{revenue_fy2023.display}}", sub="three years earlier (FY2023)"),
              it("stack", x=1360, at=C("it sold"), h=[[0, 60], [{"cue": "it sold"}, 60], [{"cue": "it sold", "offset": 3}, 480]], text="{{revenue_fy2026.display}}", sub="last full fiscal year (FY2026)", color="gold"),
              it("letters", x=960, y=420, text="{{revenue_fy2023.multiple_display}}", at=C("eight times"), size=110, color="green")],
    "callouts": [co("Sales: about eight times more in three years", 960, 150, C("eight times"), "green", screen=True)]},
    sources=["nvda_q4fy26", "nvda_xbrl"])
stage("s04_question", "open_question", {
    "zones": [Z("den", -1600, 1500, cx=760), Z("datacenter", 1500, 5000)], "worldW": 2800,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.1}, {"at": C("center of the AI"), "x": 2050, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("person", x=400, pose="type", at=0.2, scale=0.9, hair=3),
              it("sign", x=760, y=180, text="VIDEO GAME GRAPHICS", at=C("video game"), color="#B2FF59", size=32),
              GPU(2050, 620, at=C("center of the AI", -0.3), text="AT THE CENTER OF AI?", scale=1.3),
              it("letters", x=2450, y=300, text="?", at=C("stay there"), size=120, color="gold")],
    "callouts": [co("A gaming company…", 960, 150, C("gaming company"), "white", screen=True, until=C("center of the AI", -0.3)),
                 co("…at the center of the AI economy?", 960, 150, C("center of the AI"), "gold", screen=True, size=42)]})
card("s05_act2", "a2_card", "From Gaming to AI", "Millions of pixels, all at once")
stage("s06_origins", "a2_origins", {
    "zones": [Z("den", cx=1100)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}], "drift": 4,
    "items": [it("calendar", x=300, y=300, at=0.2, scale=0.8, pages=[[0, "{{founded_1993.display}}", "FOUNDED"], [{"cue": "it launched"}, "{{gpu_1999.display}}", "FIRST GPU"]]),
              GPU(560, 760, at=C("it launched"), text="THE FIRST GPU", scale=0.8),
              it("sign", x=1600, y=230, text="CHIPS FOR GRAPHICS", sub="California, three engineers", at=C("computer graphics"), color="#B2FF59", size=30),
              *crowd([1600], "cheer", at=C("drawing video games"), hair=2)],
    "callouts": [co("Its business: drawing video games, fast", 960, 960, C("drawing video games"), "white", screen=True)]},
    sources=["nvda_10k_fy2026"])
keep("p07_draw_parallel", "s08_cpu_gpu")
stage("s09_alexnet", "a2_alexnet", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("Researchers took"), "x": 1450, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("sign", x=700, y=260, text="× × × × ×", sub="piles of multiplications, side by side", at=C("enormous piles"), color="#FFF59D", size=40),
              GPU(500, 720, at=C("AlexNet"), text="GAMING CARD", scale=0.75), GPU(800, 720, at=C("AlexNet", 0.3), text="GAMING CARD", scale=0.75),
              it("sign", x=1300, y=330, text="IMAGE CONTEST: WON", at=C("won a famous"), color="#C8E6C9", size=34, hang=True, swing=True),
              *crowd([1250, 1380], "cheer", at=C("won a famous"), glasses=True),
              it("device", type="chip", x=1950, y=640, at=C("Tensor Cores"), color="gold", text="FIRST TENSOR CORE CHIP ({{tensor_2017.display}})", scale=1.1)],
    "callouts": [co("{{alexnet.display}}: AlexNet, trained on two gaming cards", 960, 150, C("AlexNet"), "white", screen=True, until=C("Tensor Cores", -0.3)),
                 co("Built from the ground up for AI", 960, 150, C("Tensor Cores"), "gold", screen=True)]},
    sources=["alexnet_2012"])
card("s10_act3", "a3_card", "The CUDA Advantage", "Software that keeps customers close")
keep("s11_stack", "s12_switch")
stage("s13_flywheel", "a3_flywheel", {
    "zones": [Z("office")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}], "drift": 4,
    "items": [it("clock", x=960, y=420, at=0.3, period=3.0, text="THE WHEEL"),
              it("sign", x=420, y=280, text="MORE DEVELOPERS", at=C("More developers"), color="#BBDEFB", size=28),
              it("sign", x=1500, y=280, text="MORE SOFTWARE", at=C("More software"), color="#C8E6C9", size=28),
              it("sign", x=1500, y=640, text="MORE CUSTOMERS", at=C("More customers"), color="#FFF59D", size=28),
              it("sign", x=420, y=640, text="NEW CHIPS + TOOLS", at=C("new chips"), color="#E1BEE7", size=28),
              *crowd([250, 1700], "type", at=C("More developers"))],
    "callouts": [co("A network effect", 960, 150, C("network effect"), "gold", screen=True, until=C("feeds itself", -0.3)),
                 co("The wheel feeds itself", 960, 150, C("feeds itself"), "green", screen=True)]})
card("s14_act4", "a4_card", "How Nvidia Makes Money", "Data centers, margins and systems")
keep("p15_build_revenue", "s16_mix", "p17_customers", "s18_margin")
stage("s19_why", "a4_why", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("Networking alone"), "x": 1450, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("sign", x=420, y=250, text="DEMAND > SUPPLY", at=C("Demand ran"), color="#FFCDD2", size=32, hang=True, swing=True),
              it("sign", x=960, y=250, text="HARD TO REPLACE", at=C("hard to replace"), color="#FFF59D", size=32, hang=True, swing=True),
              it("sign", x=1500, y=250, text="WHOLE SYSTEMS", sub="processors · networking · software", at=C("whole systems"), color="#C8E6C9", size=32, hang=True, swing=True),
              it("stack", x=1450, at=C("Networking alone"), h=[[0, 30], [{"cue": "Networking alone"}, 30], [{"cue": "Networking alone", "offset": 2}, 220]], text="{{dc_fy2026.networking_display}}", sub="networking, last fiscal year", color="gold"),
              it("stack", x=2000, at=C("reinvesting"), h=[[0, 30], [{"cue": "reinvesting"}, 30], [{"cue": "reinvesting", "offset": 2.5}, 420]], text="R&D {{rnd_total.display}}", sub="since it was founded", color="#E1BEE7")],
    "callouts": [co("Why so profitable?", 960, 960, C("Why so profitable"), "gold", screen=True)]},
    sources=["nvda_10k_fy2026"])
stage("s20_latest", "a4_latest", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.05}], "drift": 4,
    "items": [it("counter", x=760, y=300, at=0.3, steps=[[0, 0], [{"cue": "Nvidia brought in"}, 0], [{"cue": "Nvidia brought in", "offset": 2.5}, 96.2]], prefix="$", suffix="bn", decimals=1, text="quarter to July 2026"),
              it("chart", x=1400, y=420, w=560, h=330, at=0.5, dur=4, text="QUARTERLY REVENUE (schematic)", pts=[0.2, 0.3, 0.45, 0.6, 0.8, 0.95])],
    "callouts": [co("Up {{q2fy27.growth_spoken}} in a year", 960, 960, C("from a year earlier"), "green", screen=True, until=C("expected", -0.3)),
                 co("Next quarter expected: {{q2fy27.guide_display}}", 960, 960, C("expected"), "gold", screen=True)]},
    sources=["nvda_q2fy27"])
card("s21_act5", "a5_card", "The Global Supply Chain", "Designed in California, made in Asia")
# bespoke replacement for the old map (freeze at its start in the Nov 2026 render): one chip's journey, design -> wafer -> memory -> servers
stage("s22_chain", "a5_chain", {
    "zones": [Z("office", -1600, 1300), Z("fab", 1300, 2700, label="yellow"), Z("datacenter", 2700, 7000)], "worldW": 4400,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.05}, {"at": C("send the designs"), "x": 1900, "y": 520, "zoom": 1.0, "dur": 2.6},
            {"at": C("high bandwidth memory"), "x": 2500, "y": 520, "zoom": 1.05, "dur": 2.4},
            {"at": C("Contract manufacturers"), "x": 3600, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 6,
    "items": [it("sign", x=650, y=300, text="NVIDIA · CALIFORNIA", sub="designs, does not make", at=0.3, color="#C8E6C9", size=34),
              it("device", type="laptop", x=650, y=F, at=0.6),
              it("plane", x=[[0, 700], [{"cue": "send the designs"}, 700], [{"cue": "send the designs", "offset": 3}, 1700], [{"cue": "send the designs", "offset": 5}, 2400]],
                 y=[[0, 420], [{"cue": "send the designs", "offset": 3}, 250], [{"cue": "send the designs", "offset": 5}, -200]],
                 at=C("send the designs", -0.3), until=C("send the designs", 5), text="DESIGN FILES", scale=0.6),
              it("litho", x=1700, at=C("in Taiwan", -0.4), fireAt=C("prints them"), text="TSMC · TAIWAN", scale=0.6),
              it("wafer", x=2150, y=430, r=150, at=C("prints them"), spin=8, revealAt=C("silicon wafers"), fail=0.05),
              it("hbm", x=2650, y=500, at=C("high bandwidth memory", -0.2), dur=3, scale=0.6, text="GPU + HBM"),
              it("sign", x=2650, y=250, text="SK HYNIX · MICRON · SAMSUNG", sub="memory stacks", at=C("SK Hynix"), color="#BBDEFB", size=28),
              it("sign", x=2650, y=760, text="CoWoS PACKAGING", at=C("CoWoS"), color="#FFE0B2", size=30),
              it("conveyor", x0=2800, x1=4400, y=F - 40, at=C("Contract manufacturers", -0.5), n=8, speed=140, goods="chip"),
              it("device", type="server", x=3500, y=F, at=C("assemble them into servers")),
              it("device", type="server", x=3750, y=F, at=C("assemble them into servers", 0.4)),
              it("plane", x=[[0, 3700], [{"cue": "ship to data centers"}, 3700], [{"cue": "ship to data centers", "offset": 4}, 4600]], y=[[0, 600], [{"cue": "ship to data centers", "offset": 4}, 220]], at=C("ship to data centers", -0.4), text="TO DATA CENTERS", scale=0.6, tilt=-10)],
    "callouts": [co("Nvidia designs. Others make.", 960, 150, C("designs its chips"), "gold", screen=True, until=C("send the designs", -0.3)),
                 co("Wafers: {{suppliers.display}}, Taiwan", 960, 150, C("send the designs"), "white", screen=True, until=C("high bandwidth memory", -0.3)),
                 co("Memory stacks + CoWoS packaging", 960, 150, C("high bandwidth memory"), "white", screen=True, until=C("Contract manufacturers", -0.3)),
                 co("Servers, then data centers worldwide", 960, 150, C("Contract manufacturers"), "gold", screen=True)]},
    sources=["nvda_10k_fy2026"])
# bespoke replacement for the old static map (freeze check): a packaging line that jams when one input runs short
stage("s23_bottleneck", "a5_bottleneck", {
    "zones": [Z("fab", -1600, 2200, label="yellow"), Z("datacenter", 2200, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.05}, {"at": C("runs short"), "x": 1200, "y": 540, "zoom": 1.0, "dur": 2.0},
            {"at": C("everything downstream"), "x": 2500, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 5,
    "items": [it("conveyor", x0=-200, x1=2100, y=F - 40, at=0, n=8, speed=140, goods="chip", stopAt=C("runs short")),
              it("stack", x=300, at=0.3, h=[[0, 240], [{"cue": "runs short"}, 240], [{"cue": "runs short", "offset": 2}, 40]], text="HBM MEMORY"),
              it("sign", x=1150, y=330, text="CoWoS PACKAGING", at=0.4, color="#BBDEFB", size=32),
              it("sign", x=1150, y=470, text="SHORTAGE", at=C("runs short"), color="#FFCDD2", size=40, hang=True, swing=True),
              it("letters", x=1150, y=600, text="!", at=C("runs short", 0.3), size=120, color="risk"),
              *crowd([2450, 2600, 2750], "worry", at=C("everything downstream"), tie=True)],
    "callouts": [co("Only as fast as the slowest link", 960, 150, C("only as fast"), "white", screen=True, until=C("annual report", -0.3)),
                 co("10-K: a shortage of any one component can hold back sales", 960, 150, C("annual report"), "gold", screen=True, until=C("runs short", -0.3)),
                 co("Packaging or memory runs short: everyone waits", 960, 150, C("runs short"), "risk", screen=True)]},
    sources=["nvda_10k_fy2026"])
stage("s24_arizona", "a5_arizona", {
    "zones": [Z("site", -1600, 1300), Z("fab", 1300, 6000)], "worldW": 2800,
    "cam": [{"at": 0, "x": 640, "y": 560, "zoom": 1.12}, {"at": C("spread it out"), "x": 860, "y": 520, "zoom": 1.0, "dur": 2.4}, {"at": C("In October"), "x": 1900, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 6,
    "items": [it("bus", x=[[0, -300], [14, 900]], at=0),
              it("sign", x=600, y=330, text="MOSTLY IN ASIA", sub="above all in Taiwan", at=C("concentrated in Asia"), color="#FFF59D", size=32),
              it("crane", x=900, text="SPREAD IT OUT", at=C("spread it out"), progress=[[0, 0.3], [20, 0.8]], scale=0.8),
              it("wafer", x=1800, y=430, r=180, at=C("first Blackwell"), spin=6, text="FIRST U.S.-MADE BLACKWELL WAFER"),
              it("sign", x=2350, y=330, text="TSMC · ARIZONA", at=C("TSMC's factory"), color="#BBDEFB", size=30),
              it("plane", x=[[0, 2100], [{"cue": "travel back"}, 2100], [{"cue": "travel back", "offset": 6}, 3600]], y=[[0, 700], [{"cue": "travel back", "offset": 6}, 200]], text="", scale=0.6, at=C("travel back", -0.5), tilt=-12)],
    "callouts": [co("{{arizona.display}}: made in Arizona", 960, 150, C("In October"), "gold", screen=True, until=C("travel back", -0.3)),
                 co("…but packaged back in Taiwan (reports)", 960, 150, C("travel back"), "white", screen=True)]},
    sources=["nvda_10k_fy2026", "arizona_wafer"])
card("s25_act6", "a6_card", "The Competition", "Rivals, and customers who build their own")
stage("s26_rivals", "a6_rivals", {
    "zones": [Z("sciencepark")], "worldW": 2600,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 0.95}, {"at": C("some of its own"), "x": 1650, "y": 520, "zoom": 0.95, "dur": 2.6}], "drift": 0,
    "items": [it("tower", x=600, text="NVIDIA", color="#76B900", at=0.2, scale=1.0),
              it("building", x=980, style="office", color="#FFCDD2", text="AMD", at=C("chipmakers like"), scale=0.8),
              it("building", x=1330, style="office", color="#BBDEFB", text="INTEL", at=C("Intel"), scale=0.8),
              it("building", x=1680, style="office", color="#FFE0B2", text="HUAWEI", at=C("Huawei"), scale=0.8),
              it("crane", x=2000, text="GOOGLE CHIP", at=C("Google"), progress=[[0, 0.3], [20, 0.8]], scale=0.55),
              it("crane", x=2400, text="AMAZON CHIP", at=C("Amazon"), progress=[[0, 0.2], [20, 0.7]], scale=0.55),
              it("crane", x=2800, text="MICROSOFT CHIP", at=C("Microsoft"), progress=[[0, 0.1], [20, 0.6]], scale=0.55)],
    "callouts": [co("Rivals named in Nvidia's annual report", 960, 150, C("annual report"), "white", screen=True, until=C("some of its own", -0.3)),
                 co("…and its own biggest customers", 960, 150, C("some of its own"), "risk", screen=True)]},
    sources=["nvda_10k_fy2026"])
stage("s27_amd", "a6_amd", {
    "zones": [Z("datacenter")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.0}], "drift": 4,
    "items": [it("stack", x=600, at=C("brought in"), h=[[0, 30], [{"cue": "brought in"}, 30], [{"cue": "brought in", "offset": 2}, 60]], text="{{amd_dc_2025.display}}", sub="AMD data center, calendar 2025", color="#FFCDD2"),
              it("stack", x=1320, at=C("Nvidia's data center"), h=[[0, 30], [{"cue": "Nvidia's data center"}, 30], [{"cue": "Nvidia's data center", "offset": 3}, 640]], text="{{dc_fy2026.display}}", sub="Nvidia data center, FY2026", color="gold"),
              it("sign", x=600, y=330, text="ROCm", sub="AMD's open software", at=C("ROCm"), color="#FFF59D", size=34)],
    "callouts": [co("AMD sells data center GPUs too", 960, 150, C("AMD sells"), "white", screen=True)]},
    sources=["amd_fy2025", "nvda_10k_fy2026"])
stage("s28_custom", "a6_custom", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("Anthropic"), "x": 1650, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("device", type="chip", x=500, y=640, at=C("Google builds"), color="#4FB3F6", text="TPU · {{google_tpu.gen_spoken}}", scale=1.0),
              it("device", type="chip", x=1000, y=640, at=C("Amazon builds"), color="#FFB300", text="TRAINIUM", scale=1.0),
              it("sign", x=1000, y=300, text="{{aws_trainium.display}}", sub="in Project Rainier", at=C("Project Rainier"), color="#FFF59D", size=32),
              it("sign", x=1700, y=300, text="ANTHROPIC: {{google_tpu.display}}", sub="Google TPUs planned (late 2025)", at=C("Anthropic"), color="#E1BEE7", size=30),
              GPU(1700, 680, at=C("Nvidia's GPUs"), text="+ NVIDIA GPUs + AMAZON CHIPS", scale=0.9)],
    "callouts": [co("Custom chips", 960, 960, C("custom chips"), "gold", screen=True)]},
    sources=["google_ironwood", "aws_rainier", "anthropic_tpu"])
keep("s29_landscape")
card("s30_act7", "a7_card", "The Future of Nvidia", "Spending, risks and inference")
stage("s31_capex", "a7_capex", {
    "zones": [Z("site")], "worldW": 2200,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("capital projects"), "x": 1100, "y": 480, "zoom": 0.9, "dur": 2.6}], "drift": 0,
    "items": [it("crane", x=500, text="AI DATA CENTER", at=0.3, progress=[[0, 0.2], [25, 0.9]], scale=0.9),
              it("crane", x=1600, text="AI DATA CENTER", at=0.8, progress=[[0, 0.1], [25, 0.8]], scale=0.8),
              it("counter", x=1100, y=230, at=C("plan to spend"), steps=[[0, 0], [{"cue": "plan to spend"}, 0], [{"cue": "plan to spend", "offset": 2.5}, 700]], prefix="≈ $", suffix="bn", text="Amazon · Microsoft · Alphabet · Meta, 2026 (trackers)")],
    "callouts": [co("The boom rests on customers spending", 960, 960, C("whole boom"), "gold", screen=True)]},
    sources=["capex_tracker"])
stage("s32_risks", "a7_risks", {
    "zones": [Z("datacenter", -1600, 1600), Z("airport", 1600, 6000, night=True)], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("export rules"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("domino", x=300, gap=280, h=340, at=0.2, labels=["SPENDING", "NVIDIA SALES"], fallAt=[C("If that spending slows"), C("so does Nvidia")]),
              it("sign", x=1050, y=250, text="RIVAL CHIPS", at=C("rival chips"), color="#FFCDD2", size=30, hang=True, swing=True),
              it("sign", x=1400, y=420, text="FEW FACTORIES IN ASIA", at=C("handful of factories"), color="#FFF59D", size=28),
              it("barrier", x=2200, at=C("export rules", -0.3), closeAt=C("shut much"), text="CHINA"),
              it("conveyor", x0=1700, x1=2100, y=F - 30, goods="chip", n=3, speed=60, stopAt=C("shut much"))],
    "callouts": [co("If spending slows, so does Nvidia", 960, 150, C("If that spending"), "risk", screen=True, until=C("export rules", -0.3)),
                 co("Export rules: much of China shut", 960, 150, C("export rules"), "risk", screen=True)]},
    sources=["capex_tracker", "nvda_10k_fy2026", "nvda_q2fy27"])
keep("p33_inference")
stage("s34_outro", "outro", {
    "zones": [Z("datacenter", -1600, 1500), Z("sciencepark", 1500, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("single island"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("sign", x=400, y=250, text="HARDWARE", at=C("a stack"), color="#C8E6C9", size=28), it("sign", x=780, y=330, text="SOFTWARE", at=C("software"), color="#BBDEFB", size=28),
              it("sign", x=1100, y=250, text="DEVELOPERS", at=C("developers"), color="#FFF59D", size=28), it("sign", x=1350, y=330, text="SUPPLIERS", at=C("suppliers"), color="#E1BEE7", size=28),
              GPU(900, 760, at=0.3, text="NOT ONE CHIP: A STACK", scale=0.9),
              it("letters", x=2200, y=260, text="BOTTLENECK", at=C("single island"), size=90, color="gold")],
    "callouts": [co("Whoever controls the bottleneck captures the profit", 960, 150, C("whoever controls"), "gold", screen=True, until=C("single island", -0.3)),
                 co("…and one sits on a single island", 960, 150, C("single island"), "white", screen=True)]},
    sources=["nvda_10k_fy2026"])

write(OUT, "# GENERATED by tools/gen_nvidia_cartoon_storyboard.py; edit the generator, not this file.\n"
           "# Episode 06 (presenter cut) in bespoke CartoonStage worlds. The channel intro is inserted automatically after the hook.\n")
