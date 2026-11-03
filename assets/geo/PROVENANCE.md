# Map data provenance

| File | Built from | Licence |
|---|---|---|
| `europe_50m.geojson` | Natural Earth 1:50m Admin 0 Countries (Europe subset) | public domain |
| `world_emirates_50m.geojson` | Natural Earth 1:50m Admin 0 Countries (world, minus Antarctica and the UAE) + Natural Earth 1:10m Admin 1 (the UAE's seven emirates and two neutral zones). Coordinates rounded to 0.01 deg (countries) and 0.001 deg (emirates). | public domain |

Rebuild: download `ne_50m_admin_0_countries.geojson` and `ne_10m_admin_1_states_provinces.geojson` from
https://github.com/nvkelso/natural-earth-vector/tree/master/geojson and run
`python tools/build_world_geo.py <adm0> <adm1> assets/geo/world_emirates_50m.geojson`. Retrieved 2026-11-03.
