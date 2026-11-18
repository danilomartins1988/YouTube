# Quality report - why-canada-could-win-the-ai-boom / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/why-canada-could-win-the-ai-boom/documentary/why-canada-could-win-the-ai-boom--documentary.mp4 (251.0 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 11-13:20 min (channel standard 660-800 s) | PASS | 730.50 s (12:10) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 385 cues; median cue-start offset 0.04 s, p90 0.41 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.2 LUFS integrated, true peak -4.1 dBFS
- Scenes: 45; types: channel_intro x1, engine_cartoon x41, engine_draw x3
- Average scene length: 16.2 s; act cards are music-only.

## Pipeline QC report

# QC report: why-canada-could-win-the-ai-boom / documentary (long_16x9)

- Runtime: **730.5 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 251.0 MB
- Loudness: -16.2 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **23**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment c2_rank pace 118 wpm (numerals count as one word)
- [WARNING] (captions) Caption reading speed >25 chars/s: 'and this morning her phone won't stop'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'Headline after headline says the same'
- [WARNING] (presenter) Presenter scene p07_draw lasts 31.7s (target 10-25 s)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twice' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (licensing) Dataset statcan_gdp25 has no licence recorded
- [WARNING] (licensing) Dataset hq_cmp25 has no licence recorded
- [WARNING] (licensing) Dataset fed_g5a has no licence recorded
- [WARNING] (licensing) Dataset hq_cmp25 has no licence recorded
- [WARNING] (licensing) Dataset fed_g5a has no licence recorded
- [WARNING] (licensing) Dataset statcan_trade26 has no licence recorded
- [WARNING] (distinctiveness) Scene sequence 82% similar to 'will-ai-make-japan-rich-again/documentary'
- [WARNING] (distinctiveness) Scene sequence 87% similar to 'countries-that-win-the-ai-economy-without-building-ai/documentary'
- [WARNING] (distinctiveness) Scene sequence 83% similar to 'why-ai-could-make-your-electricity-bill-explode/documentary'
- [WARNING] (distinctiveness) Scene sequence 92% similar to 'who-actually-owns-americas-debt/documentary'
- [WARNING] (distinctiveness) Scene sequence 82% similar to 'who-gets-rich-when-robots-do-the-work/documentary'

## Publish blockers - claims needing human verification

- `bc_compete` (source_located): BC: AI and data-centre projects of 10 MW or more must compete for power; first two-year call targets up to 400 MW for AI and data centres (opened Jan 30, 2026).  
  
- `boc_rebound` (source_located): Bank of Canada (Oct 28, 2026): Q2 2026 GDP growth 3.3% (annualized), about 2% indicated for Q3; growth expected to slow in Q4 under new US tariffs, then pick up in 2027 (FORECAST); unemployment around 6.5%.  
  
- `crit34` (source_located): NRCan: Canada's critical minerals list has 34 minerals (June 2024 update), including nickel, copper, uranium, lithium and graphite.  
  
- `first_strategy` (source_located): CIFAR: the Pan-Canadian AI Strategy, launched 2017, was the first national AI strategy in the world.  
  
- `free_cool` (source_located): QScale (company claim, 2022): cooling at its Lévis site is free up to 80% of the year thanks to Quebec's colder climate.  
  
- `gdp_shrank` (source_located): StatCan: real GDP declined 0.4% in Q2 2025 (after +0.5% in Q1), driven by a drop in goods exports as US tariffs slowed trade.  
  
- `hinton_nobel` (source_located): Nobel Prize in Physics 2024 to John Hopfield and Geoffrey Hinton (University of Toronto) for foundational work enabling machine learning with artificial neural networks.  
  
- `hq_boston` (source_located): Same as Ep 67: Hydro-Québec 2025 comparison (rates of Apr 1, 2025, excl. taxes): a 50 MW industrial customer's bill indexed Montréal 100 vs Boston 445 (22%); Montréal ≈ 5.52 CAD cents/kWh ≈ 3.95 US cents (OUR CALC at 1.3973).  
  
- `hydro_rank` (source_located): CER: in 2023 Canada was the third-largest generator of hydroelectricity in the world.  
  
- `hydro_share` (source_located): CER: about 60% of Canada's electricity is generated from hydro.  
  
- `mine16` (source_located): IEA (2021): major mines that came online 2010-2019 took on average over 16 years from discovery to first production (global sample).  
  
- `uranium2` (source_located): CER: Canada is the world's second-largest uranium producer (about 15% of world output in 2022).  
  
- `us_exports` (source_located): StatCan: share of Canada's merchandise exports going to the US was 75.9% in 2024 and 71.7% in 2025.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

