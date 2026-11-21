"""YouTube thumbnails: a mandatory stage of every publishing package (standard of 2026-11-08).

Pipeline: ... RENDER -> VIDEO QC -> THUMBNAIL GENERATION -> THUMBNAIL QC -> YOUTUBE PACKAGE READY.

- The creative brief lives in projects/<slug>/thumbnail_brief.yaml: story analysis (mystery, most surprising verified
  fact, subject, tone, metaphor) and two concepts (A = mystery, B = consequence), each a purpose-built cinematic scene
  (remotion/src/thumbnails/CinematicThumb.tsx) plus 0-4 words of text and the claim the words rest on.
- Backend: `svg-composite` (original vector illustration rendered locally with Remotion, typography composited from an
  exact layout). Cost US$0. No image-generation API is used: the channel's rule is free/open tools only, and no image
  service has been authorised. A paid backend may be added later only with explicit approval and a budget.
- Output (per episode, in the episode's docs folder): youtube-package/thumbnail.png (1280x720, < 2 MB),
  thumbnail-preview.jpg, thumbnail-brief.json (brief + layout + QC), thumbnail-alt-<id>.png, title.txt,
  description.txt, tags.txt, chapters.txt, video.txt, PACKAGE_STATUS.json. 3840x2160 masters stay in
  output/<slug>/thumbnails/ (not committed). An existing different thumbnail.png is moved to versions/, never deleted.
- Idempotent: a concept is re-rendered only when its spec (or the renderer source) changed, or with force=True.
- Owner model (2026-11-19, docs/thumbnails/OWNER_STYLE.md): archetype `poster` (remotion/src/thumbnails/PosterThumb.tsx)
  is the default concept of new briefs; an owner-made youtube-package/thumbnail_owner.jpg always wins as the default.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import yaml
from PIL import Image, ImageFilter, ImageOps

from hiddeneco.config import REPO_ROOT

W, H = 1920, 1080
SAFE = 56                                     # margin (px at 1920) no text may cross
TIMESTAMP = (W - 330, H - 150)                # YouTube's duration badge covers the bottom-right corner
MAX_BYTES = 2 * 1024 * 1024                   # YouTube thumbnail upload limit
GLYPH = 0.64                                  # average advance of Inter Display Black capitals, in em
COMPONENT = REPO_ROOT / "remotion" / "src" / "thumbnails" / "CinematicThumb.tsx"
FACE_COMPONENTS = [REPO_ROOT / "remotion" / "src" / "thumbnails" / "FaceThumb.tsx",
                   REPO_ROOT / "remotion" / "src" / "animation-engine" / "CartoonStage" / "bust.tsx"]
POSTER_COMPONENTS = [REPO_ROOT / "remotion" / "src" / "thumbnails" / "PosterThumb.tsx", COMPONENT]
POSTER_FONT = Path("/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf")
BANNERS = {"red": ("#E3201B", "#FFFFFF"), "yellow": ("#FFD400", "#05070B")}   # banner colour, text colour
LOG = REPO_ROOT / "output" / "thumbnails" / "log.jsonl"


# ------------------------------------------------------------------------------------------------ layout
def layout(lines: list[str], side: str, accent_line: int | None, colors: dict, style: str = "plain") -> list[dict]:
    """Exact text boxes (font size, position, rendered width via textLength) for 1-3 lines in a zone."""
    zones = {"left": (90, 800, "start"), "right": (W - 90, 800, "end"), "top": (W / 2, 1560, "middle"), "bottom": (820, 1300, "middle")}
    x, zw, anchor = zones[side]
    n = len(lines)
    size = min(250, min(zw / (max(1, len(l)) * GLYPH) for l in lines))
    size = min(size, (560 if side in ("left", "right") else 330) / (n * 1.04))
    gap = size * 1.04
    if side in ("left", "right"):
        y0 = H / 2 - (n - 1) * gap / 2 + size * 0.36
    elif side == "top":
        y0 = 150 + size * 0.82
    else:
        y0 = H - 150 - (n - 1) * gap
    out = []
    for i, l in enumerate(lines):
        width = min(zw, len(l) * size * GLYPH)
        acc = i == accent_line
        t = {"text": l, "x": x, "y": round(y0 + i * gap, 1), "size": round(size, 1), "width": round(width, 1), "anchor": anchor,
             "color": colors["accent"] if acc else colors["ink"]}
        if style == "box" and acc:
            t.update({"box": colors["accent"], "color": colors.get("box_ink", "#05070B")})
        if style == "underline" and acc:
            t["underline"] = colors["accent"]
        out.append(t)
    return out


def layout_bignum(lines: list[str], colors: dict) -> list[dict]:
    """Archetype 'bignum': line 0 is a giant number filling ~60% of the width; the other line is a short kicker below."""
    big = lines[0]
    size = min(360, 1180 / (max(1, len(big)) * GLYPH))
    y0 = H / 2 + size * 0.30 - (60 if len(lines) > 1 else 0)
    out = [{"text": big, "x": 90, "y": round(y0, 1), "size": round(size, 1), "width": round(min(1180, len(big) * size * GLYPH), 1),
            "anchor": "start", "color": colors["accent"]}]
    if len(lines) > 1:
        k = lines[1]
        ks = min(120, 1100 / (max(1, len(k)) * GLYPH))
        out.append({"text": k, "x": 96, "y": round(y0 + ks * 1.15, 1), "size": round(ks, 1), "width": round(min(1100, len(k) * ks * GLYPH), 1),
                    "anchor": "start", "color": colors["ink"]})
    return out


def layout_split(lines: list[str], colors: dict) -> list[dict]:
    """Archetype 'split': before / after. Line 0 labels the left half, line 1 the right half (top of each half)."""
    out = []
    for i, l in enumerate(lines[:2]):
        size = min(150, 760 / (max(1, len(l)) * GLYPH))
        cx = W * 0.25 if i == 0 else W * 0.75
        out.append({"text": l, "x": cx, "y": round(130 + size * 0.82, 1), "size": round(size, 1), "width": round(min(760, len(l) * size * GLYPH), 1),
                    "anchor": "middle", "color": colors["ink"] if i == 0 else colors["accent"]})
    return out


# ------------------------------------------------------------------------------------------------ face archetype
# Owner request 2026-11-16: whenever a named public figure is central, the default thumbnail is a big respectful cartoon
# BUST of that person on one side (remotion/src/thumbnails/FaceThumb.tsx + CartoonStage/bust.tsx), <= 4 huge words on
# the other side and ONE bold prop or sourced number. Presets mirror BUST in bust.tsx (signature traits only).
FACE_PRESETS = {"huang": "Jensen Huang", "jassy": "Andy Jassy", "pichai": "Sundar Pichai", "musk": "Elon Musk", "sam": "Sam Walton",
                "rob": "Rob Walton", "penner": "Greg Penner", "steuart": "Steuart Walton", "furner": "John Furner", "trump": "Donald Trump",
                "vachris": "Ron Vachris", "sinegal": "Jim Sinegal",
                "wangcf": "Wang Chuanfu", "leijun": "Lei Jun",
                "gloria": "Gloria (sitcom cast)", "dash": "Dash (sitcom cast)"}
FACE_EXPRS = ("shock", "smug", "worry", "point", "laugh", "happy", "neutral")
BUST_EYE_Y, BUST_TOP, BUST_HALF_W = 736, 1000, 250        # local units at scale 1 (eye line, crown with hair, head half-width)


def face_geometry(sc: dict) -> dict:
    """Frame-space geometry of a face concept: bust side, head box, the text zone and the prop default."""
    b = sc["bust"]
    s, x, y = float(b.get("s", 0.95)), float(b["x"]), float(b.get("y", H + 10))
    side = "left" if x < W / 2 else "right"
    head = (x - BUST_HALF_W * s, y - BUST_TOP * s - (110 * s if b.get("cap") else 0), x + BUST_HALF_W * s, y - 470 * s)
    zone = (x + 430 * s + 20, W - 70) if side == "left" else (70, x - 430 * s - 20)
    return {"side": side, "dir": 1 if side == "left" else -1, "head": head, "eye": (x, y - BUST_EYE_Y * s), "zone": zone}


def layout_face(lines: list[str], sc: dict, colors: dict, accent_line: int | None = None) -> list[dict]:
    """Archetype 'face': 1-2 lines, centred in the zone opposite the bust, top of frame; the accent line (default: the
    last of two) in a red box. Leaves the lower part of the zone for the prop."""
    g = face_geometry(sc)
    x0, x1 = g["zone"]
    zw, cx = x1 - x0, (x0 + x1) / 2
    acc = (len(lines) - 1 if len(lines) > 1 else None) if accent_line is None else accent_line
    out, y = [], 70.0
    for i, l in enumerate(lines):
        boxed = i == acc
        size = min(210 if not boxed else 200, (zw - (90 if boxed else 20)) / (max(1, len(l)) * GLYPH))
        y += size * 0.80 + (26 if boxed else 0) + (8 if i else 0)
        out.append({"text": l, "x": round(cx, 1), "y": round(y, 1), "size": round(size, 1), "width": round(len(l) * size * GLYPH, 1), "anchor": "middle",
                    "color": "#FFFFFF" if boxed else colors.get("ink", "#FFFFFF"), "rotate": -3, **({"box": colors.get("box", "#FF1E1E")} if boxed else {})})
        y += size * 0.24 + (26 if boxed else 0)
    return out


def face_props(c: dict, texts: list[dict], hide_text: bool = False) -> dict:
    sc = c["scene"]
    g = face_geometry(sc)
    bust = {"dir": g["dir"], **sc["bust"]}
    prop = dict(sc["prop"]) if sc.get("prop") else None
    if prop and bust.get("expr") == "point" and "point" not in bust:
        bust["point"] = [prop["x"] - g["dir"] * 120 * prop.get("s", 1), prop["y"] - 40]
    return {"bg": sc.get("bg", ["#3A8DFF", "#0A1F5C"]), "rays": sc.get("rays", "#FFFFFF"), "bust": bust, "prop": prop, "text": texts,
            "hideText": hide_text, "brand": sc.get("brand", "none")}


# ------------------------------------------------------------------------------------------------ poster archetype
# Owner model 2026-11-19: cinematic backdrop, one big glowing hero on the right, 2-3 huge Black Italic words on the left,
# one line on a rough red/yellow brush banner (remotion/src/thumbnails/PosterThumb.tsx).
_EM: dict[str, float] = {}


def _em(text: str) -> float:
    """Advance width of `text` in em, measured with the real Inter Display Black Italic font."""
    if text not in _EM:
        try:
            from PIL import ImageFont
            _EM[text] = ImageFont.truetype(str(POSTER_FONT), 200).getlength(text) / 200
        except OSError:
            _EM[text] = len(text) * 0.66
    return _EM[text]


def layout_poster(lines: list[str], accent_line: int | None = None, banner: str = "red", zone: tuple[float, float] = (70, 1120),
                  cy: float = 520, rotate: float = -4, cap: float = 270) -> list[dict]:
    """1-3 lines in the left zone; the accent line (default: the last) sits on a brush banner. Sizes fill the zone
    width; a short line may grow up to 1.3x the smallest. Widths are exact (textLength) so QC knows every box."""
    x0, x1 = zone
    zw = x1 - x0
    acc = (len(lines) - 1) if accent_line is None else accent_line
    col, ink = BANNERS.get(banner, BANNERS["red"])
    sizes = [min(cap, zw / (_em(l) + (0.5 if i == acc else 0.04))) for i, l in enumerate(lines)]
    lo = min(sizes)
    sizes = [min(v, lo * 1.3) for v in sizes]
    pitch = [v * (1.22 if i == acc else 1.0) for i, v in enumerate(sizes)]
    y = cy - sum(pitch) / 2
    out = []
    for i, (l, v) in enumerate(zip(lines, sizes)):
        boxed = i == acc
        y += v * (0.90 if boxed else 0.80)
        t = {"text": l, "x": round(x0 + (v * 0.22 if boxed else 0), 1), "y": round(y, 1), "size": round(v, 1), "width": round(_em(l) * v, 1),
             "anchor": "start", "color": ink if boxed else "#FFFFFF", "outline": "#05070B", "rotate": rotate}
        if boxed:
            t.update({"banner": col, "box": col})
        out.append(t)
        y += v * (0.32 if boxed else 0.20)
    return out


def is_poster(c: dict) -> bool:
    return c.get("archetype") == "poster"


def text_boxes(t: list[dict]) -> list[tuple[float, float, float, float]]:
    boxes = []
    for x in t:
        left = x["x"] if x["anchor"] == "start" else x["x"] - x["width"] if x["anchor"] == "end" else x["x"] - x["width"] / 2
        boxes.append((left, x["y"] - x["size"] * 0.78, left + x["width"], x["y"] + x["size"] * 0.06))
    return boxes


# ------------------------------------------------------------------------------------------------ render
def _browser() -> str | None:
    from hiddeneco.render import remotion_bridge as rb
    return rb.browser_executable()


def render_still(props: dict, out_png: Path, scale: float = 2.0, composition: str = "CinematicThumb") -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    pj = out_png.with_suffix(".props.json")
    pj.write_text(json.dumps(props))
    cmd = ["npx", "remotion", "still", "src/index.ts", composition, str(out_png.resolve()), f"--props={pj.resolve()}",
           f"--scale={scale}", "--log=error"]
    b = _browser()
    if b:
        cmd.append(f"--browser-executable={b}")
    subprocess.run(cmd, cwd=REPO_ROOT / "remotion", check=True)


def export_1280(master: Path, out: Path) -> dict:
    im = Image.open(master).convert("RGB").resize((1280, 720), Image.LANCZOS)
    im.save(out, "PNG", optimize=True)
    how = "png"
    if out.stat().st_size > MAX_BYTES:                       # gradients + grain can exceed 2 MB: quantise, keep 1280x720
        im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB").save(out, "PNG", optimize=True)
        how = "png-quantised"
    return {"bytes": out.stat().st_size, "export": how}


# ------------------------------------------------------------------------------------------------ QC
def _lum(rgb) -> float:
    c = np.asarray(rgb, dtype=float) / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]) if c.ndim == 1 else 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def _hex(h: str):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def contrast(a: float, b: float) -> float:
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def dhash(img: Image.Image) -> np.ndarray:
    g = ImageOps.grayscale(img).resize((17, 9), Image.LANCZOS)
    a = np.asarray(g, dtype=float)
    return (a[:, 1:] > a[:, :-1]).flatten()


def hue_hist(img: Image.Image) -> np.ndarray:
    hsv = np.asarray(img.convert("HSV").resize((160, 90)), dtype=float)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    w = (s / 255) * (v / 255)
    hist, _ = np.histogram(h, bins=12, range=(0, 256), weights=w)
    tot = hist.sum() or 1
    dark = np.array([(v < 60).mean(), ((v >= 60) & (v < 160)).mean(), (v >= 160).mean()])
    return np.concatenate([hist / tot, dark])


def qc(concept: dict, png: Path, notext: Path, texts: list[dict], others: dict[str, Path]) -> dict:
    """Automated checks. Returns {'checks': [...], 'critical_fail': bool, 'score': float, 'review': [...]}."""
    checks, review = [], []
    def add(name, ok, detail, critical=True):
        checks.append({"check": name, "pass": bool(ok), "detail": detail, "critical": critical})
    im = Image.open(png)
    add("dimensions 1280x720 (16:9)", im.size == (1280, 720), f"{im.size}")
    add("RGB image", im.mode in ("RGB",), im.mode)
    add("file size < 2 MB", png.stat().st_size < MAX_BYTES, f"{png.stat().st_size / 1e6:.2f} MB")
    try:
        Image.open(png).verify(); ok = True
    except Exception as e:                                     # noqa: BLE001
        ok = False
    add("valid PNG", ok, "verified")
    words = sum(len(t["text"].split()) for t in texts)
    add("0-4 words", words <= 4, f"{words} words", critical=words > 6)
    boxes = text_boxes(texts)
    inside = all(b[0] >= SAFE and b[2] <= W - SAFE and b[1] >= SAFE and b[3] <= H - SAFE for b in boxes)
    add("no clipped text (inside safe margins)", inside, f"{[tuple(round(v) for v in b) for b in boxes]}")
    stamp = all(not (b[2] > TIMESTAMP[0] and b[3] > TIMESTAMP[1]) for b in boxes)
    add("text clear of the duration badge (bottom-right)", stamp, "bottom-right 330x150 kept free")
    mobile = min((t["size"] for t in texts), default=999) * 160 / W
    add("legible at 160 px wide (cap height >= 6 px)", mobile * 0.72 >= 6 or not texts, f"{mobile:.1f}px font at 160px wide", critical=True)
    # contrast of each line against the image behind it (render without text)
    bg = np.asarray(Image.open(notext).convert("RGB").resize((W, H)), dtype=float)
    lum = _lum(bg)
    worst = 99.0
    for t, b in zip(texts, boxes):
        x0, y0, x1, y1 = (int(max(0, v)) for v in b)
        region = lum[y0:y1, x0:x1]
        if region.size == 0:
            continue
        fill = _lum(_hex(t.get("box") or t["color"])) if not t.get("box") else _lum(_hex(t["color"]))
        base = _lum(_hex(t["box"])) if t.get("box") else _lum(_hex(t["outline"])) if t.get("outline") else float(np.percentile(region, 75))
        worst = min(worst, contrast(fill, base))
    add("text contrast >= 3:1 against its background", worst >= 3.0 or not texts, f"worst {worst:.1f}:1 (dark outline adds more)")
    # clutter: edge density at thumbnail scale
    small = ImageOps.grayscale(Image.open(png)).resize((320, 180))
    edges = np.asarray(small.filter(ImageFilter.FIND_EDGES), dtype=float)
    density = float((edges > 40).mean())
    add("uncluttered (edge density <= 0.16)", density <= 0.16, f"{density:.3f}", critical=False)
    # subject contrast: the subject region must differ from the frame average (stands out)
    full = np.asarray(ImageOps.grayscale(Image.open(notext)).resize((192, 108)), dtype=float)
    if concept.get("archetype") == "face":
        g = face_geometry(concept["scene"])
        sx, sy = int(g["eye"][0] / 10), int(g["eye"][1] / 10)
        hx0, hy0, hx1, hy1 = g["head"]
        clear = all(b[2] < hx0 or b[0] > hx1 or b[3] < hy0 or b[1] > hy1 for b in boxes)
        add("text clear of the face", clear, f"head box {tuple(round(v) for v in g['head'])}")
        add("named figure is a preset or traits object (likeness rules)", isinstance(concept["scene"]["bust"].get("who"), dict)
            or concept["scene"]["bust"].get("who") in FACE_PRESETS or concept["scene"]["bust"].get("who") == "silhouette", str(concept["scene"]["bust"].get("who")))
        review.append("Likeness is respectful: signature traits only, no mocked features, nothing implying a crime (human)")
    elif is_poster(concept):
        hero = concept["scene"]["hero"]
        sx, sy = int(min(1900, max(0, hero["x"])) / 10), int(min(1070, max(0, hero["y"])) / 10)
        phone = min((t["size"] for t in texts), default=999) * 320 / W * 0.72
        add("poster: legible at 320x180 (cap height >= 10 px)", phone >= 10 or not texts, f"{phone:.1f}px caps at 320 px wide")
        right = max((b[2] for b in boxes), default=0)
        add("poster: words stay in the left ~60% (hero owns the right)", right <= W * 0.62, f"text right edge {right:.0f}px", critical=False)
        hsv = np.asarray(Image.open(notext).convert("HSV").resize((192, 108)), dtype=float)
        lit = hsv[..., 2] > 60
        sat = float((hsv[..., 1][lit] / 255).mean()) if lit.any() else 0.0
        add("poster: vivid, saturated scene (mean saturation of lit pixels >= 0.45)", sat >= 0.45, f"{sat:.2f}", critical=False)
        rhs = np.asarray(ImageOps.grayscale(Image.open(notext)).resize((192, 108)), dtype=float)
        add("poster: the hero side is the brightest (light behind the hero)", rhs[:, 96:].mean() >= rhs[:, :96].mean(), f"right {rhs[:, 96:].mean():.0f} vs left {rhs[:, :96].mean():.0f}", critical=False)
    else:
        sx, sy = int(concept["scene"]["subject"]["x"] / 10), int(concept["scene"]["subject"]["y"] / 10)
    patch = full[max(0, sy - 18):sy + 18, max(0, sx - 28):sx + 28]
    sub_c = float(patch.std())
    add("dominant subject has strong internal contrast", sub_c >= 28, f"luma std {sub_c:.0f}", critical=False)
    # distinctness vs every other channel thumbnail
    me = Image.open(png).convert("RGB")
    mh, mc = dhash(me), hue_hist(me)
    nearest = (None, 999.0)
    for name, path in others.items():
        if not path.exists():
            continue
        o = Image.open(path).convert("RGB")
        d = float((dhash(o) != mh).mean()) * 0.6 + float(np.abs(hue_hist(o) - mc).sum()) * 0.4
        if d < nearest[1]:
            nearest = (name, d)
    distinct = nearest[0] is None or nearest[1] >= 0.22
    add("distinct from other channel thumbnails", distinct, f"nearest {nearest[0]} (distance {nearest[1]:.2f})", critical=False)
    if not concept.get("claim_basis"):
        add("text rests on a verified claim or makes no factual claim", False, "missing claim_basis")
    else:
        add("text rests on a verified claim or makes no factual claim", True, concept["claim_basis"][:140])
    review += ["Subject recognisable at a glance (human)", "Tone matches the documentary (human)", "Not misleading / not clickbait (human)",
               "Spelling of the words on the image (human)"]
    crit = any(not c["pass"] and c["critical"] for c in checks)
    score = (min(worst, 8) / 8) * 0.35 + min(mobile / 14, 1) * 0.25 + (1 - min(density / 0.16, 1)) * 0.15 + min(nearest[1] / 0.5, 1) * 0.15 + min(sub_c / 60, 1) * 0.10
    return {"checks": checks, "critical_fail": crit, "design_score": round(score, 3),
            "score_note": "internal design score (contrast, legibility, clutter, distinctness); it does not predict YouTube CTR",
            "needs_human_review": review, "nearest": nearest[0]}


# ------------------------------------------------------------------------------------------------ package text
def _section(md: str, head: str) -> str | None:
    m = re.search(rf"## {re.escape(head)}[^\n]*\n+```\n(.*?)```", md, re.S)
    if m:
        return m.group(1).strip()
    m = re.search(rf"## {re.escape(head)}[^\n]*\n+(.+?)(?:\n\n|\Z)", md, re.S)
    return m.group(1).strip() if m else None


def package_texts(brief: dict) -> dict:
    """title / description / tags / chapters from the episode's existing youtube package (kept unchanged)."""
    docs = REPO_ROOT / brief["docs_dir"]
    md = None
    for f in [docs / "youtube_package.md", docs / "metadata_documentary.md", REPO_ROOT / "output" / brief["slug"] / brief.get("deliverable", "documentary") / "metadata.md"]:
        if f.exists():
            md = f.read_text(encoding="utf-8")
            src = f
            break
    if md is None:
        return {"missing": True}
    desc = _section(md, "Description") or ""
    tags = _section(md, "Tags") or _section(md, "Keywords / tags") or ""
    chapters = "\n".join(l for l in desc.splitlines() if re.match(r"^\d{1,2}:\d{2}\s", l))
    from hiddeneco.cta import DESCRIPTION_LINE    # every description carries the subscribe line (docs/CTA_STANDARD.md)
    if desc and "subscribe" not in desc.lower():
        ls = desc.rstrip().split("\n")
        k = len(ls) - 1 if ls[-1].lstrip().startswith("#") else len(ls)
        cand = "\n".join(ls[:k] + ["", DESCRIPTION_LINE, ""] + ls[k:]).replace("\n\n\n", "\n\n")
        desc = cand if len(cand) <= 5000 else desc
    return {"title": brief["title"], "description": desc, "tags": tags.replace("\n", " ").strip(), "chapters": chapters,
            "source": str(src.relative_to(REPO_ROOT))}


# ------------------------------------------------------------------------------------------------ run
def _hash(obj, face: bool = False, comps: list[Path] | None = None) -> str:
    h = hashlib.sha256(json.dumps(obj, sort_keys=True).encode())
    for f in (comps or (FACE_COMPONENTS if face else [COMPONENT])):
        h.update(f.read_bytes())
    return h.hexdigest()[:16]


def _log(**kw) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"at": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z", **kw}) + "\n")


def load_brief(slug: str) -> dict | None:
    f = REPO_ROOT / "projects" / slug / "thumbnail_brief.yaml"
    if not f.exists():
        return None
    b = yaml.safe_load(f.read_text(encoding="utf-8"))
    b["slug"] = slug
    return b


def concept_props(b: dict, c: dict, hide_text: bool = False) -> tuple[dict, list[dict]]:
    sc = dict(c["scene"])
    pal = sc.get("palette") or {"ink": "#FFFFFF", "accent": "#FFD23F"}
    cols = {"ink": pal.get("ink", "#F4EFE4"), "accent": pal["accent"], "box_ink": c.get("box_ink", "#05070B")}
    arch = c.get("archetype", "classic")
    if not c.get("text"):
        texts = []
    elif arch == "bignum":
        texts = layout_bignum(c["text"], cols)
    elif arch == "split":
        texts = layout_split(c["text"], cols)
    elif arch == "face":
        texts = layout_face(c["text"], sc, {**cols, "ink": pal.get("ink", "#FFFFFF") if pal else "#FFFFFF"}, c.get("accent_line"))
        return face_props(c, texts, hide_text), texts
    elif arch == "poster":
        texts = layout_poster(c["text"], c.get("accent_line"), c.get("banner", "red"), cy=c.get("text_y", 520), rotate=c.get("rotate", -4))
        return {**sc, "text": texts, "hideText": hide_text}, texts
    else:
        texts = layout(c["text"], c.get("text_side", "left"), c.get("accent_line"), cols, c.get("text_style", "plain"))
    props = {**sc, "text": texts, "hideText": hide_text, "archetype": arch}
    if arch != "classic":
        props.setdefault("brand", "none")      # new archetypes drop the corner tag (noise at 160 px)
    return props, texts


def is_face(c: dict) -> bool:
    return c.get("archetype") == "face"


def face_file(c: dict) -> str:
    """package file of a face/poster concept: thumbnail_face.png / thumbnail_poster.png (or the concept's `file`)."""
    return c.get("file") or ("thumbnail_poster.png" if is_poster(c) else "thumbnail_face.png")


def named(c: dict) -> bool:
    """face and poster concepts are always also written to their own package file"""
    return is_face(c) or is_poster(c)


def component(c: dict) -> tuple[str, list[Path] | None]:
    if is_face(c):
        return "FaceThumb", FACE_COMPONENTS
    if is_poster(c):
        return "PosterThumb", POSTER_COMPONENTS
    return "CinematicThumb", None


def _write_face(pkg: Path, r: dict) -> Path:
    out = pkg / face_file(r["concept"])
    out.write_bytes(r["png"].read_bytes())
    prev = Image.open(r["png"]).convert("RGB")
    sheet = Image.new("RGB", (640 + 24 + 320, 360), "#0B0D12")
    sheet.paste(prev.resize((640, 360), Image.LANCZOS), (0, 0))
    sheet.paste(prev.resize((320, 180), Image.LANCZOS), (664, 90))      # phone size
    sheet.save(out.with_name(out.stem + "-preview.jpg"), quality=90)
    (out.with_name(out.stem + "-brief.json")).write_text(json.dumps({**r["concept"], "layout": r["texts"], "qc": r["qc"],
        "backend": "svg-composite (Remotion " + ("PosterThumb" if is_poster(r["concept"]) else "FaceThumb + CartoonStage bust") + ", original vector art)", "cost_usd": 0.0,
        "generated": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"}, indent=2, default=str), encoding="utf-8")
    return out


def generate(slug: str, others: dict[str, Path] | None = None, force: bool = False, only: list[str] | None = None) -> dict:
    """Render the concepts, QC them, pick the default, write the youtube-package folder. Safe to re-run.

    Face concepts (archetype 'face') are also written to youtube-package/thumbnail_face.png (+ -preview.jpg, -brief.json).
    Default rule: the brief's `default`; else, when `analysis.public_figure` is set, the best QC-passed face concept;
    else the best design score. `only=[ids]` renders just those concepts and writes their own files (face file or
    thumbnail-alt-<id>.png) WITHOUT touching thumbnail.png, the default or the package status."""
    b = load_brief(slug)
    if b is None:
        _log(slug=slug, event="no_brief")
        return {"slug": slug, "status": "no_brief"}
    work = REPO_ROOT / "output" / slug / "thumbnails"
    pkg = REPO_ROOT / b["docs_dir"] / "youtube-package"
    pkg.mkdir(parents=True, exist_ok=True)
    results = {}
    for c in b["concepts"]:
        if only and c["id"] not in only:
            continue
        props, texts = concept_props(b, c)
        comp, comps = component(c)
        key = _hash({"props": props}, comps=comps)
        master, nt = work / f"master_{c['id']}.png", work / f"notext_{c['id']}.png"
        small = work / f"thumb_{c['id']}.png"
        stamp = work / f"{c['id']}.hash"
        if force or not (stamp.exists() and stamp.read_text() == key and master.exists() and nt.exists() and small.exists()):
            render_still(props, master, 2.0, comp)
            render_still(concept_props(b, c, hide_text=True)[0], nt, 0.5, comp)
            exp = export_1280(master, small)
            stamp.write_text(key)
            _log(slug=slug, event="rendered", concept=c["id"], backend="svg-composite", cost_usd=0.0, **exp)
        results[c["id"]] = {"concept": c, "texts": texts, "png": small, "notext": nt, "master": master}
    oth = {k: v for k, v in (others or {}).items() if k != slug}
    for cid, r in results.items():
        r["qc"] = qc(r["concept"], r["png"], r["notext"], r["texts"], oth)
    for cid, r in results.items():
        if named(r["concept"]):
            r["face_file"] = _write_face(pkg, r)
            _log(slug=slug, event="face", concept=cid, file=str(r["face_file"].relative_to(REPO_ROOT)), qc_fail=r["qc"]["critical_fail"])
    if only:
        for cid, r in results.items():
            if not named(r["concept"]):
                shutil.copyfile(r["png"], pkg / f"thumbnail-alt-{cid}.png")
        return {"slug": slug, "only": only, "results": results, "pkg": pkg,
                "files": {cid: str(r.get("face_file") or pkg / f"thumbnail-alt-{cid}.png") for cid, r in results.items()},
                "qc": {cid: ("fail" if r["qc"]["critical_fail"] else "pass") for cid, r in results.items()}}
    ok = [cid for cid, r in results.items() if not r["qc"]["critical_fail"]]
    forced = b.get("default")
    faces = [cid for cid in ok if is_face(results[cid]["concept"])]
    if forced in ok:
        default = forced
    elif (b.get("analysis") or {}).get("public_figure") and faces:
        default = max(faces, key=lambda k: results[k]["qc"]["design_score"])
    else:
        default = max(ok, key=lambda k: results[k]["qc"]["design_score"]) if ok else None
    owner = pkg / "thumbnail_owner.jpg"
    if owner.exists():                        # an owner-made thumbnail always takes precedence as the default
        default = "owner"
    # write package (version an existing different thumbnail first)
    out = pkg / "thumbnail.png"
    if default:
        if default == "owner":
            import io
            buf = io.BytesIO()
            Image.open(owner).convert("RGB").resize((1280, 720), Image.LANCZOS).save(buf, "PNG", optimize=True)
            newb = buf.getvalue()
        else:
            newb = results[default]["png"].read_bytes()
        if out.exists() and out.read_bytes() != newb:
            vdir = pkg / "versions"
            vdir.mkdir(exist_ok=True)
            ts = _dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            shutil.move(str(out), str(vdir / f"thumbnail-{ts}.png"))
            _log(slug=slug, event="versioned", file=f"versions/thumbnail-{ts}.png")
        out.write_bytes(newb)
        prev = Image.open(owner if default == "owner" else results[default]["png"]).convert("RGB")
        sheet = Image.new("RGB", (640 + 24 + 160, 360), "#0B0D12")
        sheet.paste(prev.resize((640, 360), Image.LANCZOS), (0, 0))
        sheet.paste(prev.resize((160, 90), Image.LANCZOS), (664, 135))   # what a phone shows
        sheet.save(pkg / "thumbnail-preview.jpg", quality=90)
    for cid, r in results.items():
        alt = pkg / f"thumbnail-alt-{cid}.png"
        if cid != default:
            shutil.copyfile(r["png"], alt)
        elif alt.exists():
            alt.unlink()                      # this concept is now the default: no stale duplicate as "alternative"
    texts = package_texts(b)
    if not texts.get("missing"):
        (pkg / "title.txt").write_text(texts["title"] + "\n", encoding="utf-8")
        (pkg / "description.txt").write_text(texts["description"] + "\n", encoding="utf-8")
        (pkg / "tags.txt").write_text(texts["tags"] + "\n", encoding="utf-8")
        (pkg / "chapters.txt").write_text(texts["chapters"] + "\n", encoding="utf-8")
    video = REPO_ROOT / b.get("video", "")
    (pkg / "video.txt").write_text(f"{b.get('video', '')}\n(MP4 not committed: it stays in output/; nothing is uploaded)\n", encoding="utf-8")
    brief_json = {k: v for k, v in b.items() if k != "concepts"}
    brief_json["concepts"] = [{**r["concept"], "layout": r["texts"], "qc": r["qc"]} for r in results.values()]
    brief_json.update({"default": default, "backend": "svg-composite (Remotion, original vector art)", "cost_usd": 0.0,
                       "generated": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
                       "master": str(results[default]["master"].relative_to(REPO_ROOT)) if default in results else None})
    (pkg / "thumbnail-brief.json").write_text(json.dumps(brief_json, indent=2, default=str), encoding="utf-8")
    ready = (bool(default) and not texts.get("missing") and video.exists() and b.get("status", "completed") == "completed"
             and not b.get("draft"))
    status = {"slug": slug, "title": b["title"], "thumbnail_qc": "pass" if default else "fail", "default_concept": default,
              "metadata": "missing" if texts.get("missing") else "ok", "video_exists": video.exists(), "brief": "draft" if b.get("draft") else "approved",
              "package_ready": ready, "needs_human_review": True,
              "note": "Ready means: video, metadata and a QC-passed thumbnail exist. Upload stays manual."}
    (pkg / "PACKAGE_STATUS.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    _log(slug=slug, event="package", default=default, ready=ready)
    return {**status, "results": results, "pkg": pkg}


# ------------------------------------------------------------------------------------------------ future episodes
TONE_SUBJECT = {  # a first visual idea per tone; the director replaces it in the brief
    "thriller": ("ledger", "room"), "crisis": ("crash", "void"), "strategy": ("surge", "void"), "trade": ("ship", "sea"),
    "tech": ("chip", "void"), "history": ("ledger", "room"), "reflective": ("ledger", "room"), "bright": ("coin", "void")}
TONE_PALETTE = {
    "thriller": dict(sky0="#040609", sky1="#141B26", haze="#6E89A8", key="#B9D2F0", accent="#E8B04A", ink="#F4EFE4"),
    "crisis": dict(sky0="#070405", sky1="#1E0D10", haze="#E5443A", key="#FFB4A8", accent="#FFD24A", ink="#FFFFFF"),
    "strategy": dict(sky0="#05070C", sky1="#15233A", haze="#4D8BD6", key="#BFD8FF", accent="#FFC93C", ink="#FFFFFF"),
    "trade": dict(sky0="#0A1A2E", sky1="#2B4A6A", haze="#F2A65A", key="#FFD3A0", accent="#FFC93C", ink="#FFFFFF"),
    "tech": dict(sky0="#020611", sky1="#0A1A33", haze="#3FD0FF", key="#B0ECFF", accent="#3FD0FF", ink="#FFFFFF"),
    "history": dict(sky0="#120C06", sky1="#3A2A16", haze="#D9B26A", key="#FFE2A8", accent="#E8B04A", ink="#FFF6E6"),
}


TONE_POSTER = {  # first poster scene per tone (backdrop, hero); the director replaces it in the brief
    "thriller": ("ocean", "bonds"), "crisis": ("rays", "arrow"), "strategy": ("map", "wafer"), "trade": ("map", "ship"),
    "tech": ("map", "wafer"), "history": ("skyline", "bonds"), "reflective": ("coast", "house"), "bright": ("rays", "cash")}


def draft_brief(slug: str, deliverable: str, project: dict, alias: str | None) -> Path:
    """Write a DRAFT brief for a new episode (tone from its visual direction plan). A draft never makes a package
    'ready': the director must replace the subject and words, set claim_basis, and delete `draft: true`."""
    from hiddeneco import visual_direction as vdir
    vd = vdir.load(REPO_ROOT / "projects" / slug) or {}
    tone = (vd.get("thumbnail") or {}).get("tone") or vd.get("primary_tone") or "strategy"
    subj, back = TONE_SUBJECT.get(tone, ("coin", "void"))
    words = re.sub(r"[^A-Za-z0-9$ ]", "", project.get("title", slug)).upper().split()
    text = [" ".join(words[:2]), " ".join(words[2:4])] if len(words) > 2 else [" ".join(words)]
    docs = REPO_ROOT / "docs" / "episodes" / slug
    pb, ph = TONE_POSTER.get(tone, ("map", "wafer"))
    b = {"title": project.get("title", slug), "docs_dir": str(docs.relative_to(REPO_ROOT)), "video": alias or "", "deliverable": deliverable,
         "status": "completed", "draft": True, "default": "P",
         "analysis": {"mystery": "TODO", "surprising_fact": "TODO (a verified claim id)", "subject": subj, "tone": tone, "metaphor": "TODO"},
         "concepts": [
             {"id": "P", "angle": "poster (owner model, default)", "archetype": "poster", "text": text[:2], "accent_line": len(text[:2]) - 1,
              "banner": "red", "claim_basis": "",
              "scene": {"backdrop": {"kind": pb, "arcs": [["ny", "london"], ["london", "shanghai"]] if pb == "map" else []},
                        "hero": {"kind": ph, "x": 1440, "y": 560, "s": 0.85}, "light": {"color": "#FFB238"},
                        "particles": {"n": 60, "region": [900, 0, 1920, 1080], "size": 4}}},
             {"id": "A", "angle": "mystery", "text": text, "accent_line": len(text) - 1, "text_side": "left", "claim_basis": "",
              "scene": {"palette": TONE_PALETTE.get(tone, TONE_PALETTE["strategy"]), "backdrop": back, "subject": {"kind": subj, "x": 1340, "y": 560, "s": 0.8},
                        "particles": {"n": 50, "region": [700, 60, 1900, 1000], "size": 2}, "brand": "tl"}},
             {"id": "B", "angle": "consequence", "text": text[-1:], "accent_line": 0, "text_side": "right", "claim_basis": "",
              "scene": {"palette": TONE_PALETTE.get(tone, TONE_PALETTE["strategy"]), "backdrop": back, "subject": {"kind": subj, "x": 600, "y": 560, "s": 0.75},
                        "particles": {"n": 50, "region": [0, 60, 1200, 1000], "size": 2}, "brand": "tr"}}]}
    who = public_figure(project)
    if who:   # a named public figure is central: the face archetype is the first alternative (poster stays default)
        b["analysis"]["public_figure"] = {"who": who, "name": FACE_PRESETS.get(who, who)}
        b["concepts"].insert(1, {"id": "F", "angle": "face (named public figure)", "archetype": "face", "text": text[:2], "claim_basis": "",
                                 "scene": {"bg": ["#3A8DFF", "#0A1F5C"], "bust": {"who": who, "expr": "point", "x": 470, "s": 0.92},
                                           "prop": {"kind": "number", "text": "?", "x": 1390, "y": 760, "s": 0.8}}})
    f = REPO_ROOT / "projects" / slug / "thumbnail_brief.yaml"
    f.write_text("# DRAFT thumbnail brief (auto). Replace subject/words, add claim_basis, remove `draft: true`.\n" +
                 yaml.safe_dump(b, sort_keys=False, allow_unicode=True, width=140), encoding="utf-8")
    _log(slug=slug, event="draft_brief")
    return f


FACE_NAMES = {"huang": ["jensen huang", "huang"], "pichai": ["sundar pichai", "pichai"], "musk": ["elon musk", "musk"],
              "jassy": ["andy jassy", "jassy"], "sam": ["sam walton"], "trump": ["donald trump", "trump"],
              "vachris": ["ron vachris", "vachris"], "sinegal": ["jim sinegal", "sinegal"]}


def public_figure(project: dict) -> str | None:
    """The bust preset of the named public figure central to an episode: `public_figure` in project.yaml (a preset key
    or {who: ...}), else a preset person's name in the title. None when no named figure is central."""
    pf = project.get("public_figure")
    if isinstance(pf, dict):
        pf = pf.get("who")
    if pf:
        return str(pf)
    title = str(project.get("title", "")).lower()
    for who, names in FACE_NAMES.items():
        if any(re.search(rf"\b{re.escape(n)}\b", title) for n in names):
            return who
    return None


def channel_thumbnails(exclude: str | None = None) -> dict[str, Path]:
    out = {}
    for f in (REPO_ROOT / "projects").glob("*/thumbnail_brief.yaml"):
        s = f.parent.name
        if s == exclude:
            continue
        try:
            b = yaml.safe_load(f.read_text(encoding="utf-8"))
            out[s] = REPO_ROOT / b["docs_dir"] / "youtube-package" / "thumbnail.png"
        except Exception:                               # noqa: BLE001
            pass
    return out
