# Ep 51: How SpaceX Actually Makes Money (research notes)

Checked 2026-11-11. All figures are US dollars. "$M" means millions, as reported in the filings.
- **Fetched**: I read the primary page myself (SEC EDGAR document downloaded and read in full text, or an official agency page opened directly).
- **Snippet**: seen only in search results or secondary coverage, not confirmed on a primary page.
- **Computed**: our own arithmetic on Fetched figures. Say "about" on air, and label it as our math in sources.yaml.

These are notes, not yet sources.yaml. A named human reviewer must sign off.

## Primary sources
EDGAR access worked: data.sec.gov submissions JSON plus sec.gov/Archives documents, read with a declared User-Agent. Company CIK is 0001181412, "SPACE EXPLORATION TECHNOLOGIES CORP (SPCX)". ir.spacex.com returned HTTP 403 to automated fetches, so it was not read. spaceforce.mil also returned 403.

- [S1] Form S-1, filed 2026-05-20: https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/spaceexplorationtechnologi.htm (downloaded; the 424B4 was used for quotes)
- [S1A] S-1/A, filed 2026-06-03, with an expected price of $135.00: https://www.sec.gov/Archives/edgar/data/1181412/000162828026040364/spaceexplorationtechnologib.htm
- [PROS] Final prospectus 424B4, dated 2026-06-11 and filed 2026-06-12: https://www.sec.gov/Archives/edgar/data/1181412/000162828026042639/spaceexplorationtechnologi.htm
- [8K-IPO] 8-K for the IPO closing, 2026-06-15: https://www.sec.gov/Archives/edgar/data/1181412/000162828026043288/spaceexplorationtechnologi.htm
- [8K-CURSOR1] 8-K for the Cursor merger agreement, 2026-06-16: https://www.sec.gov/Archives/edgar/data/1181412/000162828026043411/spaceexplorationtechnologi.htm
- [8K-CASH] 8-K updating the cash balance and launching the notes offering, 2026-06-22: https://www.sec.gov/Archives/edgar/data/1181412/000162828026044489/spcx8-kxlaunchseniornotes.htm
- [8K-BOND] Ex. 99.1 announcing the $25B bond pricing, 2026-06-23: https://www.sec.gov/Archives/edgar/data/1181412/000162828026044955/exhibit991-pricing8xk.htm
- [Q2REL] Q2 2026 earnings release, Ex. 99.1, 2026-08-04: https://www.sec.gov/Archives/edgar/data/1181412/000162828026052515/earningsreleaseq22608042.htm
- [10Q2] 10-Q for Q2 2026, 2026-08-04: https://www.sec.gov/Archives/edgar/data/1181412/000162828026052535/spcx-20260630.htm
- [8K-CURSOR2] 8-K for the Cursor closing, 2026-08-14: https://www.sec.gov/Archives/edgar/data/1181412/000162828026056945/spcx-20260814.htm
- [Q3REL] Q3 2026 earnings release, Ex. 99.1, 2026-10-20: https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm
- [10Q3] 10-Q for Q3 2026, 2026-10-22: https://www.sec.gov/Archives/edgar/data/1181412/000162828026066880/spcx-20260930.htm
- [8K-APOLLO] 8-K on the Apollo GPU lease, 2026-10-26: https://www.sec.gov/Archives/edgar/data/1181412/000110465926118614/tm2628247d1_8k.htm
- [NASA-HLS21] NASA release, 2021-04-16: https://www.nasa.gov/news-release/as-artemis-moves-forward-nasa-picks-spacex-to-land-next-americans-on-moon/
- [NASA-HLS22] NASA release, 2022-11-15: https://www.nasa.gov/humans-in-space/nasa-awards-spacex-second-contract-option-for-artemis-moon-landing
- [NASA-CREW26] NASA release, 2026-09-18: https://www.nasa.gov/missions/station/commercial-crew/nasa-awards-spacex-three-crew-flights-to-space-station/
- [SSC-NSSL] Space Systems Command release, 2025-04-04 (the page returned 403 and was not read): https://www.spaceforce.mil/News/Article-Display/Article/4146459/space-systems-command-awards-national-security-space-launch-phase-3-cont/

## 1. Listing facts
- **Timeline.** The confidential DRS was filed 2026-03-30. The public S-1 was filed 2026-05-20 (Reg. No. 333-296070). The SEC "EFFECT" notice is dated 2026-06-11, as is the prospectus. Trading began 2026-06-12, and the IPO closed 2026-06-15. Sources: EDGAR filing index, Fetched. [8K-BOND] says: "Registration Statement on Form S-1, filed on May 20, 2026, as amended (No. 333-296070)". Fetched.
- **Ticker, exchanges and state of incorporation.** "We have been approved to list our Class A common stock on The Nasdaq Stock Market LLC ("Nasdaq") and Nasdaq Texas, LLC ("Nasdaq Texas") under the symbol "SPCX."" The company is "a Texas corporation". [PROS] cover, Fetched.
- **Price and base deal.** "The initial public offering price is $135.00 per share." The base deal was 555,555,555 shares, for a total of "$74,999,999,925". Underwriting discount: "$0.90" per share, "$500,000,000" in total. [PROS] cover, Fetched.
- **Final size, including the over-allotment.** "On June 15, 2026, the Company completed its IPO of 638,888,888 shares ... at an offering price of $135.00 per share, which includes the exercise in full by the Underwriters ... of their option to purchase ... an additional 83,333,333 shares". [8K-IPO], Fetched.
  - Gross proceeds ≈ **$86.25B** (Computed).
  - Net proceeds: "net proceeds of approximately $85.7 billion. The shares of Class A common stock began trading on the Nasdaq Global Select Market and Nasdaq Texas on June 12, 2026". [Q2REL], Fetched.
- **Lead banks.** Goldman Sachs, Morgan Stanley, BofA, Citigroup and J.P. Morgan were the representatives. [PROS] and [8K-IPO], Fetched.
- **Valuation at the IPO price.** The filings give no single "valuation" figure. Shares outstanding after the offering (before the over-allotment) were 7,488,063,555 Class A plus 5,602,790,410 Class B. [PROS] ownership section, Fetched. At $135 that is **about $1.77 trillion** (Computed). With the over-allotment shares added, it is about $1.78T (Computed).
- **Musk's voting control.** "Elon Musk ... will hold approximately 82.4% of the voting power of our common stock ... of which approximately 81.1% is attributable to his ownership of our Class B common stock." Class B carries "10 votes per share". [PROS] cover, Fetched. SpaceX is a "controlled company" under Nasdaq rules.
  - The ownership table, which uses a May 1 basis, shows Musk after the offering with 849,494,440 Class A shares (11.3%) and 5,569,053,075 Class B shares (93.6%), for **84.4% combined voting power**. [PROS] p. 248, Fetched.
  - The Class B count includes 1,302,072,285 restricted shares. Of these, 1.0B vest only on market-cap milestones and "a permanent human colony on Mars with at least one million inhabitants". The other 302M vest on "non-Earth-based data centers capable of delivering 100 terawatts of compute per year". [PROS], Fetched.
  - Musk's economic stake is roughly **46–48% of shares** (Computed). It includes unvested restricted shares and 350M options. Always say "about half" and "includes unvested shares".
- **Cash after the IPO.** "as of June 19, 2026, it held approximately $100.8 billion in cash and cash equivalents". [8K-CASH], Fetched.
- **Bond issue.** SpaceX then issued "$25 billion inaugural bond issuance" in five tranches with coupons from 5.350% to 6.650%. The proceeds repaid a bridge loan. [8K-BOND], Fetched.

## 2. Revenue, profit, capex and cash
**Important framing.** The historical financials are *recast to include xAI and X (Twitter)*: "retrospectively recast for all periods presented to include (i) the historical results of X.AI Holdings Corp., which was acquired by SpaceX, effective February 2, 2026 (the "xAI Merger"), and X Holdings Corp. ..., which was acquired by xAI, effective March 28, 2025". [PROS], Fetched. So "SpaceX 2023 revenue $10.4B" includes X's advertising business.

- **Revenue by segment and year.** Source: [PROS] Note 3, Fetched.

  | $M | FY2023 | FY2024 | FY2025 |
  |---|---|---|---|
  | Space | 3,557 | 3,796 | 4,086 |
  | Connectivity (Starlink) | 3,869 | 7,599 | 11,387 |
  | AI (xAI + X) | 2,961 | 2,620 | 3,201 |
  | **Total** | **10,387** | **14,015** | **18,674** |

  - Within Space, Launch Services was 1,964 / 2,584 / 2,576 and Launch & Development was 1,593 / 1,212 / 1,510.
  - Within Connectivity, Consumer was 2,817 / 4,830 / 7,208 and Enterprise & Government was 1,052 / 2,769 / 4,179.
  - Within AI, Advertising was 2,323 / 1,728 / 1,844 and AI Solutions & Infrastructure was 638 / 892 / 1,357.
  - Space plus Connectivity only ("legacy SpaceX"): 2023 $7,426M, 2025 $15,473M (Computed).
- **Operating income or loss by segment, FY2023 / FY2024 / FY2025 ($M).** Source: [PROS], Fetched.
  - Space: (1) / 21 / (657).
  - Connectivity: 469 / 2,006 / 4,423.
  - AI: (3,973) / (1,561) / (6,355).
  - Consolidated: (3,505) / 466 / (2,589).
- **Net income or loss, FY2023 / FY2024 / FY2025.** $(4,628)M / $791M / $(4,937)M. [PROS], Fetched.
- **Capex by segment ($M).** [PROS], Fetched.
  - FY2023 total 4,415. FY2024 total 11,163.
  - FY2025: Space 3,832, Connectivity 4,178, AI 12,727, total 20,737. In 2025, capex exceeded revenue (Computed comparison).
- **Cash and cash equivalents.** $11,385M at Dec 31, 2024 and $24,747M at Dec 31, 2025. [PROS], Fetched.
- **Accumulated deficit.** $(37,035)M at Dec 31, 2025 and $(41,311)M at Mar 31, 2026. [PROS], Fetched. The "cumulative losses >$37B" claim in secondary coverage matches the Dec 2025 figure.
- **Q1 2026** (the quarter ended March 31, 2026). [PROS], Fetched.
  - "revenue on a consolidated basis of $4,694 million, loss from operations of $(1,943) million". **Verified.**
  - Revenue by segment: Space 619, Connectivity **3,257** (verified), AI 818.
  - Segment operating results: Space (662), Connectivity 1,188, AI (2,469).
  - Net loss $(4,276)M. Capex $10,107M, of which AI was $7,723M. Cash $15,852M.
- **Q2 2026.** [Q2REL], Fetched.
  - "Revenues of $7.8 billion, up 92% from $4.1 billion". "Net loss of $541 million".
  - Revenue by segment: Space 962, Connectivity 4,291, AI 2,561, total 7,814.
  - Segment operating results: Space (542), Connectivity 1,656, AI (1,257). Consolidated loss from operations $(143)M.
  - Capex $18,369M, of which AI was $15,828M. Cash $93,522M plus marketable securities $6,487M.
  - "Closed multiple industry-leading Cloud Services Agreements resulting in $14.1 billion of contracted sales."
- **Q3 2026.** [Q3REL], Fetched.
  - "Revenues of $14.6 billion, up 161% from $5.6 billion". "Net income of $4.4 billion".
  - Revenue by segment: Space 1,767, Connectivity 5,248, **SI 7,560**, total **14,575**. **Verified.**
  - Operating income by segment: Space (7), Connectivity 2,367, SI 431, total **2,791**.
  - Capex $19,593M, of which SI was $16,444M. Cash $51,294M plus marketable securities $38,561M. Total assets $254,045M.
  - Nine-month figures: revenue $27,083M, capex $48,069M (SI $39,995M, or 83%, Computed), operating cash flow $13,097M.
  - Q3 net income was helped by a $390M tax benefit and other income of $1,025M. That includes a $561M related-party unrealized gain on The Boring Company stake. [10Q3], Fetched.
- **What the "AI" segment is, now called "SI".** "Super Intelligence (SI) refers to the operating and reportable segment previously reported as Artificial Intelligence (AI)." [Q3REL], Fetched. The segment includes "(i) SI infrastructure solutions, (ii) frontier LLM Grok, (iii) SI-assisted software engineering platform Cursor, and (iv) ... X." [10Q3], Fetched.
  - It is the former xAI (with X inside). SpaceX acquired xAI effective 2026-02-02.
  - It added Cursor (Anysphere): "implied equity value of $60 billion", closed 2026-08-14. "The GAAP purchase consideration was $42.5 billion". "Cursor contributed $608 million of revenue". [Q3REL] and [8K-CURSOR2], Fetched.
- **Where the SI revenue comes from: renting GPUs to other AI labs.** "in May 2026, we entered into Cloud Services Agreements with Anthropic PBC ... approximately 325,000 NVIDIA GPUs ... the customer has agreed to pay us $1.25 billion per month through May 2029 ... After the initial three-month period, the agreements may be terminated by either party upon 90 days' notice." [PROS], Fetched. That is about $15B a year (Computed).
- **Q3 revenue mix.** SI was 52%, Connectivity 36% and Space 12% (Computed). SI overtook Connectivity for the first time in Q3 2026.
- **Debt-like financing for GPUs.**
  - Apollo-managed lessor: "aggregate principal payments under the lease schedules ... approximately $40 billion". [8K-APOLLO], Fetched.
  - Valor (director Antonio Gracias's firm) GPU leases are recorded as related-party debt of $2,181M (current) plus $10,716M (non-current). [10Q3], Fetched.
- **Backlog.** $28,377M at Dec 31, 2025 [PROS], and "$62,959 million as of September 30, 2026" [10Q3]. Fetched.

## 3. Starlink
- **Subscribers.** "approximately 10.3 million Starlink Subscribers across 164 countries, territories, and other markets" as of Mar 31, 2026. [PROS], Fetched. **Verified.**
  - Year-end counts: 2.3M (2023), 4.4M (2024), 8.9M (2025). Then 12.0M (Q2 2026). [PROS] and [Q2REL], Fetched.
  - "13.6 million Starlink consumer subscribers" at Sep 30, 2026, plus "hundreds of thousands of additional enterprise subscribers". [Q3REL], Fetched.
- **ARPU is falling.** Starlink ARPU per month was $99 (2023), $91 (2024), $81 (2025), $66 (Q1 2026), $66 (Q2) and $69 (Q3). [PROS], [Q2REL] and [Q3REL], Fetched. The filing explains: "22.9% decline in Starlink Subscriber ARPU, primarily due to international expansion and the addition of lower priced service plans." [PROS], Fetched.
- **Satellites and countries.** "approximately 9,600 Starlink broadband and mobile satellites in Low-Earth Orbit" (Mar 31, 2026). "SpaceX owns and operates approximately 75% of all active maneuverable satellites." [PROS], Fetched. By Q3: "over 11,100 Starlink broadband and mobile satellites" and "174 countries, territories, and other markets". [10Q3], Fetched.
- **Consumer share of revenue.** "In 2025, revenue from consumer subscribers represented over 60% of Connectivity segment revenue." [PROS], Fetched.
- **Connectivity margin.** FY2025 operating income was $4,423M on $11,387M revenue, about 39% (Computed). Q3 2026 was $2,367M on $5,248M, about 45% (Computed).
- **Government and Starshield.** No standalone Starshield revenue figure is disclosed. Government connectivity growth is disclosed: "+$1,250 million" (2024) and "+$193 million" (2025). Q1 2026 shows "a decrease of $175 million in our government connectivity business". [PROS], Fetched. Q2 2026: "Awarded over $6 billion in multi-year U.S. government contracts for Starshield ... primarily from two major Space Force contracts". [Q2REL], Fetched.
- **Starlink Mobile.** "approximately 650 V1 Mobile satellites ... approximately 7.4 million monthly unique devices across approximately 30 countries" as of Mar 31, 2026. [PROS], Fetched.

## 4. Launch
- **Total launches.** 98 (2023), 138 (2024), 170 (2025), counting all rockets, Starship included. [PROS] metrics table, Fetched.
- **Falcon launches, customer vs internal.** "the number of launches for the years ended December 31, 2023, 2024, and 2025 totaled 96, 134, and 165, respectively, of which customer launches totaled 33, 45, and 43, respectively, and internal launches totaled 63, 89, and 122". [PROS], Fetched.
  - About **74% of 2025 Falcon launches carried SpaceX's own Starlink satellites** (Computed).
  - Internal launches earn no revenue: "For launches of our Starlink satellites, the Company does not recognize any inter-segment revenue". [PROS], Fetched.
- **Falcon launches in 2026.** 9M 2026: 110 Falcon launches (29 customer, 81 internal) plus 3 Starship. Q3 alone: 33 Falcon (12 customer) plus 2 Starship. "To date, all Starship launches have been classified as internal." [10Q3], Fetched.
- **Market share.** "Since 2023, we have launched more than 80% of mass to orbit for the world each year". In 2025 Falcon 9 accounted for "over half of all global orbital launches". [PROS], Fetched.
- **Reuse.** "Falcon 9 has achieved over 570 successful booster landings and more than 540 launches completed by a flight-proven Falcon rocket". [PROS], Fetched. The 2025 cost of revenue fell partly from "increased reusability ... resulting in lower deprecation of $240 million" (the typo is in the original). [PROS], Fetched.
- **Price.** No Falcon 9 price appears in the filings. "Space customer launches and average price per launch remained relatively flat year over year" (2025). [PROS], Fetched.
  - Launch Services revenue per customer launch in 2025 was about $60M ($2,576M ÷ 43; Computed). This mixes Falcon 9 and Heavy and is not a list price.
  - The list price of $69.75M "through 2024" on the spacex.com capabilities sheet is Snippet only (the PDF URL returned 404 to our fetch). A 2026 figure of $74M is Snippet and unverified.
- **First revenue Starship flight.** "Successfully launched our first revenue-generating Starship mission, delivering 26 Starlink V3 satellites". [Q3REL], Fetched. Because Starship launches are classed as internal, "revenue-generating" here means Starlink capacity, not a paying launch customer.

## 5. Government
- **Largest customer.** "Customer A" was 25.2% (2023), 24.2% (2024) and 20.9% (2025) of consolidated revenue. "Revenue from this customer relates to all three segments." [PROS], Fetched.
  - It was 16.6% in Q3 2026. [10Q3], Fetched.
  - **Customer A is not named.** It is consistent with the U.S. government, but do not state that as fact.
  - 20.9% of 2025 revenue is about $3.9B (Computed).
- **Who the government customers are.** "numerous direct contracts with the U.S. government, primarily NASA, the Department of War, the General Services Administration, and certain Intelligence Community agencies ... All of our launch contracts with U.S. government agencies are firm fixed-price contracts with milestone-based payments." [PROS], Fetched.
- **Launch provider for the U.S. government.** "We are the primary launch provider for the U.S. government. In 2025, we launched 11 of 12 National Security Space Launch ("NSSL") medium and heavy lift missions and all five U.S. crew and cargo missions to the International Space Station for NASA." [PROS], Fetched.
- **NSSL Phase 3 Lane 2.** [PROS] says: "approximately $13.7 billion across the National Security Space Launch ("NSSL") Program's Phase 3 Lane 2 contracts through 2032, supporting approximately 54 missions". Fetched; this is the industry-wide total. SpaceX's own share, "more than $5.9 billion" for 28 missions (awarded April 4, 2025), is Snippet only because spaceforce.mil returned 403. In Q3 2026 SpaceX signed "18 National Security Space Launch missions". [Q3REL], Fetched.
- **NASA Commercial Crew.** A 2026-09-18 NASA release covers Crew-15 to Crew-17 for "$946 million", bringing the cumulative CCtCap value to "$5.92 billion" and the SpaceX total to "17" missions. [NASA-CREW26], Fetched.
- **NASA HLS (Artemis).** "The firm-fixed price, milestone-based contract total award value is $2.89 billion." [NASA-HLS21], 2021-04-16, Fetched. Option B: "The contract modification has a value of about $1.15 billion." [NASA-HLS22], 2022-11-15, Fetched. The total is about $4.0B (Computed). Any later HLS modifications were not checked.
- **What drives government revenue in Space.** 2025 Launch & Development growth came from "an extended contract with NASA for additional Cargo Resupply Services (CRS) missions ... and increased revenue from a U.S. Department of War contract". [PROS], Fetched.
- **A note on naming.** The filings use "Department of War" for the DoD.

## 6. Starship
- **Total spending.** "investing over $15 billion in our next-generation rocket, Starship." [PROS], Fetched.
- **Starship R&D by period.** "our Space segment funded $930 million and $3,004 million in research and development expense during the three months ended March 31, 2026 and the year ended December 31, 2025, respectively, for our next-generation Starship launch vehicle program". [PROS], Fetched.
  - Space segment R&D was $1,076M in Q2 2026 and $1,225M in Q3 2026. [Q2REL] and [Q3REL], Fetched.
- **Starship is why the launch business loses money.** The Space segment posted an operating loss of $(657)M in 2025, against positive Space Segment Adjusted EBITDA of $653M. [PROS], Fetched.
- **Risk factor.** "Any failure or delay in the development of Starship at scale or in achieving the required launch cadence, reusability and capabilities thereafter would delay or limit our ability to execute our growth strategy, including the deployment of next-generation satellites, global satellite-to-mobile connectivity, and orbital AI compute". [PROS], Fetched.
- **Orbital compute plan.** "We expect to begin deploying our orbital AI compute satellites as early as 2028." [PROS], Fetched.
- **New spaceport.** Starbase, Louisiana, "with the first launch targeted for 2029". [Q3REL], Fetched.

## 7. Risk factors and related parties worth quoting
- **Key-person risk.** "We are highly dependent on the continued service and performance of Mr. Musk ... We do not maintain key-person life insurance on Mr. Musk. Further, ... he does not devote his full time and attention to our businesses ... Mr. Musk currently serves as Technoking and Chief Executive Officer of Tesla". [PROS], Fetched.
- **Conflicts of interest.** "Under our charter, Mr. Musk and his affiliates are not restricted from owning assets or engaging in businesses that compete directly or indirectly with us". The prospectus also mentions collaborations "with Tesla, including with respect to Macrohard and Terafab". [PROS], Fetched.
- **Government dependence.** "We derive significant revenue from U.S. government contracts that were awarded through a competitive bidding process." [PROS], Fetched. And: "we may prioritize our own launch payloads over additional U.S. government" missions (the sentence is truncated in our extract). [PROS], Fetched.
- **AI customer concentration.** "a significant portion of our AI infrastructure revenue is concentrated in a small number of customers. Our cloud services agreements ... may be terminated by either party upon 90 days' notice." [10Q2], Fetched.
  - "Customer B" (SI segment) was 19.5% of Q2 revenue and **34.5% of Q3 2026 revenue**, about $5.0B (Computed). [10Q2] and [10Q3], Fetched.
- **Tesla related-party purchases.** "purchased $151 million and $480 million, respectively, of Megapack products from Tesla" (Q3 and 9M 2026). Before that, "$506 million of Megapack products and $131 million of Cybertrucks at manufacturer's suggested retail price". [10Q3], Fetched.
- **Possible Tesla merger.** "our board of directors has formed a special committee to evaluate a potential combination between SpaceX and Tesla, Inc. ... No determination by our special committee has been made". [10Q3], Fetched.
- **xAI merger.** The xAI deal was a common-control transaction, since Musk controlled both companies, so the historical results were pooled. [PROS], Fetched.

## Flags
- **Corrected: segment name.** The "AI" segment was renamed **"Super Intelligence (SI)"** in Q3 2026. The $7.56B Q3 figure is correct but belongs to "SI". It includes X advertising and Cursor (from Aug 14).
- **Corrected: comparing years.** FY2023–2025 figures include xAI and X retroactively. Don't call FY2023's $10.4B "SpaceX's rocket and Starlink revenue". That figure is $7.4B (Computed).
- **Corrected: state of incorporation.** SpaceX is a **Texas** corporation, not a Delaware one. It is listed on **both** Nasdaq and Nasdaq Texas.
- **Corrected: IPO size.** The often-quoted "$75B" is the base deal. With the over-allotment, gross proceeds were about $86.25B (Computed) and net proceeds were "approximately $85.7 billion" (Fetched).
- **Valuation.** "$1.75T" in coverage roughly matches our ~$1.77T computed at $135. "Over $2 trillion" is not supported by the filings. No first-day trading price or market cap was verified, so don't quote one.
- **Contradiction: Musk's voting power.** The 424B4 cover says 82.4% (based on Mar 31 share counts). The ownership table says 84.4% (based on May 1). Say "more than 80%" or cite one and give its basis.
- **Definition changes.** Starting Q3, "Starlink Subscribers" became "Starlink consumer subscribers", which excludes managed enterprise and government lines. The satellite count now includes de-orbit-approved satellites (about 400 more). Don't compare satellite counts across the change without a caveat.
- **Typo in the source.** The Q2 release says compute rose to 1.4 GW from "0.4 GW in Q2 2026". From context it means Q2 2025, so don't quote that line.
- **Do NOT say "Customer B is Anthropic."** The filings name Anthropic as a cloud-services counterparty ($1.25B/month) but do not identify Customer B. Q3 Customer B revenue (about $5.0B) exceeds 3 × $1.25B, so it is either a larger set of agreements or a different customer. Unverified.
- **Do NOT say "Customer A is the U.S. government."** The filings don't name it.
- **Do NOT give a Starshield revenue figure.** None is disclosed. Only growth deltas and the "over $6 billion" in contract awards are available.
- **Unverified (Snippet).** SpaceX's NSSL Phase 3 Lane 2 share (>$5.9B for 28 missions). The Falcon 9 list prices ($69.75M through 2024; $74M in 2026).
- **Not read.** ir.spacex.com (403), including the call transcripts. spaceforce.mil (403). Musk's call remarks about renting out compute or the Tesla merger come only from secondary coverage (Snippet).
- **Profit caveat.** Q3 2026 net income of $4.4B includes a tax benefit and a $561M gain on The Boring Company stake. SI's $431M operating profit includes Cursor (with $1.2B of acquisition stock comp). Don't present Q3 as proof that the AI business is "profitable" without these caveats.
- **No Q4 2025 release exists.** Q4 2025 revenue was about $4.96B (FY minus 9M; Computed).
