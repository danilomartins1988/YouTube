# Quality report - why-norway-is-so-rich / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | output/norway_documentary.mp4 (131.7 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 10-12 min | PASS | 654.70 s (10:54) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 275 cues; median cue-start offset 0.05 s, p90 0.39 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>6 s) | FAIL | 95.2s, 155.8s, 176.8s, 267.9s, 294.7s, 386.8s, 462.2s, 475.4s, 512.6s, 531.5s, 570.6s, 605.3s, 623.0s |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Scenes: 48; types: act_title x10, bar_chart x3, big_counter x3, compare x5, donut x2, fund_flow x4, isometric x2, kinetic_text x6, line_chart x2, map x5, oil_platform x3, people_ratio x1, timeline x2
- Average scene length: 13.6 s; act cards are music-only.

## Pipeline QC report

# QC report: why-norway-is-so-rich / documentary (long_16x9)

- Runtime: **654.7 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 131.7 MB
- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **54**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment open_stake pace 86 wpm (numerals count as one word)
- [WARNING] (timing) Segment p1_economy pace 117 wpm (numerals count as one word)
- [WARNING] (timing) Segment p2_doubt pace 120 wpm (numerals count as one word)
- [WARNING] (timing) Segment p2_shelf pace 112 wpm (numerals count as one word)
- [WARNING] (timing) Segment p2_ekofisk pace 102 wpm (numerals count as one word)
- [WARNING] (timing) Segment p2_production pace 83 wpm (numerals count as one word)
- [WARNING] (timing) Segment p3_commandments pace 101 wpm (numerals count as one word)
- [WARNING] (timing) Segment p3_statoil pace 94 wpm (numerals count as one word)
- [WARNING] (timing) Segment p3_tax pace 114 wpm (numerals count as one word)
- [WARNING] (timing) Segment p4_cashflow pace 117 wpm (numerals count as one word)
- [WARNING] (timing) Segment p4_exports pace 114 wpm (numerals count as one word)
- [WARNING] (timing) Segment p4_problem pace 115 wpm (numerals count as one word)
- [WARNING] (timing) Segment p5_law pace 101 wpm (numerals count as one word)
- [WARNING] (timing) Segment p6_world pace 105 wpm (numerals count as one word)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'billion' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'thousand' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'quarter' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'third' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (render) Picture static for >4 s from 96.07s (pacing?)
- [WARNING] (render) Picture static for >4 s from 156.23s (pacing?)
- [WARNING] (render) Picture static for >4 s from 177.00s (pacing?)
- [WARNING] (render) Picture static for >4 s from 187.50s (pacing?)
- [WARNING] (render) Picture static for >4 s from 192.50s (pacing?)
- [WARNING] (render) Picture static for >4 s from 197.87s (pacing?)
- [WARNING] (render) Picture static for >4 s from 230.13s (pacing?)
- [WARNING] (render) Picture static for >4 s from 267.97s (pacing?)
- [WARNING] (render) Picture static for >4 s from 278.30s (pacing?)
- [WARNING] (render) Picture static for >4 s from 289.60s (pacing?)
- [WARNING] (render) Picture static for >4 s from 294.80s (pacing?)
- [WARNING] (render) Picture static for >4 s from 336.63s (pacing?)
- [WARNING] (render) Picture static for >4 s from 342.20s (pacing?)
- [WARNING] (render) Picture static for >4 s from 387.20s (pacing?)
- [WARNING] (render) Picture static for >4 s from 464.20s (pacing?)
- [WARNING] (render) Picture static for >4 s from 475.47s (pacing?)
- [WARNING] (render) Picture static for >4 s from 483.90s (pacing?)
- [WARNING] (render) Picture static for >4 s from 493.50s (pacing?)
- [WARNING] (render) Picture static for >4 s from 497.93s (pacing?)
- [WARNING] (render) Picture static for >4 s from 512.40s (pacing?)
- [WARNING] (render) Picture static for >4 s from 520.33s (pacing?)
- [WARNING] (render) Picture static for >4 s from 531.40s (pacing?)
- [WARNING] (render) Picture static for >4 s from 570.80s (pacing?)
- [WARNING] (render) Picture static for >4 s from 605.50s (pacing?)
- [WARNING] (render) Picture static for >4 s from 624.90s (pacing?)

## Publish blockers - claims needing human verification

- `ageing` (source_located): SSB's 2024-based projections (main alternative) imply 3.2 people aged 20-64 for every person aged 65+ in 2024, falling to 2.1 by 2050 (31.7 and 47.6 people aged 65+ per 100 aged 20-64).  
  Ratios are our calculation from SSB table 14288.
- `allocation_q3_2026` (source_located): Fund allocation at 30 September 2026: equities 72.1%, fixed income 25.8%, unlisted real estate 1.6%, unlisted renewable energy infrastructure 0.5%.  
  
- `bad_years` (source_located): The fund returned -23.3% in 2008 (financial crisis) and -14.1% in 2022; it returned 15.1% in 2025.  
  
- `budget_2026_deficit` (source_located): The 2026 budget's structural non-oil deficit is NOK 579.4 billion, 2.8% of the fund's value and 13.1% of mainland trend GDP.  
  From search snippet of the Ministry page (403). The revised budget restates it as NOK 584.0bn (price basis).
- `budget_share` (source_located): According to the IMF (2026 Article IV), withdrawals from the fund finance about a fourth of public expenditure; NBIM's own page says almost 20 percent of the government budget.  
  Sources differ (IMF 2026 'about a fourth' of expenditure; NBIM undated 'almost 20 percent' of the budget). Narration attributes to the IMF.
- `cashflow_2022` (source_located): In 2022 the state's net cash flow from petroleum activities reached a record NOK 1,285 billion.  
  
- `cashflow_series` (source_located): Net government cash flow from petroleum activities, NOK billion (SSB): 2022 1,285; 2023 978; 2024 702; 2025 664.  
  
- `deposits_less_than_half` (source_located): According to NBIM, petroleum-revenue deposits account for less than half of the fund's value; the rest is investment return.  
  
- `ekofisk_1969` (source_located): Phillips Petroleum reported the Ekofisk discovery to the Norwegian government just before Christmas 1969 (23 December); it was then the world's largest offshore field.  
  Discovery (October 1969) vs announcement (23 December). The script uses the announcement. 'World's largest offshore field' is from the Petroleum Museum (secondary).
- `ekofisk_production` (source_located): Production from Ekofisk started on 15 June 1971.  
  
- `equinor_67` (source_located): The Norwegian state owns 67% of the shares in Equinor (formerly Statoil).  
  
- `first_transfer_1996` (source_located): On 30 May 1996 the Ministry of Finance made the first transfer, of almost 2 billion kroner, to the Government Petroleum Fund.  
  
- `fiscal_rule` (source_located): Under the fiscal rule (since 2001), transfers from the fund to the budget shall over time follow the expected real return on the fund, set at 4% in 2001 and reduced to 3% in 2017.  
  Ministry page returned 403; wording from snippet. Reviewer to read the page.
- `frontfag` (source_located): In Norwegian wage bargaining, industries exposed to international competition negotiate first, setting a norm for the rest of the economy (SSB, 2023).  
  
- `fund_companies` (source_located): At the end of 2025 the fund held shares in 7,201 companies, with investments in 68 countries.  
  
- `fund_law_1990` (source_located): In 1990 the Storting passed a law establishing the Government Petroleum Fund to receive petroleum revenue.  
  
- `fund_ownership_share` (source_located): At the end of 2025 the fund's average holding in the world's listed companies was 1.5 percent.  
  
- `fund_per_person` (source_located): Our calculation: NOK 22,014bn (30 Sep 2026) divided by Norway's population of 5,636,904 (1 July 2026, SSB) is about NOK 3.9 million per person.  
  Derived figure (not published by NBIM). Label 'our calculation' on screen.
- `fund_value_q3_2026` (source_located): The Government Pension Fund Global was valued at NOK 22,014 billion on 30 September 2026.  
  
- `fund_value_series` (source_located): Fund market value at year end, NOK billion (NBIM): 1996 47.4; 1999 222.4; 2001 613.7; 2005 1,399.1; 2008 2,275.4; 2010 3,077.4; 2012 3,815.8; 2014 6,430.7; 2016 7,510.5; 2018 8,256.0; 2020 10,913.8; 2022 12,429.1; 2023 15,764.8; 2024 19,755.0; 2025 21,268.  
  Read from the NBIM history timeline, which lists each value against the following year; confirm the year mapping with NBIM's key-figures data. nbim.no market-value page gives 15,757 (2023) and 19,742 (2024). Points are uneven years, so the chart interpolates between them.
- `gas_share_europe` (source_located): Norway's gas exports in 2025 equalled more than 30% of the total gas consumption of the EU and the UK, through a pipeline network of about 8,800 km.  
  
- `geology_1958` (source_located): In 1958 the Geological Survey of Norway told the Foreign Ministry that the chance of finding coal, oil or sulphur on the continental shelf could be discounted.  
  
- `gini_2024` (source_located): Norway's Gini coefficient for equivalised household income was 0.256 in 2024 (SSB).  
  "One of the most equal" is comparative; confirm against OECD income distribution data before publishing, or drop the comparison.
- `governance` (source_located): The Storting sets the fund's framework in the Government Pension Fund Act, the Ministry of Finance has overall responsibility and issues guidelines, and Norges Bank manages it.  
  
- `hydro_1905` (source_located): Norsk Hydro was founded on 2 December 1905, using hydropower to produce nitrogen fertiliser.  
  
- `imf_insulate` (source_located): IMF (2014): the fiscal rule and the Government Pension Fund Global would largely insulate the economy from the direct effects of lower oil revenue.  
  
- `imf_strength` (source_located): IMF (3 Sep 2026): Norway 'faces a challenging global environment from a position of strength'.  
  
- `maddison_1970` (source_located): Maddison Project 2023, GDP per capita in 2011 international dollars, 1970: Norway 15,983, Sweden 20,269, Denmark 20,221 (Norway about 79% of Sweden).  
  Ratio is our arithmetic from the 1970 values. Use decade points (the annual Swedish series has a jump 1960-65).
- `mainland_share` (source_located): In 2025, Mainland Norway (excluding petroleum activities and ocean transport) produced 79.8% of GDP: NOK 4,397,716m of NOK 5,511,334m (our calculation from SSB table 09189).  
  Derived shares (petroleum activities and ocean transport = 20.2% in 2025, 34.9% in 2022). Official norskpetroleum figure for the petroleum sector alone is 19.6% (2025) / 34.1% (2022).
- `merchant_fleet_1956` (source_located): In 1956 the US Naval Institute described Norway's merchant fleet as the third largest in the world, behind the United States and the British Commonwealth.  
  Secondary (1956 article). Attribute as 'by the mid-1950s'.
- `nbim_1998` (source_located): Norges Bank Investment Management was established on 1 January 1998, when the fund began investing in equities; it was renamed the Government Pension Fund Global in 2006.  
  
- `no_norway_investment` (source_located): The fund cannot invest in securities issued by Norwegian entities, in Norwegian kroner, or in real estate and infrastructure located in Norway.  
  
- `oecd_productivity` (source_located): The OECD (2024) says Norway's productivity growth is among the lowest in the OECD, and its living-standards lead over the richer half of OECD countries has shrunk from around 42% to 27% over 15 years.  
  
- `oil_crash_2014` (source_located): After mid-2014 the oil price fell below USD 40 a barrel, around a third of its summer-2014 level; the krone was 30% weaker at the end of 2015 than two years earlier (Norges Bank).  
  
- `petroleum_exports_share` (source_located): In 2025 crude oil, natural gas and condensate exports were worth about NOK 1,000 billion, 57% of the value of Norway's goods exports.  
  
- `petroleum_tax` (source_located): Oil and gas companies pay the ordinary 22% company tax plus a 71.8% special tax, for a combined marginal rate of 78%.  
  
- `production_forecast` (source_located): The Norwegian Offshore Directorate forecasts petroleum production of 239.3 million Sm3 o.e. in 2025 and 205.2 million in 2030.  
  
- `resources_produced` (source_located): Of Norway's total expected recoverable petroleum resources (about 15.72 billion Sm3 o.e.), 57% had been produced by the end of 2025.  
  
- `returns_since_1998` (source_located): Between 1998 and 2025 the fund's average annual return was 6.6%; the annual net real return, after inflation and management costs, was 4.3%.  
  
- `sdfi_1985` (source_located): From 1 January 1985 the state's interests were split between Statoil and the State's Direct Financial Interest (SDFI), managed by Petoro since 2001.  
  
- `shelf_1965` (source_located): In March 1965 Norway agreed median-line shelf boundaries with the UK and Denmark, and on 13 April 1965 announced its first licensing round with 22 production licences.  
  
- `statoil_1972` (source_located): On 14 June 1972 the Storting decided to establish the state oil company Statoil and the Norwegian Petroleum Directorate, both in Stavanger.  
  
- `stress_test` (source_located): NBIM's stress test (data at 31 Dec 2025): the 'Fragmented world' scenario gives a 37% drawdown of the fund; a replay of the global financial crisis gives -29.8%.  
  
- `ten_commandments` (source_located): On 14 June 1971 the Storting adopted the 'ten oil commandments', principles for national control of petroleum activities.  
  
- `top_holdings` (source_located): The fund's largest holdings at 30 June 2026: NVIDIA (NOK 612bn), Apple (NOK 522bn), Alphabet (NOK 499bn).  
  
- `trust_2025` (source_located): In the OECD Trust Survey, 57% of Norwegians had high or moderately high trust in the national government in 2025, against an OECD average of 40%.  
  From search snippet of the OECD country note (403). Confirm figures and year.
- `unemployment_2014_16` (source_located): Norway's LFS unemployment rate rose from 3.6% in 2014 to 4.7% in 2016 (SSB).  
  
- `union_density` (source_located): Union density in Norway was 52% in 2024 (Fafo), and collective agreements covered 71% of employees in 2019.  
  
- `us_share` (source_located): The United States was the fund's largest country exposure, 52.9% of the fund at the end of 2025.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

