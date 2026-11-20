# Research notes: Anthropic's $1.5 Trillion IPO: The AI Gold Rush or the Next Bubble? (Ep 72)

Read on 2026-11-20 (the day after the first trading day). Primary documents first, downloaded from SEC EDGAR with a generic client name:
Anthropic's final prospectus (Form 424B4, filed 2026-11-19, File No. 333-299633, CIK 0002130357), the pricing free writing prospectus
(FWP, dated 2026-11-18), the EDGAR filing index (DRS 2026-06-01; S-1 2026-10-26; S-1/A 2026-11-02, -10, -17; effective 2026-11-18),
Amazon's Q3 2026 Form 10-Q (filed 2026-10-30) and Alphabet's Q3 2026 Form 10-Q (filed 2026-10-29). Market data from named press reports.
Claims and URLs: `projects/anthropics-1-5-trillion-ipo/sources.yaml`.

**Neutrality.** Anthropic makes the AI model used to produce this episode. Nothing here comes from inside knowledge: every statement about the
company is taken from its public filings or from named press reports, quoted or attributed. See `EDITORIAL_QC.md` for the neutrality check.

## 1. The deal (verified on the FWP and the 424B4)
- Price **$83.00** per Class A share (range $70-$78; CNBC, Nov 16 and Nov 18). Pricing Nov 18; trading Nov 19; settlement Nov 20, 2026.
  Nasdaq Global Select Market, ticker **ANT**. Lead bookrunners Goldman Sachs and Morgan Stanley.
- Size **$81,340,000,000** = 980,000,000 shares × $83 (upsized from 825 million, CNBC).
- **Primary vs secondary (verified):** 956,351,354 shares sold by the company (97.6%) and 23,648,646 by the selling stockholders (2.4%),
  the seven co-founders, 3,378,378 shares each (our division; CNBC: "each co-founder sold 3.38 million shares"; ≈$280m gross each, our calc).
  Underwriters' option: up to 147,000,000 more shares, 100% primary (not exercised as of the prospectus; CNBC: deadline Nov 20).
- **Concurrent private placement:** $26.0bn of non-voting Class N stock (313,253,007 shares) at $83, bought by Google ($10.0bn), NVIDIA
  ($10.0bn), AMD ($2.5bn), Broadcom, Micron, Microsoft ($1.0bn each) and TSMC ($0.5bn). Not part of the public offering; restricted
  securities, not under the lock-up. IPO + placement = **$107.3bn** (The National: the largest on record, above SpaceX's $86bn in June).
- Net proceeds to the company ≈ **$104.8bn** (IPO primary + placement, after fees; $117.0bn if the option is exercised).
- Lock-up: up to **180 days**; up to **365 days** for co-founders and holders of >0.5% of fully diluted shares; up to 10% of the lock-up
  securities of non-founder directors, officers, employees and consultants may be sold from the first trading day; ≈3.7bn shares under the
  180-day lock-up may become eligible early.
- Voting: one Class F share held by the co-founders' Founder LLC carries **50.1%** of all votes; Class N has no vote.

## 2. The first day (press; exchange data not reachable programmatically)
- Open **$111.50** (CNBC, Forbes, TechRepublic; first trade around 11:48 a.m. ET), intraday high **$115.10** (Forbes), close **$97.17**, up
  ≈17% (CNBC, Forbes, The National). Volume > 846 million shares (CNBC). This is the **latest close available on 2026-11-20** (the Nov 20
  session had not closed when the film was locked); the film says "the first close" and labels the date.

## 3. Why the valuations differ (our reconciliation)
Same company, different share counts and different prices:

| Basis | Shares | At $83 | At $97.17 (Nov 19 close) | Reported |
|---|---|---|---|---|
| Outstanding after the offering and placement (424B4) | 13,219,642,276 | ≈ $1.10tn | ≈ $1.28tn | ≈ $1.27tn "on shares outstanding" (The National; the brief also cites Forbes, whose page blocked automated reading) |
| Fully diluted (adds 1.77bn options, 1.03bn unvested RSUs, full conversion of the Amazon Notes beyond the cap ≈1.55bn, the option shares; our build-up from the 424B4 ≈ 17.6-17.8bn) | ≈ 18.0bn implied by the press figures | ≈ $1.5tn (CNBC) | ≈ $1.75-1.8tn (The National ≈$1.75tn; CNBC "roughly $1.8 trillion"; ≈$1.76-1.77tn attributed to CNN / Reuters in the brief: NOT verified here (pages not readable)) | |
| At the open ($111.50), fully diluted | | | "nearly $2.01 trillion" (CNBC) | |

- The press "fully diluted" counts imply ≈18.0bn shares ($1.5tn ÷ $83 ≈ $1.75tn ÷ $97.17 ≈ 18.0bn); our own build-up from the prospectus
  gives 17.6-17.8bn (≈ $1.46-1.48tn at $83; ≈ $1.71-1.73tn at $97.17). The remaining gap is plan reserves, post-Sep-30 grants and
  rounding; the film says "about one and a half trillion" and shows the bases on screen (p05).
- The 846,840,960 Class N shares of the Initial Public Benefit Issuance are legally outstanding but not outstanding for accounting; excluding
  them, outstanding × $97.17 ≈ $1.20tn. The ≈$1.27tn press figure sits between the two; the film shows "≈ $1.27T today's shares" attributed.
- **Proceeds ≠ market value:** $81.3bn is what the shares sold for; $1.5tn is the price of all shares (fully diluted).
- **Equity value ≠ enterprise value:** Anthropic held ≈$132bn of cash and short-term investments on Sep 30 (before ≈$104.8bn of net
  proceeds) and $6.2bn of debt; its enterprise value is therefore materially lower than its equity value. The film's multiple is labelled
  "equity value ÷ run rate".
- **CNN live page** (cnn.com/2026/11/19/business/live-news/anthropic-ipo) returned HTTP 451 to automated reading and no Reuters story on the
  close could be opened; the $1.76-1.77tn figures are therefore not used on screen. The film uses ≈$1.75tn (The National) and the CNBC range.

## 4. The business (424B4)
- Founded January 2021; co-founders include Dario Amodei (CEO; previously VP of Research at OpenAI, earlier Google Brain) and Daniela Amodei
  (President, Chair) plus five others; public benefit corporation; Claude launched publicly in Q1 2023; Claude Code is the coding agent.
- Revenue: 2023 **$41m**; 2024 $386m; 2025 **$4,585m**; nine months 2025 $2,545m; nine months 2026 **$33,242m** (Q3 2026 $17.0bn).
- **Run-Rate Revenue ≈ $81bn** at Oct 31, 2026 (up $10bn from Sep 30). Run rate is a snapshot of the current pace annualized, not revenue
  earned. Consumption-based 79% and subscriptions 21% of nine-month 2026 revenue.
- Cloud marketplaces (CSPs) 47% of 2025 revenue, 44% of nine-month 2026 revenue; recognized **gross** ("the Company is the principal"),
  partner fees as an expense. Customers with ≥$100k TTM revenue: >11,900 (from >950 a year earlier).
- Operating loss: 2025 $(8,060)m; nine months 2026 **$(1,260)m**; Q3 2026 $(567)m (incl. $5.0bn of short-term compute and $2.0bn of non-cash
  donation-matching charges). Adjusted Operating Income (non-GAAP) $4.1bn in nine months 2026 (not used in narration).
- Net loss: 2023 $(1,531)m; 2024 $(8,309)m; 2025 $(41,965)m; nine months 2026 **$(104,039)m**, of which **$(94,324)m** is the change in fair
  value of convertible notes, derivative liabilities and SAFEs (non-cash, driven by the rising valuation).
- Operating cash flow nine months 2026 **+$6,569m** (nine months 2025 −$2,024m). Capex $925m plus $1,955m prepayments for leased assets.
  "Free cash flow" is not a company-defined figure here; the film says only that cash flow "turned positive" (operating cash flow).
- Cash $95.6bn + short-term investments $36.3bn (Sep 30, 2026); total indebtedness $6.2bn (the Amazon Notes, expected to settle in shares).
- Compute and infrastructure expense: 2025 **$7,326m** (≈$1.60 per $1 of revenue, our calc); nine months 2026 **$18,808m** (≈$0.57, our calc).

## 5. The cost of building intelligence: commitments (424B4)
- Purchase commitments and leases, incl. short-term and not-yet-commenced leases, as of and after Sep 30, 2026: **≈$900.9bn** aggregate;
  ≈$451.6bn before end-2030; the rest mostly 2031-2045; ≈$70.7bn due in the 12 months after Sep 30, 2026. (CNBC headlines quote $895.4bn
  from an earlier amendment; the final prospectus says ≈$900.9bn; the CEO was quoted on "$900 billion in AI commitments".)
- Named arrangements: Microsoft ≥$47.2bn (Nov 2026-Jun 2033) "regardless of actual usage"; Google CSP hosting ≥≈$121.3bn (Apr 2026-Jul 2033),
  true-up if spend falls short, plus an estimated $125-150bn of further TPU compute (not in the table); **Amazon ≥$110.0bn (May 2026-Apr
  2036)**, true-up if spend falls short; SpaceXAI up to $120.5bn into 2029 (≈$3.1bn a month at full delivery, cancellable on 90 days' notice
  after initial periods); AMD Helios systems, expected >$20bn; Nscale up to ≈$44.6bn; Lambda ≈$41.3bn; a Broadcom accelerator lease with up
  to $42.0bn of convertible notes available to finance it.
- Commitment ≠ spending ≠ debt ≠ expense: commitments are promises to buy later; spending is cash out; debt is borrowed money ($6.2bn);
  expense is recognized as the service is used.

## 6. The relationships (424B4; Amazon and Alphabet 10-Qs)
- **Amazon (10-Q):** $8.0bn of convertible notes (Q3 2023-Q4 2025) + $10.0bn of non-voting preferred in nine months 2026 (incl. $5.0bn of
  Series G in Q2) = **≈$18bn invested (our sum)**. Sep 30, 2026 carrying amounts: preferred ≈$92.5bn + notes ≈$146.2bn = **≈$238.7bn (our
  sum, before the IPO)**. Upward adjustments of $62.8bn recorded in other income in nine months 2026; $15.2bn of related discrete tax
  expense. AWS: "expansion of the strategic collaboration and existing multi-year commitment by more than $100.0 billion over 10.0 years". A
  new financing facility of up to $20.0bn. Ownership after the offering: 1,936,452,353 Class N shares = **14.6%** of outstanding capital stock
  (23.6% if the notes were fully converted without the cap). CNBC: Amazon and Google stakes each valued at over $100bn.
- **Google (424B4):** Series H $10.0bn (May 2026), earlier notes converted in 2025, a 2026 NPA of up to $30.0bn ($20.0bn left), $10.0bn in the
  private placement; ownership 1,774,959,745 Class N = **13.4%**. **Alphabet's 10-Q does not name Anthropic** (non-marketable equity
  securities carried at $128.2bn in total); Google figures in the film come from Anthropic's prospectus.
- Risk factor (verbatim): reliance on a limited number of CSPs and suppliers, "some of which have strategic and investment relationships with
  us and are our customers, creates complex dynamics that could give rise to conflicts of interest and adversely affect our access to compute."

## 7. The criticism (presented in full, attributed)
- Reuters (Sep 30, 2026, on the confidential filing): an "increasingly circular" relationship: Amazon and Google invested tens of billions
  while Anthropic committed to buy enormous computing capacity from them; deep dependence on Big Tech partners.
- Axios (Oct 8, 2026) and others: OpenAI's revenue chief reportedly argued that Anthropic's gross counting of cloud-partner sales overstates
  its run rate; both companies say they follow standard accounting. (Axios blocked automated reading; summary from search excerpts. The
  gross-basis policy itself is primary, 424B4.) The film says "a rival has argued" and shows "REPORTED" on screen.
- Tech Policy Press (opinion): the SEC should block the IPO; ordinary investors could be "left holding the bag". Shown as OPINION.
- The other side (from the filings): the cash is real (operating cash flow +$6.6bn), most revenue does not come through cloud marketplaces
  (56% in nine months 2026), >11,900 large customers, gross recognition is a GAAP principal/agent judgment, and every arrangement is
  disclosed. Vendor financing (e.g. carmakers' finance arms lending to car buyers) is an established practice. **No accusation of wrongdoing is
  made or implied.**

## 8. Who got rich (paper vs realized)
- Series A preferred original issue price **$2.57** (post 10-for-1 split of Sep 17, 2026); each preferred converts into about ten common
  shares, so **≈$0.26 per common share (our calc)**; $97.17 ÷ $0.26 ≈ **378×** on paper (hypothetical investor; before fees, taxes, any
  dilution adjustments). Total Series A ≈ $125m (carrying value). Later rounds: Series G $259.14 and Series H $589.01 per preferred
  (≈$25.91 and ≈$58.90 per common, our calc).
- Employees: 1,774,342,693 options at a weighted-average exercise price of $2.91; 1.03bn unvested RSUs. CNBC (reported): "over 400 employees
  expected to be worth $100 million or more", average employee "over $40 million". Paper wealth; locked up (see §1).
- Co-founders sold ≈23.6m shares in total (≈$1.96bn gross); co-founders have each pledged 80% of personal equity to philanthropy (424B4).
- **Dilution sources** (424B4): options and RSUs; Amazon Notes converting each quarter up to the cap; up to $77.0bn of further convertible
  notes under partner NPAs; Public Benefit Issuances (up to 2% more shares to the Anthropic Public Benefit Fund each time the price rises 50%
  above the prior milestone, starting from the IPO price).

## 9. Is it worth it (our calculations, labelled)
- Value ÷ sales pace: ≈$1.75tn ÷ ≈$81bn ≈ **21.6×** run rate (≈18.5× at $1.5tn). Equity value, not EV.
- What the price assumes (HYPOTHETICAL): at 25 times earnings, ≈$1.75tn needs ≈ **$70bn a year** of net profit; today the company reports
  an operating loss. Not a forecast; no probabilities on the bull / base / bear roads.

## Not used (and why)
- Probabilities for scenarios, price targets, buy/sell views (not investment advice).
- Nov 20 trading (not closed when locked). Analyst forecasts of 2027 revenue (not verifiable on primary pages).
- The "MisAnthropic Statement" and lobbying debates (CNBC) and the D.C. Circuit decision in the filing: real but outside the money question.
- Reports about Nvidia leadership changes in market commentary (outside scope).
