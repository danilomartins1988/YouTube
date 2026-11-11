"""v2 thumbnails (PunchThumb) for every episode: loud sunburst background, giant sticker hero, the channel's presenter
(main character) shocked and pointing, 2 short lines of huge text. Every number comes from the episode's own
thumbnail brief / sources (see `claim` on each spec). Writes docs/episodes/NN/youtube-package/thumbnail_v2.png
(1280x720) and docs/thumbnails/v2_contact_sheet.jpg.  Run: python tools/punch_thumbs.py [episode ...]
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BG = {"orange": ["#FFE14D", "#FF6A00"], "red": ["#FF6B6B", "#9B0000"], "green": ["#B9F5A0", "#11A34A"],
      "blue": ["#8FD3FF", "#0B4DB3"], "purple": ["#E1A6FF", "#5B1A99"], "teal": ["#8CF2E6", "#00796B"],
      "yellow": ["#FFF59D", "#F9A825"], "pink": ["#FFB3D1", "#C2185B"], "navy": ["#7FA8FF", "#0D1B4D"],
      "gold": ["#FFE9A8", "#B8860B"]}
RAYS = {"navy": "#FFD54F", "red": "#FFD54F", "purple": "#FFD54F", "blue": "#FFFFFF"}

# ep: (bg, side, hero, line1, line2, box, extras, claim)
S = {
 "01-switzerland": ("red", "L", {"kind": "goldvault", "s": 0.95}, "NO SEA. NO OIL.", "STILL RICH?", "#0B0B0F", {}, "landlocked, no oil; rich (premise)"),
 "02-dubai": ("yellow", "R", {"kind": "towers", "s": 0.85, "spire": True}, "DUBAI ISN'T RICH", "FROM OIL", "#FF1E1E", {}, "over 95% of Dubai GDP non-oil"),
 "03-formula1": ("red", "L", {"kind": "racer", "s": 0.75, "rot": -6}, "$3.9 BILLION", "WHO GETS PAID?", "#0B0B0F", {}, "F1 revenue $3,873m 2025"),
 "04-norway": ("blue", "R", {"kind": "oilrig", "s": 0.9}, "$2 TRILLION", "SAVED, NOT SPENT", "#FF1E1E", {}, "fund ≈ $2T; fiscal rule"),
 "06-nvidia": ("green", "L", {"kind": "chip", "s": 1.0, "rot": -8, "label": "AI"}, "IT DOESN'T", "MAKE ITS CHIPS", "#0B0B0F", {}, "Nvidia is fabless (10-K)"),
 "07-taiwan-v2": ("teal", "R", {"kind": "chipland", "s": 0.85}, "ONE SMALL ISLAND", "RUNS YOUR TECH", "#FF1E1E", {}, "72.5% foundry revenue; 69% <10nm"),
 "08-asml": ("purple", "L", {"kind": "euv", "s": 0.9}, "$250M MACHINE", "ONLY 1 MAKER", "#FF1E1E", {}, "only EUV maker; $250m (Reuters estimate)"),
 "09-cables": ("navy", "R", {"kind": "globecables", "s": 0.9}, "99% OF DATA", "UNDER THE OCEAN", "#FF1E1E", {}, ">99% intl data by cable (ITU)"),
 "10-anguilla": ("teal", "L", {"kind": "island", "s": 0.95, "sign": ".AI"}, "$85M FROM", "TWO LETTERS", "#FF1E1E", {}, "≈ $85.3m .ai revenue 2025"),
 "11-flags": ("blue", "R", {"kind": "ship", "s": 0.95}, "NOT THEIR", "REAL FLAG", "#FF1E1E", {}, "ships registered abroad (UNCTAD)"),
 "12-wirecard": ("red", "L", {"kind": "vault", "s": 0.95, "empty": True}, "$2 BILLION", "NEVER EXISTED", "#0B0B0F", {}, "≈ $2.2bn cash did not exist"),
 "13-volkswagen": ("navy", "R", {"kind": "bigarrow", "s": 0.8, "dir": "up"}, "VOLKSWAGEN", "WORLD'S #1?!", "#FF1E1E", {}, "briefly world's largest company 28 Oct 2008"),
 "14-memory": ("orange", "L", {"kind": "ram", "s": 0.76, "rot": -14, "flames": True}, "RAM PRICES", "EXPLODED", "#FF1E1E",
                {"big": "$48", "crossed": "$8.70"}, "16Gb DDR5 $8.70 → $48 (TrendForce)"),
 "15-nanoimprint": ("purple", "R", {"kind": "stamp", "s": 0.95, "rot": 8}, "$400M MACHINE", "VS A STAMP", "#FF1E1E", {}, "high-NA EUV $400m (MIT TR)"),
 "16-terafab": ("navy", "L", {"kind": "chip", "s": 1.0, "rot": 8, "label": "TERA"}, "MUSK'S OWN", "CHIP FACTORY", "#FF1E1E", {}, "Terafab plan (TechCrunch)"),
 "17-india-chips": ("orange", "R", {"kind": "chip", "s": 1.0, "rot": -8, "label": "IN"}, "INDIA'S CHIP PLANTS", "DON'T MAKE CHIPS?", "#0B0B0F", {}, "plants package/test chips (PIB)"),
 "18-chip-chemicals": ("teal", "L", {"kind": "flask", "s": 0.95, "hot": True, "label": "RESIST"}, "NO BOTTLE,", "NO CHIPS", "#FF1E1E", {}, "photoresist needed for patterning"),
 "19-quibi": ("red", "L", {"kind": "phone", "s": 0.95, "rot": 12, "money": True}, "$1.75 BILLION", "DEAD IN 6 MONTHS", "#0B0B0F", {}, "$1.75bn raised; shut after 6 months"),
 "20-notpetya": ("navy", "R", {"kind": "hacked", "s": 0.8}, "ONE UPDATE", "$10 BILLION", "#FF1E1E", {}, "M.E.Doc update; >$10bn damage"),
 "21-citibank": ("green", "L", {"kind": "goldvault", "s": 0.95}, "$900 MILLION", "BY MISTAKE", "#FF1E1E", {}, "≈ $900m wired by mistake (SDNY)"),
 "22-iceland": ("blue", "R", {"kind": "bigarrow", "s": 0.8, "dir": "down"}, "3 BANKS = 9X", "THE COUNTRY", "#FF1E1E", {}, "bank assets almost 9x GDP (IMF)"),
 "23-tokyo": ("pink", "L", {"kind": "towers", "s": 0.85}, "1 TOKYO GARDEN", "= CALIFORNIA?", "#0B0B0F", {}, "palace land = California (LSE paper)"),
 "24-debeers": ("purple", "R", {"kind": "gem", "s": 1.0, "halo": True}, "DIAMONDS", "= LOVE?", "#FF1E1E", {}, "'A Diamond Is Forever' 1947"),
 "25-nickel": ("teal", "L", {"kind": "ingots", "s": 1.0, "tag": "NI"}, "$13 BILLION", "ERASED", "#FF1E1E", {}, "$13.373bn trades cancelled (FCA)"),
 "26-mcdonalds": ("red", "R", {"kind": "burger", "s": 1.0}, "30,000 PEOPLE", "FOR A BURGER", "#0B0B0F", {}, "30,000 customers 31 Jan 1990"),
 "27-oil": ("navy", "L", {"kind": "oilbarrel", "s": 1.0, "money": True}, "OIL AT", "−$37.63", "#FF1E1E", {}, "WTI May 2020 settled −$37.63"),
 "28-bigtech-ai": ("purple", "L", {"kind": "campus", "s": 0.95}, "$200 BILLION", "IN 3 MONTHS", "#FF1E1E", {}, "≈ $202.9bn quarterly capex (filings)"),
 "29-us-healthcare": ("blue", "R", {"kind": "ledger", "s": 0.9, "heading": "PER PERSON", "amount": "$14,775", "magnifier": False}, "AMERICA PAYS", "ALMOST 2X", "#FF1E1E", {}, "$14,775 vs $7,860 (Peterson-KFF)"),
 "30-credit-cards": ("orange", "L", {"kind": "ccard", "s": 0.95, "rot": -12, "coins": True}, "$160 BILLION", "IN CARD INTEREST", "#FF1E1E", {}, "$160bn interest 2024 (CFPB)"),
 "31-us-housing": ("teal", "R", {"kind": "house", "s": 0.95, "price": "$120K"}, "$120K A YEAR", "TO BUY A HOME", "#FF1E1E", {}, "$68.7k (2020) → $120.8k (2025) Harvard JCHS"),
 "32-costco": ("red", "L", {"kind": "cart", "s": 0.95}, "$5.9 BILLION", "JUST FROM FEES", "#0B0B0F", {}, "$5,907m membership fees FY2026"),
 "33-student-debt": ("navy", "R", {"kind": "gradcap", "s": 1.0, "chain": True}, "$1.65 TRILLION", "STUDENT DEBT", "#FF1E1E", {}, "$1.65T 2026:Q2 (NY Fed)"),
 "34-car-dealers": ("yellow", "L", {"kind": "sedan", "s": 1.0, "color": "#E53935"}, "THE CAR ISN'T", "THE PROFIT", "#FF1E1E", {}, "new vehicles 13% of gross profit"),
 "35-electricity": ("orange", "R", {"kind": "meter", "s": 1.0, "text": "+35%"}, "POWER BILLS", "+35%", "#FF1E1E", {}, "CPI electricity +34.8% 2021-26 (our calc)"),
 "36-car-insurance": ("pink", "L", {"kind": "sedan", "s": 1.0, "color": "#1E88E5"}, "+22.6%", "IN ONE YEAR", "#0B0B0F", {}, "CPI motor insurance +22.6% Apr 2024"),
 "37-amazon-prime": ("blue", "R", {"kind": "parcels", "s": 0.95}, "$102.7 BILLION", "ON SHIPPING", "#FF1E1E", {}, "shipping costs $102.7bn 2025"),
 "38-airports": ("purple", "L", {"kind": "sedan", "s": 1.0, "color": "#FFC21A", "sticker": "$/DAY"}, "$6.9 BILLION", "FROM PARKING", "#FF1E1E", {}, "parking $6.9bn FY2025 (FAA)"),
 "39-visa-mastercard": ("navy", "R", {"kind": "ccard", "s": 0.95, "rot": 10, "coins": True}, "355 BILLION", "VISA PAYMENTS", "#FF1E1E", {}, "355bn transactions FY2026"),
 "41-tariff-refund": ("blue", "R", {"kind": "cart", "s": 0.95}, "$166 BILLION", "TARIFF REFUND", "#FF1E1E", {}, "≈ $166bn IEEPA duties (CBP estimate)"),
 "46-overdrafts": ("red", "L", {"kind": "ccard", "s": 0.95, "rot": -8, "sticker": "$35"}, "$5.8 BILLION", "OVERDRAFT FEES", "#0B0B0F", {}, "$5.83bn 2023, banks > $1bn (CFPB)"),
 "44-iv-bags": ("blue", "R", {"kind": "ivbag", "s": 0.8}, "60% OF IV FLUIDS", "ONE FACTORY", "#FF1E1E", {}, "≈ 60% of U.S. IV solutions (AHA estimate)"),
 "45-prediction-markets": ("purple", "L", {"kind": "yesnoticket", "s": 0.85}, "$25 BILLION", "PREDICTION MARKETS", "#FF1E1E", {}, "$25bn event contracts, Mar 2026 (CFTC)"),
 "47-post-office": ("navy", "R", {"kind": "parcels", "s": 0.95}, "$118 BILLION", "POST OFFICE LOSSES", "#FF1E1E", {}, "≈ $118bn net losses since FY2006 (GAO)"),
 "48-alaska-dividend": ("blue", "L", {"kind": "bigcheck", "s": 0.75, "amount": "$1,200"}, "$1,200 EACH", "ALASKA PAYS YOU", "#FF1E1E", {}, "2026 PFD $1,200 (PFD Division)"),
 "49-college-sports": ("orange", "R", {"kind": "trophy", "s": 0.95}, "$20.5 MILLION", "COLLEGE PAYROLL", "#FF1E1E", {}, "$20.5M cap per school 2025-26 (CSC)"),
 "byb-microsoft-2026-11": ("navy", "L", {"kind": "chip", "s": 1.0, "rot": -8, "label": "CLOUD"}, "MICROSOFT STOCK", "66× FREE CASH?!", "#FF1E1E", {}, "price/FCF 66x (our calc., Nov 10, 2026 close; TTM FCF $60.0bn)"),
 "byb-meta-2026-11": ("navy", "L", {"kind": "coin", "s": 1.0, "symbol": "−$"}, "META STOCK", "CASH BELOW ZERO?!", "#FF1E1E", {}, "Q3 2026 free cash flow −$2.12bn (Meta definition; Q3 release)"),
 "byb-alphabet-2026-11": ("navy", "L", {"kind": "chip", "s": 1.0, "rot": -8, "label": "SEARCH"}, "ALPHABET STOCK", "178× FREE CASH?!", "#FF1E1E", {}, "price/FCF 178x (our calc., Nov 10, 2026 close; TTM FCF $19.7bn)"),
 "byb-amazon-2026-11": ("navy", "L", {"kind": "parcels", "s": 0.9}, "AMAZON STOCK", "CASH BELOW ZERO?!", "#FF1E1E", {}, "TTM free cash flow −$42.4bn (Amazon definition; Q3 release)"),
 "byb-tesla-2026-11": ("navy", "L", {"kind": "sedan", "s": 0.9}, "TESLA STOCK", "466× PROFIT?!", "#FF1E1E", {}, "market cap / TTM net income 466x (our calc., Nov 10, 2026 close)"),
 "byb-apple-2026-11": ("navy", "L", {"kind": "coin", "s": 1.0, "symbol": "38×"}, "APPLE STOCK", "38× PROFIT?!", "#FF1E1E", {}, "trailing P/E 38.3x (our calc., Nov 10, 2026 close; FY2026 net income)"),
 "52-nvidia-probe": ("navy", "L", {"kind": "chip", "s": 1.0, "rot": -10, "label": "AI"}, "NVIDIA", "-$428 BILLION", "#FF1E1E", {}, "≈ -$428bn market value Nov 6-10, 2026 (our estimate: closes × 24.1bn shares)"),
 "51-spacex": ("navy", "L", {"kind": "rocket", "s": 0.75}, "SPACEX", "NOT ROCKETS?!", "#FF1E1E", {}, "Q3 2026: SI $7.6bn > Starlink $5.2bn > Space $1.8bn (Q3 release)"),
 "50-mf-global": ("navy", "L", {"kind": "vault", "s": 0.95}, "$1.6 BILLION", "VANISHED", "#FF1E1E", {}, "≈ $1.6bn customer shortfall (SIPA trustee)"),
 "42-penny": ("orange", "R", {"kind": "coin", "s": 1.0, "symbol": "1¢"}, "IT COSTS 3.69¢", "TO MAKE 1¢", "#FF1E1E", {}, "penny unit cost 3.69¢ FY2024 (Mint)"),
 "43-gold-reserve": ("gold", "L", {"kind": "ingots", "s": 1.05, "tag": "$42.22"}, "$1 TRILLION", "BOOKED AT $11B", "#FF1E1E", {}, "≈ $1.0tn at Sept 2025 price vs $11.04bn book"),
 "40-grocery": ("green", "R", {"kind": "dollar", "s": 0.78, "rot": -6}, "FARMERS GET", "ONLY 11.8¢", "#FF1E1E", {"slice": True}, "farm share 11.8¢ (USDA ERS)"),
}


def size_for(text: str, max_w: float = 1000, cap: int = 132) -> int:
    return int(min(cap, max_w / (0.6 * max(len(text), 1))))


def props(ep: str) -> dict:
    bg, side, hero, l1, l2, box, ex, _ = S[ep]
    L = side == "L"
    hx, hy = (1290, 650) if L else (630, 650)
    tx = 560 if L else 1360
    hero = {**hero, "x": hx + hero.pop("dx", 0), "y": hy}
    if hero["kind"] == "dollar":
        hero["x"] = 1100 if L else 820
    p = {"bg": BG[bg], "rays": RAYS.get(bg, "#FFFFFF"), "hero": hero,
         "presenter": {"x": 300 if L else 1620, "y": 1640, "s": 2.3, "face": 1 if L else -1,
                       "point": [hx - 380 if L else hx + 380, hy + 60]},
         "text": [{"text": l1, "x": tx, "y": 170, "size": size_for(l1), "rotate": -4},
                  {"text": l2, "x": tx, "y": 315, "size": size_for(l2), "box": box, "rotate": -4,
                   "color": "#FFE14D" if box == "#0B0B0F" else "#FFFFFF"}]}
    if "big" in ex:   # memory: crossed old price + giant new price above the hero
        p["text"].append({"text": ex["big"], "x": 1600, "y": 340, "size": 240, "color": "#FFE14D", "rotate": -6})
        p["crossed"] = {"text": ex["crossed"], "x": 1190, "y": 225, "size": 96}
        p["presenter"]["point"] = [880, 720]
    elif "crossed" in ex:
        p["crossed"] = {"text": ex["crossed"], "x": tx, "y": 430, "size": 90}
    if ex.get("slice"):
        sx = p["hero"]["x"] - 0.78 * 760 * 0.99
        p["circle"] = {"x": sx, "y": hy + 50, "r": 230}
        p["presenter"]["point"] = [sx + 40, hy + 60]
        if not L:
            p["presenter"] = {"x": 1640, "y": 1640, "s": 2.3, "face": -1, "point": [sx + 60, hy + 40]}
    return p


def main() -> None:
    eps = sys.argv[1:] or list(S)
    work = ROOT / "output/thumbs_v2"
    work.mkdir(parents=True, exist_ok=True)
    jobs = []
    for ep in eps:
        pj = props(ep)
        jobs.append({"composition": "PunchThumb", "props": pj, "out": str((work / f"{ep}.png").resolve()), "scale": 0.6667})
    jf = work / "jobs.json"
    jf.write_text(json.dumps(jobs))
    subprocess.run(["node", "scripts/render_stills.mjs", str(jf)], cwd=ROOT / "remotion", check=True)
    tiles = []
    for ep in eps:
        src = work / f"{ep}.png"
        dst = ROOT / "docs/episodes" / ep / "youtube-package/thumbnail_v2.png"
        if dst.parent.exists():
            Image.open(src).convert("RGB").save(dst, optimize=True)
        tiles.append((ep, src))
    cols, tw, th = 4, 480, 270
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 10) + 10, rows * (th + 40) + 10), "white")
    d = ImageDraw.Draw(sheet)
    for i, (ep, src) in enumerate(tiles):
        x, y = 10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 40)
        sheet.paste(Image.open(src).convert("RGB").resize((tw, th)), (x, y + 30))
        d.text((x, y + 8), ep, fill="black")
    out = ROOT / ("docs/thumbnails/v2_contact_sheet.jpg" if not sys.argv[1:] else "output/thumbs_v2/sheet.jpg")
    sheet.save(out, quality=88)
    print("wrote", len(tiles), "thumbnails;", out)


if __name__ == "__main__":
    main()
