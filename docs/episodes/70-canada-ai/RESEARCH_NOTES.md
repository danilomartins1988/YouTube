# Research notes: Why Canada Could Be the Biggest Winner of the AI Boom (Ep 70)

Collected 2026-11-18. Full source records and claim texts: `projects/why-canada-could-win-the-ai-boom/sources.yaml`. USD only: CAD at the
Fed G.5A 2025 annual average, 1.3973 CAD per USD (release of Jan 5, 2026), the same rate Ep 67 uses.

## Access log (honest)
- **Natural Resources Canada (nrcan.gc.ca)**: returned a "very high traffic" outage page to automated fetches all session. The critical
  minerals list was read on the canada.ca news release (June 10, 2024); NRCan's electricity and minerals fact pages could not be read, so
  hydro and uranium figures come from the **Canada Energy Regulator** profile instead (read in full).
- **canada.ca**: some pages reset HTTP/2 connections; read through a second fetch path (ISED release, NRCan release, Major Projects Office page).
- **Hydro-Québec / Régie / BLG**: not re-fetched; Ep 67's verified records are reused verbatim (same figures, same rate).
- **BC Hydro**: the call itself is described on gov.bc.ca (framework page + Jan 2026 release), both read. Outcome of the call (Sept 2026)
  **not verified**.
- **Microsoft**: company blog (Dec 9, 2025) confirmed via search on microsoft.com; secondary coverage agrees (C$19bn 2023-27, C$7.5bn+ in two years).
- **Bell AI Fabric**: Bell's own article read (500 MW across six B.C. facilities, PLAN; Kamloops/TRU waste heat).
- **QScale free cooling**: company claim reported by Sustainable Biz Canada (2022); a CLAIM, labelled on screen.
- **Mila, Vector, CIFAR, NobelPrize.org, StatCan, Bank of Canada**: read on their own pages.
- **Google Trends**: unavailable; demand is qualitative. YouTube autocomplete: `autocomplete_2026-11-18.txt`.

## What the evidence says
1. **The "crash" is half true.** StatCan: real GDP fell 0.4% in Q2 2025 as goods exports dropped under US tariffs (cars, machinery). Bank of
   Canada (Oct 28, 2026): Q2 2026 growth 3.3% annualized, about 2% indicated in Q3, Q4 to slow under new US tariffs, recovery in 2027
   (FORECAST); unemployment around 6.5%. A rough patch with sector damage, not a collapse.
2. **Power.** CER: ~60% of electricity from hydro; Canada the world's no. 3 hydro generator (2023). Quebec: cheap for big industry (Ep 67:
   a 50 MW customer pays ~22% of Boston, Hydro-Québec's own comparison) but surplus is over, 5 MW+ loads need ministerial authorization, and
   a PROPOSED data-center rate ≈ 2.5× today's large-power price (our calc; BLG "roughly double"). B.C.: AI/data-centre projects ≥ 10 MW
   must compete; first two-year call up to 400 MW.
3. **Cold.** Outside-air ("free") cooling claims up to ~80% of the year in Quebec (QScale; Vantage advertises 80-86% at its Quebec campuses,
   not used). Waste-heat reuse planned at Thompson Rivers University, Kamloops (Bell).
4. **Money arriving.** Microsoft C$19bn (≈ US$13.6bn) 2023-27 (PLAN); Bell up to 500 MW hydro-powered AI compute in B.C. (PLAN).
5. **Minerals.** 34 critical minerals on the 2024 list (incl. nickel, copper, uranium, lithium, graphite); Canada no. 2 uranium producer (CER,
   2022). IEA: major mines took 16+ years from discovery to first production (2010-19, world). The Major Projects Office (2025) aims to speed
   federal approvals; McIlvenna Bay: referred Sept 2025, first copper June 2026 (but ~88% built by Jan 2026).
6. **Brains.** Hinton (U of Toronto) shared the 2024 Nobel Prize in Physics; Mila (founded by Bengio, 1993) calls itself the world's largest
   academic deep-learning research center; Vector launched 2017 (C$135m); CIFAR: the 2017 Pan-Canadian strategy was the world's first
   national AI strategy. ISED opened the sovereign compute infrastructure call on Apr 15, 2026 (Canadian-owned AI supercomputer).
7. **Brain drain, nuanced.** StatCan (Jul 2025): STEM graduate retention has improved; international grads leave more. The pull of US pay,
   compute and capital on top talent and startups is widely reported (TD Economics, Universities Canada, The Logic) but not quantified here.
8. **US dependence.** StatCan: 75.9% of merchandise exports went to the US in 2024, 71.7% in 2025.

## Not used / unverified
- Budget 2026's reported "500 MW of sovereign compute" backstop and the June 2026 national AI strategy (secondary coverage only).
- Exact share of AI graduates who leave; outcome of B.C.'s 2026 call; Régie decision on Rate CD (pending at publication).
