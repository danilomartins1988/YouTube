# Before You Buy: Alphabet (GOOGL / GOOG): research notes, Nov 2026 edition

**DATA AS OF close 2026-11-10 · LATEST REPORT: Q3 2026 (quarter ended 2026-09-30)**
Compiled 2026-11-11. USD throughout. Labels: **[F]** = Fetched (we opened the primary document, an SEC EDGAR filing or the Yahoo chart API, and read the figure there). **[S]** = Snippet (from a search result or a secondary news page, not a company document). **[C]** = Computed (our calculation from [F] inputs; the formula is shown).

## Sources (all Fetched unless marked)
| Key | Document | URL |
|---|---|---|
| PR-Q3 | 8-K Ex. 99.1, Q3 2026 earnings release, dated 2026-10-28 | https://www.sec.gov/Archives/edgar/data/1652044/000165204426000080/googexhibit991q32026.htm |
| 10-Q | Form 10-Q, quarter ended 2026-09-30, filed 2026-10-29 | https://www.sec.gov/Archives/edgar/data/1652044/000165204426000084/goog-20260930.htm |
| 10-K | Form 10-K, FY2025, filed 2026-02-05 | https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm |
| PR-Q4 | Q4 2025 release (8-K 2026-02-04) | https://www.sec.gov/Archives/edgar/data/1652044/000165204426000012/googexhibit991q42025.htm |
| PR-Q1 | Q1 2026 release (8-K 2026-04-29) | https://www.sec.gov/Archives/edgar/data/1652044/000165204426000043/googexhibit991q12026.htm |
| PR-Q2 | Q2 2026 release (8-K 2026-07-22) | https://www.sec.gov/Archives/edgar/data/1652044/000165204426000066/googexhibit991q22026.htm |
| 8-K-1105 | 8-K 2026-11-05 (€6B notes offering closed) | https://www.sec.gov/Archives/edgar/data/1652044/000119312526449835/d174184d8k.htm |
| XBRL | EDGAR companyfacts (balance-sheet share counts) | https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json |
| Price | Yahoo chart API, GOOGL and GOOG daily closes | https://query1.finance.yahoo.com/v8/finance/chart/GOOGL · https://query1.finance.yahoo.com/v8/finance/chart/GOOG |
| Proxy | DEF 14A filed 2026-04-24 (listed only; **not read** for this pass) | https://www.sec.gov/Archives/edgar/data/1652044/000130817926000342/goog-20260424.htm |
| MB | MarketBeat call recap, 2026-10-29 (secondary source) | https://www.marketbeat.com/instant-alerts/transcript-alphabet-q3-earnings-call-highlights-2026-10-29/ |

abc.xyz/investor returned HTTP 403 (a Cloudflare challenge), so we could not open the company's own call transcript.

---

## 1. Edition stamp
- **Latest reported quarter:** Q3 2026, ended 2026-09-30. Earnings 8-K 2026-10-28; 10-Q filed 2026-10-29. [F]
- **Close 2026-11-10:** GOOGL (Class A) **$287.38**; GOOG (Class C) **$284.92**. [F, Yahoo; re-checked 2026-11-11]
- **Shares outstanding (10-Q cover):** "As of October 21, 2026, there were 5,888 million shares of Alphabet's Class A stock outstanding, 827 million shares of Alphabet's Class B stock outstanding, and 5,579 million shares of Alphabet's Class C stock outstanding." [F, 10-Q] Total **12,294M**.
- **Market cap (our calc):** (5,888M + 827M) × $287.38 + 5,579M × $284.92 = $1,929.8B + $1,589.6B = **$3.519T** [C]. Class B is unlisted, so it is valued at the GOOGL price, as in the ranking file.
  - Excluded: the 6.25% mandatory convertible preferred stock (19M shares, liquidation preference $1,000 each, so about $19B), which converts on about 2029-05-15 into 2.2520–2.8160 Class A shares (Series A) or 2.2740–2.8420 Class C shares (Series B) per preferred share [F, 10-Q Note 11]. That is about 43–54M common shares at conversion [C], roughly 0.4% of the share count.

## 2. Business today

### Revenue and operating income by segment, fiscal years ($M) [F, 10-K segment note]
| | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Google Services revenue | 272,543 | 304,930 | 342,721 |
| Google Cloud revenue | 33,088 | 43,229 | 58,705 |
| Other Bets revenue | 1,527 | 1,648 | 1,537 |
| Hedging | 236 | 211 | (127) |
| **Total revenue** | **307,394** | **350,018** | **402,836** |
| Services operating income (margin [C]) | 95,858 (35.2%) | 121,263 (39.8%) | 139,404 (40.7%) |
| Cloud operating income (margin [C]) | 1,716 (5.2%) | 6,112 (14.1%) | 13,910 (23.7%) |
| Other Bets operating income | (4,095) | (4,444) | (7,515) |
| Alphabet-level activities | (9,186) | (10,541) | (16,760) |
| **Total operating income** | **84,293** | **112,390** | **129,039** |

Of which Google Search & other: 175,033 / 198,084 / 224,532; YouTube ads: 31,510 / 36,147 / 40,367 [F, 10-K].

### Last four quarters ($M) [F, PR-Q4, PR-Q1, PR-Q2, PR-Q3]
| | Q4 2025 | Q1 2026 | Q2 2026 | Q3 2026 | TTM [C] |
|---|---|---|---|---|---|
| Google Search & other | 63,073 | 60,399 | 63,271 | 63,350 | 250,093 |
| YouTube ads | 11,383 | 9,883 | 11,055 | 11,207 | 43,528 |
| Google Network | 7,828 | 6,971 | 7,303 | 7,455 | 29,557 |
| Subscriptions, platforms & devices | 13,578 | 12,384 | 12,911 | 14,290 | 53,163 |
| **Google Services revenue** | 95,862 | 89,637 | 94,540 | 96,302 | 376,341 |
| **Google Cloud revenue** | 17,664 | 20,028 | 24,768 | 30,709 | 93,169 |
| Other Bets revenue | 370 | 411 | 382 | 372 | 1,535 |
| **Total revenue** | 113,828 | 109,896 | 119,796 | 127,577 | **471,097** |
| Services operating income (margin [C]) | 40,132 (41.9%) | 40,589 (45.3%) | 39,544 (41.8%) | 39,157 (40.7%) | 159,422 |
| Cloud operating income (margin [C]) | 5,313 (30.1%) | 6,598 (32.9%) | 8,814 (35.6%) | 11,121 (36.2%) | 31,846 |
| Other Bets operating income | (3,617) | (2,100) | (1,799) | (2,047) | |
| Alphabet-level activities | (5,894) | (5,391) | (5,789) | (7,655) | |
| **Total operating income** | 35,934 | 39,696 | 40,770 | 40,576 | **156,976** (33.3% margin [C]) |

- Q3 2026 year over year [F, PR-Q3]: revenue +25%; Services +11%; Search & other +12%; Cloud **+103%**; operating margin 31.8%.
- PR-Q3 quote: "Google Cloud delivered record growth as revenues increased 103% to $30.7 billion … TPU systems sales were also a meaningful contributor to revenue growth." [F]
- 10-Q segment description: "Google Cloud generates product revenues primarily from the sale of TPU systems." [F] This is a new hardware-sale revenue type within Cloud.
- Search monetization, Q3 2026 year over year [F, 10-Q]: paid clicks +8%, cost-per-click +4%. Network impressions −14%.
- Pichai (PR-Q3): "We had a strong quarter and are now on a half-trillion dollar revenue run rate." [F; company claim. Q3 × 4 = $510B [C]]

### Geography [F, 10-Q]
Q3 2026: US 53% ($67.7B, +39% YoY), EMEA 26%, APAC 16%, Other Americas 5%. 9M 2026: US 51%, EMEA 27%, APAC 16%, Other Americas 6%. FY2025: US 48% [F, 10-K].
The US jumped from 48% to 53% in Q3, in line with US-heavy Cloud and TPU demand. We infer this; the filing does not explain it.

### Customer concentration
- 10-K: "No individual customer or groups of affiliated customers represented more than 10% of our revenues in 2023, 2024, or 2025." [F]
- 10-K: "We generated more than 70% of total revenues from online advertising in 2025." [F] Advertising was 82,012 / 127,577 = 64% of Q3 2026 revenue [C], so the share is falling as Cloud grows.
- Backlog concentration is **not** disclosed by customer. The only named item: Q3 backlog "included $16.8 billion associated with a multi-year commercial agreement with Crux AI, an unconsolidated equity method joint venture and a related party" [F, 10-Q].

## 3. Cash
| TTM to Q3 2026 ($M) | Value | Label |
|---|---|---|
| Operating cash flow | 179,551 | [F, PR-Q3 TTM table] |
| Capex (purchases of property and equipment) | 159,804 | [F] |
| **Free cash flow** (OCF − capex) | **19,747** | [C]; matches the company's non-GAAP TTM FCF [F] |
| Quarterly FCF, Q4'25 / Q1 / Q2 / Q3 | 24,551 / 10,116 / **(5,855)** / **(9,065)** | [F] |
| Net income TTM (Q4'25 34,455 + 9M'26 201,239) | 235,694 (to common: 235,310) | [C from F] |
| Of which: pre-tax gains on equity securities TTM (Q4'25 2,302 + 9M'26 127,282) | 129,584 | [C from F] |
| Operating income TTM | 156,976 | [C] |
| Cash, cash equivalents & marketable securities (2026-09-30) | 265,098 (includes $90.4B marketable equity, of which $75.2B is SpaceX shares "subject to short-term restrictions on the ability to sell") | [F] |
| Non-marketable securities | 135,230 (carrying value of $128.2B under the measurement alternative, "primarily … our investment in one private company") | [F] |
| Long-term debt (2026-09-30) | 125,102 + 1,016 current = 126,118 (vs 46,547 at 2025-12-31) | [F]; sum [C] |
| Additional debt after the quarter | €6B notes closed 2026-11-05 [F, 8-K-1105]. Waymo $5.0B secured term loan, Oct 2026, "not guaranteed by Alphabet" [F, 10-Q] | |
| Buybacks TTM | 5,499 (all in Q4 2025). **Zero in 2026**: "In the three and nine months ended September 30, 2026, there were no repurchases" | [F] |
| Dividends TTM (common + preferred) | 2,536 + 8,167 = 10,703 | [C from F] |
| New equity raised in 2026 | Common stock net $42,870 (June offering $20.5B; Berkshire Hathaway affiliate private placement $10.0B; ATM $12.4B) + mandatory convertible preferred $19,063 | [F, 10-Q] |

**Share-count trend** (balance-sheet shares outstanding, XBRL [F]): 12,629M (2023-06-30) → 12,211M (2024-12-31) → **12,077M (2025-09-30, the low)** → 12,088M (2025-12-31) → 12,116M → 12,230M → **12,294M (2026-09-30)**. That is up 217M shares, or +1.8%, year over year [C]. After years of shrinking, the share count is now rising.
- The 10-Q gives the June 2026 offering price as "$355.1982 per share" (Class A). The 2026-11-10 close of $287.38 is 19% below it [C].
- ATM program: up to $40.0B; "$27.6 billion remained available" at 2026-09-30. Stated purpose: "primarily intended to be used to meet tax obligations associated with employee equity grants." [F]

## 4. Priced-in inputs (our calculations, illustration only)
| Multiple [C] | Value |
|---|---|
| Trailing P/E (market cap / TTM net income $235.7B) | **14.9x** |
| Same, excluding TTM equity-security gains ($129.6B pre-tax, taxed at an *assumed* 21%; our assumption) | ~26.4x |
| Price / TTM FCF ($19.7B) | **178x** |
| Price / TTM operating cash flow ($179.6B) | 19.6x |
| Price / TTM operating income ($157.0B) | 22.4x |

Read P/E with care. The GAAP P/E looks low because TTM net income includes about $130B of mostly unrealized gains on SpaceX and one unnamed private company (10-Q: OI&E YTD "primarily related to net unrealized gains on our nonmarketable equity securities largely from a private company, and SpaceX prior to its initial public offering").

**Reverse-DCF illustration (our calculation; not a valuation).**
Formula: Market cap = Σ_{t=1..10} F·(1+g)^t/(1+r)^t + [F·(1+g)^10·(1+g_T)/(r−g_T)]/(1+r)^10. We solve for g by bisection. Inputs: market cap $3.519T (2026-11-10), F = TTM cash flow, r = 8% or 10%, g_T = 3%, 10 years. Equity value is used as is: no adjustment for net cash, the investment portfolio or the preferred stock.

| Base cash flow F | r = 8% | r = 10% |
|---|---|---|
| TTM FCF $19.7B | **g ≈ 31%/yr** for 10 years (FCF reaches ≈$299B in year 10) | **g ≈ 38%/yr** (year 10 ≈ $476B) |
| TTM operating cash flow $179.6B (shown because FCF is depressed by record capex) | g ≈ 2.4%/yr (year 10 ≈ $227B) | g ≈ 6.9%/yr (year 10 ≈ $349B) |

Script line: "On today's free cash flow, the price assumes that cash flow grows about 31 to 38 percent a year for a decade. On operating cash flow before any investment, it assumes only about 2 to 7 percent. The gap between those two is the AI capex bet." The OCF version treats capex as zero, so it understates what the price requires. It is a bracket, not an estimate.

## 5. Guidance
- **Company outlook in filings (verbatim):** "In 2026, we expect to significantly increase, relative to 2025, our investment in our technical infrastructure, including servers and network equipment and data centers." [F, 10-Q] Alphabet gives no revenue or EPS guidance.
- **Capex range:** "Alphabet maintained its 2026 CapEx guidance of $195 billion to $205 billion" [Fetched secondary page MB, 2026-10-29, in the article's own words, not a company quote]. The page paraphrases that management "expects capital expenditures to increase significantly in 2027" and that more TPU system revenue is expected in 2027 [MB, paraphrase]. **This must be verified against the official transcript or webcast before it airs.** 9M 2026 capex was $132.0B [F], so the guide implies Q4 capex of about $63–73B [C].
- **Analyst consensus:** none for Q4 2026 or FY2027 was visible on a page we opened. One search snippet: "Zacks reports EPS of $2.12 against a $2.94 consensus" for Q3 [S, Zacks via search]. That miss is driven by the $8.7B equity-security loss (PR-Q3: it lowered EPS by $0.55). Don't use it on screen as a clean miss. MB: "Alphabet currently has a Moderate Buy rating among analysts" [MB]; we will not use it. **Consensus is otherwise not available.**

## 6. What has to happen (tied to filing numbers)
1. **The Cloud backlog turns into revenue at today's margins.** Backlog was **$567.7B**, of which **$560.8B is Google Cloud**. The company expects "to recognize just over 55% of the revenue backlog as revenues over the next 24 months" [F, 10-Q], or about $312B over two years [C], against TTM Cloud revenue of $93.2B. Cloud margin needs to hold in the mid-30s (36.2% in Q3 [C]) while TPU *hardware* sales, which carry inventory costs, grow.
2. **Capex has to start paying back in FCF.** TTM capex of $159.8B consumed 89% of OCF [C]. FCF has been negative two quarters running (Q2 −$5.9B, Q3 −$9.1B) [F]. Depreciation is rising: 9M $22.0B vs $15.1B [F]. The price (section 4) assumes FCF rises roughly 15–24x over 10 years [C].
3. **Search holds up through AI and the remedies.** Search & other is $250B TTM, about 53% of revenue [C]. It grew 12% in Q3 on paid clicks +8% [F]. The DOJ search judgment requires sharing data and syndication with rivals (section 7).
4. **The equity funding gap closes.** 2026 needed $42.9B of new common, $19.1B of preferred and $85.2B of gross debt (9M) [F]. To stop dilution, OCF growth has to catch up with capex. The ATM still has $27.6B of capacity [F].

## 7. What could go wrong
- **AI capex and contingent obligations.** 10-Q risk factor: "Our investments ultimately may not be commercially viable or may not result in an adequate return of capital." [F] Also: "We also have a number of large, long-duration commercial agreements … including backstops and financial guarantees … and contingent repurchase obligations for certain hardware and embedded software at prices below original cost. … we may incur additional liabilities, have excess capacity or inventory that we cannot easily redeploy, and not receive payments from our counterparties or customers." [F] Disclosed amounts [F, 10-Q Notes 5 and 10]:
  - total commitments of **$802.1B**, "mostly long-term supply agreements"
  - leases not yet commenced: **$130.5B**
  - energy-related guarantees: up to **$16.2B**
  - TPU repurchase guarantees: up to **$6.6B**
  - Crux AI backstops: up to **$10.0B**
  - a contingent **$20.0B** capital commitment to "a private company … through 2030"
- **Dilution and financing.** New 10-Q risk factor: "… combined with the dilutive impact of current or future equity issuances, could harm our financial condition, depress our stock price or reduce our financial and business flexibility." [F]
- **Antitrust (10-Q Note 10) [F]:**
  - **DOJ Search:** the final judgment (Dec 2025) "imposes restrictions on how Google distributes its services and requires Google to share certain search data with and offer syndication services to certain competitors." Both sides have appealed. No $ amount is disclosed.
  - **DOJ Ad Tech:** in September 2026 the court denied "the DOJ's request for structural divestitures … instead ordering certain behavioral remedies." Google plans to appeal. A Texas state AG trial follows. "We cannot estimate a possible loss."
  - **EC Android:** fine final; "we made a cash payment of $5.2 billion for the fine plus accrued interest" (July 2026).
  - **EC ad tech:** €3.0B fine, $3.5B charge, under appeal.
  - **EU DMA:** €430M (Play) + €460M (Search); "$1.0 billion" charge in Q3 2026, under appeal.
  - **PriceRunner (Stockholm):** "approximately $2.1 billion … in principal damages plus accrued interest", under appeal.
  - Short-term accrued legal and regulatory fines and settlements: **$13.8B** at 2026-09-30.
- **Advertising concentration (10-K):** "We generate a significant portion of our revenues from advertising. Reduced spending by advertisers, a loss of partners, shifts in online advertising … could harm our business." [F] Also: "We believe AI is quickly reshaping the advertising industry … There is no assurance that we will adapt effectively." [F]
- **Investment-gain volatility:** Q3 OI&E was −$8.2B, "net unrealized losses in our marketable equity securities largely from SpaceX" [F]. Reported EPS will keep swinging with the SpaceX share price.
- **Control:** the 10-K says Class B stock held by Larry and Sergey "represented approximately 52.7% of the voting power." [F]

## 8. Upside the price may not include (attributed)
- **Backlog jump:** $242.8B (2025-12-31, 10-K) → $567.7B (2026-09-30) [F]. **Not like-for-like:** "In the first quarter of 2026, we elected to change our reporting of revenue backlog to also include contracts with an original expected term of one year or less." [F]
- **TPU systems as a product line:** TPU sales are a "meaningful contributor" to Cloud growth [F, PR-Q3]. Q3 inventory rose to $13.3B from $2.4B at year end [F], which is consistent with hardware sales. Kurian reportedly said "nearly 100 customers" use TPU systems [MB paraphrase; verify].
- **Gemini and AI usage (company claims):** "the Gemini app has reached one billion users"; first-party model APIs "processing nearly 32 billion tokens per minute, more than four times what we processed a year ago"; "150 million YouTube Music and Premium subscribers … including trials" [F, PR-Q3; company claims].
- **Investment stakes on the balance sheet:** SpaceX shares $75.2B (restricted) [F]; one private company carried at about $128.2B [F]. Together about 5.8% of market cap [C]. These are marks, not cash.
- **Waymo:** a $5.0B standalone, non-recourse loan [F] shows outside lenders funding it. The 10-Q gives no Waymo revenue on its own. Other Bets revenue was $372M in Q3 [F].
- **Pending:** the GFiber divestiture, for $1.5B cash, a $2.0B note and a 49.99% stake, is expected to close late 2026 [F].

## 9. Scorecard: three numbers for Q4 2026
1. **Google Cloud revenue and operating margin.** Q3: $30.7B, +103% YoY, 36.2% margin [F/C]. Also watch the backlog vs $567.7B.
2. **Capex and FCF.** Q4 capex vs the implied $63–73B (from the $195–205B guide; [MB]/[C]). Quarterly FCF has been −$9.1B [F]. Watch the 2027 capex number given on the Q4 call.
3. **Google Search & other growth.** Q3 +12% to $63.35B [F]; paid clicks +8%.
- Also watch: the share count (12,294M) and ATM use.
- **Next earnings date:** **not announced**. Last year's Q4 release was 2026-02-04 (8-K) [F], so we expect early February 2027 (estimate).

## 10. Flags
- **P/E distortion:** the GAAP P/E of 14.9x includes about $129.6B of equity gains. Show the adjusted ~26x only as our illustration with its assumed tax rate, or lead with price/FCF and price/OCF instead.
- **Capex guide source:** the $195–205B is from MarketBeat [Fetched secondary], not a company document we could open (abc.xyz returned 403). Verify against the transcript.
- **Backlog definition change** in Q1 2026 (above). Don't present $243B → $568B as pure growth.
- **The "private company" is not named in the filing.** Don't name it on screen unless a primary source does.
- **Market cap excludes the convertible preferred** (about $19B, about 0.4% dilution at conversion [C]). Class B is valued at the GOOGL price.
- **Contradiction to handle carefully:** a buyback authorization of "$69.5 billion remained available" [F] sits alongside active share *issuance* (ATM, June offering). Both are true. Don't call it a buyback story.
- "Half-trillion run rate", "fastest-growing product", Gemini user counts: company claims, to be attributed.
- Search "miss" headlines (e.g., investinglive) are [S]. Don't use them without a sourced consensus.
- **What not to say:** no "cheap" or "expensive", no fair value, no buy or sell. The reverse DCF shows what the price assumes, not whether that is right. Keep the disclaimer after the hook.
