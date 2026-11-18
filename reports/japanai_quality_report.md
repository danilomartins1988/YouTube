# Quality report - will-ai-make-japan-rich-again / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/will-ai-make-japan-rich-again/documentary/will-ai-make-japan-rich-again--documentary.mp4 (207.7 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 11-13:20 min (channel standard 660-800 s) | PASS | 702.03 s (11:42) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 341 cues; median cue-start offset 0.03 s, p90 0.36 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.2 LUFS integrated, true peak -4.1 dBFS
- Scenes: 36; types: channel_intro x1, end_card x1, engine_cartoon x30, engine_draw x4
- Average scene length: 19.5 s; act cards are music-only.

## Pipeline QC report

# QC report: will-ai-make-japan-rich-again / documentary (long_16x9)

- Runtime: **702.03 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 207.7 MB
- Loudness: -16.2 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **18**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment c3_world pace 114 wpm (numerals count as one word)
- [WARNING] (captions) Caption reading speed >25 chars/s: 'That's a plan,'
- [WARNING] (captions) Caption shorter than 0.25 s: 'First,'
- [WARNING] (presenter) Presenter scene p17_draw lasts 31.7s (target 10-25 s)
- [WARNING] (presenter) Presenter scene p23_draw lasts 30.8s (target 10-25 s)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'eleven' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'seven' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (licensing) Dataset stat_pop24 has no licence recorded
- [WARNING] (licensing) Dataset mhlw_jobs has no licence recorded
- [WARNING] (licensing) Dataset fed_g5a has no licence recorded
- [WARNING] (licensing) Dataset cao_gdp has no licence recorded
- [WARNING] (distinctiveness) Scene sequence 88% similar to 'why-ai-could-make-your-electricity-bill-explode/documentary'
- [WARNING] (distinctiveness) Scene sequence 81% similar to 'how-black-friday-actually-makes-money/documentary'
- [WARNING] (distinctiveness) Scene sequence 81% similar to 'who-gets-rich-when-robots-do-the-work/documentary'

## Publish blockers - claims needing human verification

- `astra_year` (source_located): Seven-Eleven Japan and Telexistence target in-store deployment of the 'Astra' humanoid in 2029 (a plan).  
  
- `care_need` (source_located): MHLW (Jul 2024): about 2.72 million care workers needed by FY2040, about 570,000 more than in FY2022 (prefecture estimates).  
  
- `care_study` (source_located): Lee, Iizuka & Eggleston: robot adoption in Japanese nursing homes accompanied by more employment and retention and more 'human touch' care.  
  
- `density_x` (source_located): IFR WR 2025: robot density 2024 Korea 1,220 vs Japan 446 per 10,000 manufacturing employees; OUR CALCULATION 2.7x; Japan 4th... listed after Singapore 818, China 567, Germany 449.  
  
- `fv_japan` (source_located): Fernández-Villaverde, Ventura & Yao: 1998-2019 GDP per working-age adult +31.9% in Japan vs +29.5% in the US.  
  
- `gdp25` (source_located): Cabinet Office: real GDP +1.2% in 2025, +0.1% in 2024.  
  
- `ifr_prod` (source_located): IFR (Jul 2025): Japan is 'the world's predominant robot manufacturing country representing 38% of global robot production'.  
  
- `jobs_ratio` (source_located): MHLW: active job openings-to-applicants ratio 1.19 (Sept 2026, seasonally adjusted); 1.22 average in 2025.  
  
- `jp_debt` (source_located): IMF F&D (Sept 2026): gross public debt about 207% of GDP, highest among advanced economies; net debt 89-186% depending on the assets counted.  
  
- `jpc_rank` (source_located): Japan Productivity Center (Dec 2025, OECD data): Japan's 2024 output per hour worked $60.1 PPP, 28th of 38 OECD countries.  
  
- `kawasaki69` (source_located): Kawasaki: 1968 license with Unimation (US); 1969 started production of the first industrial robot in Japan.  
  
- `truck_gap` (source_located): MLIT White Paper 2024: without measures, a 34% shortfall in trucking capacity in FY2030 (14% in FY2024); driver overtime cap from April 2024.  
  
- `tx_drinks` (source_located): Telexistence (company claim): one robot restocks about 1,000 beverages a day; remote operator takes over on failures.  
  
- `wa_2070` (source_located): IPSS 2023 medium-fertility projection: working-age population 45.35m in 2070 = 52% of the 1995 peak of 87.26m (OUR CALCULATION). A PROJECTION.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

