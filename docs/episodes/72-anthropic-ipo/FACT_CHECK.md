# Fact check: Anthropic's $1.5 Trillion IPO: The AI Gold Rush or the Next Bubble? (Ep 72)

Status: every spoken figure traced to `projects/anthropics-1-5-trillion-ipo/sources.yaml`; claims stay `source_located` / `data_derived` until a
named human reviewer signs off. Primary documents: Anthropic 424B4 (2026-11-19) and pricing FWP; Amazon and Alphabet Q3 2026 10-Qs. Spoken
figures: **14** (≤1 per segment; `tools/count_numbers.py` reports 15 on `narration_plain.txt` because it counts "eighty-one billion" twice
and reads "and a" in c4_loop as a number phrase). USD only. Latest close used: **$97.17, Nov 19, 2026** (labelled on screen).

| # | Segment | Spoken | Exact value and source | Label |
|---|---|---|---|---|
| 1 | co_hook | "eighty-three dollars" | IPO price $83.00 per Class A share, priced Nov 18, 2026 (pricing FWP; 424B4; CNBC) | FACT |
| 2 | c1_day | "about ninety-seven dollars" | First-day close $97.17 (+≈17%), Nov 19, 2026; open $111.50, high $115.10 (CNBC, Forbes, The National) | FACT (press) |
| 3 | c1_three | "about one and a half trillion dollars" | Fully diluted market value at $83 ≈ $1.5tn (CNBC); outstanding 13,219,642,276 shares (424B4); bases on screen | FACT + OUR CHECK |
| 4 | c1_raise | "about eighty-one billion dollars" | $81,340,000,000 = 980,000,000 × $83 (FWP); 956,351,354 primary (97.6%), 23,648,646 secondary (2.4%) | FACT |
| 5 | c2_rocket | "thirty-three billion dollars" | Revenue nine months to Sep 30, 2026: $33,242m (424B4); "so far this year, through September" | FACT |
| 6 | c3_dollar | "about a dollar sixty" | 2025 compute and infrastructure $7,326m ÷ revenue $4,585m = $1.598 (424B4) | OUR CALC |
| 7 | c3_better | "about fifty-seven cents" | Nine months 2026: $18,808m ÷ $33,242m = $0.566 (424B4) | OUR CALC |
| 8 | c3_commit | "about nine hundred billion dollars" | Purchase commitments and leases ≈ $900.9bn as of and after Sep 30, 2026, to 2045 (424B4) | FACT |
| 9 | c4_amazon | "at least a hundred and ten billion dollars" | ≥ $110.0bn with Amazon, May 2026-Apr 2036, "regardless of actual usage" (424B4); Amazon 10-Q: "more than $100.0 billion over 10.0 years" | FACT |
| 10 | c5_vc | "about a quarter" (a share) | Series A original issue price $2.57 per preferred after the 10-for-1 split; ≈10 common per preferred → ≈$0.26 (424B4) | OUR CALC; HYPOTHETICAL investor |
| 11 | c5_staff | "more than four hundred" (employees) | "over 400 employees are expected to be worth $100 million or more" (CNBC, Nov 19, 2026) | REPORTED |
| 12 | c5_lock | "six months" | Lock-up up to 180 days; 365 for co-founders and >0.5% holders (424B4) | FACT |
| 13 | c6_multiple | "about twenty times" | ≈$1.75tn fully diluted at the close (The National) ÷ run rate ≈$81bn (424B4, Oct 31) = 21.6× (18.5× at $1.5tn); equity value, not EV | OUR CALC |
| 14 | c7_close | "two different things" | Rhetorical (owner's closing line), not a statistic | — |

## Non-numeric claims checked
- "barely old enough for kindergarten" = founded January 2021 (424B4). "It doesn't make chips. It doesn't own a giant cloud." Anthropic buys
  compute from CSPs and suppliers (424B4 compute arrangements). "its biggest partners are also its shareholders, its suppliers and its
  rivals": Amazon and Google (424B4 ownership; risk factor on CSPs that "develop and offer their own AI models").
- "The shares went to the first buyers the night before, at June's price": priced Nov 18, trade date Nov 19 (FWP). Retail allocation ≈15%
  (CNBC); June is fictional.
- "the biggest stock offering on record": CNBC ("largest offering on record, topping SpaceX"); The National (IPO + placement $107.3bn vs
  SpaceX $86bn).
- "almost all of that money went to the company, as new shares": 97.6% primary (FWP). "The co-founders each sold only a sliver": 3,378,378
  shares each of 980m (our division).
- "a group of chip and cloud giants agreed to buy even more stock, at the same price": $26.0bn concurrent private placement at $83 (424B4).
- "A group of researchers left OpenAI": co-founders' biographies (424B4: Dario Amodei VP of Research at OpenAI; Brown, Clark, Kaplan at
  OpenAI). "a brother and sister" (Dario and Daniela Amodei, widely documented; same surname, both co-founders per 424B4). Titles per 424B4.
  "public benefit corporation" (424B4).
- "Programmers used it to write code" (Claude Code, 424B4). "most of the money ... comes from usage": consumption-based 79% (424B4).
- "net profit ... a giant loss, mostly accounting on notes that turn into stock": net loss $104.0bn incl. $94.3bn fair-value changes
  (424B4). "cash flow ... turned positive": operating cash flow +$6.6bn, nine months 2026 (424B4).
- "Training ... Running it ... inference": general mechanism (our explanation).
- "much of it is promised, whether the customers show up or not": Microsoft, Google and Amazon commitments "regardless of actual usage", with
  true-ups (424B4).
- "its actual debt is small next to its cash pile": $6.2bn vs $95.6bn + $36.3bn (Sep 30, 2026, 424B4).
- "It has invested billions in Anthropic since its early days": $8.0bn notes from Q3 2023, $10.0bn preferred in 2026 (Amazon 10-Q).
  "Amazon also sells Claude to its cloud customers": CSP marketplaces (424B4). "builds AI models of its own": 424B4 risk factor (CSPs that
  develop their own models).
- c4_loop: investment in (10-Q); compute payments (424B4 commitments); "Amazon books that as sales" (AWS revenue, mechanism); "keeps a cut"
  (partner fees recorded as expense, 424B4); "the stake on Amazon's books rises": $62.8bn upward adjustments in nine months 2026 (10-Q);
  Google as investor, cloud supplier (≥$121.3bn hosting deal) and rival (424B4).
- c4_critics: "Circular financing" criticism (Reuters, Sep 30, 2026, on the confidential filing); "A rival has argued ..." (Axios, Oct 8,
  2026, reported; summary via search excerpts); "Some warn the risk lands on ordinary investors" (Tech Policy Press, opinion); "conflicts of
  interest" (424B4 risk factor, verbatim words).
- c4_defense: "most of Claude's paying customers are ordinary businesses": 56% of revenue not via cloud marketplaces and marketplace sales
  are also to end customers; >11,900 customers ≥$100k (424B4). "Counting cloud sales in full is a standard accounting choice": principal vs
  agent under GAAP, 424B4 note; "both rivals say they follow the rules" (Axios, reported). "Carmakers do it every day": captive auto-finance
  arms (general knowledge, no figure). "it's all disclosed" (424B4).
- c4_twist: the seven placement buyers (424B4). "Most of them are, directly or indirectly, part of the supply chain": Google, Microsoft (cloud
  commitments), AMD (Helios), Broadcom (accelerator lease), NVIDIA (GPUs via SpaceXAI, Nscale, Lambda) direct or via providers; Micron
  (memory) and TSMC (chip manufacturing) indirect, labelled INDIRECT on screen. "part of what they put in can come back as sales": OUR ANALYSIS.
- c5_giants: Amazon ≈$18bn invested vs ≈$238.7bn carried on Sep 30, 2026, before the IPO (our sums from the 10-Q); "much of that gain flowing
  into its reported profits" ($62.8bn in other income, nine months 2026; the notes' gains sit in other comprehensive income).
- c5_staff: options "the right to buy shares at an old, low price": 1.77bn options at $2.91 weighted average (424B4).
- c5_lock: "When the locks open, a wave of sellers can arrive at once" (general mechanism; ≈3.7bn shares may become eligible early, 424B4).
- c5_june: "Her share has no lockup" (shares bought in the IPO are freely tradable; lock-ups bind insiders).
- c6_need: HYPOTHETICAL: $1.75tn ÷ 25 ≈ $70bn of yearly net profit (our calc); "on the scale of the most profitable companies on Earth"
  (the largest US companies' annual net profits are of that order; no figure spoken). Today: operating loss (424B4).
- c6_bear: "every new share it sells makes June's slice smaller": dilution sources (424B4).
- c7_shovels: analysis; chipmakers and clouds are paid under the commitments above; "Some get paid twice, as investors and as suppliers"
  (Google, Amazon, NVIDIA, AMD, Broadcom, Microsoft are both, per the 424B4).

## Could not verify (handled)
- **CNN live page and a Reuters story on the close** (cited in the brief for ≈$1.76-1.77tn fully diluted at the close): CNN returned HTTP 451
  and no Reuters close story could be opened. Not used on screen; the film uses ≈$1.75tn (The National) and CNBC's "roughly $1.8 trillion".
- **Forbes** live page (open $111.50, high $115.10, ≈$1.27tn outstanding per the brief) blocked automated reading (HTTP 403); open and close
  confirmed by CNBC and The National; the $115.10 high comes from Forbes via search excerpts (shown in the description as "reported").
- **Axios** (revenue-accounting dispute) blocked automated reading; used only as an attributed, reported criticism.
- **Nov 20 close**: the session had not closed when the film was locked; the Nov 19 close is labelled with its date.
- **Alphabet 10-Q** does not name Anthropic; Google's stake and investments come from Anthropic's prospectus.
