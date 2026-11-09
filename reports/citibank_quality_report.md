# Quality report - the-bank-that-accidentally-sent-900-million / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | /home/user/YouTube/output/the-bank-that-accidentally-sent-900-million/documentary/the-bank-that-accidentally-sent-900-million--documentary.mp4 (227.1 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 11-13:20 min (channel standard 660-800 s) | PASS | 691.50 s (11:31) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 337 cues; median cue-start offset 0.05 s, p90 0.46 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.2 LUFS integrated, true peak -4.2 dBFS
- Scenes: 39; types: act_title x5, channel_intro x1, end_card x1, engine_cartoon x25, engine_draw x3, kinetic_text x4
- Average scene length: 17.7 s; act cards are music-only.

## Pipeline QC report

# QC report: the-bank-that-accidentally-sent-900-million / documentary (long_16x9)

- Runtime: **691.5 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 227.1 MB
- Loudness: -16.2 LUFS integrated, true peak -4.2 dBFS
- Errors: **0**, warnings: **46**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment m2_transition pace 104 wpm (numerals count as one word)
- [WARNING] (timing) Segment m3_question pace 231 wpm (numerals count as one word)
- [WARNING] (timing) Segment m4_question pace 189 wpm (numerals count as one word)
- [WARNING] (captions) Caption reading speed >25 chars/s: 'It could have bought the same debt'
- [WARNING] (presenter) Presenter scene p06_plumbing lasts 31.7s (target 10-25 s)
- [WARNING] (tone) Scene s01_hook (thriller): a cheering crowd; check it suits the moment
- [WARNING] (tone) Scene s23_why (crisis): a cheering crowd; check it suits the moment
- [WARNING] (sources) Number word 'billion' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'hundred' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'million' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'nine' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'six' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'third' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'hundred' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'million' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'nine' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'nine' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'hundred' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'million' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'third' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'third' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'thirty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'six' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (distinctiveness) Scene sequence 86% similar to 'the-chemicals-that-decide-who-makes-chips/documentary'

## Publish blockers - claims needing human verification

- `checkbox` (source_located): Furman opinion: Citibank's payments ran on Flexcube; the easiest way to pay the interest was to enter a full payoff and send the principal to an internal 'wash account'; the manual said 'ALL of the below field[s] must be set to the wash account: FRONT[;] FUND[; and] PRINCIPAL'; between 5:15 and 5:45 p.m. the maker checked only PRINCIPAL; the 'six-eye' procedure requires three people to review and approve; the checker and the senior approver ('Looks good, please proceed. Principal is going to wash.') also believed it was correct; a 'stop sign' warned 'Account used is Wire Account and Funds will be sent out of the bank. Do you want to continue?' without showing the amount. Several team members were Wipro employees in India working exclusively for Citibank.  
  Read in the opinion; names in text only.
- `distress` (source_located): Furman opinion: in May 2020 Revlon completed a transaction that obtained over $800 million in new financing and moved collateral that had secured the 2016 loan to a new facility; some lenders challenged it, and on August 12, 2020 lenders authorized UMB Bank to sue Revlon and Citibank over it; Revlon was backed by Ronald Perelman's MacAndrews & Forbes, which owned approximately 85% of Revlon. Kelley Drye: Revlon was in severe financial distress, with the loan trading for less than 30 cents on the dollar; Revlon has since filed for chapter 11.  
  Read on 2026-11-09.
- `loan` (source_located): Furman opinion: in 2016, Revlon took out a seven-year, $1.8 billion syndicated loan; Citibank is the Administrative Agent, which receives payments from Revlon and passes them on to the lenders. Kelley Drye: the loan was not due until 2023.  
  Read on 2026-11-09.
- `morning` (source_located): Furman opinion: around 9:00 a.m. on August 12, a team manager reviewing 'cash breaks' found the discrepancy; a Skype message: 'bad news… wires look[] like they went out the door'; at approximately 2:25 p.m. Citibank began sending Recall Notices; further notices followed that evening and the next days. Allstate replied: 'It is not at all clear that the funds were paid in error.'  
  Read on 2026-11-09.
- `occ` (source_located): Banking Dive (Feb 2021): the overpayment 'called into question the bank's system of checks and balances, and potentially contributed to the $400 million fine the Office of the Comptroller of the Currency (OCC) levied against Citi in October.'  
  Link to the fine is Banking Dive's 'potentially'; said as such.
- `ruling_2021` (source_located): Furman opinion (16 Feb 2021, after a December 2020 bench trial): New York law generally requires mistaken payments to be returned, but the 'discharge-for-value' defense lets a creditor keep money it is owed if it had no notice of the mistake (Banque Worms, 1991: such a beneficiary 'should be able to consider the transfer of funds as a final and complete transaction'); 'the Court holds that Citibank is not entitled to its money back. Instead, Defendants' clients are entitled to keep the money.' Banking Dive: Citi said it would appeal.  
  Quotes read in the opinion.
- `ruling_2022` (source_located): Torys / Kelley Drye (Sep-Oct 2022): the Second Circuit reversed and remanded on September 8, 2022; the lenders were not bona fide creditors because the debt was not yet due; they were on inquiry notice given four red flags: no prepayment notice from Revlon; Revlon paying off the loan three years early despite poor finances; it could have bought the debt for under 30 cents on the dollar; and an exchange offer days earlier designed to prevent acceleration of the loan. Torys: the market had already added erroneous-payment provisions drafted by the Loan Syndication and Trading Association.  
  Followed through law-firm summaries as read.
- `split` (source_located): Banking Dive (Feb 2021): some asset managers returned about $385 million, 10 refused; the judge ruled they do not need to return $504 million. Furman opinion: defendants were ten investment advisory firms (including Brigade, HPS and Symphony) whose clients received more than $500 million; Citibank sought $504,169,401.45.  
  Read on 2026-11-09.
- `wired` (source_located): Furman opinion: on August 11, 2020, Citibank, as Administrative Agent for a syndicated term loan to Revlon, intended to wire approximately $7.8 million in interest payments to Revlon's lenders; 'Instead, it made one of the biggest blunders in banking history: It mistakenly wired, in addition to Revlon's $7.8 million, almost $900 million of its own money as well. The resulting payments equaled — to the penny — the amounts of principal and interest that Revlon owed.' Screenshots showed $7.8 million in interest and $894 million in principal.  
  Read in the opinion on 2026-11-09.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

