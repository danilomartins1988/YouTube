# Quality report - how-dubai-really-makes-money / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/how-dubai-really-makes-money/documentary/how-dubai-really-makes-money--documentary.mp4 (204.0 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 10-12 min | PASS | 708.87 s (11:48) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 295 cues; median cue-start offset 0.06 s, p90 0.36 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | FAIL | 652.7s |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.2 LUFS integrated, true peak -4.1 dBFS
- Scenes: 48; types: act_title x9, end_card x1, engine_cartoon x28, engine_chart x3, engine_draw x4, engine_map x3
- Average scene length: 14.8 s; act cards are music-only.

## Pipeline QC report

# QC report: how-dubai-really-makes-money / documentary (long_16x9)

- Runtime: **708.87 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 204.0 MB
- Loudness: -16.2 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **21**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment open_puzzle pace 100 wpm (numerals count as one word)
- [WARNING] (timing) Segment a1_oil_split pace 103 wpm (numerals count as one word)
- [WARNING] (timing) Segment a2_pearls pace 118 wpm (numerals count as one word)
- [WARNING] (timing) Segment a3_offshore pace 84 wpm (numerals count as one word)
- [WARNING] (timing) Segment a4_jafza pace 104 wpm (numerals count as one word)
- [WARNING] (timing) Segment a4_trade pace 114 wpm (numerals count as one word)
- [WARNING] (timing) Segment a4_dpworld pace 114 wpm (numerals count as one word)
- [WARNING] (timing) Segment a5_launch pace 104 wpm (numerals count as one word)
- [WARNING] (timing) Segment a5_results pace 119 wpm (numerals count as one word)
- [WARNING] (timing) Segment a5_dxb pace 120 wpm (numerals count as one word)
- [WARNING] (timing) Segment a6_visitors pace 77 wpm (numerals count as one word)
- [WARNING] (timing) Segment a6_property pace 108 wpm (numerals count as one word)
- [WARNING] (timing) Segment a6_prices pace 107 wpm (numerals count as one word)
- [WARNING] (timing) Segment a7_difc pace 100 wpm (numerals count as one word)
- [WARNING] (timing) Segment a8_crash pace 116 wpm (numerals count as one word)
- [WARNING] (timing) Segment a8_bailout pace 116 wpm (numerals count as one word)
- [WARNING] (timing) Segment a9_end pace 118 wpm (numerals count as one word)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Segment a9_balance has analysis but no note
- [WARNING] (sources) Segment a9_end has analysis but no note

## Publish blockers - claims needing human verification

- `art23_resources` (source_located): Under Article 23 of the UAE Constitution, the natural resources and wealth in each emirate are the public property of that emirate.  
  
- `bailout_2009` (source_located): On 14 December 2009 Abu Dhabi provided $10 billion to Dubai, part of which repaid a maturing Nakheel Islamic bond.  
  
- `burj_renamed` (source_located): The world's tallest building opened on 4 January 2010 and was renamed from Burj Dubai to Burj Khalifa, after Abu Dhabi's ruler and UAE President Sheikh Khalifa.  
  
- `crash_2009` (source_located): Dubai property prices fell by about half from their mid-2008 peak by mid-2009 (Colliers International, as reported by Gulf News).  
  
- `creek_dredging` (source_located): Dubai Creek was dredged from 1959, financed largely by a loan from Kuwait together with local 'creek bonds'.  
  Loan amount varies across sources (GBP 400k-600k); the script does not state it.
- `ct_rate` (source_located): The UAE corporate tax rate is 9% on taxable income above AED 375,000 (0% below), for financial years starting on or after 1 June 2023.  
  Threshold AED 375,000 = $102,110 at the 3.6725 peg.
- `d33_goal` (source_located): The Dubai Economic Agenda D33 (January 2023) aims to double the size of Dubai's economy over the next decade.  
  
- `difc_2025` (source_located): At the end of 2025 the DIFC had 8,844 active companies and a workforce of 50,200, including more than 290 banks and capital-markets firms.  
  
- `difc_courts` (source_located): The DIFC, created under Dubai law in 2004, has its own English-language common-law courts.  
  
- `dmtt` (source_located): Since financial years starting on or after 1 January 2025, large multinational groups (global revenue of EUR 750 million or more) pay a 15% domestic minimum top-up tax in the UAE.  
  
- `dpworld_owner` (source_located): In 2020 Port and Free Zone World, a wholly-owned subsidiary of the Dubai government's Dubai World, moved to buy out DP World's minority shareholders and delist it.  
  The release announces the offer; confirm completion of the delisting.
- `dpworld_revenue_2025` (source_located): DP World reported revenue of $24.4 billion and gross throughput of 93.4 million TEU across its global portfolio in 2025.  
  
- `dwc_plan` (source_located): In April 2024 Dubai approved a AED 128 billion passenger terminal at Al Maktoum International Airport, with capacity of up to 260 million passengers.  
  USD at the 3.6725 peg: $34.9bn.
- `dxb_intl_rank_2025` (source_located): In ACI World's preliminary 2025 ranking, DXB was the world's busiest airport for international passengers.  
  Preliminary ranking, to be confirmed by ACI in July 2026. Check final status.
- `dxb_pax_2025` (source_located): Dubai International Airport (DXB) handled 95.2 million passengers in 2025.  
  
- `emaar_owner` (source_located): Since May 2026 Dubai Holding, a government-owned group, is Emaar Properties' largest shareholder with 29.73%, after buying the Investment Corporation of Dubai's 22.27% stake.  
  
- `emirates_fy26` (source_located): In the year to 31 March 2026 the Emirates Group reported revenue of AED 150.5 billion and profit after tax of AED 21.0 billion, and paid a AED 3.5 billion dividend to its owner, the Investment Corporation of Dubai.  
  USD at the 3.6725 peg.
- `emirates_launch` (source_located): Emirates was launched in 1985 with about $10 million of start-up capital and two aircraft leased from Pakistan International Airlines.  
  Secondary sources only; aircraft types differ between accounts, so types are not named.
- `free_zones` (source_located): Dubai has more than 20 free zones (Invest in Dubai).  
  Commercial sites say 25-30+; government wording "20+". Confirm the page.
- `gdp_h1_2026` (source_located): Dubai's real GDP was AED 473 billion in H1 2026, 2.3% lower than a year earlier, according to DDSE.  
  
- `hotel_occupancy_2025` (source_located): Average hotel occupancy in Dubai was 80.7% in 2025.  
  
- `hrw_findings` (source_located): HRW reports that the kafala sponsorship system ties migrant workers' visas to their employers, that interviewees paid recruitment fees, and that the UAE relies on a summer midday work ban to manage heat risk, which HRW calls ineffective; it cites 46,819 unpaid-wage cases handled by the labour ministry in 2022.  
  
- `imf_correction_risk` (source_located): The IMF warns the real estate sector may be affected by a slowdown or reversal of capital flows or a shift in investor sentiment that could lead to an unexpected price correction.  
  
- `imf_gre_info` (source_located): The IMF notes that limited information on the financial positions of individual GREs and the absence of aggregate public sector financial statements hinder comprehensive risk assessment.  
  
- `imf_prices` (source_located): IMF (2025 Article IV) - Dubai prices rose 117.6% for villas and 46.2% for apartments between 2020Q1 and 2025Q2; 83.4% of 2024 residential transactions were non-mortgaged.  
  
- `jafza_firms` (source_located): Jebel Ali Free Zone (Jafza), established in 1985, started with 19 companies and now hosts over 11,000 businesses from 157 countries.  
  
- `jafza_port_gdp` (source_located): According to the Dubai Media Office, Jafza and Jebel Ali Port together account for 36% of Dubai's GDP.  
  Government claim (May 2025), likely on the pre-revision GDP series and including indirect effects. Attribute it on screen.
- `jafza_trade_2024` (source_located): Jafza recorded AED 713 billion in non-oil trade in 2024.  
  USD at the 3.6725 peg: $194.1bn.
- `jebel_ali_opened` (source_located): Jebel Ali Port was formally opened on 26 February 1979.  
  
- `jebel_ali_teu_2025` (source_located): Jebel Ali handled about 15.55 million TEU in 2025 and was ranked ninth among world container ports by Lloyd's List.  
  
- `lingah_shift` (source_located): According to Lorimer's Gazetteer, Dubai grew rapidly after 1902, helped by the decline of Lingeh, and became the chief commercial emporium of the Trucial Coast.  
  Phrase found in a QDL extract volume (IOR/R/15/1/729). Confirm in the Gazetteer's Dibai entry. Do not state the exact duty decree date (sources conflict 1894-1904).
- `midday_break` (source_located): The UAE bans outdoor work in direct sun from 12:30 to 15:00 between 15 June and 15 September; 2025 was the 21st consecutive year.  
  
- `migrant_share` (source_located): Human Rights Watch says migrant workers make up 88% of the UAE's population (2023).  
  NGO figure for the whole UAE. Always attribute to HRW.
- `no_pit` (source_located): The UAE does not levy personal income tax on individuals' employment income (PwC, reviewed March 2026).  
  Secondary; find an official UAE statement before publishing.
- `non_oil_share` (source_located): The Government of Dubai states that over 95% of Dubai's GDP is non-oil based.  
  Confirm the exact wording and page on dubai.ae. Do not upgrade to "under 1% oil" without a primary statistical table.
- `oil_discovery` (source_located): Oil was discovered offshore Dubai at the Fateh field in 1966.  
  
- `oil_first_export` (source_located): Dubai's first oil export shipment left in 1969.  
  
- `oil_peak` (source_located): Dubai's oil production peaked in 1991 and has declined since.  
  The 410,000 b/d peak figure was not confirmed, so only the year is used.
- `onshore_ownership` (source_located): Since 1 June 2021, foreign investors can own 100% of most onshore UAE companies, after the amendment of the Commercial Companies Law (Federal Decree-Law No. 26 of 2020).  
  
- `pearl_collapse` (source_located): The Gulf pearling industry declined after Japan developed cultured pearls from 1916 onward, compounded by the 1929 financial crash, from which it never fully recovered.  
  
- `pop_dubai_2025` (source_located): Dubai's population was about 4.58 million at the end of 2025 (DDSE estimate, revised methodology).  
  DDSE changed method in 2026; the older population clock showed ~4.0m. Confirm the WAM article and wording.
- `qfzp` (source_located): A Qualifying Free Zone Person pays 0% corporate tax on qualifying income and 9% on other income, subject to substance and other conditions.  
  
- `re_2025` (source_located): Dubai real estate recorded over 270,000 transactions worth AED 917 billion in 2025, up from AED 761 billion in 2024.  
  AED 917bn covers all transaction types (sales and other deals) per DLD; sales alone were lower. Label as "transactions". USD at the 3.6725 peg.
- `re_series` (source_located): Dubai real-estate transactions, AED billion - 2024 761, 2025 917.  
  USD at the 3.6725 peg.
- `reach_claim` (source_located): Dubai's government says one-third of the world's population lives within four hours' flight of Dubai, and two-thirds within eight hours.  
  Government marketing claim, not an independent calculation. Always attribute ("Dubai says").
- `reserves_split` (source_located): Abu Dhabi holds about 94% of the UAE's oil reserves and Dubai about 4% (US ITA citing the 2019 UAE State of Energy Report).  
  Secondary (US government) citing a 2019 UAE report. Look for a current UAE primary source.
- `sectors_h1_2026` (source_located): Shares of Dubai's real GDP, H1 2026 (DDSE, revised series): wholesale and retail trade 20.5%, financial and insurance 14.0%, real estate 11.8%, transport and storage 10.7%.  
  Read the DDSE table; confirm that shares are of real GDP for H1 2026 on the revised series.
- `standstill_2009` (source_located): On 25 November 2009 Dubai asked creditors of Dubai World and its property units for a standstill on about $26 billion of debt.  
  
- `uae_seven` (source_located): The United Arab Emirates is a federation of seven emirates, of which Dubai is one; Abu Dhabi is the federal capital.  
  
- `vat` (source_located): VAT was introduced across the UAE on 1 January 2018 at a standard rate of 5%.  
  
- `visitors_2025` (source_located): Dubai received 19.59 million international overnight visitors in 2025, up from 18.72 million in 2024 and 16.73 million in 2019.  
  
- `visitors_series` (source_located): International overnight visitors to Dubai (millions) - 2019 16.73, 2024 18.72, 2025 19.59.  
  
- `war_2026` (source_located): Reporting by The National ties the 2026 slowdown to the regional war that began on 28 February 2026, which disrupted travel and trade; Q1 2026 real GDP still grew 2.4%.  
  Cause attribution is from press reporting, not DDSE. Narration attributes it ("amid", not "because of").

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

