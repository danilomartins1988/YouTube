# Quality report - who-gets-rich-when-robots-do-the-work / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/who-gets-rich-when-robots-do-the-work/documentary/who-gets-rich-when-robots-do-the-work--documentary.mp4 (214.5 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 11-13:20 min (channel standard 660-800 s) | PASS | 676.77 s (11:16) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 351 cues; median cue-start offset 0.03 s, p90 0.33 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Scenes: 51; types: channel_intro x1, end_card x1, engine_cartoon x44, engine_draw x5
- Average scene length: 13.3 s; act cards are music-only.

## Pipeline QC report

# QC report: who-gets-rich-when-robots-do-the-work / documentary (long_16x9)

- Runtime: **676.77 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 214.5 MB
- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **37**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment a5_britain pace 117 wpm (numerals count as one word)
- [WARNING] (timing) Segment a8_verdict pace 188 wpm (numerals count as one word)
- [WARNING] (timing) Segment a8_close pace 192 wpm (numerals count as one word)
- [WARNING] (captions) Caption shorter than 0.25 s: 'This spring,'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'the robots arrived.'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'And the money those hours used to'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'In other words,'
- [WARNING] (captions) Caption shorter than 0.25 s: 'First,'
- [WARNING] (captions) Caption shorter than 0.25 s: 'Third,'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'that's a group where the richest tenth'
- [WARNING] (captions) Caption reading speed >25 chars/s: 'Dana's question now has a second part.'
- [WARNING] (sources) Number word 'hundred' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'hundred' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'quarter' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'forty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'third' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'four' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (licensing) Dataset bls_ls has no licence recorded
- [WARNING] (licensing) Dataset bea_gdi has no licence recorded
- [WARNING] (licensing) Dataset bea_gdi has no licence recorded
- [WARNING] (licensing) Dataset bea_gdi has no licence recorded
- [WARNING] (licensing) Dataset bea_gdi has no licence recorded
- [WARNING] (licensing) Dataset bls_ls has no licence recorded
- [WARNING] (licensing) Dataset fed_dfa has no licence recorded
- [WARNING] (licensing) Dataset fed_dfa has no licence recorded
- [WARNING] (licensing) Dataset fed_dfa has no licence recorded
- [WARNING] (licensing) Dataset fed_dfa has no licence recorded
- [WARNING] (licensing) Dataset bls_ls has no licence recorded
- [WARNING] (licensing) Dataset bls_edu has no licence recorded
- [WARNING] (licensing) Dataset fed_dfa has no licence recorded
- [WARNING] (distinctiveness) Scene sequence 86% similar to 'could-ai-end-chinas-manufacturing-dominance/documentary'
- [WARNING] (distinctiveness) Scene sequence 81% similar to 'will-ai-make-japan-rich-again/documentary'
- [WARNING] (distinctiveness) Scene sequence 85% similar to 'how-black-friday-actually-makes-money/documentary'
- [WARNING] (distinctiveness) Scene sequence 86% similar to 'could-ai-bring-europe-back-to-power/documentary'

## Publish blockers - claims needing human verification

- `acemoglu` (source_located): Acemoglu (NBER w32487), a forecast: AI adds no more than 0.66% to total factor productivity over 10 years (possibly under 0.53%); AI predicted to widen the gap between capital and labor income.  
  
- `amzn_fcf` (source_located): Amazon Q3 2026 release: free cash flow for the trailing twelve months was 'an outflow of $42.4 billion'.  
  
- `bryn` (source_located): Brynjolfsson, Li & Raymond (NBER w31161): AI assistance raised issues resolved per hour by 14% on average among 5,179 support agents, 34% for novice and low-skilled workers, minimal for experienced workers.  
  
- `canaries` (source_located): Brynjolfsson, Chandar & Chen (Stanford, rev. Aug 2026): employment of workers aged 22-25 in AI-exposed occupations stands 19% below where it would be had it kept pace with less-exposed peers; no comparable gap for experienced workers; descriptive, not causal.  
  
- `capex` (source_located): Trailing twelve months to Sep 30, 2026 (company filings; verified in our Before You Buy episodes): Amazon $210.7bn (net), Alphabet $159.8bn, Microsoft $135.9bn (cash), Meta $108.0bn (incl. finance leases); about $614bn combined (our sum; definitions differ slightly).  
  
- `dc` (source_located): Federal Reserve DFA, 2026 Q2: of defined-contribution pension entitlements (401(k)-type), the top 10% held 55.5% and the bottom 50% held 4.8%.  
  
- `degree` (source_located): BLS CPS (FRED), 2026 Q3: median usual weekly earnings, full-time workers 25+: bachelor's degree and higher $1,752; high school graduates, no college $993. Ratio 1,752/993 = 1.76, i.e. about 76% more (our calculation).  
  
- `equities` (source_located): Federal Reserve DFA, 2026 Q2: the top 10% of households by wealth held 88.1% of household corporate equities and mutual fund shares (top 1% 50.9%; next 9% 37.2%; next 40% 11.4%; bottom 50% 0.6%).  
  
- `esop` (source_located): NCEO (Jan 2026; plan year 2023): ESOPs cover 15.1 million participants (10.9 million active) in 6,609 plans.  
  
- `gdi` (source_located): BEA (FRED): compensation of employees was 58.4% of gross domestic income in 1970 and 50.9% in 2025; domestic corporate profits after tax were 4.5% in 1970 and 9.3% in 2025.  
  
- `humlum` (source_located): Humlum & Vestergaard (NBER w33777, rev. 2026): in Denmark, precise null effects of AI chatbots on earnings and recorded hours, ruling out effects larger than 2% two years after ChatGPT's launch.  
  
- `labor_share` (source_located): BLS (PRS85006173): the nonfarm business labor share index (2017=100) was 93.7 in 2026 Q3, the lowest value since the series begins in 1947; peak 117.1 in 1960 Q4; about 20% below the peak (our calculation).  
  
- `newwork` (source_located): Autor, Chin, Salomons & Seegmiller (NBER w30389): the majority of current employment is in new job specialties introduced after 1940.  
  
- `nvda` (source_located): NVIDIA Q3 FY2027 (quarter ended Oct 25, 2026): revenue $115.8bn; net income $65.3bn = about 56% of revenue (our calculation); gross margin 74.8%.  
  
- `robots` (source_located): Acemoglu & Restrepo (NBER w23285): 1990-2007, one more robot per thousand workers reduced the employment-to-population ratio by about 0.18-0.34 percentage points and wages by 0.25-0.5 percent.  
  
- `scf` (source_located): Federal Reserve SCF 2025: 56% of families held stock directly or indirectly; 31% in the bottom half by usual income, 97% in the top decile; retirement accounts held by 54.9% of families.  
  
- `shift` (source_located): Our arithmetic: the 7.5-point fall in the compensation share (1970 to 2025) applied to 2025 GDI of about $30.9 trillion equals about $2.3 trillion a year. Illustrative; not a claim of money lost.  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

