# Quality report - could-ai-bring-europe-back-to-power / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/could-ai-bring-europe-back-to-power/documentary/could-ai-bring-europe-back-to-power--documentary.mp4 (223.9 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 11-13:20 min (channel standard 660-800 s) | PASS | 780.40 s (13:00) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 370 cues; median cue-start offset 0.02 s, p90 0.33 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.2 LUFS integrated, true peak -4.1 dBFS
- Scenes: 48; types: channel_intro x1, end_card x1, engine_cartoon x40, engine_draw x6
- Average scene length: 16.3 s; act cards are music-only.

## Pipeline QC report

# QC report: could-ai-bring-europe-back-to-power / documentary (long_16x9)

- Runtime: **780.4 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 223.9 MB
- Loudness: -16.2 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **14**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment a5_siemens pace 112 wpm (numerals count as one word)
- [WARNING] (captions) Caption reading speed >25 chars/s: 'And engineers test the whole line in'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'Nora is cautious.'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'And it doesn't make a single chip.'
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (licensing) Dataset imf_weo has no licence recorded
- [WARNING] (licensing) Dataset ecb_2025_avg has no licence recorded
- [WARNING] (licensing) Dataset ecb_2025_avg has no licence recorded
- [WARNING] (licensing) Dataset ecb_2025_avg has no licence recorded
- [WARNING] (licensing) Dataset epe_ben26 has no licence recorded
- [WARNING] (distinctiveness) Scene sequence 85% similar to 'why-the-world-still-depends-on-chinese-factories/documentary'
- [WARNING] (distinctiveness) Scene sequence 80% similar to 'why-americans-can-no-longer-afford-a-home/documentary'
- [WARNING] (distinctiveness) Scene sequence 85% similar to 'how-costco-makes-billions-selling-almost-nothing/documentary'
- [WARNING] (render) Picture static for >4 s from 695.70s (pacing?)

## Publish blockers - claims needing human verification

- `airbus` (source_located): Airbus 2025: revenues EUR 73.4bn ≈ $82.9bn; 793 commercial aircraft delivered; backlog 8,754 aircraft; self-financed R&D EUR 3.15bn ≈ $3.6bn (our conversion). Registered in Leiden (NL), operations run from Blagnac near Toulouse (FR).  
  
- `asml` (source_located): ASML (Veldhoven, NL), 2025: total net sales EUR 32.7bn ≈ $37.0bn; net income EUR 9.6bn ≈ $10.8bn; R&D EUR 4.7bn ≈ $5.3bn (our conversion); about 5,100 suppliers; the only maker of EUV lithography systems.  
  
- `az_ai` (source_located): AstraZeneca FY2025 results: 'In Q4 2025, Modella AI was acquired by AstraZeneca. The acquisition will embed Modella AI's multi-modal foundation models and AI agents into AstraZeneca's oncology R&D environment.'  
  
- `br_charges` (source_located): PwC / Instituto Acende Brasil: in 2024 taxes (30%) and sector charges (14.8%) were 44.8% of the gross operating revenue of a sample of 44 Brazilian power companies (about two-thirds of the market).  
  
- `br_power` (source_located): EPE Brazilian Energy Balance 2026: renewables were 86.8% of Brazil's electricity matrix in 2025 (88.2% in 2024).  
  
- `br_vat` (source_located): Brazil's Constitutional Amendment 132/2023 creates a dual VAT (CBS and IBS) replacing five consumption taxes, tested from 2026 with the transition running to 2033 (Agencia Senado).  
  
- `draghi_gap` (source_located): Draghi report (Sep 2024): EU-US gap in the level of GDP at 2015 prices widened from slightly more than 15% in 2002 to 30% in 2023; around 70% of the gap in per-capita GDP at PPP is explained by lower productivity in the EU.  
  
- `drug_odds` (source_located): EFPIA Key Data 2026: an average of 12-13 years elapses from first synthesis to market; only one to two of every 10,000 substances synthesised pass all stages.  
  
- `energy` (source_located): Draghi report (Sep 2024): EU companies face electricity prices 2-3 times those in the US and natural gas prices 4-5 times higher.  
  
- `gdp` (source_located): IMF WEO (DataMapper, read 2026-11-18): GDP at current prices, 2025 estimates: United States $30.9T; European Union $21.3T; China $19.6T.  
  
- `ifr_ai` (source_located): IFR World Robotics 2026: machine vision 'already established and industry-grade'; predictive maintenance, process optimization and AI-based inspection 'increasingly used'; general-purpose physical AI 'not yet industry-grade'.  
  
- `ifr_europe` (source_located): IFR: 2025 industrial robot installations in Europe 73,054 (-14%), China 354,226, US 38,428. Robot density 2025 (per 10,000 manufacturing employees): Germany 469, US 323, EU 240, China 193, world 152.  
  
- `novo` (source_located): Novo Nordisk 2025: net sales DKK 309,064m ≈ $46.8bn; R&D DKK 52,039m ≈ $7.9bn (16.8% of sales); HQ Bagsvaerd, Denmark (our conversion).  
  
- `pharma_surplus` (source_located): Eurostat COMEXT via EFPIA Key Data 2026: EU-27 trade balance in medicinal and pharmaceutical products (SITC 54), 2025: EUR 220,463m = about $249bn at 1.13 (our conversion). The US took 43.8% of EU pharma exports.  
  
- `siemens` (source_located): Siemens fiscal 2026 (to Sep 30, 2026): revenue EUR 83.4bn ≈ $96.9bn; Digital Industries software revenue EUR 7.2bn ≈ $8.4bn (+13% comparable); at 1.1616 USD/EUR (ECB daily average over the fiscal year; our conversion).  
  
- `workforce` (source_located): Draghi report (Sep 2024): by 2040 the EU's workforce is projected to shrink by close to 2 million workers each year; ratio of working to retired people expected to fall from around 3:1 to 2:1.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

