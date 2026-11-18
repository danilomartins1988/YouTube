# Editorial QC: Could Cheap Electricity Become the New Oil? (Ep 67)

Build: `OPENBLAS_NUM_THREADS=1 python -m hiddeneco build could-cheap-electricity-become-the-new-oil -d documentary --tts openai --allow-paid`
(2026-11-18). Runtime **736.2 s (12:16)**, 1920x1080 H.264/AAC, -16.2 LUFS, true peak -4.1 dBFS. **QC: 0 errors**, 30 warnings, 14 claims
awaiting human sign-off. Visual QC: no black gaps, no frozen picture over 5 s (freezedetect), licensed assets only. Narration US$0.27
(ledger; gpt-4o-mini-tts, voice ash, 9,035 characters, one take).

| Check | Result |
|---|---|
| Hook first, then channel intro | PASS (co_hook 0:00-0:35, intro, title card 0:40) |
| One protagonist, one journey | PASS (Nia + Cubby, office → map → six pins → report) |
| Spoken numbers 10-15, ≤1 per scene | PASS: 11 (FACT_CHECK.md); counter tool reports 6 (it misses comparisons) |
| One big number on screen at a time, labelled pill | PASS (pmtag callouts: FACT / FORECAST / PLAN / PROPOSED / OUR CALC / FINDING) |
| ≥3 presenter explanatory animations | PASS (p07, p24, p30) |
| Runtime 660-800 s | PASS (736.2 s) |
| USD only, dated rate | PASS (Fed G.5A 2025, 1.3973 CAD/USD) |
| Forecasts/plans/proposals labelled | PASS (IEA FORECAST, UAE PLAN, Quebec Rate CD PROPOSED) |
| Overlaps | PASS: Ep 65 and Ep 04 linked by title only; Ep 63 Brazil beat not repeated |
| Counterpoints | PASS: grids and waits, cooling, solar at night, latency, politics, taxes and charges, dry years, Ireland |
| Neutral, no stereotypes, no flags/logos, no real person drawn | PASS (companies only on plain plaques when named) |
| Title without "—", ≤4-word thumbnails naming power | PASS ("POWER: THE NEW OIL?", "CHEAP POWER NEW OIL?", "AI FOLLOWS CHEAP POWER") |

QC warnings (reviewed, accepted): 2 caption reading-speed lines; 16 number-word notes ("one" in "one rule", "one ingot", "six pins",
etc., not statistics; "quarter", "double", "half", "twenty" are sourced in FACT_CHECK.md); 7 dataset licence notes (public statistics,
cited); 5 scene-sequence similarity notes vs other cartoon episodes (shared pipeline structure; sets are new).
Known limits: iea.org/openai.com blocked automated reads (figures confirmed in named coverage); ERCOT queue figure from press coverage
(on screen only, labelled "requests, not forecasts"); Norway's crypto-mining ban: announced plan, final status unverified; Quebec Rate CD
not yet decided by the Régie.
Shorts: `output/shorts/67-power-new-oil_short.mp4` (37.7 s), `-b_short.mp4` (46.4 s), `-c_short.mp4` (39.4 s), cut from the light copy.
