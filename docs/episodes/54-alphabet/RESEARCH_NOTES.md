# Ep 54: How Google Actually Makes Money (research notes)

Checked 2026-11-13. All figures are US dollars; "$M" = millions as reported.
- **Fetched**: I read the primary page myself (SEC EDGAR document downloaded and read as full text, court opinion PDF read as text, official IR transcript).
- **Computed**: our own arithmetic on Fetched figures. Said as "by our calculation / by our count" on air and labelled on screen.
- Reused from `docs/series/research/alphabet_2026-11.md` (Before You Buy, Fetched 2026-11-11): Q1 and Q2 2026 release figures for the trailing-four-quarter sums. Everything else re-read today.

This is a business-model episode, not a valuation: no share price, market cap, multiples or buy/sell language.

## Primary sources
- [10-K] Alphabet Form 10-K FY2025, filed 2026-02-05: https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm
- [Q4REL] Q4/FY2025 release, 8-K Ex. 99.1, 2026-02-04: https://www.sec.gov/Archives/edgar/data/1652044/000165204426000012/googexhibit991q42025.htm
- [Q1REL] Q1 2026 release: https://www.sec.gov/Archives/edgar/data/1652044/000165204426000043/googexhibit991q12026.htm (via the BYB notes)
- [Q2REL] Q2 2026 release: https://www.sec.gov/Archives/edgar/data/1652044/000165204426000066/googexhibit991q22026.htm (via the BYB notes)
- [Q3REL] Q3 2026 release, 2026-10-28: https://www.sec.gov/Archives/edgar/data/1652044/000165204426000080/googexhibit991q32026.htm
- [10-Q] Form 10-Q, quarter ended 2026-09-30, filed 2026-10-29: https://www.sec.gov/Archives/edgar/data/1652044/000165204426000084/goog-20260930.htm
- [CALL] Q3 2026 earnings call transcript (Alphabet IR): https://s206.q4cdn.com/479360582/files/doc_events/2026/Oct/28/2026_Q3_Earnings_Transcript.pdf
- [MEHTA] US v. Google LLC, D.D.C. No. 20-cv-3010, Memorandum Opinion, Doc. 1033, 2024-08-05: https://storage.courtlistener.com/recap/gov.uscourts.dcd.223205/gov.uscourts.dcd.223205.1033.0.pdf
- [REMEDY] Same case, remedies Memorandum Opinion, Doc. 1436, 2025-09-02: https://storage.courtlistener.com/recap/gov.uscourts.dcd.223205/gov.uscourts.dcd.223205.1436.0.pdf
- abc.xyz/investor returned HTTP 403 to automated fetches; the transcript PDF on Alphabet's IR CDN was used instead.

## 1. Revenue map, FY2025 [10-K Note 2, Fetched]
| $M | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Google Search & other | 175,033 | 198,084 | 224,532 |
| YouTube ads | 31,510 | 36,147 | 40,367 |
| Google Network | 31,312 | 30,359 | 29,792 |
| Subscriptions, platforms & devices | 34,688 | 40,340 | 48,030 |
| Google Services | 272,543 | 304,930 | 342,721 |
| Google Cloud | 33,088 | 43,229 | 58,705 |
| Other Bets | 1,527 | 1,648 | 1,537 |
| Total | 307,394 | 350,018 | 402,836 |
- "We generated more than 70% of total revenues from online advertising in 2025." [10-K]
- Search & other = 55.7% of FY2025 revenue; ≈ $1.10bn of revenue per day (402,836 / 365) [Computed].
- Segment operating income FY2023/24/25: Services 95,858 / 121,263 / 139,404; Cloud 1,716 / 6,112 / 13,910; Other Bets (4,095) / (4,444) / (7,515); Alphabet-level (9,186) / (10,541) / (16,760). Cloud margins 5.2% / 14.1% / 23.7% [Computed].
- Network: "decreased $567 million from 2024 to 2025, primarily due to a decrease in AdSense revenues" [10-K]. Q3 2026 Network was $7,455M vs $7,354M (+1%) [Q3REL], so the script says only that it shrank last year.
- Other Bets: "generated primarily from the sale of autonomous transportation services and internet services" [10-K].

## 2. The auction [MEHTA, Fetched]
- FOF 240: "Google's text ads auction is a classic second-price auction, with modifications. A second-price auction is one where ... the winner, instead of paying the price of their highest bid, pays one cent above the first runner-up."
- FOF 241-242: "An auction winner is not determined solely based its bid ... LTV = bid x pCTR – β"; pCTR "is a score between 0 and 1".
- FOF 243-252: "pricing knobs" (squashing, format pricing, rGSP); "Google strategically has used pricing knobs to raise text ads prices"; "Similar studies showed that Google could raise prices using squashing without losing advertisers."
- Monetization metrics [10-K]: FY2025 paid clicks +6%, cost-per-click +7%; Network impressions −7%. [10-Q]: Q3 2026 y/y paid clicks +8%, CPC +4%; Network impressions −14%.
- The on-screen bids ($2.00 / $1.50 / $1.20) and click chances (0.05 / 0.20 / 0.10) are ILLUSTRATIVE and labelled so.

## 3. Tolls: TAC and Apple
- [10-K]: TAC $59,926M (2025) vs $54,900M (2024); "The TAC rate decreased from 20.7% to 20.3%"; distribution partners = "browser providers, mobile carriers, original equipment manufacturers, and software developers"; on Network, "most of the advertiser revenues ... are paid as TAC to our Google Network partners". [10-Q]: Q3 2026 TAC $16,366M, rate 20.0%.
- [MEHTA] FOF 289: "In 2021, Google paid out a total of $26.3 billion in revenue share under these contracts" (Apple, Mozilla, Samsung/Motorola/Sony, AT&T/Verizon/T-Mobile), "listed in its financial statements as 'traffic acquisition costs'".
- [MEHTA] FOF 298-299: Google pays Apple a percentage of ad revenue on Safari and Chrome; "In 2022, Google's revenue share payment to Apple was an estimated $20 billion (worldwide queries)"; "more than all of its other revenue share payments combined".
- [MEHTA] conclusion: "Google is a monopolist, and it has acted as one to maintain its monopoly."
- [REMEDY]: "Google will be barred from entering or maintaining any exclusive contract ..."; "Google will not be barred from making payments or offering other consideration to distribution partners"; "Cutting off payments from Google almost certainly will impose substantial—in some cases, crippling—downstream harms to distribution partners"; no Chrome divestiture.
- [10-K]: final judgment Dec 2025 "requires us to share certain search data with and offer syndication services to certain competitors"; Google appealed Jan 2026; DOJ and states appealed Feb 2026.

## 4. YouTube, subscriptions, devices
- YouTube ads $40,367M (2025) [10-K]; "YouTube revenue across ads and subscriptions exceeded $60 billion for the full year 2025" [Q4REL, company claim].
- "In Q3, Living Room accounted for over one-third of total YouTube ads revenues." [CALL, Schindler]
- Other cost of revenues rose "primarily due to increases in content acquisition costs, largely for YouTube, depreciation expense, and other technical infrastructure operations costs" [10-K].
- Subscriptions, platforms & devices $48,030M [10-K]; includes "YouTube TV, YouTube Music and Premium, and NFL Sunday Ticket, as well as Google One; the sale of apps and in-app purchases; and consumer devices" [10-Q]. "over 325 million paid subscriptions across consumer services" [Q4REL, Pichai]. "150 million YouTube Music and Premium subscribers ... including trials" [Q3REL] (not used on air after trimming).

## 5. Cloud and Other Bets
- Q3 2026: Cloud revenue $30,709M (+103%), operating income $11,121M (36.2% [Computed]); "TPU systems sales were also a meaningful contributor" [Q3REL]. Services $96,302M / $39,157M (40.7% [Computed]). Other Bets $372M / $(2,047)M.
- Trailing four quarters Q4 2025-Q3 2026 [Computed from releases]: Search 250,093; Cloud 93,169; Subs 53,163; YouTube 43,528; Network 29,557.
- Pichai: "now on a half-trillion dollar revenue run rate" [Q3REL]; Q3 × 4 ≈ $510bn [Computed].
- Waymo: "more than 300 million fully autonomous miles", "15 major U.S. cities" [CALL, Pichai; company claims].

## 6. Where the cash goes
- 2025 [10-K cash flow statement]: operating cash 164,713; purchases of property and equipment (91,447); repurchases (45,709); dividends (10,049). FCF ≈ 73,266 [Computed]; buybacks + dividends ≈ 76% of FCF [Computed].
- Jan-Sep 2026 [10-Q]: operating cash 127,149; capex (131,953); "there were no repurchases"; dividends (8,167); common stock issued 42,870; mandatory convertible preferred net $19.0bn; debt issued 85,222.
- Capex guide: "our full-year 2026 CapEx guidance range of $195-$205 billion remain unchanged"; "We continue to expect our CapEx to increase significantly in 2027" [CALL, CFO]. 2026 guide ÷ 2025 capex = 2.1-2.2× [Computed].

## 7. Threats
- AI Mode: "the strong growth in AI Mode queries had an impact because of the lower monetization we were seeing in AI Mode"; "we're now scaling ads within both AI Overviews and AI Mode" [CALL, Schindler].
- "our year-over-year query growth rate is the highest it's been in the last five years" [Q3REL, Pichai]; Search & other Q3 $63,350M, +12%.
- Ad tech [10-K]: April 2025 mixed decision; publisher tools "unfairly excluded rivals". [10-Q]: September 2026 remedies decision denied "structural divestitures ... instead ordering certain behavioral remedies"; Google plans to appeal the adverse portion. EU DMA fines €430M + €460M, $1.0bn Q3 charge (not used on air after trimming).

## Not used
Market cap, P/E, share price, backlog (definition changed in Q1 2026), equity-security gains, contingent commitments: all valuation topics for the Before You Buy edition. The identity of the "private company" stake is not named.
