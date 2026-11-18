# Quality report - why-ai-could-make-your-electricity-bill-explode / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/why-ai-could-make-your-electricity-bill-explode/documentary/why-ai-could-make-your-electricity-bill-explode--documentary.mp4 (228.6 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 11-13:20 min (channel standard 660-800 s) | PASS | 741.00 s (12:21) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 369 cues; median cue-start offset 0.05 s, p90 0.40 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.2 LUFS integrated, true peak -4.2 dBFS
- Scenes: 38; types: channel_intro x1, end_card x1, engine_cartoon x32, engine_draw x4
- Average scene length: 19.5 s; act cards are music-only.

## Pipeline QC report

# QC report: why-ai-could-make-your-electricity-bill-explode / documentary (long_16x9)

- Runtime: **741.0 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 228.6 MB
- Loudness: -16.2 LUFS integrated, true peak -4.2 dBFS
- Errors: **0**, warnings: **29**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment c5_gs5 pace 120 wpm (numerals count as one word)
- [WARNING] (timing) Segment c6_maya pace 191 wpm (numerals count as one word)
- [WARNING] (captions) Caption reading speed >25 chars/s: 'The market monitor estimates that across'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'its last several auctions,'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'data centers were behind almost half of'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'None of it has settled the real'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'question.'
- [WARNING] (sources) Number word 'double' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'triple' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'third' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (licensing) Dataset eia_srp has no licence recorded
- [WARNING] (licensing) Dataset eia_srp has no licence recorded
- [WARNING] (licensing) Dataset steo_nov26 has no licence recorded
- [WARNING] (licensing) Dataset steo_nov26 has no licence recorded
- [WARNING] (licensing) Dataset steo_nov26 has no licence recorded
- [WARNING] (distinctiveness) Scene sequence 85% similar to 'why-the-world-still-depends-on-chinese-factories/documentary'
- [WARNING] (distinctiveness) Scene sequence 85% similar to 'who-actually-owns-americas-debt/documentary'
- [WARNING] (distinctiveness) Scene sequence 81% similar to 'why-americans-can-no-longer-afford-a-home/documentary'
- [WARNING] (distinctiveness) Scene sequence 81% similar to 'who-gets-rich-when-robots-do-the-work/documentary'
- [WARNING] (distinctiveness) Scene sequence 86% similar to 'how-costco-makes-billions-selling-almost-nothing/documentary'

## Publish blockers - claims needing human verification

- `aep_ohio` (source_located): AEP Ohio data center tariff adopted by PUCO (Case 24-0508; AEP release July 9, 2025): new data centers of 25 MW or more pay for at least 85% of subscribed capacity; contract up to 12 years incl. a ramp of up to 4 years; exit fee of 36 months of minimum charges.  
  
- `bra2829` (source_located): PJM 2028/29 BRA (Jul 14, 2026): cleared at the FERC-approved cap $325/MW-day (2.5% below $333.44 in 2027/28); cleared supply x price = $16.4 billion; 6,831 MW short of the reliability requirement; grid serves more than 67 million people in 13 states and DC; first auctions in PJM history (this and 2027/28) in which the whole RTO fell short; 525 MW UCAP new generation and uprates cleared. 2024/25 RTO price: $28.92/MW-day (OUR CALCULATION: $325 / $28.92 = 11.2 times).  
  
- `capex` (source_located): 2025 Forms 10-K: Dominion Energy planned capital expenditures 2026-2030 total $65.7 billion; AEP forecasts $12.2 billion in 2026 plus $59.7 billion for 2027-2030 (OUR SUM: $71.9 billion, 2026-2030). OUR SUM of both: $137.6 billion.  
  
- `dc_twh` (source_located): DOE/LBNL (Dec 2024): US data center electricity use 58 TWh (2014) -> 176 TWh (2023), 4.4% of US electricity; projected 325-580 TWh by 2028 (6.7-12%), a FORECAST range.  
  
- `deals` (source_located): Disclosed deals: Microsoft, 20-year PPA with Constellation for the restarted Crane Clean Energy Center, 835 MW (Constellation); Meta, 20-year PPA for 1,121 MW from Clinton from June 2027, replacing a state support program 'without ratepayer support' (Constellation); Amazon, 1,920 MW of nuclear power from Talen's Susquehanna through 2042 (Talen release as reported by APPA).  
  
- `gs5` (source_located): Virginia SCC final order: new rate class GS-5 for customers of 25 MW or more with load factor >= 75%; for service agreements from Jan 1, 2027 the contract term is 14 years (ramp up to 4 years); minimum demand charges 85% of contracted demand for distribution and transmission, 60% for generation; exit fee covering outstanding minimum charges.  
  
- `imm_cost` (source_located): PJM Market Monitor (Jul 28, 2026): total cost of wholesale power Jan-Jun 2026 $114.50/MWh vs $76.16 Jan-Jun 2025 (+50.3%); capacity costs +207.1%, 17.1% of total; energy 63.5%; transmission 17.4%; $11.11/MWh (9.7%) of the H1 2026 total attributed to data center load (monitor's estimate). Winter Storm Fern also raised H1 2026 energy costs (EIA STEO Oct 2026).  
  Data-center share is the monitor's own estimate, attributed in narration. "tripled" = +207.1% (rounded).
- `imm_dc` (source_located): PJM Market Monitor (Jul 28, 2026): of the $16.4B 2028/29 capacity charges, $6.3B (38.2%) resulted from data center load; over the last four auctions $29.4B (46.2%). Data center load in the forecast: 7,927 MW (2025/26) -> 21,470 MW (2028/29). Monitor's estimates.  
  Monitor's own estimates, attributed.
- `lbnl_load` (source_located): LBNL report summarized by Brattle (Oct 17, 2025): 'Load growth has tended to depress retail electricity prices in recent years, though it is unclear to what extent this will hold in the future.' National average retail prices have tracked inflation.  
  
- `pjm_peak` (source_located): PJM 2026 Long-Term Load Forecast (Jan 14, 2026): summer peak forecast ~222,000 MW in 2036 (2025 actual: over 161,000 MW); 3.6%/yr over ten years vs 0.3%/yr in the 2021 forecast (OUR CALCULATION: 12 times the growth rate); data centers the main driver; near-term 2027 peak trimmed 3,735 MW.  
  
- `scc_bill` (source_located): Virginia SCC final order: approved base-rate increases mean a typical residential customer (1,000 kWh/month) pays about $11.24 (7.5%) more a month in 2026 and $2.36 (1.5%) more in 2027; Dominion had proposed $14.73 (9.8%). OUR CALCULATION: $11.24 / 7.5% = about $150 implied typical monthly bill.  
  
- `scc_ror` (source_located): Virginia SCC final order PUR-2025-00058: the class cost-of-service study shows customers that will form GS-5 (large, mostly data centers) earned a per-books return of 3.01% on the transmission function vs 22.41% for remaining GS-4 customers (6.28% vs 20.75% overall); the commission will examine transmission cost allocation in the next proceeding. OUR CALCULATION: 3.01 / 22.41 = 0.13, about one-seventh.  
  
- `steo_res` (source_located): EIA STEO (Nov 10, 2026): US residential electricity price 16.5 cents/kWh (2024), 17.2 (2025), 18.2 (2026 projected), 18.7 (2027 projected). OUR CALCULATION: 2024 -> 2027 = +13%.  
  
- `steo_supply` (source_located): EIA STEO (Nov 10, 2026): about 72 GW of new solar and 20 GW of new wind capacity expected this year and next.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

