# QC report: how-dubai-really-makes-money / tiktok (extended_9x16)

- Runtime: **89.0 s**
- Video: 1080x1920 @ 30/1 h264, audio aac 48000 Hz, 46.7 MB
- Loudness: -14.7 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **5**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment hook pace 102 wpm (numerals count as one word)
- [WARNING] (timing) Segment buyers pace 110 wpm (numerals count as one word)
- [WARNING] (timing) Segment crash pace 110 wpm (numerals count as one word)
- [WARNING] (timing) Segment bailout pace 110 wpm (numerals count as one word)
- [WARNING] (timing) Segment outro pace 104 wpm (numerals count as one word)

## Publish blockers - claims needing human verification

- `bailout_2009` (source_located): On 14 December 2009 Abu Dhabi provided $10 billion to Dubai, part of which repaid a maturing Nakheel Islamic bond.  
  
- `burj_renamed` (source_located): The world's tallest building opened on 4 January 2010 and was renamed from Burj Dubai to Burj Khalifa, after Abu Dhabi's ruler and UAE President Sheikh Khalifa.  
  
- `crash_2009` (source_located): Dubai property prices fell by about half from their mid-2008 peak by mid-2009 (Colliers International, as reported by Gulf News).  
  
- `emaar_owner` (source_located): Since May 2026 Dubai Holding, a government-owned group, is Emaar Properties' largest shareholder with 29.73%, after buying the Investment Corporation of Dubai's 22.27% stake.  
  
- `imf_correction_risk` (source_located): The IMF warns the real estate sector may be affected by a slowdown or reversal of capital flows or a shift in investor sentiment that could lead to an unexpected price correction.  
  
- `imf_prices` (source_located): IMF (2025 Article IV) - Dubai prices rose 117.6% for villas and 46.2% for apartments between 2020Q1 and 2025Q2; 83.4% of 2024 residential transactions were non-mortgaged.  
  
- `re_2025` (source_located): Dubai real estate recorded over 270,000 transactions worth AED 917 billion in 2025, up from AED 761 billion in 2024.  
  AED 917bn covers all transaction types (sales and other deals) per DLD; sales alone were lower. Label as "transactions".
- `standstill_2009` (source_located): On 25 November 2009 Dubai asked creditors of Dubai World and its property units for a standstill on about $26 billion of debt.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.
