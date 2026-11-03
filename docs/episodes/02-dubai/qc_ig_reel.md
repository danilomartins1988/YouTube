# QC report: how-dubai-really-makes-money / ig_reel (short_9x16)

- Runtime: **44.1 s**
- Video: 1080x1920 @ 30/1 h264, audio aac 48000 Hz, 23.2 MB
- Loudness: -14.6 LUFS integrated, true peak -4.2 dBFS
- Errors: **0**, warnings: **3**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment hook pace 82 wpm (numerals count as one word)
- [WARNING] (timing) Segment rules pace 116 wpm (numerals count as one word)
- [WARNING] (timing) Segment courts pace 109 wpm (numerals count as one word)

## Publish blockers - claims needing human verification

- `ct_rate` (source_located): The UAE corporate tax rate is 9% on taxable income above AED 375,000 (0% below), for financial years starting on or after 1 June 2023.  
  
- `difc_2025` (source_located): At the end of 2025 the DIFC had 8,844 active companies and a workforce of 50,200, including more than 290 banks and capital-markets firms.  
  
- `difc_courts` (source_located): The DIFC, created under Dubai law in 2004, has its own English-language common-law courts.  
  
- `free_zones` (source_located): Dubai has more than 20 free zones (Invest in Dubai).  
  Commercial sites say 25-30+; government wording "20+". Confirm the page.
- `jafza_firms` (source_located): Jebel Ali Free Zone (Jafza), established in 1985, started with 19 companies and now hosts over 11,000 businesses from 157 countries.  
  
- `onshore_ownership` (source_located): Since 1 June 2021, foreign investors can own 100% of most onshore UAE companies, after the amendment of the Commercial Companies Law (Federal Decree-Law No. 26 of 2020).  
  
- `qfzp` (source_located): A Qualifying Free Zone Person pays 0% corporate tax on qualifying income and 9% on other income, subject to substance and other conditions.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.
