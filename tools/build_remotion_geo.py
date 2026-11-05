"""Pre-project Natural Earth countries (public domain) to Web-Mercator SVG paths for the Remotion engine.

World size S=4096 units (must match remotion/src/scenes/MapScene.tsx). Writes
assets/geo/remotion_<layer>.json = {view, paths: {ADM0_A3: d}}.

    python tools/build_remotion_geo.py <ne_10m_admin_0_countries.geojson> <ne_50m_admin_0_countries.geojson>
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

S = 4096
OUT = Path(__file__).resolve().parents[1] / "assets" / "geo"


def merc(lon, lat):
    lat = max(-85.0, min(85.0, lat))
    x = (lon + 180) / 360 * S
    y = S / 2 - S / (2 * math.pi) * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y


def path_d(geom, min_step, bbox=None):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    out = []
    for poly in polys:
        ring = poly[0]  # outer ring only; lakes/holes are not needed at this scale
        if bbox:
            lons = [p[0] for p in ring]; lats = [p[1] for p in ring]
            if max(lons) < bbox[0] or min(lons) > bbox[2] or max(lats) < bbox[1] or min(lats) > bbox[3]:
                continue
        pts, last = [], None
        for lon, lat in ring:
            x, y = merc(lon, lat)
            if last is None or abs(x - last[0]) + abs(y - last[1]) >= min_step:
                pts.append((x, y)); last = (x, y)
        if len(pts) >= 4:
            out.append("M" + " ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z")
    return "".join(out)


def layer(src, bbox, min_step, codes=None):
    paths = {}
    for f in json.load(open(src, encoding="utf-8"))["features"]:
        code = f["properties"].get("ADM0_A3")
        if code == "ATA" or (codes and code not in codes):
            continue
        d = path_d(f["geometry"], min_step, bbox)
        if d:
            paths[code] = paths.get(code, "") + d
    return paths


def main(ne10, ne50):
    europe_bbox = (-45, 30, 60, 83)
    europe = layer(ne10, europe_bbox, 0.06)
    (OUT / "remotion_europe.json").write_text(json.dumps({"view": list(europe_bbox), "paths": europe}, separators=(",", ":")))
    world = layer(ne50, None, 0.6)
    (OUT / "remotion_world.json").write_text(json.dumps({"view": [-180, -60, 180, 83], "paths": world}, separators=(",", ":")))
    for n in ("europe", "world"):
        print(n, (OUT / f"remotion_{n}.json").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main(*sys.argv[1:3])
