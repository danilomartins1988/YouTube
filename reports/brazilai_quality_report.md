# Quality report - could-brazil-become-the-worlds-factory-for-robots / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/could-brazil-become-the-worlds-factory-for-robots/documentary/could-brazil-become-the-worlds-factory-for-robots--documentary.mp4 (249.8 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 11-13:20 min (channel standard 660-800 s) | PASS | 684.20 s (11:24) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 363 cues; median cue-start offset 0.03 s, p90 0.38 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.2 LUFS integrated, true peak -4.2 dBFS
- Scenes: 35; types: channel_intro x1, end_card x1, engine_cartoon x30, engine_draw x3
- Average scene length: 19.5 s; act cards are music-only.

## Pipeline QC report

# QC report: could-brazil-become-the-worlds-factory-for-robots / documentary (long_16x9)

- Runtime: **684.2 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 249.8 MB
- Loudness: -16.2 LUFS integrated, true peak -4.2 dBFS
- Errors: **0**, warnings: **19**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment c2_draw pace 115 wpm (numerals count as one word)
- [WARNING] (presenter) Presenter scene p23_draw lasts 31.0s (target 10-25 s)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (licensing) Dataset epe_ben26 has no licence recorded
- [WARNING] (licensing) Dataset usgs_fe26 has no licence recorded
- [WARNING] (licensing) Dataset usgs_nb26 has no licence recorded
- [WARNING] (licensing) Dataset usgs_ree26 has no licence recorded
- [WARNING] (licensing) Dataset usgs_li26 has no licence recorded
- [WARNING] (licensing) Dataset usda_soy has no licence recorded
- [WARNING] (licensing) Dataset ibge_pop25 has no licence recorded
- [WARNING] (licensing) Dataset ibge_cnt has no licence recorded
- [WARNING] (licensing) Dataset wb_db20 has no licence recorded
- [WARNING] (licensing) Dataset wb_lpi23 has no licence recorded
- [WARNING] (licensing) Dataset bcb_selic has no licence recorded
- [WARNING] (licensing) Dataset fed_g5a has no licence recorded
- [WARNING] (distinctiveness) Scene sequence 92% similar to 'why-the-world-still-depends-on-chinese-factories/documentary'
- [WARNING] (distinctiveness) Scene sequence 84% similar to 'why-americans-can-no-longer-afford-a-home/documentary'
- [WARNING] (distinctiveness) Scene sequence 80% similar to 'could-ai-bring-europe-back-to-power/documentary'
- [WARNING] (distinctiveness) Scene sequence 87% similar to 'how-costco-makes-billions-selling-almost-nothing/documentary'

## Publish blockers - claims needing human verification

- `br_byd` (source_located): Ford idled its Camacari (Bahia) plant in January 2021; BYD took over the site and began producing cars there on July 1, 2025.  
  
- `br_iron` (source_located): USGS MCS 2026: Brazil is the world's second-largest iron ore producer (420 Mt usable ore in 2025e, after Australia's 980 Mt).  
  
- `br_nb` (source_located): USGS MCS 2026: Brazil accounts for approximately 93% of global niobium production (104,000 t of 112,000 t, 2025e).  
  
- `br_pop` (source_located): IBGE: Brazil's estimated population was 213.4 million on July 1, 2025.  
  
- `br_ree` (source_located): USGS MCS 2026: Brazil holds the world's second-largest rare-earth reserves (11 Mt REO vs China 44 Mt), but mined only about 2,000 t in 2025 vs China's 270,000 t.  
  
- `br_renew` (source_located): EPE Brazilian Energy Balance 2026: renewables were 86.8% of Brazil's electricity matrix in 2025 (88.2% in 2024).  
  
- `br_road` (source_located): CNT Transport and Logistics Plan 2026 (industry study): road transport carries 65.8% of Brazil's freight.  
  
- `br_selic` (source_located): Banco Central do Brasil: Selic target rate 13.75% a year (held on Nov 4, 2026).  
  
- `br_vat` (source_located): EC 132/2023 and LC 214/2025: the dual VAT (CBS + IBS) is tested from 2026 and the old consumption taxes (ICMS, ISS) are fully extinguished in 2033.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

