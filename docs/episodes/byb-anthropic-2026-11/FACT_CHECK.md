# Fact check: Anthropic Stock Before You Buy: 7 Things to Check (Nov 2026)

Status: every spoken figure traced to `projects/before-you-buy-anthropic-2026-11/sources.yaml`; claims stay `source_located` / `data_derived`
until a named human reviewer signs off. Primary: Anthropic 424B4 (filed 2026-11-19, dated Nov 18, 2026), pricing FWP, Amazon Q3 2026 10-Q, peer
filings. Research notes: `docs/series/research/anthropic_2026-11.md`. USD only. Latest close used: **$97.17, Nov 19, 2026** (labelled on screen;
the Nov 20 session had not closed when the film was locked).

## Spoken figures (13; at most one per segment)
| # | Segment | Spoken | Exact value and source | Label |
|---|---|---|---|---|
| 1 | h_open | "eighty-three dollars" | IPO price $83.00 per Class A share (424B4, FWP) | FACT |
| 2 | h_day | "about ninety-seven dollars" | Close $97.17, Nov 19, 2026; open $111.50 (CNBC, The National, Yahoo Finance) | FACT |
| 3 | c1_votes | "just over half" (of the votes) | Class F share = 50.1% of total voting power on matters submitted to stockholders generally (424B4) | FACT |
| 4 | c1_float | "fewer than one in ten" | 980,000,000 IPO shares ÷ 13,219,642,276 outstanding = 7.4% (424B4) | OUR CALC |
| 5 | c1_draw | "about a third more" (shares) | Fully diluted ≈17.6-18.0bn vs 13.22bn outstanding (options 1.77bn, RSUs 1.03bn, Amazon Notes, etc.; CNBC $1.5tn ÷ $83) = +33-36% | OUR CALC |
| 6 | c2_ps | "about thirty-six times" (sales) | 13.22bn × $97.17 ≈ $1,284.6bn ÷ TTM revenue $35,282m ≈ 36.4x (424B4; close Nov 19) | OUR CALC |
| 7 | c2_draw | "about ten times" | Nvidia ≈9.7x, Microsoft ≈10.7x trailing sales at Nov 19 closes (peer filings, Yahoo) | OUR CALC |
| 8 | c3_gate | "May seventeenth" (next year) | Close of the 180th day after the Nov 18, 2026 prospectus = May 17, 2027, or earlier: 2nd full trading day after the Q1 2027 release (424B4) | FACT + OUR DATE CALC |
| 9 | c3_size | "up to three billion shares" | Up to 2.7bn Class A + 336m Class N = 3.0bn at that step, the largest in the release table (424B4) | FACT |
| 10 | c4_cost | "about fifty-seven cents" | 9M 2026 compute and infrastructure $18,808m ÷ revenue $33,242m = $0.566 (2025: $1.60) (424B4) | OUR CALC |
| 11 | c4_cash | "about nine hundred billion dollars" | Purchase commitments and leases ≈$900.9bn as of and after Sep 30, 2026 (424B4) | FACT |
| 12 | c6_fb | "about half" (the offer price) | Facebook offer $38; lowest close $17.73 on Sep 4, 2012 = 47% (Yahoo); lock-up expiry Aug 16, 2012, close $19.87 (AP) | FACT + OUR CALC |
| 13 | c6_arm | "nearly half" (in a single day) | Arm +48% on Feb 8, 2024 ($77.01 → $113.89) after its quarterly report (Bloomberg; Yahoo) | FACT |

`tools/count_numbers.py` on the resolved narration also counts "Third" (an ordinal in a list in c4_draw), not a figure.

## Non-numeric claims checked
- "the company behind the Claude A I models" (424B4). "sold its first shares to the public": priced Nov 18, trading Nov 19 (FWP).
- "The stock opened far above the offer, slid back all afternoon": open $111.50, close $97.17 (CNBC; intraday high $115.10 reported).
- c1_classes: Class A one vote; Class N same economic rights, no vote except as required by law, "holders ... are primarily strategic business
  partners"; Classes T, F and E have no economic rights (424B4).
- c1_votes: Class F held by the Founder LLC, of which the seven co-founders are the sole members; Class T held by the LTBT elects a majority
  of the board (424B4). "the big decisions are already spoken for" = analysis of these two facts.
- c1_float: "most of them can't sell" (lock-up and market standoff covering directors, officers and substantially all holders; 424B4).
- c1_dilute: Amazon Notes convert at the end of each fiscal quarter up to the ownership cap; 2026 Plan and ESPP annual automatic increases;
  Public Benefit Issuances of up to 2% of then-outstanding shares each time the price rises 50% above the prior milestone, at the board's
  discretion, to the Anthropic Public Benefit Fund (a wholly owned subsidiary) (424B4).
- c2_ps: "barely makes an operating profit yet": operating loss $1.26bn in 9M 2026 (Q3 2026 −$567m); adjusted operating income positive (non-GAAP,
  not used) (424B4). Run rate ≈$81bn (Oct 31) → ≈15.9x (our calc). "many times what it was a year earlier": 9M 2026 $33.2bn vs 9M 2025 $2.5bn.
- c2_value: cash $95.6bn + short-term investments $36.3bn (Sep 30, 2026); ≈$104.8bn net proceeds; debt $6.2bn (424B4).
- c3_waves: release table dates Nov 19, Dec 15, 2026; Jan 5, Jan 19, Feb 2, 2027; FY2026 release + 2 trading days, up to 1.7bn (424B4).
- c3_year: co-founders and holders of >0.5% of fully diluted shares: earlier of the 2nd full trading day after the Q3 2027 release ("results for
  next summer", July-September 2027) and the 365th day (Nov 18, 2027); timed automatic expirations apply (424B4).
- c3_meaning: placement shares "will not be subject to the lock-up ... restricted securities" under Rule 144 (424B4).
- c4_when: first annual results cover the year ending Dec 31, 2026; the release triggers a lock-up step; no date announced (424B4; as of 2026-11-20).
- c4_cost "Last year, it was bigger than the sales": 2025 compute $7,326m > revenue $4,585m (424B4).
- c4_cash: "much of it owed whether customers show up or not": Microsoft, Google, Amazon arrangements "regardless of actual usage" / true-ups;
  operating cash flow 9M 2026 +$6.569bn (424B4).
- c5_partners/c5_draw: Amazon 14.6%, Google 13.4% (424B4); compute arrangements; CSP marketplaces; risk factor on CSPs that develop their own models
  and "conflicts of interest" (424B4); Amazon investments (10-Q).
- c5_chips: "AWS Trainium, Google TPUs, NVIDIA GPUs, and AMD GPUs" (424B4); Google, NVIDIA, AMD are placement buyers; Amazon and Google holders.
- c5_customers: no customer ≥10% of 9M 2026 revenue; 2025 Customers A and B 12% each ("big enough to be named in the filing" = listed as a ≥10%
  customer; identities are not disclosed); CSP marketplaces 44% of 9M 2026 revenue (424B4).
- c6_arm: "listed in the fall" (Sep 14, 2023), "popped on day one" (close $63.59 vs $51), "slipped below its offer within weeks" ($47.87, Oct 20).
- c6_lesson: analysis of these two cases only; no forecast for ANT.
- c7_pbc: PBC; purpose quoted (424B4). c7_trust: "financially disinterested" trustees; controlled company may opt out of certain Nasdaq
  requirements (424B4). c7_meaning: risk factor quoted; supporters' view attributed generally (the 424B4 describes the LTBT's aim of long-term
  balance).

## Could not verify (handled)
- Nov 20, 2026 close (session open when locked); intraday not used.
- FY2026 results date (not announced).
- Competitors' metrics (not inferred).
