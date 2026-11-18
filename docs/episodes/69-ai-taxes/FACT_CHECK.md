# Fact check: If AI Replaces Workers, Who Pays the Taxes? (Ep 69)

Story frame: Rosa (mayor), Pinewick, Stub (pay stub), Rivet (robot), Ray (forklift driver) are FICTIONAL; on-screen pill "STORY ·
FICTIONAL CAST". The town losing its jobs is a SCENARIO (c1_whatif says so), not a forecast. Sight gags (Rivet has no pockets, Stub
counting on his fingers, "RIVET ITSELF: $0") are comic and carry no claim beyond the mechanism (robots earn no wages, so no income or
payroll tax). Neutral: each proposal gets one good reason and one catch; no politician is a character; Bill Gates is quoted, not drawn.
Status: source_located / data_derived until a named human reviewer signs off. USD only.

| Spoken (segment) | Exact value | Source | Status |
|---|---|---|---|
| "almost nine out of every ten dollars the federal government collects come from people" (c2_big) | FY2026: individual income $2,845.5bn + social insurance $1,811.8bn = $4,657.3bn of $5,403.3bn = 86.2% (OUR CALC). Individual income tax also covers investment income | Treasury MTS Table 4 (FY2026); CBO MBR Nov 2026 | data_derived |
| "about seven cents of every federal tax dollar in the year that just ended" (c2_corp) | $381.4bn / $5,403.3bn = 7.1% (FY2026; FY2025 8.6%) | Treasury MTS | data_derived |
| Social Security "paid for mainly by one tax, the payroll tax" (c2_ss) | Off-budget receipts $1,341.5bn FY2026 | Treasury MTS; Trustees 2026 | source_located |
| Reserve fund "is projected to run dry in 2034" (c2_ss, c5_clock) | Combined OASI+DI depleted Q3 2034 (PROJECTION, intermediate assumptions) | 2026 Trustees Report; AAA one-pager | source_located (same as Ep 59) |
| "only part of every check, unless Congress changes the law" (c2_ss2) | ≈ 83% of scheduled benefits payable after 2034 | Trustees 2026 | source_located (same as Ep 59) |
| "about half of all tax money comes from taxes on work and personal income" (c2_world) | OECD avg 2023: PIT 23.7% + SSC 25.5% = 49.2% (OUR CALC); payroll taxes add a little | OECD Revenue Statistics 2025; Accounting Times | data_derived |
| "Washington already spends more than it collects" (c2_debt) | FY2026 deficit $2.0tn | CBO MBR Nov 2026 | source_located |
| Gates "in 2017": tax a robot "at a similar level" (c3_robot) | Quartz interview, Feb 17, 2017 | Fortune / WEF coverage of Quartz | source_located |
| South Korea "trimmed a tax break for companies that buy automation machines", "first robot tax" nickname (c3_korea) | Aug 2017 plan: automation-investment credit (3-7%) cut by up to 2 pts; exact post-cut rates disputed in later accounts, so not spoken | Korea Times 2017 | source_located |
| "Europe's lawmakers looked at a robot tax and turned it down" (c3_robot_scale) | European Parliament vote, Feb 16, 2017 | Fortune / Quartz coverage | source_located |
| Catch: firms "may just buy fewer" machines (c3_robot_scale) | One study (Hotmann et al. 2025, via ITIF): Korean robot installs -28% vs Japan, employment effect insignificant | ITIF 2026 (advocacy; labelled one study, not spoken) | source_located (context) |
| Profits "can travel" to lower-tax countries (c3_profit_scale) | Profit shifting; 15% global minimum tax | OECD BEPS | source_located |
| "America is the only one in the club without" a national VAT (c3_shop) | Only OECD member without a VAT; VAT ≈ 20.5% of OECD tax revenue (2023) | OECD | source_located |
| Shopping tax "takes a bigger bite" from lower-income budgets (c3_shop_scale) | VAT likely regressive vs current income | CBO budget option 54820 | source_located |
| Alaska "sends a check to nearly every resident" from an oil fund (c4_alaska) | 2025: 618,863 paid; population 738,737 | Alaska PFD Division (Ep 48 FACT_CHECK) | source_located (same as Ep 48) |
| Size of the check "a political fight" (c4_div_scale) | 2016 veto cut; yearly appropriation | Ep 48 FACT_CHECK | source_located |
| Stockton "$500 a month, no strings attached" to "a small group" (c4_stockton) | 125 residents, $500/mo, 24 months from Feb 2019 | SEED | source_located |
| "after a year, more of them had full-time jobs than in a comparison group" (c4_stockton) | 28% -> 40% vs 32% -> 37% (preliminary) | SEED first-year analysis (2021) | source_located |
| OpenResearch "a thousand dollars a month, for years" vs "almost nothing" (c4_or) | $1,000/mo for 3 years vs $50/mo; 1,000 vs 2,000 people | NBER w32719 | source_located |
| "worked a little less, on average about an hour or two a week"; no better jobs; happiness boost faded (c4_or2) | -1 to -2 hrs/week; participation -3.9 pts; earned income -$1,800/yr; no job-quality effect; well-being reverts after year 1 | NBER w32719 rev. Sept 2025 | source_located |

On-screen only (not spoken): "≈ 9 IN 10", "≈ 7¢", "2034", "≈ HALF", "$500 A MONTH", "$1,000 A MONTH", "1-2 HOURS", "$40 TRILLION"
(inside the Ep 59 title), "2017", "A 3-YEAR STUDY", "STOCKTON, CA · 2019".

## Cross-episode consistency
- Ep 59 ("Who Actually Owns America's $40 Trillion in Debt?"): Social Security 2034 and ≈83% payable — identical (2026 Trustees).
- Ep 48 ("Alaska: The State That Pays You to Live There"): no dividend amounts repeated; 2025 recipients 618,863 / population 738,737 identical.
- Ep 64 ("Who Gets Rich When Robots Do the Work?"): no figures shared; linked by title only.

## Spoken-number count
10 distinct figures (nine in ten, seven cents, 2034 twice, half, 2017, $500, a thousand dollars, an hour or two); at most one per
segment. `python tools/count_numbers.py` on the narration reports 14 (it counts "nine ... ten" as two and "booth three"/"all three
booths" as numbers).

## Unverified / caveats
- cbo.gov, ssa.gov and oecd.org blocked automated reading; their figures were cross-checked against Treasury data, the AAA one-pager,
  OECD excerpts and named coverage. OECD PIT and VAT shares come from a secondary (Accounting Times) citing the OECD report.
- Gates quote via reprints of the Quartz interview (original page not read).
- Korea: exact post-cut credit rates differ between sources; only the direction is claimed.
