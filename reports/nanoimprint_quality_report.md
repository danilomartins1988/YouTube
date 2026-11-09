# Quality report - the-stamp-that-could-break-asmls-monopoly / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/the-stamp-that-could-break-asmls-monopoly/documentary/the-stamp-that-could-break-asmls-monopoly--documentary.mp4 (222.5 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 11-13:20 min (channel standard 660-800 s) | PASS | 712.40 s (11:52) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 325 cues; median cue-start offset 0.06 s, p90 0.46 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Scenes: 35; types: act_title x5, channel_intro x1, end_card x1, engine_cartoon x21, engine_draw x3, kinetic_text x4
- Average scene length: 20.4 s; act cards are music-only.

## Pipeline QC report

# QC report: the-stamp-that-could-break-asmls-monopoly / documentary (long_16x9)

- Runtime: **712.4 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 222.5 MB
- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **39**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment m1_question pace 186 wpm (numerals count as one word)
- [WARNING] (timing) Segment m2_question pace 191 wpm (numerals count as one word)
- [WARNING] (timing) Segment m5_question pace 97 wpm (numerals count as one word)
- [WARNING] (presenter) Presenter scene p19_speed lasts 30.5s (target 10-25 s)
- [WARNING] (tone) Backdrop 'fab' fills 16/32 cartoon zones: vary the worlds
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'double' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'thousand' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (distinctiveness) Scene sequence 88% similar to 'the-chemicals-that-decide-who-makes-chips/documentary'
- [WARNING] (distinctiveness) Scene sequence 89% similar to 'why-elon-musk-wants-his-own-chip-factory/documentary'
- [WARNING] (distinctiveness) Scene sequence 89% similar to 'indias-chip-plants-dont-make-chips/documentary'
- [WARNING] (distinctiveness) Scene sequence 83% similar to 'the-day-volkswagen-became-the-most-valuable-company/documentary'

## Publish blockers - claims needing human verification

- `china_wafer` (source_located): MIT Technology Review: Jeff Koch, a former ASML employee and SemiAnalysis analyst: China 'would be very happy to have a tool that does one wafer per hour and it costs them a fortune to run'; they would build a fab with a thousand of those.  
  An expert's opinion, attributed.
- `cn_euv` (source_located): Reuters (17 Dec 2025): a prototype EUV machine in a high-security Shenzhen lab, completed in early 2025 and under testing, fills nearly an entire factory floor, built by former ASML engineers who reverse-engineered ASML's machines (two people with knowledge of the project); parts from older ASML machines came from secondary markets; goal of working chips by 2028. Engadget/Reuters: it generates EUV light but is not yet making chips; experts see 2030 as more likely. ASML told Reuters its first EUV prototype was built in 2001 and it took nearly two decades before chips in 2019.  
  Anonymous sources via Reuters; the film says 'according to Reuters'. Goals labelled.
- `cn_light` (source_located): Tom's Hardware (Aug 2026): one Chinese light-source team (Harbin Institute of Technology) has reached around 100 W of EUV output against the roughly 600 W that ASML's production sources deliver; the prototype generates EUV photons but has not yet exposed a wafer. China's domestic lithography output is about five machines in 2026, against roughly 130 immersion systems ASML deploys in a typical year; many critical components are still imported from Japan; the Chinese tool reaches finer nodes through multipatterning, the route SMIC already runs on its ASML fleet. MIT Technology Review: China will lean hard on DUV with multi-patterning.  
  Read on 2026-11-08.
- `euv_history` (source_located): MIT Technology Review: around 2001 ASML, then a smaller player, bet on EUV; Nikon and Canon were working on it as well but dropped out; it took 16 years and about $10 billion in research; first EUV machines went on the market in 2017 at well over $100 million each; EUV light is made by shooting lasers at molten tin drops tens of thousands of times a second; in 2025 ASML sold nearly 50 EUV machines and had nearly $40 billion in revenue.  
  Read on 2026-11-08. Revenue as given by MIT Technology Review in dollars.
- `euv_price` (source_located): Reuters (17 Dec 2025): ASML's EUV machines cost around $250 million; ASML is the only company that has mastered EUV; no EUV system has ever been sold to a customer in China (ASML to Reuters).  
  Read in the Reuters text reprinted by Taiwan News.
- `high_na` (source_located): MIT Technology Review (Jun 2026): ASML's new high-NA EUV machines (8 nm resolution) are shipping to fabs at $400 million each.  
  Read on 2026-11-08.
- `lace` (source_located): MIT Technology Review: Lace Lithography (Norway) uses a beam of helium atoms instead of light, with a precision of 0.1 nm against EUV's 13.5 nm wavelength; it aims to have machines ready to sell by 2029 or 2030.  
  Company goal, labelled.
- `nil_energy` (source_located): IEEE Spectrum: Canon estimates NIL consumes one-tenth the energy of an EUV system with a 250-watt light source; EUV systems are as big as double-decker buses, about 200 cubic meters; a cluster of four NIL systems takes less than half that volume (plus a 50 m3 mask-replication tool).  
  Canon's estimate, attributed as such.
- `nil_how` (source_located): IEEE Spectrum (Jan 2025): NIL writes the pattern on a quartz master mask with an electron beam, makes replica masks, presses a replica onto a wafer coated with liquid resist like a stamp, and hardens the resist with UV light from a mercury lamp, the kind used in the 1970s; it patterns features as small as 14 nm. The Register: Canon says 14 nm line width is equivalent to the 5 nm process; it does not require a light source like EUV. Canon began NIL work in 2004, bought Molecular Imprints (Austin, Texas) in 2014; it took 20 years to reach the market.  
  Read on 2026-11-08. The 5 nm equivalence is Canon's claim, attributed.
- `nil_price` (source_located): Bloomberg via The Japan Times (6 Nov 2023): Canon CEO Fujio Mitarai: 'The price will have one digit less than ASML's EUVs'; a final pricing decision hasn't been made. Tom's Hardware: Mitarai: 'I do not expect nanoimprint technology to overtake EUVs, but I'm confident this will create new opportunities'.  
  Price not final (said in the film). We do not state a dollar figure for the Canon tool.
- `nil_problems` (source_located): Tom's Hardware: NIL tends to pick up defects because the mold touches the wafer; any particle can introduce flaws. IEEE Spectrum: Canon had to stop air bubbles and control overlay between layers. The Register: Gartner's Gaurav Gupta saw 'a big gap between research and development at leading-edge nodes versus high-volume execution'.  
  Read on 2026-11-08.
- `nil_sales` (source_located): The Register (Oct 2024): Canon's Kazunori Iwamoto expects to sell around 10 to 20 nanoimprint lithography units annually within five years.  
  Company target, labelled as such.
- `nil_ship` (source_located): IEEE Spectrum / The Register: in September 2024 Canon shipped its first commercial NIL system (FPA-1200NZ2C) to the Texas Institute for Electronics for R&D and prototypes; Kioxia has tested NIL for years and is evaluating it for prototype memory chips.  
  Read on 2026-11-08.
- `nil_speed` (source_located): IEEE Spectrum: each replica mask can make up to 80 lots of 25 wafers, i.e. one circuit layer for 2,000 wafers; Canon's comparison uses an NIL system at 80 wafers per hour and targets 100 wph. MIT Technology Review: ASML's EUV machines crank out about 200 wafers an hour.  
  The two throughput numbers come from different sources and are not a like-for-like benchmark; the film says 'about'.
- `substrate` (source_located): MIT Technology Review: Substrate, a San Francisco startup founded four years ago, works on lithography with x-ray light from a compact particle accelerator; goal: chips at scale by 2030 in its own fab; it predicts finished wafers at $10,000, a tenth of where its CEO says the industry is heading (toward $100,000). Marc Hijink thinks mastering both a new lithography and fab techniques is probably 'unachievable and impossible'.  
  Company goals and predictions, labelled as such.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

