# Episode 27: The Day Oil Was Worth Less Than Nothing (WTI below zero, 20 April 2020; top-10 #10)

- Project: `projects/the-day-oil-was-worth-less-than-nothing` (sources, script, visual direction, thumbnail brief)
- Storyboard generator: `tools/gen_oil_storyboard.py` (39 scenes; presenter: where the extra oil goes, sell or take the oil, the price of a tank, that Monday)
- New engine pieces in CartoonStage: `tankfarm` set; `oiltank` (fill gauge) and `barrel` (price tag, money paid away) items; `tradescreen` now supports negative values (`min`, a $0 line, `decimals`, `lamp: false`, `haltText`). New thumbnail subject `oilbarrel`.
- Main sources: the CFTC interim staff report (Nov 2020), EIA Today in Energy (Apr 2020, Jan 2021), CRS Insight IN11354.
- No claim about who caused the drop (the CFTC interim report names no cause).
- Output (after render): `output/oil_documentary.mp4`; package in `youtube-package/`; Short in `youtube-short/`.
