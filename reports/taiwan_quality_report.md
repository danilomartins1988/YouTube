# Quality report - why-taiwan-matters / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/why-taiwan-matters/documentary/why-taiwan-matters--documentary.mp4 (168.6 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 10-12 min | PASS | 713.50 s (11:53) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 320 cues; median cue-start offset 0.03 s, p90 0.31 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.1 LUFS integrated, true peak -3.6 dBFS
- Scenes: 42; types: act_title x5, bar_chart x1, channel_intro x1, compare x10, domino x1, end_card x1, kinetic_text x11, map x5, presenter x4, supply_chain x1, timeline_network x1, whiteboard x1
- Average scene length: 17.0 s; act cards are music-only.

## Pipeline QC report

# QC report: why-taiwan-matters / documentary (long_16x9)

- Runtime: **713.5 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 168.6 MB
- Loudness: -16.1 LUFS integrated, true peak -3.6 dBFS
- Errors: **0**, warnings: **46**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment m3_question pace 117 wpm (numerals count as one word)
- [WARNING] (timing) Segment m4_chain pace 116 wpm (numerals count as one word)
- [WARNING] (timing) Segment m5_race pace 97 wpm (numerals count as one word)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'seven' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'ten' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'six' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'thirty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'ten' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'thirty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'thirty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.

## Publish blockers - claims needing human verification

- `advanced_q4` (source_located): In Q4 2025, technologies of 7 nanometers and more advanced accounted for 77% of TSMC's wafer revenue (3nm 28%, 5nm 35%, 7nm 14%).  
  
- `apple_tsmc` (source_located): Apple-designed chips are manufactured by TSMC, including at its Arizona fab.  
  
- `asml_only` (source_located): ASML is the only company that makes EUV lithography systems, the machines used to print the smallest chip features; it shipped 48 EUV systems in 2025.  
  Sole-supplier status from ASML; shipment count from coverage of ASML's 2025 results.
- `auto_2021` (source_located): AlixPartners forecast that the 2021 chip shortage would cost the global auto industry $210 billion in revenue and 7.7 million vehicles of lost production.  
  
- `bloomberg_scenarios` (source_located): Bloomberg Economics' January 2024 scenarios: a war over Taiwan could cut world GDP by about 10% (roughly $10 trillion) in the first year; a yearlong blockade by about 5%. Bloomberg stresses the results depend heavily on assumptions.  
  
- `capex_2026` (source_located): In January 2026 TSMC guided 2026 capital spending of US$52-56 billion (later reports say the range was raised).  
  
- `chips_act_figs` (source_located): The 2022 US CHIPS and Science Act provides $52.7 billion for semiconductors, including $39 billion in manufacturing incentives.  
  
- `eu_target` (source_located): The European Chips Act aims to double the EU's share of global chip production to 20% by 2030.  
  
- `exports_2025` (source_located): Taiwan's exports reached a record US$640.75 billion in 2025, up 34.9%, with the United States taking 30.9%.  
  
- `fab_investment` (source_located): SIA/BCG project about $2.3 trillion of wafer-fab capital expenditure worldwide in 2024-2032.  
  
- `foundry_share` (source_located): TSMC held 72.5% of global foundry revenue among the top ten foundries in the second quarter of 2026 (TrendForce).  
  Share of FOUNDRY revenue (contract manufacturing), not of all chipmaking.
- `germany_esmc` (source_located): TSMC, Bosch, Infineon and NXP are building ESMC in Dresden, Germany, with production targeted for the end of 2027.  
  
- `japan_jasm` (source_located): TSMC's Japanese venture JASM opened its first fab in Kumamoto in February 2024; total investment is to exceed $20 billion.  
  
- `lt10_capacity` (source_located): SIA/BCG: in 2022 Taiwan held 69% of global wafer-fab capacity for logic chips below 10 nm, South Korea 31% and the US 0%; in its 2032 forecast Taiwan has 47% and the US 28%.  
  
- `nvda_1993` (source_located): NVIDIA was incorporated in California in April 1993; it designs chips and relies on foundry partners such as TSMC to manufacture them (10-K).  
  
- `taiwan_area` (source_located): Taiwan's total area is 35,980 sq km and Switzerland's 41,277 sq km (CIA World Factbook): Taiwan is smaller.  
  
- `total_capacity` (source_located): SIA/BCG: in 2022 Taiwan held 18% of total global wafer-fabrication capacity across all chip types (China 24%, Korea 17%, Japan 17%, US 10%), and South Korea held 52% of DRAM memory capacity.  
  
- `tsmc_1987` (source_located): TSMC was established in 1987 as the world's first dedicated semiconductor foundry, with backing from Taiwan's government and Philips.  
  
- `tsmc_customers` (source_located): TSMC's 2025 annual report shows its largest customer at 19% of revenue and the second at 17%; Nvidia's CEO has said Nvidia is the largest, and the second is widely reported to be Apple. Nvidia's 10-K lists TSMC as a wafer supplier.  
  
- `tsmc_revenue_2025` (source_located): TSMC's 2025 revenue was US$122.42 billion, up 35.9% in US dollar terms (4Q25 earnings call).  
  
- `tsmc_us_165` (source_located): In March 2025 TSMC said it would expand its US investment to $165 billion, for six fabs, two advanced packaging plants and an R&D center in Arizona.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

