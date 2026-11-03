# QC report: why-switzerland-is-so-rich / documentary (long_16x9)

- Runtime: **487.23 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 250.7 MB
- Loudness: -16.0 LUFS integrated, true peak -3.4 dBFS
- Errors: **0**, warnings: **10**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment puzzle_caveat pace 187 wpm (numerals count as one word)
- [WARNING] (timing) Segment spec_why pace 185 wpm (numerals count as one word)
- [WARNING] (timing) Segment skills_gii pace 115 wpm (numerals count as one word)
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.

## Publish blockers - claims needing human verification

- `aeoi_2018` (source_located): In 2018 Switzerland exchanged financial account information automatically with partner states for the first time, covering around 2 million financial accounts (FTA release, 5 October 2018), under the global AEOI standard.  
  Title of the FTA release says 'around 2 million financial accounts'. Partner count differs between sources (36 vs 38) - deliberately not used.
- `banking_act_1934` (source_located): The 1934 Federal Act on Banks and Savings Banks (in force 1 March 1935) made breaching banking secrecy a criminal offence (Article 47); before that, banking secrecy was protected by civil law.  
  Secondary sources (academic chapter + law firm). Ideally confirm against the Act's text on fedlex.admin.ch (Article 47) and cite it.
- `constitution_1848` (source_located): The Federal Constitution of 12 September 1848 established the Swiss federal state, turning a group of cantons into a federal state with new federal authorities.  
  parlament.ch reportedly says the present constitution's basis is the Constitution of 12 September 1848, which established the Swiss federal state. Confirm wording.
- `cs_ubs_2023` (source_located): On 19 March 2023 FINMA approved the takeover of Credit Suisse by UBS; the Swiss Confederation and the SNB supported the deal (federal guarantee for additional SNB liquidity assistance, emergency law).  
  Confirm on FINMA release and the Federal Department of Finance timeline.
- `eu_bilateral` (source_located): Switzerland is not a member of the European Union; it pursues its European policy through bilateral sectoral agreements.  
  Confirm on the FDFA 'bilateral path' page.
- `geo_landlocked` (source_located): Switzerland is landlocked (it has no sea coast).  
  Visible in the Natural Earth boundaries used for the map; a reviewer only needs to confirm and sign off. ('Mountainous' was cut from the script because it had no citation.)
- `gii_2025_rank` (source_located): In the Global Innovation Index 2025, WIPO ranked Switzerland first of 139 economies.  
  Confirm 139 economies and rank in WIPO's press release. Secondary sources disagree on the length of the streak (14th vs 15th year), so the script deliberately does not mention it.
- `gii_2025_top5` (source_located): GII 2025 top five: Switzerland, Sweden, United States, Republic of Korea, Singapore.  
  Confirm order in WIPO's ranking table.
- `neutrality_1815` (source_located): Europe's great powers formally recognised Swiss neutrality in 1815 (Congress of Vienna and the Second Treaty of Paris).  
  admin.ch dates the recognition to 1815 via the Congress of Vienna and the Treaty of Paris. Check exact wording on both pages.
- `pharma_hq_basel` (source_located): Roche and Novartis both have their global headquarters in Basel.  
  Sources are news articles; confirm on roche.com and novartis.com (Novartis HQ is only implied by the found sources).
- `pharma_share_2024` (source_located): Chemical and pharmaceutical products accounted for 52.7% of Swiss (goods) exports in 2024 (CHF 149,058 million).  
  Figure taken from a search summary of the FOCBS 2024 annual report. Confirm the 52.7% and which export total it refers to (FOCBS 'Total 1' business-cycle total excludes gold and other precious metals) and word the on-screen label accordingly.
- `price_level_2024` (source_located): In 2024 Switzerland had the highest price level among the countries compared by Eurostat, with a price level index of 158.8 (EU = 100) at GDP level.  
  158.8 comes from press reports of Eurostat data (GDP-level price index). Confirm in Eurostat dataset prc_ppp_ind and which aggregate (GDP vs household consumption) before publishing; adjust the on-screen label.
- `snb_floor_2011` (source_located): On 6 September 2011 the Swiss National Bank set a minimum exchange rate of CHF 1.20 per euro, saying it would no longer tolerate a EUR/CHF rate below it.  
  The ECB statement of 6 Sep 2011 quotes the SNB decision. Locate and cite the SNB's own press release of that date if possible.
- `snb_floor_end_2015` (source_located): On 15 January 2015 the Swiss National Bank discontinued the minimum exchange rate of CHF 1.20 per euro with immediate effect and ceased the associated foreign currency purchases; the franc appreciated sharply and markets were surprised.  
  Decision wording from SNB press-conference text (BIS). 'Appreciated sharply / surprise' is press coverage - keep it qualitative, no magnitude.
- `snb_floor_interventions` (source_located): According to the SNB (April 2015), the minimum exchange rate could only have been enforced through permanent currency interventions of rapidly increasing magnitude.  
  Confirm wording in the SNB speech of 24 April 2015.
- `vet_share` (source_located): About two-thirds of young people in Switzerland enter vocational education and training (VET); the most common form is dual-track VET combining classroom instruction with workplace training.  
  SERI states that two-thirds of young people benefit from VET. Confirm exact phrasing; do not conflate with annual 'Transition Barometer' interest percentages.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.
