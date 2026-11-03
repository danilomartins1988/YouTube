# QC report: why-switzerland-is-so-rich / short_exports (short_9x16)

- Runtime: **34.63 s**
- Video: 1080x1920 @ 30/1 h264, audio aac 48000 Hz, 17.4 MB
- Loudness: -14.4 LUFS integrated, true peak -4.3 dBFS
- Errors: **0**, warnings: **4**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment reveal pace 106 wpm (numerals count as one word)
- [WARNING] (timing) Segment payoff pace 106 wpm (numerals count as one word)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.

## Publish blockers - claims needing human verification

- `geo_landlocked` (source_located): Switzerland is landlocked (it has no sea coast).  
  Visible in the Natural Earth boundaries used for the map; a reviewer only needs to confirm and sign off. ('Mountainous' was cut from the script because it had no citation.)
- `pharma_share_2024` (source_located): Chemical and pharmaceutical products accounted for 52.7% of Swiss (goods) exports in 2024 (CHF 149,058 million).  
  Figure taken from a search summary of the FOCBS 2024 annual report. Confirm the 52.7% and which export total it refers to (FOCBS 'Total 1' business-cycle total excludes gold and other precious metals) and word the on-screen label accordingly.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.
