# Ep. 45 — "How Prediction Markets Make Money Off Your Hunches": Research Notes

Fact-check compiled 2026-11-10. Amounts in US dollars. One bullet per claim: quote or figure, then URL, then the date published.
Unless a bullet says otherwise, each claim was read on the primary page or document itself, not taken from a search snippet.
Labels: **[PENDING]** marks litigation that is not final. **[ALLEGATION]** marks claims not proven in court. **[SETTLED ORDER]** marks CFTC findings in a settlement. **[THIRD-PARTY]** marks a source that is not official.

---

## 1. What these companies are (regulatory status)

### Kalshi
- The CFTC "issued an Order of Designation to KalshiEX LLC, granting it status as a designated contract market (DCM)." — https://www.cftc.gov/PressRoom/PressReleases/8302-20 — Nov 4, 2020
- The CFTC granted Kalshi's clearinghouse arm, Kalshi Klear LLC, registration as a derivatives clearing organization (DCO). Source is the CFTC press-release index title "CFTC Grants Kalshi Klear LLC DCO Registration" (Release 8957-24). I saw the title in the CFTC index but did not open the release body. — https://www.cftc.gov/PressRoom/PressReleases/8957-24 — 2024 (exact day not checked)

### Polymarket (offshore, 2022 enforcement)
- CFTC headline: "CFTC Orders Event-Based Binary Options Markets Operator to Pay $1.4 Million Penalty." The respondent was Blockratize, Inc. d/b/a Polymarket. The order found it was "operating an illegal unregistered or non-designated facility for event-based binary options" from about June 2020, having failed to obtain DCM designation or SEF registration. **[SETTLED ORDER]** — https://www.cftc.gov/PressRoom/PressReleases/8478-22 — Jan 3, 2022
- Quote from Acting Enforcement Director Vincent McGonagle: "All derivatives markets must operate within the bounds of the law regardless of the technology used." — same URL — Jan 3, 2022

### Polymarket's U.S. return (official)
- The amended order says that on July 9, 2025, the CFTC issued an order "designating QCX LLC (the 'Exchange,' which now operates under the business name Polymarket US) as a contract market". The original order barred FCM intermediation. The amended order removes that bar, following "submissions dated August 14, 2025 through November 24, 2025". — The text is a CFTC order, but the copy I read is hosted by a third party (DeFi Rate): https://defirate.com/wp-content/uploads/2026/04/Polymarket-US-Amended-Order-of-Designation_Signed_11-24-2025.pdf — signed Nov 24, 2025. I found no CFTC press release for this order.
- CFTC staff no-action letter 25-28 went to "QCX LLC and QC Clearing LLC". The letter says "QCX LLC is a designated contract market ('DCM') and QC Clearing LLC is a registered derivatives clearing organization ('DCO')." The relief covers only swap-data reporting and recordkeeping for fully collateralized binary and variable-payout contracts. — https://www.cftc.gov/csl/25-28/download — Sep 2, 2025
- CFTC press release on that letter: "The no-action letter applies only in narrow circumstances and is comparable to no-action letters issued for other similarly situated designated contract markets…" — https://www.cftc.gov/PressRoom/PressReleases/9113-25 — Sep 3, 2025
- Polymarket US is trading. Its 2026 CFTC filings are signed "QCX LLC d/b/a Polymarket US" and report fee changes that "took effect", for example on Sept 17, 2026. This is evidence of live operations, not a launch announcement. — https://www.cftc.gov/filings/orgrules/rules09212628660.pdf — Sep 21, 2026

### ICE investment in Polymarket (SEC filing)
- ICE 8-K, Exhibit 99.1: "ICE will invest up to $2 billion in Polymarket, reflecting a valuation of approximately $8 billion pre-investment." ICE "will become a global distributor of Polymarket's event-driven data". The investment "will be in cash and is not expected to have a material impact on ICE's 2025 financial results". — https://www.sec.gov/Archives/edgar/data/1571949/000094787125000890/ss5432176_ex9901.htm — filed Oct 7, 2025
- The same exhibit describes Polymarket this way: "every trade matched peer-to-peer through smart contracts." — same URL — Oct 7, 2025

---

## 2. How the operator makes money

### Kalshi: fees, not betting against you
- Kalshi Help Center: "Kalshi makes money by charging a transaction fee on the expected earnings on the contract." The page also says: "Maker fees are charged for orders placed that are not immediately matched and are instead left as resting orders on the orderbook" and "there are no fees associated with canceling a resting order." — https://help.kalshi.com/trading/fees — page dated Apr 19, 2026
- Kalshi fee schedule as filed with the CFTC: "fees = round up(0.07 x C x P x (1-P))", where P is the contract price in dollars, C is the number of contracts, and "round up = rounds to the next cent". The same schedule says "There is no settlement fee" and "There is no processing fee." In this 2022 version, makers paid no trading fee. The index-market variant was "round up(0.035 x C x P x (1-P))". — https://cftc.gov/filings/orgrules/rule091222kexdcm003.pdf — PDF metadata Sep 9, 2022
  - Worked example (my arithmetic): one contract at 50¢ gives 0.07 × 0.5 × 0.5 = $0.0175, which rounds up to $0.02. The fee is largest at 50¢ and shrinks toward 1¢ or 99¢.
- Kalshi blog: S&P 500 and Nasdaq-100 fees "are dropping from 1.75c to 0.875c per contract at the midpoint price. Rounding applies." This matches 0.07 × 0.25 = 1.75¢ at 50¢. — https://news.kalshi.com/p/were-halving-the-fees — Sep 14, 2022
- Kalshi Help Center: "On Kalshi, you are always trading against another member of the platform, not the exchange itself." Also: "Market makers make money by collecting the spread (the difference between the bid and ask)" and "There are a number of market makers on Kalshi, primarily individuals and small institutions." — https://help.kalshi.com/trading/who-are-you-trading-with — Aug 14, 2026
- **Nuance (affiliate market maker):** Kalshi's notice says the exchange's board "approved Kalshi Trading LLC ('Trading'), an affiliate of the Exchange, to be a member of the Exchange. Beginning June 28, 2021, Trading commenced trading". It adds that "Trading was established as a profit-making enterprise to help support liquidity on the Exchange, principally through spread trading … Trading both aggresses and enters passive orders" and that there are "strict informational barriers". — https://kalshi-public-docs.s3.amazonaws.com/Kalshi+Text+of+Website+Notice+of+Affiliate+Entity+Member+09.21.21.pdf — Sep 21, 2021
- Kalshi's 2026 liquidity-provider program filing with the CFTC: "Affiliates of Kalshi are excluded to avoid conflicts of interest." — https://www.cftc.gov/filings/orgrules/rules10182634499.pdf — Oct 19, 2026
- Kalshi says Susquehanna International Group "has onboarded as a market maker" and "set up a dedicated trading division just for prediction markets on Kalshi." — https://news.kalshi.com/p/kalshi-kit-liquidity-sig-market-makers — Apr 3, 2024
- Kalshi files incentive programs with the CFTC. Its filing says the "Liquidity Incentive Program" exists "to increase liquidity on the central limit order book." — https://www.cftc.gov/filings/orgrules/rules07152610358.pdf — Jul 15, 2026

### Polymarket (international and Polymarket US)
- Polymarket docs, fees page: "Makers are never charged fees. Only takers pay fees." The formula is "fee = C × feeRate × p × (1 - p)". Category rates: Crypto 0.07; Sports 0.05; Finance, Politics, Mentions and Tech 0.04; Economics, Culture, Weather and Other 0.05; Geopolitics 0. Fees fund a "Maker Rebates Program" that "redistributes fees daily to market makers." — https://docs.polymarket.com/polymarket-learn/trading/fees — page undated (read 2026-11-10)
- Polymarket US (QCX) CFTC notice: "Fee = Θ × C × p × (1 − p)". The taker coefficient rose "from Θ = +0.06 to Θ = +0.0695". The maker rebate is "Θ = −0.0125", and the change "took effect on Thursday, September 17, 2026". — https://www.cftc.gov/filings/orgrules/rules09212628660.pdf — Sep 21, 2026
  - Earlier step: the taker coefficient went "from 0.05 to 0.06". — https://www.cftc.gov/filings/orgrules/rules0707269057.pdf — Jul 7, 2026
  - Table tennis: "taker fee coefficient for table tennis Contracts is increased from Θ = +0.0695 to Θ = +0.10". — https://www.cftc.gov/filings/orgrules/rules10142633348.pdf — Oct 13, 2026
- Polymarket US market-maker program: "rebates are paid to the Program Participant out of fee revenue actually collected by the Exchange". — https://www.cftc.gov/filings/orgrules/rules09302630736.pdf — Sep 30, 2026

### Sportsbook-owned prediction products (SEC filings)
- DraftKings 10-Q: "DraftKings Predictions launched in December 2025 as an introducing broker". Its prediction revenue includes "(ii) transaction fees earned by its designated contract market, DKeX, and (iii) revenue generated by its market maker, GUS CAP LLC, from providing liquidity and trading on DKeX and third-party exchanges." This is a counterexample: at DraftKings, an affiliate does trade on the operator's own exchange. — https://www.sec.gov/Archives/edgar/data/1883685/000188368526000041/dkng-20260930.htm — filed Nov 6, 2026
- DraftKings 10-Q: putative class actions allege "that DraftKings Predictions offers unlawful sports betting". **[ALLEGATION / PENDING]** — same URL — Nov 6, 2026
- Flutter 10-Q: "In December 2025, we launched FanDuel Predicts in partnership with CME Group ('CME') in five states … with sports available for trading in 18 non-sportsbook states including California, Texas and Florida." Also: "We are, however, beginning to see an impact on sportsbook customer acquisition costs from the substantial market spend from prediction market operators." — https://www.sec.gov/Archives/edgar/data/1635327/000163532726000059/flut-20260930.htm — filed Nov 4, 2026

---

## 3. Volume and sports share

- CFTC proposed rule: event-contract activity has grown "especially since October 2025, reaching $25 billion in March 2026". Footnote: "The $25 billion in event contracts is approximately 0.08% of the $31 trillion total notional value in futures contracts regulated by the Commission". — 91 FR 35806, https://www.govinfo.gov/content/pkg/FR-2026-06-12/pdf/2026-11854.pdf — Jun 12, 2026
- Kalshi (company claim): "annualized trading volume now exceeds $1 trillion". Also "over $1 billion in non-sports annualized revenue", "Crypto trading volume has reached $140 billion annualized", and "we account for over 75% of prediction market trading volume". Kalshi gives no sports percentage. — https://news.kalshi.com/p/kalshi-series-g-40-billion-valuation — Oct 29, 2026 ($1B Series G at a $40B post-money valuation)
- Kalshi (company claim, May): annualized volume grew "from $52 billion to $178 billion" over six months, with "over 90% of U.S. prediction market activity". — https://news.kalshi.com/p/kalshi-raises-1-billion-22-billion-valuation-institutional-demand-surges — May 7, 2026 ($1B Series F at a $22B valuation)
- Sports share **[THIRD-PARTY]**: Pew Research Center analysed data from The Block and found sports "the most traded topic on both platforms by a large margin". From Pew's table, Kalshi July 2026 sports volume was $31.4B of about $40.1B (≈78%). Polymarket was $10.6B of about $12.9B (≈82%). The percentages are my arithmetic. Combined Kalshi and Polymarket volume was $53.0B in July 2026. — https://www.pewresearch.org/short-reads/2026/09/23/prediction-markets-trading-volume-doubled-between-may-and-july-largely-driven-by-sports/ — Sep 23, 2026
- I found **no official sports-share figure** from Kalshi, Polymarket or the CFTC. Kalshi's choice to report a "non-sports" revenue figure suggests sports revenue is large, but that is an inference.

---

## 4. Courts — the state-vs-federal fight [mostly PENDING]

- **Third Circuit (New Jersey), Kalshi won 2–1 at the preliminary-injunction stage:** "Kalshi's sports-related event contracts are swaps traded on a CFTC-licensed DCM, so the CFTC has exclusive jurisdiction." — KalshiEX v. Flaherty, No. 25-1922, https://www2.ca3.uscourts.gov/opinarch/251922p.pdf — decided Apr 6, 2026
  - Judge Roth, dissenting: "I see Kalshi's actions as a performative sleight meant to obscure the reality that Kalshi's products are sports gambling." — same URL
  - The opinion recounts New Jersey's cease-and-desist letter, which said Kalshi's sports contracts violate "New Jersey's constitution and gambling laws that prohibit betting on collegiate sports". — same URL
- **Ninth Circuit (Nevada), Kalshi lost:** the panel held "the sports event contracts were not 'swaps' because they were sports bets." It affirmed dissolution of the injunction as to sports and "remanded for the district court to consider Nevada's challenges to Kalshi's election contracts". The opinion also relies on 17 C.F.R. § 40.11, which bars gaming contracts. — KalshiEX v. Assad, No. 25-7516, https://cdn.ca9.uscourts.gov/datastore/opinions/2026/08/28/25-7516.pdf — filed Aug 28, 2026
- **Supreme Court [PENDING]:** No. 26-299, *Flaherty v. KalshiEX, LLC*. The petition was filed Sep 2, 2026 and docketed Sep 8. Amicus briefs include the "National Football League" and the "American Gaming Association". Kalshi's response deadline was extended "to and including December 7, 2026." Cert has **not** been granted. — https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/26-299.html — docket read 2026-11-10
- **Maryland district court, Kalshi lost:** "Kalshi has failed to show a likelihood of success on the merits of its claim that the Commodity Exchange Act preempts Maryland's gaming laws. The motion for a preliminary injunction will be denied." — KalshiEX v. Martin, No. 25-cv-1283, https://www.govinfo.gov/content/pkg/USCOURTS-mdd-1_25-cv-01283/pdf/USCOURTS-mdd-1_25-cv-01283-0.pdf — Aug 1, 2025. The Fourth Circuit appeal (No. 25-1892) is **[PENDING]**; see Flags.
- **D.C. Circuit (election contracts):** the order says "the motion for stay be denied without prejudice to renewal should substantiating evidence of irreparable harm arise". This let Kalshi list congressional-control contracts. — No. 24-5205, https://storage.courtlistener.com/recap/gov.uscourts.cadc.41256/gov.uscourts.cadc.41256.1208667688.0.pdf — Oct 2, 2024
  - Background: the CFTC had "determined the contracts involve gaming and activity that is unlawful under state law and are contrary to the public interest". — https://www.cftc.gov/PressRoom/PressReleases/8780-23 — Sep 22, 2023
- **State regulators:** Nevada's Gaming Control Board said offering "event-based contracts" on sports and elections "is unlawful in Nevada, unless and until approved as licensed gaming". It set a deadline of "5:00 p.m. on March 14, 2025". Chairman Hendrick: "Any unlawful attempts to circumvent Nevada's right to regulate gaming activity within its borders will be met with the full force of criminal and civil penalties." — https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/press-release/NGCB%20-%20News%20Release%20-%20KalshiEX%20Cease%20and%20Desist%20Order%20(3-4-2025).pdf — Mar 4, 2025

---

## 5. The CFTC under Chairman Selig (2026): siding with the platforms

- The CFTC withdrew the 2024 proposal that would have banned political and sports event contracts, along with the staff sports advisory. Selig: "The 2024 event contracts proposal reflected the prior administration's frolic into merit regulation…" — https://www.cftc.gov/PressRoom/PressReleases/9179-26 — Feb 4, 2026
- The CFTC sued Arizona, Connecticut and Illinois. Each "had sent cease and desist letters to CFTC-regulated entities", and Arizona was also "pursuing criminal charges". — https://www.cftc.gov/PressRoom/PressReleases/9208-26 — Apr 9, 2026. A temporary restraining order "barring Arizona from continuing to pursue criminal charges" followed. — https://www.cftc.gov/PressRoom/PressReleases/9211-26 — Apr 10, 2026 **[PENDING]**
- The CFTC sued New York, which "has sought to enforce state laws against CFTC-registered entities through cease-and-desist letters and civil enforcement suits." — https://www.cftc.gov/PressRoom/PressReleases/9218-26 — Apr 24, 2026 **[PENDING]**
- The CFTC stayed a Kalshi rule change that responded to a Michigan court order to cancel trades. Selig: "A state cannot force a DCM to violate its obligations, and federal law does not permit a DCM to discriminate against a state's residents." The release lists CFTC suits against "Arizona, Connecticut, Illinois, Kentucky, Minnesota, New Mexico, New York, Rhode Island, and Wisconsin." — https://www.cftc.gov/PressRoom/PressReleases/9267-26 — Jul 14, 2026
- The June 2026 proposed rule would set "a 90-day review process" and "a set of public interest factors… on a contract-by-contract basis", and it "defines key statutory terms, including 'involve' and 'gaming.'" — https://www.cftc.gov/PressRoom/PressReleases/9249-26 — Jun 10, 2026 (proposal, not final)
- Two October 2026 actions:
  - A proposed rule to define "swap" to include event contracts "including those based on sports, politics, cultural, and weather-related events" (proposal). — https://www.cftc.gov/PressRoom/PressReleases/9310-26 — Oct 9, 2026
  - An interim final rule excluding "casino-style gambling products, including wagers placed on sportsbooks and casino games" from the swap definition. — https://www.cftc.gov/PressRoom/PressReleases/9309-26 — Oct 9, 2026

---

## 6. Integrity, insider trading, leagues

- CFTC settled with a White House teleprompter operator who traded "presidential mention market contracts". He must "disgorge … $107,539.02 and pay a civil monetary penalty of $65,000". The release adds: "The CFTC appreciates the assistance of KalshiEX in this matter." **[SETTLED ORDER]** — https://www.cftc.gov/PressRoom/PressReleases/9289-26 — Aug 28, 2026
- CFTC settled with former Rep. George Santos over a "Who will attend the State of the Union?" contract "whose underlying event Santos controlled". He paid $17,569.98 in disgorgement and a $17,500 penalty. **[SETTLED ORDER]** — https://www.cftc.gov/PressRoom/PressReleases/9276-26 — Jul 31, 2026
- CFTC–NBA memorandum of understanding. Selig: "The NBA joins the MLB and NHL in taking a responsible step toward protecting sports integrity". — https://www.cftc.gov/PressRoom/PressReleases/9314-26 — Oct 26, 2026
- NBA statement: Kalshi and Polymarket are the league's "Preferred Prediction Market Exchanges". The agreements include "limitations on permissible markets" and "affirmative prohibitions on trading NBA event contracts by league and team personnel." — https://www.nba.com/news/nba-establishes-integrity-framework-and-commercial-partnerships-for-prediction-markets — Oct 26, 2026
- NCAA: President Charlie Baker called on the CFTC to "pause all college sport offerings in prediction markets". Quotes: "Just as we need Congress to stabilize eligibility, we need federal regulators to stabilize these markets" and "The answer cannot be the status quo." — https://www.ncaa.org/news/media-center-ncaa-urges-federal-agency-to-suspend-college-sport-prediction-markets/ — Jan 14, 2026

---

## Flags / not verified

1. **Kalshi's current fee PDF and live fee page were not readable.** Both https://kalshi.com/docs/kalshi-fee-schedule.pdf and https://kalshi.com/fee-schedule returned HTTP 429 (Vercel bot challenge). The 0.07 formula above comes from the 2022 CFTC-filed copy. I could not confirm that **0.07 is still the general taker rate today** or that the maker formula is **0.0175 × C × P × (1−P)**. The 0.0175 figure appears only in third-party guides. Re-check in a browser before quoting.
2. **"Kalshi never bets against users" needs care.** The exchange says you trade "against another member … not the exchange itself". But Kalshi's affiliate **Kalshi Trading LLC** has traded on the exchange since June 28, 2021, per the 2021 notice. Press reports say a Kalshi spokesperson put the affiliate at about 1.5% of 2026 volume and that the CFTC is weighing conflict rules for affiliated market makers (91 FR 50926, "Conflicts and Affiliations", Aug 6, 2026). I have not verified either point on the primary page. Safe wording: "the exchange doesn't take the other side; an affiliated trading firm has been a market participant." DraftKings' affiliate GUS CAP LLC is openly disclosed as a market maker on its own DCM.
3. **Official sports share of volume was not found.** The ~78–82% figures come from Pew's analysis of The Block data, not company or CFTC data. The 79% (Bank of America) and 85% (Dune) figures I saw in search snippets were not checked.
4. **Kalshi's volume figures are company claims and hard to reconcile:** $178B annualized in May 2026, then more than $1T annualized in October 2026. The October figure includes perpetual futures and crypto. Attribute both to Kalshi and avoid presenting them as audited.
5. **Fourth Circuit (Maryland) status was not checked on a primary source.** Secondary sources say the case was argued in May 2026 with no decision yet, and that Maryland agreed not to enforce while the appeal is pending.
6. **Ninth Circuit rehearing en banc** was reportedly denied around Nov 6–9, 2026, per Prediction News. Not verified on the court docket.
7. **D.C. Circuit dismissal** of the CFTC's appeal (reported May 7, 2025, after a CFTC motion on May 5) was not checked on the docket. Justia returned 403, and CourtListener needs authentication. The Oct 2, 2024 stay-denial order is verified.
8. **Polymarket US launch details** are secondary or social-media sourced and unverified: the December 2025 waitlist rollout, the May 2026 waitlist removal, iOS-only, the $112M QCEX price, and Coplan's "green light" post. The CFTC orders and QCX filings are verified. The amended order copy I read is hosted by DeFi Rate rather than cftc.gov.
9. **Polymarket international fee page** is undated. The rates may have changed.
10. **Not checked:** the MLB and NHL MOUs (mentioned only in the CFTC quote); the NFL's position beyond its amicus filing in No. 26-299; Kalshi's own Series G press-release wording on Business Wire; CME's 10-K description of FanDuel Predicts. The EDGAR search shows CME's 10-K mentions event contracts, but I did not read it.
11. **Kalshi's "100% legal in all 50 states" post** (https://news.kalshi.com/p/game-on-kalshi-sports-trading-is-now-100-legal-in-all-50-states-2, Jan 24, 2025) is marked as an opinion piece. It is contradicted by the later Ninth Circuit and Maryland rulings. Do not repeat the claim as fact.
12. **Pending or allegation items:** all state cases, CFTC-v-state suits, the cert petition and the DraftKings class actions are unresolved. The CFTC press release titled "Charges Google Employee with Insider Trading" (9237-26) is an allegation and was not read.
