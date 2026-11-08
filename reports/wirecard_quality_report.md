# Quality report - the-2-billion-that-never-existed / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/the-2-billion-that-never-existed/documentary/the-2-billion-that-never-existed--documentary.mp4 (221.0 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 10-12 min | PASS | 660.13 s (11:00) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 313 cues; median cue-start offset 0.07 s, p90 0.37 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.2 LUFS integrated, true peak -4.0 dBFS
- Scenes: 37; types: act_title x5, channel_intro x1, end_card x1, engine_cartoon x21, engine_draw x4, kinetic_text x5
- Average scene length: 17.8 s; act cards are music-only.

## Pipeline QC report

# QC report: the-2-billion-that-never-existed / documentary (long_16x9)

- Runtime: **660.13 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 221.0 MB
- Loudness: -16.2 LUFS integrated, true peak -4.0 dBFS
- Errors: **0**, warnings: **34**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment m5_question pace 116 wpm (numerals count as one word)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'eight' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'hundred' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'percent' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twice' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'third' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'six' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'billion' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.

## Publish blockers - claims needing human verification

- `asia` (source_located): Quartr: by early 2016 the stock was up roughly 800% since 2005 and about 40% of Wirecard's revenue came from Southeast Asia and the Middle East; in 2017 it posted revenue of over €1 billion for the first time (about US$1.13bn at the 2017 average of 1.1297).  
  Read on 2026-11-07. Revenue conversion is ours at the official 2017 average.
- `dax` (source_located): Reuters (Sept 2018): Commerzbank was expelled from the DAX to make room for Wirecard, effective Sept. 24; Wirecard's market value was double Commerzbank's (€10.6bn); Wirecard had a staff of less than 5,000, one tenth that of Commerzbank.  
  Read on 2026-11-07. Narration says "September twenty eighteen".
- `ey_ban` (source_located): Irish Times / FT (3 April 2023): EY was banned from taking on listed companies as new audit clients in Germany for two years; the firm and five current and former employees were fined up to €500,000 each; Wirecard had received unqualified audits from EY for more than a decade.  
  Read on 2026-11-07. "According to people familiar with the matter" in the source; regulator APAS did not name EY.
- `founded` (source_located): Quartr: Wirecard was founded in 1999, based in the Munich suburb of Aschheim; it processed payments for high-risk online merchants such as adult content and online gambling; in 2005 it merged into InfoGenie Europe AG, listed in Frankfurt.  
  Read on 2026-11-07 (AI fact-check; needs a named human reviewer).
- `ft_2015` (source_located): Quartr: Financial Times journalist Dan McCrum wrote in 2015 an article raising questions about Wirecard's acquisitions and accounting; in January 2019 the FT (McCrum and Stefania Palma) reported suspicions raised by a whistleblower, the former head of legal for Wirecard Asia, in Singapore.  
  Read on 2026-11-07 (secondary account of the FT's reporting).
- `hufeld` (source_located): Irish Times (29 Jan 2021): BaFin president Felix Hufeld departed; finance minister Olaf Scholz called it a mutual decision to allow a fresh start at an organisation that 'overlooked Germany's greatest postwar accounting fraud'; deputy Elisabeth Roegele (securities supervision) also left.  
  Read on 2026-11-07.
- `insolvency` (source_located): Reuters (25 June 2020): Wirecard collapsed, becoming the first DAX company to go out of business, leaving creditors owed nearly US$4 billion.  
  Read on 2026-11-07. Narration gives the date as June twenty-fifth, twenty twenty.
- `kpmg` (source_located): Wirecard release (28 April 2020): KPMG's special investigation found that not all data could be obtained that would have been required to prove the revenues of the third-party acquiring business, because the data were primarily in the control of third parties; the company said incriminating evidence for the allegations of balance sheet forgery had not been identified.  
  The company's own release; the film describes it as such.
- `marsalek` (source_located): Reuters (Mar 2025): former COO Jan Marsalek, an Austrian national, is wanted by German authorities; his whereabouts are unknown but he is believed to be in Russia; three Bulgarians were convicted in London of spying for Russia in a unit run by Marsalek. CPS: between August 2020 and February 2023 the group gathered information about individuals and locations of interest to the Russian state; Orlin Roussev reported to Marsalek and was jailed for 10 years and eight months on 12 May 2025.  
  Marsalek has not been tried; the film says "wanted" and "believed".
- `missing` (source_located): Irish Times (18 June 2020): EY refused to sign Wirecard's annual accounts due to a missing €1.9 billion; shares plunged as much as 71 per cent; a trustee had sought to 'deceive the auditor'. Al Jazeera (22 June 2020): €1.9bn ($2.13bn), about a quarter of its assets; the board said there was a 'prevailing likelihood' that the trust account balances 'do not exist'; BPI and BDO said the documents were false and Wirecard was not a client; the Philippine central bank said the money did not appear to have entered the country; CEO Markus Braun quit on Friday 19 June.  
  €1.9bn × 1.1422 (2020 average) = US$2.17bn; Al Jazeera's own conversion was $2.13bn. The title rounds to $2 billion.
- `peak` (source_located): Reuters (June 2020): Wirecard was worth US$28 billion at its peak; Quartr: its market capitalisation briefly topped €24 billion around its DAX entry (≈ US$28bn at the 2018 average of 1.1810).  
  Reuters gives US$28bn directly; the euro figure converts to the same.
- `short_ban` (source_located): Reuters (18 Feb 2019): BaFin banned the taking or increasing of short positions in Wirecard until April 18, a first for an individual stock; Munich prosecutors said they were investigating a Financial Times journalist in response to a criminal complaint; the FT rejected allegations as 'baseless and false'. Irish Times (2021): the regulator also filed complaints against two FT journalists.  
  Read on 2026-11-07. "Two months" = 18 February to 18 April.
- `trial` (source_located): LTO (Aug 2025): the criminal trial of Markus Braun began on 8 December 2022 at the Munich Regional Court, on charges of commercial gang fraud, false accounting and breach of trust, with up to 15 years in prison if convicted. eNCA/AFP (Feb 2023): Braun said 'I reject all the charges' and blamed Marsalek. Bavarian judiciary (May 2026): further hearing dates were set up to 23 December 2026, with no conclusion about the end of the trial.  
  No verdict was found in the sources read (the latest is from May 2026). The narration states the trial was still going on.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

