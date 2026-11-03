# QC report: how-dubai-really-makes-money / yt_short (short_9x16)

- Runtime: **44.27 s**
- Video: 1080x1920 @ 30/1 h264, audio aac 48000 Hz, 22.7 MB
- Loudness: -14.6 LUFS integrated, true peak -4.2 dBFS
- Errors: **0**, warnings: **1**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment proof pace 79 wpm (numerals count as one word)

## Publish blockers - claims needing human verification

- `dxb_pax_2025` (source_located): Dubai International Airport (DXB) handled 95.2 million passengers in 2025.  
  
- `non_oil_share` (source_located): The Government of Dubai states that over 95% of Dubai's GDP is non-oil based.  
  Confirm the exact wording and page on dubai.ae. Do not upgrade to "under 1% oil" without a primary statistical table.
- `reserves_split` (source_located): Abu Dhabi holds about 94% of the UAE's oil reserves and Dubai about 4% (US ITA citing the 2019 UAE State of Energy Report).  
  Secondary (US government) citing a 2019 UAE report. Look for a current UAE primary source.
- `sectors_h1_2026` (source_located): Shares of Dubai's real GDP, H1 2026 (DDSE, revised series): wholesale and retail trade 20.5%, financial and insurance 14.0%, real estate 11.8%, transport and storage 10.7%.  
  Read the DDSE table; confirm that shares are of real GDP for H1 2026 on the revised series.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.
