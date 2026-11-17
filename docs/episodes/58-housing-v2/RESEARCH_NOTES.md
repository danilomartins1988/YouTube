# Ep 58: Why Americans Can No Longer Afford a Home — research notes

Re-make of Ep 31 ("Why American Homes Became So Expensive", 2026-11-10) in the sitcom format, with every figure re-read on
its primary page or data file on **2026-11-17** and updated to the latest release. Ep 31's dossier
(`projects/why-american-homes-became-so-expensive/sources.yaml`) was the starting point. A named human reviewer must sign
off before publishing (claims stay `source_located`).

## Updated to the latest data (Nov 2026)
- **NAR, Existing-Home Sales, October 2026** (released 2026-11-12),
  https://www.nar.realtor/newsroom/existing-home-sales-decreased-5-5-percent-october-nar-report
  - "The median existing-home sales price increased 0.4% to $416,700" (from $414,900 a year earlier; 40th straight month of
    year-over-year gains). Sales fell 5.5% to a seasonally adjusted annual rate of 3.75 million; inventory 1.59 million
    (5.1 months); first-time buyers 29% of October sales; cash sales 29%.
  - "The Housing Affordability Index registered at 100.7, down from 107.3 one year ago."
  - (NAR's monthly HAI web page still showed October 2025 data on 2026-11-17, so the release is the source used.)
- **NAR, HAI methodology**, https://www.nar.realtor/research-and-statistics/housing-statistics/housing-affordability-index/methodology
  - "a value of 100 means that a family with the median income has exactly enough income to qualify"; "assumes a down
    payment of 20 percent of the home price and ... a qualifying ratio of 25 percent"; "the monthly P&I payment cannot exceed
    25 percent of the median family monthly income."
- **Freddie Mac PMMS** (https://www.freddiemac.com/pmms, read 2026-11-17): "The 30-year fixed-rate mortgage averaged 7.11% as
  of November 12, 2026, down from last week when it averaged 7.18%. A year ago at this time, the 30-year FRM averaged 6.24%."
  Historical weekly file (`/pmms/docs/historicalweeklydata.xlsx`): series low 2.65% (2021-01-07); 3.22% (2022-01-06);
  7.08% (2022-10-27); 2023 peak 7.79% (2023-10-26); 2026 low 5.98% (2026-02-26); 2026 high 7.40% (2026-10-08 and 10-15).
  The rollercoaster track uses every 4th weekly value since Jan 2019 plus those extremes
  (`projects/why-americans-can-no-longer-afford-a-home/pmms_weekly_sample.json`).
- **Census Bureau, Income in the United States: 2025** (story 2026-09-15),
  https://www.census.gov/library/stories/2026/09/median-household-income.html: "U.S. real median household income was
  $87,460 in 2025, up 2.6% from the previous year", highest since 1967; higher than 2019 and 2024.
- **NAR 2026 Profile of Home Buyers and Sellers** (2026-11-05, transactions July 2025–June 2026, 7,125 responses):
  first-time share 22% (from a record low 21%), "about half the historical norm of 40% seen before 2008"; median first-time
  buyer age 40 (matching the all-time high); repeat buyers 62; first-time median down payment 9%.

## Re-verified (unchanged since Ep 31)
- **Harvard JCHS, State of the Nation's Housing 2026, Key Facts** (PDF re-downloaded 2026-11-17): price-to-income 3.2 (1990s),
  4.1 (2019), 5.0 (2022 peak), 4.7 (2025); payment $1,240 (end 2020) → $2,420; income needed $68,700 → $120,800 (end 2025);
  metros needing > $100k: 31 (2020) → 169 of 387 (2025); listings affordable at ≤ $75k: 49% (Mar 2019) → 23% (Mar 2026);
  half of mortgages below 4% (late 2025); mobility record low 11.2% (2024); existing sales 4.1M (2025), 30-year low, two-thirds
  of 6.1M (2021); construction input prices +40% since Jan 2020; shortage estimates "between 1.2 and 5.5 million units".
- **JCHS press release** (2026-06-17): "Home prices have increased 54 percent nationwide since 2020".
- **Census completions (COMPUTNSA)**, our sums (data file of 2026-11-10, recomputed): 15.64M (2000–09), 9.15M (2010–19),
  585k in 2011 (lowest since 1968), 1.49M in 2025. FRED was unreachable from this machine on 2026-11-17 (empty replies).
- **Up for Growth 2025**: underproduction 3.85M (2022) → 3.78M (2023).
- **NAHB, Government Regulation in the Price of a New Home: 2026** (PDF, Eric Lynch, 2026-06-08): 26.4% of the final price;
  $131,734 on a $499,500 average new home; also "NAHB estimates the U.S. has a structural housing deficit of 1.2 million units."
- **UC Berkeley OBI** (2022): "77.70 percent of residential land in Greater LA is exclusively reserved for single-family housing."

## New in this version
- **FHFA Working Paper 24-03, "The Lock-In Effect of Rising Mortgage Rates"** (Batzer, Coste, Doerner, Seiler, 2024-03-18),
  abstract read on fhfa.gov: each percentage point of market rate above the origination rate cuts the probability of sale by
  18.1%; lock-in "prevented 1.33 million sales between 2022Q2 and 2023Q4"; "increased home prices by 5.7%, outweighing the
  direct impact of elevated rates, which decreased prices by 3.3%."
- **Our calculation** (NAR method): $416,700 × 80% = $333,360 over 30 years: $1,343/month at 2.65%, $2,243 at 7.11%
  (≈ $900 more); income needed at 7.11% = $2,243 × 12 / 0.25 ≈ $107,600, vs the Census median household income $87,460.
  Principal and interest only. NAR's own index uses median FAMILY income, a different (higher) concept: said as "our
  calculation" and the comparison is shown as such.

## Flagged, not used
- White House CEA "about 10 million homes" (single-family, Apr 2026): only news coverage was readable; primary not opened.
- Realtor.com 2026 Housing Supply Gap (4.03M): site blocked to our fetcher.
- Secondary-site HAI and qualifying-income numbers for mid-2026 conflicted with each other; not used.
