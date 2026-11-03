"""Minimal map rendering from GeoJSON: equirectangular projection with latitude correction."""
from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


@lru_cache(maxsize=4)
def load_countries(path: str) -> dict[str, dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = {}
    for f in data["features"]:
        code = f["properties"]["ADM0_A3"]
        geom = f["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        rings = []
        for poly in polys:
            for i, ring in enumerate(poly):
                arr = np.asarray(ring, dtype=np.float64)
                rings.append({"xy": arr, "hole": i > 0,
                              "bbox": (arr[:, 0].min(), arr[:, 1].min(), arr[:, 0].max(), arr[:, 1].max())})
        outer = [r for r in rings if not r["hole"]]
        biggest = max(outer, key=lambda r: (r["bbox"][2] - r["bbox"][0]) * (r["bbox"][3] - r["bbox"][1]))
        out[code] = {"name": f["properties"]["NAME"], "rings": rings,
                     "label_lonlat": tuple(biggest["xy"].mean(axis=0))}
    return out


class View:
    """Camera: centre (lon, lat), horizontal span in degrees of longitude, screen anchor point."""

    def __init__(self, lon: float, lat: float, span_deg: float, W: int, H: int, anchor=(0.5, 0.5)):
        self.lon, self.lat, self.span = lon, lat, span_deg
        self.W, self.H = W, H
        self.k = W / span_deg
        self.ky = self.k / math.cos(math.radians(lat))
        self.cx, self.cy = W * anchor[0], H * anchor[1]

    def project(self, lonlat: np.ndarray) -> np.ndarray:
        x = (lonlat[..., 0] - self.lon) * self.k + self.cx
        y = self.cy - (lonlat[..., 1] - self.lat) * self.ky
        return np.stack([x, y], axis=-1)

    def visible(self, bbox) -> bool:
        (x0, y1), (x1, y0) = self.project(np.array([[bbox[0], bbox[1]], [bbox[2], bbox[3]]]))
        return x1 >= 0 and x0 <= self.W and y1 >= 0 and y0 <= self.H


def interpolate_view(a: dict, b: dict, u: float, W: int, H: int, anchor_a=(0.5, 0.5),
                     anchor_b=(0.5, 0.5)) -> View:
    """Zoom in log space so the push-in feels constant-speed."""
    span = math.exp(math.log(a["span_deg"]) * (1 - u) + math.log(b["span_deg"]) * u)
    lon = a["lon"] + (b["lon"] - a["lon"]) * u
    lat = a["lat"] + (b["lat"] - a["lat"]) * u
    anchor = (anchor_a[0] + (anchor_b[0] - anchor_a[0]) * u, anchor_a[1] + (anchor_b[1] - anchor_a[1]) * u)
    return View(lon, lat, span, W, H, anchor)


def draw_map(img: Image.Image, countries: dict, view: View, land, border, fills: dict | None = None,
             ss: int = 2, border_px: float = 1.2) -> None:
    """Render land polygons onto img (RGB) with supersampling for smooth coastlines."""
    fills = fills or {}
    W, H = img.size
    big = img.resize((W * ss, H * ss), Image.NEAREST)
    d = ImageDraw.Draw(big)
    width = max(1, int(round(border_px * ss)))
    order = sorted(countries, key=lambda c: c in fills)  # highlighted countries drawn last
    for code in order:
        c = countries[code]
        colour = fills.get(code, land)
        for ring in c["rings"]:
            if not view.visible(ring["bbox"]):
                continue
            pts = (view.project(ring["xy"]) * ss).ravel().tolist()
            if len(pts) < 6:
                continue
            if not ring["hole"]:  # enclaves are separate features, so holes can be skipped
                d.polygon(pts, fill=colour, outline=border, width=width)
    img.paste(big.resize((W, H), Image.BOX))
