# Before You Buy: Microsoft (MSFT) research notes, Nov 2026 edition

Compiled 2026-11-11. Data date: close of 2026-11-10. USD only.

**Provenance labels.** *Fetched* means we retrieved a primary source directly (an SEC EDGAR filing or API, a Microsoft IR document, or the Yahoo chart API for prices). *Snippet* means a search-result summary we did not open. *Computed* means our own calculation from labelled inputs.

**Core sources (all Fetched)**
- 10-Q Q1 FY27 (period ended 2026-09-30, filed 2026-10-28): https://www.sec.gov/Archives/edgar/data/789019/000119312526436133/msft-20260930.htm
- Earnings release, 8-K Ex. 99.1 (2026-10-28): https://www.sec.gov/Archives/edgar/data/789019/000119312526436122/msft-ex99_1.htm
- 8-K Item 8.01 (2026-10-28): FY24–FY26 recast to the new segments, Ex. 99.1: https://www.sec.gov/Archives/edgar/data/789019/000119312526436149/msft-ex99_1.htm
- 10-K FY2026 (period ended 2026-06-30, filed 2026-07-29): https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm
- Earnings call transcript FY27 Q1 (Microsoft IR; https://aka.ms/transcriptfy27q1 redirects to https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptQandAFY27Q1.docx) and event page https://www.microsoft.com/en-us/investor/events/fy-2027/earnings-fy-2027-q1
- 8-K debt issuance (underwriting agreement 2026-10-29, filed 2026-11-04): https://www.sec.gov/Archives/edgar/data/789019/000119312526447173/d178557d8k.htm
- 8-K Item 5.02 (2026-11-05), director not standing for re-election: https://www.sec.gov/Archives/edgar/data/789019/000119312526448357/d177209d8k.htm
- Proxy DEF 14A filed 2026-10-21 (annual meeting 2026-12-08 per EDGAR metadata): https://www.sec.gov/Archives/edgar/data/789019/000119312526427849/d61756ddef14a.htm. **Not read in full**; no proxy figures are used.
- EDGAR XBRL company facts: https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json
- Price: Yahoo Finance chart API, https://query1.finance.yahoo.com/v8/finance/chart/MSFT

---

## 1. Edition stamp

| Item | Value | Label |
|---|---|---|
| Latest reported quarter | Q1 FY2027, ended **2026-09-30** (8-K and 10-Q both 2026-10-28) | Fetched |
| Close 2026-11-10 | **$533.16** | Fetched (Yahoo chart API) |
| Shares outstanding | **7,426,194,552** as of 2026-10-22 (10-Q cover) | Fetched |
| Market cap | 7,426,194,552 × $533.16 = **$3,959.3B (≈$3.96T)** | Computed |

On-screen stamp: **DATA AS OF 2026-11-10 CLOSE · LATEST REPORT: Q1 FY27 (Sep 30, 2026)**

**Segment change:** starting in FY27, Microsoft reports two segments, **Agents and Infra** and **Devices and Consumer**. They replace the old three-segment structure. FY24–FY26 were recast in the 2026-10-28 8-K: "The updates do not represent a restatement".

---

## 2. The business today

### Segments, last 3 fiscal years, recast ($M) (8-K Ex. 99.1, Fetched; margins Computed)
| | FY2024 | FY2025 | FY2026 | FY26 growth | FY26 op. margin |
|---|---|---|---|---|---|
| Agents and Infra revenue | 186,910 | 218,783 | **268,127** | +23% | |
| Agents and Infra op. income | 94,462 | 110,814 | 136,365 | +23% | 50.9% |
| Devices and Consumer revenue | 58,212 | 62,941 | 63,712 | +1% | |
| Devices and Consumer op. income | 14,971 | 17,714 | 18,872 | +7% | 29.6% |
| **Total revenue** | **245,122** | **281,724** | **331,839** | **+18%** | |
| **Total op. income** | 109,433 | 128,528 | 155,237 | +21% | 46.8% |
| Net income | 88,136 | 101,832 | 133,749 | +31% | |

### Revenue by product line, recast ($M) (8-K Ex. 99.1; Q1 data from the 10-Q, Fetched)
| Product line | FY2024 | FY2025 | FY2026 | Q1 FY26 | Q1 FY27 | Q1 y/y |
|---|---|---|---|---|---|---|
| Azure | 54,070 | 72,610 | **101,938** | 22,384 | **33,165** | +48% |
| Microsoft 365 cloud | 73,457 | 84,605 | 100,299 | 23,694 | 27,778 | +17% |
| Productivity & server licensing | 34,976 | 35,391 | 37,285 | 8,678 | 8,407 | −3% |
| Search & advertising | 19,679 | 22,171 | 24,835 | 5,942 | 6,554 | +10% |
| XBOX | 21,503 | 23,455 | 21,790 | 5,508 | 5,379 | −2% |
| Industry solutions | 16,813 | 18,417 | 20,345 | 4,894 | 5,337 | +9% |
| Windows OEM & devices | 17,030 | 17,315 | 17,087 | 4,551 | 3,551 | **−22%** |
| Frontier & support services | 7,594 | 7,760 | 8,260 | 2,022 | 2,108 | +4% |
| **Total** | 245,122 | 281,724 | 331,839 | 77,673 | 92,279 | +19% |

Azure is now disclosed in dollars. It was **35.9% of Q1 FY27 revenue** (Computed). The "Microsoft Cloud" metric (Azure + M365 commercial cloud + Industry solutions cloud) was $63.9B in Q1, +30%. The FY26 recast figure was $214.4B (+27%).

### Last 4 quarters, totals ($M) (XBRL and 10-Q, Fetched; Q4 FY26 = FY − 9M, Computed)
| | Q2 FY26 (Dec-25) | Q3 FY26 (Mar-26) | Q4 FY26 (Jun-26) | Q1 FY27 (Sep-26) |
|---|---|---|---|---|
| Revenue | 81,273 | 82,886 | 90,007 | **92,279** |
| Operating income | 38,275 | 38,398 | 40,603 | **45,915** |
| Net income | 38,458 | 31,778 | 35,766 | **36,629** |

Recast quarterly segment data for Q2–Q4 FY26 is **not published**. Only Q1 FY26 comparatives were recast in the 10-Q.

### Q1 FY27 segments (10-Q, Fetched; margins Computed)
- Agents and Infra: revenue $76,795M (+25%), op. income $40,558M (+24%), **margin 52.8%**.
- Devices and Consumer: revenue $15,484M (−3%), op. income $5,357M (+2%), margin 34.6%.
- Company operating margin 49.8%. Microsoft Cloud gross margin fell to **66%** "driven by sales mix shift to Azure."

### Geography (10-Q / recast, Fetched; shares Computed)
- Q1 FY27: U.S. $49,459M (53.6%), other countries $42,820M (46.4%).
- FY26: U.S. $170,794M, other countries $161,045M.

### Customer concentration: OpenAI (Fetched)
- 10-Q: "For the three months ended September 30, 2026, we recorded revenue from commercial arrangements with OpenAI, inclusive of revenue-sharing payments, of $10.0 billion." That is **10.8% of Q1 revenue** (Computed). On the call, Gabriela Borges (Goldman Sachs) put it as "you have OpenAI at 11% of revenue in the quarter" (transcript). This is an analyst's framing; management did not dispute it.
- FY26: $24.1B, or 7.3% of FY26 revenue (Computed). The recast 10-K says: "No sales to an individual customer or country other than the United States accounted for more than 10% of revenue for fiscal years 2026, 2025, or 2024."
- Microsoft holds "an approximate 24% interest on an as-converted basis" (equity method). Receivables from OpenAI were $7.2B. Funding commitments total $13.0B, of which $12.0B is funded.

---

## 3. Cash

TTM = Q2 FY26 through Q1 FY27 (Computed from XBRL and 10-Q figures, Fetched).

| Item | TTM | Quarterly Q2 FY26 / Q3 / Q4 / Q1 FY27 | Label |
|---|---|---|---|
| Operating cash flow | **$195,878M** | 35,758 / 46,679 / 55,441 / 58,000 | Computed |
| Capex (cash additions to P&E) | **$135,921M** (39% of revenue) | 29,876 / 30,876 / 35,802 / 39,367 | Computed |
| **Free cash flow** (OCF − cash capex) | **$59,957M** | 5,882 / 15,803 / 19,639 / 18,633 | Computed |
| Net income (GAAP) | **$142,631M** | | Computed |
| Net income excluding OpenAI gains/losses | ≈$134.3B (TTM OpenAI net-income impact ≈ +$8.3B: FY26 +$5.0B, Q1 FY26 −$3.086B reversed, Q1 FY27 +$0.207B) | | Computed (FY26 figure rounded) |
| Buybacks (cash) | $21,000M | | Computed |
| Dividends paid | $27,033M | | Computed |
| Capital returned | $48.0B = **80% of FCF** | | Computed |
| Revenue TTM | $346,445M | | Computed |

- CFO cross-check (transcript): "Cash flow from operations was $58 billion, up 29% ... free cash flow was $18.6 billion reflecting higher capital expenditures." Q1 FY26 FCF was $25.7B, so FCF fell about 27% y/y (Computed).
- Capex definitions differ. The CFO: "Capital expenditures were $45.2 billion ... This quarter, finance leases were $7.4 billion ... cash paid for P, P, and E was $39.4 billion." Our FCF uses the **cash** figure, which matches the company's $18.6B.
- Also in investing, "Other, net" was −$12.9B in Q1, "primarily to facilitate the purchase of components" (10-Q). It is **not** in our capex and not in our FCF.

**Balance sheet, 2026-09-30 (10-Q, Fetched):**
- Cash + short-term investments $64.5B.
- Debt $4.39B current + $31.09B long-term = **$35.5B**.
- Finance lease liabilities **$71.0B**.
- After the quarter: **$25.0B** of new notes, ten tranches maturing 2028–2066 (8-K, Fetched; sum Computed). CFO: "we will access additional sources of funding when we believe it is attractive to do so."

**Off-balance-sheet commitments (FY26 10-K, Fetched):**
- "additional leases, primarily for datacenters, that had not yet commenced of $329.1 billion", commencing FY27–FY33.
- Purchase commitments of $194.1B.
- Total contractual obligations of $743.8B.

**Share-count trend** (cover pages, Fetched): 7,429.8M (Jul-2023) → 7,432.4M (Oct-2025) → **7,426.2M (Oct-2026)**, about flat (−0.08% y/y, Computed). Buybacks roughly offset stock compensation. $37.7B remains under the $60B program. Quarterly dividend is $0.98 (up from $0.91).

---

## 4. What's priced in (our calculations, illustration only)

| Ratio | Value | Inputs |
|---|---|---|
| Trailing P/E (GAAP) | **27.8×** | $3,959.3B ÷ $142.6B (Computed) |
| Trailing P/E excluding OpenAI gains | ≈29.5× | ÷ ≈$134.3B (Computed) |
| Price / FCF | **66.0×** | $3,959.3B ÷ $59.96B (Computed) |
| FCF yield | 1.5% | Computed |

### Reverse DCF (ILLUSTRATION, our calculation; it is not a valuation)
Market cap = Σₜ₌₁¹⁰ FCF₀·(1+g)ᵗ/(1+r)ᵗ + [FCF₀·(1+g)¹⁰·(1+g_T)/(r−g_T)]/(1+r)¹⁰

Solved for g. Inputs: market cap $3,959.3B (equity value; net debt and leases ignored), FCF₀ = $59.957B TTM, g_T = 3%, 10 years.

| Discount rate r | Implied annual FCF growth, yrs 1–10 | FCF in year 10 | Share of value from terminal | Value at zero growth |
|---|---|---|---|---|
| 8% | **≈17.9% per year** | ≈$310B | 75% | ≈$0.97T |
| 10% | **≈23.3% per year** | ≈$489B | 70% | ≈$0.71T |

Sensitivity: using FY26 FCF ($66.99B = $182.9B − $115.9B), the implied growth is ≈16.4% at 8% and ≈21.8% at 10% (Computed).

**Context for the script:** TTM FCF is compressed by record capex. Capex was 39% of TTM revenue, while OCF was $195.9B. The implied rate is really a bet on **FCF recovering as capex-to-revenue falls** as well as on revenue growth. The company guides revenue +18–19% for Q2 and calls the capex plan "approximately $170 billion" for calendar 2026.

Script line: "At an 8% discount rate, today's price works out to free cash flow growing about 18% a year for a decade. At 10%, it is about 23%. Our calculation, using the assumptions on screen."

---

## 5. Guidance (Q2 FY27, verbatim from the CFO's prepared remarks, transcript, Fetched)

The release itself says: "Microsoft will provide forward-looking guidance in connection with this quarterly earnings announcement on its earnings conference call and webcast."

- "We expect revenue from Agents and Infra of $80.1 to $80.7 billion, or growth of 24 to 25%."
- "In Azure, we expect revenue growth of 49 to 50% in constant currency ... Customer demand continues to exceed available supply."
- "In M365 Commercial cloud, we expect growth of approximately 19% in constant currency"
- "Microsoft Cloud gross margin percentage should be roughly 65%"
- "In devices and consumer, we expect revenue to be $15.9 to $16.4 billion." Also: "Windows OEM and Devices revenue should decline in the mid-thirties."
- "Therefore, at the total company level, revenue should be between $96 and $97.1 billion or growth of 18 to 19%."
- "We expect COGS of $32.7 to $32.9 billion, or growth of 26 to 27%. And operating expense of $18.5 to $18.6 billion or growth of 9% ... Operating margins should be down slightly year-over-year."
- "we expect our Q2 effective tax rate to be approximately 20%."
- Capex: "In Q2, we expect CapEx spend will be over $50 billion. Therefore, for the calendar year, spend should be approximately $170 billion due to the 3P capacity delays noted earlier. In the second half of the fiscal year, we currently expect CapEx spend to accelerate".
- FY27: "we expect to continue to remain free cash flow positive in FY27." No numeric full-year revenue or margin guide was given.
- Bookings: "Commercial bookings decreased 12% and 11% in constant currency driven by the impact from large Azure commitments in the prior year". Q2 bookings "will be impacted by the significant Azure commitments signed in the prior year."

**Analyst consensus: not available** from any fetched page. A search snippet cited a "Street's 45.1%" Azure forecast without attribution. **Do not use it.**

---

## 6. What has to happen (tied to filed numbers)

1. **Azure keeps growing near 50% while capacity lands.** Q1 was +48% ($33.2B) and the guide is 49–50% cc. The CFO says "demand that exceeds supply" and that 3P GPU contracts were "delayed to H2."
2. **RPO converts to revenue.** Commercial RPO is **$677B** (+73%). "roughly 30% will be recognized in revenue in the next 12 months", about $203B (Computed). The rest, beyond 12 months, "increased 98%" (CFO).
3. **Capex intensity peaks and FCF recovers.** TTM capex is $135.9B against FCF of $60.0B. CY2026 capex is ~$170B, plus $329.1B of datacenter leases not yet commenced. The CFO: "each dollar of capex has the potential to support more revenue and higher returns over time."
4. **Copilot / M365 ARPU offsets the Windows/PC drag.** M365 commercial cloud is +17% reported, with a ~19% cc guide and "we continue to expect revenue growth to accelerate through the year". That has to outrun Windows OEM & devices at −22% (guide: mid-thirties decline).

---

## 7. What could go wrong (10-Q risk factors and notes, Fetched)

- **AI capex risk:** "These investments are being made at significant scale and on an accelerated timeline, require substantial and increasing capital expenditures and continued access to capital, and are in advance of fully developed revenue streams. The associated revenue may not be realized in the expected timeframes or at expected levels." Also: "Overestimation of demand or misalignment of capacity investments may result in underutilization of infrastructure and may lead to impairment of assets".
- **OpenAI and partner concentration:** "In some cases, these parties are significant customers of Azure and other cloud services. The economic benefits we expect to derive from these relationships, including through commercial arrangements, technology access, and Azure consumption, may not be realized or sustained." OpenAI revenue was $10.0B in Q1 (10.8%), with $7.2B receivable and a ~24% equity stake. Partnership risk: "If an arrangement fails to adequately anticipate changing circumstances and interests of a party, it may result in early termination or renegotiation".
- **AI unit economics:** "if pricing for AI products and services declines as a result of competition, commoditization, or other market forces, our margins ... could be adversely affected." Microsoft Cloud gross margin was 69% in FY25, then 66% in FY26 and Q1, with ~65% guided.
- **IRS:** "the IRS is seeking an additional tax payment of $28.9 billion plus penalties and interest" for 2004–2013 (Microsoft disputes it). Unrecognized tax benefits are $30.6B.
- **Legal accruals:** "we accrued aggregate legal liabilities of $582 million ... adverse outcomes that we estimate could reach approximately $400 million in aggregate beyond recorded amounts are reasonably possible." LinkedIn GDPR fine: under appeal; **the amount is not stated in the filing**.
- **Competition and regulation:** "Government agencies closely scrutinize us under U.S. and foreign competition laws ... including markets such as the EU, the United Kingdom, the U.S., and China." AI regulation: "the EU's AI Act may increase costs". Trade: "The volatility of U.S. tariffs has triggered economic uncertainty and could impact cloud and devices supply chain cost competitiveness." AI export rules: "The potential replacement of the rescinded AI Diffusion Rule ... could adversely affect Microsoft's business".
- **PC/Windows:** "Inventory levels remain elevated" (CFO); "the range of potential outcomes remains wider than normal."
- **Execution:** CFO cited "weaker sales execution in our M365 E3 and standalone SKUs". Industry solutions "bookings trends continued to moderate."

---

## 8. Upside the price may not include (company-attributed claims)

- **Foundry:** "Foundry revenue more than tripled year-over-year" (CFO). "revenue from open source models on Foundry increased 10X" (CEO).
- **Copilot:** CEO: "Daily users are up nearly 50 percent quarter over quarter, and over 5X year over year" and "The number of customers with more than 50,000 Copilot seats increased over 8X year over year". He says Volkswagen "announced plans to deploy Copilot to more than 330,000 employees". The CFO says E7 "has already reached millions of paid seats". Copilot revenue is **not disclosed in dollars**.
- **Efficiency upside:** CFO: "engineering work enabled us to identify and monetize underutilized capacity", plus "higher revenue per token" in Q1. These are levers that could lift Azure without new capex. The CFO calls their timing unpredictable.
- **First-party models (MAI):** CEO: "MAI Code Flash had 3 million users in GitHub Copilot last month alone". Microsoft also "hold[s] rights to OpenAI's intellectual property, including models and infrastructure" (10-Q).
- **OpenAI equity:** a ~24% as-converted stake carried under the equity method (HLBV). Its market value is **not disclosed**. Do not size it.

---

## 9. Scorecard: three numbers to watch next quarter

1. **Azure growth vs the 49–50% cc guide** (Q1: +48%, $33.2B).
2. **Capex and FCF:** capex "over $50 billion" in Q2 vs Q1's $45.2B (incl. leases) or $39.4B cash. The test is whether FCF stays near Q1's $18.6B.
3. **Commercial RPO ($677B) and the OpenAI share of revenue ($10.0B, 10.8%)**: does the backlog broaden beyond one customer?

**Next earnings:** Q2 FY27, **not announced**. Estimate is late January 2027, based on last year's Q2 earnings 8-K of 2026-01-28 (Fetched date; the 2027 date is an estimate).

---

## 10. Flags

- **OpenAI 10% issue:** the annual 10-K disclosure says no customer exceeded 10% of revenue in FY24–FY26. In Q1 FY27, OpenAI was 10.8% of quarterly revenue. This is not a contradiction (one is annual, the other quarterly), but say "about 11% of revenue last quarter", not "Microsoft's biggest customer is over 10%" as a fiscal-year fact.
- **Capex has three numbers:** $45.2B (CFO, includes $7.4B finance leases), $39.4B (cash, used for our FCF), plus −$12.9B "Other, net" for components. Always say which one.
- **GAAP EPS is distorted by OpenAI:** Q1 net income +32% GAAP vs +18% excluding OpenAI. Use the non-GAAP growth only with the label.
- **Segment recast:** do not compare the new "Agents and Infra" with old "Intelligent Cloud" figures from earlier episodes or sites.
- **Bookings −12%** sits alongside RPO +73%. Both are true, because of lumpy large Azure commitments. Do not cherry-pick one.
- Reverse DCF is an **illustration**. It uses capex-depressed FCF and ignores $71B of finance leases and $329B of uncommenced leases. Say "our calculation, assumptions on screen".
- Third-party claims (e.g. "~$170B calendar-year capex" from secondary outlets) were checked against the transcript; use the transcript wording.
- Board: director Emma Walmsley is not standing for re-election (8-K 2026-11-05). This is not material to the thesis.
- **What not to say:** no "fair value", "cheap/expensive", "buy/sell", or targets. Say "the price assumes ...", never "Microsoft will ...".

---

## Addendum 2026-11-11: depreciation, for the capex-boom gauge base (series method rule)
- XBRL `us-gaap:Depreciation` (depreciation expense on property and equipment, notes to the 10-Q/10-K), Fetched from
  https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json: Q2 FY26 $7.9B; Q3 FY26 $9.0B; FY26 $34.3B (so Q4 FY26
  $10.3B, Computed); Q1 FY27 $11.1B. **TTM depreciation ≈ $38.3B** (Computed).
- Proxy base (labelled proxy): OCF − depreciation = 195.9 − 38.3 = **$157.6B** (yield 4.0% on $3,959.3B; Computed).
  Reverse calculation on this base (same model): **≈ 5.5% a year (8%) / ≈ 10.2% (10%)**; zero-growth value ≈ $2.56T / $1.86T.
  This proxy assumes capex falls back to roughly the depreciation level; FCF-based result (≈ 17.9% / 23.3%) is the other end.
- "What the capex must earn" (our rough illustration): if capex stays at the TTM cash pace ($135.9B a year), the year-10
  FCF the price implies (≈ $310B at 8%, ≈ $489B at 10%) needs operating cash of FCF + capex; the extra over today's OCF
  ($195.9B), spread over ten years of capex ($1,359B), is **≈ 18 cents (8%) to ≈ 32 cents (10%) of yearly operating cash per
  dollar of capex** (Computed).
