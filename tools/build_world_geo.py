"""Build assets/geo/world_emirates_50m.geojson from Natural Earth (public domain).

World countries at 1:50m (coordinates rounded to 0.01 deg) with the United Arab Emirates replaced by
its seven emirates at 1:10m (rounded to 0.001 deg). Every feature keeps the two properties the
renderer needs: ADM0_A3 (an ISO 3166-1 alpha-3 code, or an ISO 3166-2 code such as AE-DU for an
emirate) and NAME.

    python tools/build_world_geo.py ne_50m_admin_0_countries.geojson \
        ne_10m_admin_1_states_provinces.geojson assets/geo/world_emirates_50m.geojson
"""
from __future__ import annotations

import json
import sys


def _round(coords, nd):
    if isinstance(coords[0], (int, float)):
        return [round(coords[0], nd), round(coords[1], nd)]
    return [_round(c, nd) for c in coords]


def _dedupe(geom):
    """Drop consecutive duplicate points created by rounding; drop degenerate rings."""
    def ring(r):
        out = [r[0]]
        for p in r[1:]:
            if p != out[-1]:
                out.append(p)
        return out if len(out) >= 4 else None
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    cleaned = []
    for poly in polys:
        rings = [x for x in (ring(r) for r in poly) if x]
        if rings:
            cleaned.append(rings)
    return {"type": "MultiPolygon", "coordinates": cleaned} if cleaned else None


def main(adm0: str, adm1: str, out: str) -> None:
    feats = []
    for f in json.load(open(adm0, encoding="utf-8"))["features"]:
        p = f["properties"]
        if p["ADM0_A3"] in ("ARE", "ATA"):
            continue
        g = _dedupe({"type": f["geometry"]["type"], "coordinates": _round(f["geometry"]["coordinates"], 2)})
        if g:
            feats.append({"type": "Feature", "properties": {"ADM0_A3": p["ADM0_A3"], "NAME": p["NAME"]},
                          "geometry": g})
    for f in json.load(open(adm1, encoding="utf-8"))["features"]:
        p = f["properties"]
        if p.get("adm0_a3") != "ARE":
            continue
        code = p["iso_3166_2"].rstrip("~")
        name = (p.get("name_en") or p["name"]).replace("Emirate of ", "")
        g = _dedupe({"type": f["geometry"]["type"], "coordinates": _round(f["geometry"]["coordinates"], 3)})
        if g:
            feats.append({"type": "Feature", "properties": {"ADM0_A3": code, "NAME": name}, "geometry": g})
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": feats}, fh, separators=(",", ":"))
    print(f"{len(feats)} features -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
