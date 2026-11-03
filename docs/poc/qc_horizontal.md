# QC report: why-switzerland-is-so-rich / horizontal (long_16x9)

- Runtime: **82.37 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 42.1 MB
- Loudness: -16.6 LUFS integrated, true peak -4.2 dBFS
- Errors: **0**, warnings: **1**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment compare pace 194 wpm (numerals count as one word)

## Publish blockers - claims needing human verification

- `geo_landlocked` (source_located): Switzerland is a landlocked, mountainous country.  
  Landlocked status is visible in the Natural Earth boundaries. 'Mountainous' needs a citation (e.g. Swiss Federal Statistical Office land-use statistics) or should be cut.
- `gii_2025_rank` (source_located): In the Global Innovation Index 2025, WIPO ranked Switzerland first of 139 economies.  
  Confirm 139 economies and rank in WIPO's press release. Secondary sources disagree on the length of the streak (14th vs 15th year), so the script deliberately does not mention it.
- `gii_2025_top5` (source_located): GII 2025 top five: Switzerland, Sweden, United States, Republic of Korea, Singapore.  
  Confirm order in WIPO's ranking table.
- `neutrality_1815` (source_located): Europe's great powers formally recognised Swiss neutrality in 1815 (Congress of Vienna and the Second Treaty of Paris).  
  admin.ch dates the recognition to 1815 via the Congress of Vienna and the Treaty of Paris. Check exact wording on both pages.
- `pharma_share_2024` (source_located): Chemical and pharmaceutical products accounted for 52.7% of Swiss (goods) exports in 2024 (CHF 149,058 million).  
  Figure taken from a search summary of the FOCBS 2024 annual report. Confirm the 52.7% and which export total it refers to (FOCBS 'Total 1' business-cycle total excludes gold and other precious metals) and word the on-screen label accordingly.
- `vet_share` (source_located): About two-thirds of young people in Switzerland enter vocational education and training (VET); the most common form is dual-track VET combining classroom instruction with workplace training.  
  SERI states that two-thirds of young people benefit from VET. Confirm exact phrasing; do not conflate with annual 'Transition Barometer' interest percentages.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.
