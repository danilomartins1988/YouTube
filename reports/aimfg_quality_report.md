# Quality report - could-ai-end-chinas-manufacturing-dominance / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/could-ai-end-chinas-manufacturing-dominance/documentary/could-ai-end-chinas-manufacturing-dominance--documentary.mp4 (346.3 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 11-13:20 min (channel standard 660-800 s) | PASS | 704.90 s (11:44) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 359 cues; median cue-start offset 0.03 s, p90 0.32 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Scenes: 43; types: channel_intro x1, end_card x1, engine_cartoon x35, engine_draw x6
- Average scene length: 16.4 s; act cards are music-only.

## Pipeline QC report

# QC report: could-ai-end-chinas-manufacturing-dominance / documentary (long_16x9)

- Runtime: **704.9 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 346.3 MB
- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **26**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment a2_wage pace 190 wpm (numerals count as one word)
- [WARNING] (timing) Segment a4_result pace 118 wpm (numerals count as one word)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'forty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twice' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'quarter' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'hundred' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (licensing) Dataset fred_ipman has no licence recorded
- [WARNING] (licensing) Dataset fred_manemp has no licence recorded
- [WARNING] (licensing) Dataset wdi_mva has no licence recorded
- [WARNING] (licensing) Dataset bls_ces has no licence recorded
- [WARNING] (licensing) Dataset fed_g5a has no licence recorded
- [WARNING] (licensing) Dataset census_asm21 has no licence recorded
- [WARNING] (licensing) Dataset census_asm21 has no licence recorded
- [WARNING] (distinctiveness) Scene sequence 84% similar to 'how-black-friday-actually-makes-money/documentary'
- [WARNING] (distinctiveness) Scene sequence 85% similar to 'who-actually-owns-americas-debt/documentary'

## Publish blockers - claims needing human verification

- `ar_jobs` (source_located): Acemoglu & Restrepo (JPE 2020): one more robot per thousand workers reduced the employment-to-population ratio by 0.2 percentage points and wages by 0.42% (US commuting zones, 1990-2007).  
  
- `asm` (source_located): Census 2021 ASM: shipments $6.1T; cost of materials $3.34T (sum of subsectors) -> 55% (our calculation); annual payroll $785.2bn -> about 13% of shipments (our calculation; all employees, wages and salaries before benefits).  
  2021 is the last ASM year; payroll excludes benefits; shares are our calculation.
- `foxconn_twin` (source_located): NVIDIA blog (Jun 2, 2024): Foxconn's digital twin of a new factory in Guadalajara, Mexico; engineers define processes and train robots in the virtual environment.  
  Company statement about a plan and its tools; not evidence of a lights-out factory.
- `ieare` (source_located): IEA GCMO 2026: China's share of magnet rare earth refining 85% in 2025 (90% in 2024).  
  
- `ifr_ai` (source_located): IFR WR 2026 executive summary: machine vision for detection and robot guidance 'already established and industry-grade'; predictive maintenance, process optimization and AI-based inspection 'increasingly used'; general-purpose physical AI 'not yet industry-grade'; 'Most humanoids remain prototypes or pilot-stage technologies'; 'industrial robots are economically superior for industrial production tasks'.  
  
- `ifr_cn_plan` (source_located): IFR China release (Sep 24, 2026): labor shortage due to demographic change makes robotic automation a preferred solution; China's 15th Five-Year Plan (2026-2030) robotics strategy emphasises self-reliance and 'aims to focus its AI research on physical applications'.  
  
- `ifr_countries` (source_located): IFR press release Sep 24, 2026: 2025 installations Japan 36,219 (-19%); Republic of Korea 30,000 (-1%); Germany fewer than 25,000; the US 'now the second-largest market'. Operational stock 5,079,078 (2025).  
  
- `ifr_density` (source_located): IFR (Nov 12, 2026), robots per 10,000 manufacturing employees, 2025: Korea 1,066; Singapore 873; Germany 469; Japan 452; US 323 (8th); China 193 (19th; National Economic Census employment base; +147% 2020-2025); world 152.  
  China's density uses a new employment base (IFR); not compared with older editions.
- `ifr_dom` (source_located): IFR (Sep 24, 2026): Chinese domestic suppliers' installations +15% in 2025, 55% of China's installations; share around 30% in 2019-2021 (WR 2026 executive summary); more than half since 2024.  
  
- `ifr_inst` (source_located): IFR World Robotics 2026: 603,307 industrial robots installed worldwide in 2025 (+11%, record); China 354,226 (+20%), 59% of the world; US 38,428 (+12%). China/US = 9.2 (our calculation).  
  
- `ifr_jp` (source_located): IFR (Jul 15, 2025): 'Japan is the world's predominant robot manufacturing country representing 38% of global robot production'.  
  
- `mva` (source_located): World Bank WDI (updated 2026-11-11): China manufacturing value added $4,822.7bn in 2025, World $17,601.1bn -> 27.4% (our calculation). Current US$.  
  
- `us_output` (source_located): Fed G.17 IPMAN: June 1979 47.61 -> Oct 2026 99.72 (x2.09, our calculation); BLS MANEMP: June 1979 19.553M -> Oct 2026 12.681M (-35%, our calculation).  
  
- `wages` (source_located): BLS CES3000000008: US manufacturing production workers ≈ $29.05/hour (2025 average, our calculation). NBS (May 2026): 2025 average annual wage of production and related personnel in enterprises above designated size 80,739 yuan ≈ $11,200 at 7.1875 yuan/USD (Fed G.5A; our conversion). Ratio per hour is a rough comparison (different definitions, hours unknown): roughly a fifth (our calculation).  
  Different definitions; comparison labelled rough, our calculation.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

