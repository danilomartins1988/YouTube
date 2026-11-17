# SEO research package: Why Americans Can No Longer Afford a Home (Ep 58, why-americans-can-no-longer-afford-a-home)

Per docs/SEO_DIRECTIVE.md §14. Evidence collected: 2026-11-17T17:35Z. Data limits: YouTube autocomplete = real
suggestions, no volumes; Google Trends = not available (demand history below is a qualitative assessment).

## 1. Primary keyword
**why americans can't afford homes** (YouTube autocomplete suggestion for the seed "why can't americans afford a home",
alongside "why americans can't afford houses anymore").

## 2. Secondary keywords (5)
1. why are houses so expensive (autocomplete: "why are homes so expensive", "why houses are so expensive in usa")
2. housing affordability crisis (autocomplete for "housing affordability")
3. nobody can afford a house (autocomplete for "can't afford a house")
4. housing affordability index (autocomplete for "housing affordability")
5. housing crisis explained (autocomplete for "housing shortage explained")

## 3. Long-tail keywords (10)
All are real autocomplete suggestions collected 2026-11-17 (`python tools/yt_autocomplete.py ... --expand`):
1. why americans can't afford houses anymore
2. who can afford a house in 2026
3. how can people afford houses
4. why us houses are so expensive
5. why are homes so expensive
6. can't buy a house
7. mortgage rate lock explained
8. mortgage rates right now
9. housing shortage
10. solution to housing crisis

(No first-time-buyer-age phrase surfaced in autocomplete; that fact is used in the film, not targeted as a keyword.)

## 4. Search intent analysis
| Keyword | Intent | Covered where in the film |
|---|---|---|
| why americans can't afford homes | learn | whole film; payoff answers it (≈ $108K needed vs $87K median, five forces) |
| why are houses so expensive | learn | Act 1 (price = 4.7 years of income; +54% since 2020) |
| housing affordability index | learn | Act 2 (NAR HAI 100.7, Oct 2026) |
| mortgage rate lock explained | learn | Act 3 (lock-in; FHFA estimate) — note: "rate lock" also means a lender's rate lock; our film covers the homeowner lock-in effect |
| mortgage rates right now | news | Act 2 (7.11% on Nov 12, 2026) — dated; not the title promise |
| housing shortage / housing crisis explained | learn | Act 4 (estimates 1.2M–5.5M; why estimates differ) |
| solution to housing crisis | decide | Act 5 + payoff (zoning, building, unlocking supply), framed as analysis, not advocacy |
| who can afford a house in 2026 | learn/news | hook + income test (our calculation) |

## 5. Historical demand assessment
Qualitative (no Trends data): **evergreen with recurring spikes**. Home affordability is a standing household concern;
interest typically rises with mortgage-rate news, the spring buying season and major data releases (NAR monthly sales,
Freddie Mac weekly rates). Autocomplete shows political phrasing in Nov 2026 ("housing affordability bill", "...trump"),
which suggests news-driven interest right now; we do not chase it in the title.

## 6. Competitor analysis (public data only)
| Video | Channel | Published | Duration | Public views | Angle / gap |
|---|---|---|---|---|---|
| Why buying a house in the US is so hard right now | Vox | not verified | ≈ 9.5 min (per an index page) | not verified by us | zoning focus; no 2026 data |
| How the US made affordable homes illegal | Vox | not verified | not verified | not verified | zoning/policy; no rates or lock-in |
| Why can't young Americans afford homes? | ReasonTV | not verified | ≈ 17 min (per an index page) | not verified | policy-led argument |
| Housing-market segments | Breaking Points | not verified | clips | not verified | news/opinion talk format |
| The U.S. Housing Shortage Explained & How To Fix It | Valuetainment | not verified | not verified | not verified | interview/talk format |

Found via web search (index pages such as rosetta.to / planetizen.com), 2026-11-17; YouTube pages themselves were not
opened, so dates and view counts are left blank rather than guessed. **Our gap:** one animated story with all five causes
(price, rate, lock-in, supply, zoning), Nov 2026 numbers, an income test viewers can redo, and a sitcom format.

## 7. Title candidates (10)
| # | Type | Title | Chars | Notes |
|---|---|---|---:|---|
| 1 | Search | Why Americans Can No Longer Afford a Home | 41 | owner's title; matches primary keyword intent |
| 2 | Search | Why Americans Can't Afford Houses Anymore | 41 | exact autocomplete phrasing |
| 3 | Search | Why Are Homes So Expensive in the US? (2026) | 44 | year dates the video |
| 4 | Curiosity | Record Paychecks, Unaffordable Homes: What Broke? | 49 | contradiction |
| 5 | Curiosity | The Same House Now Costs $900 More a Month | 42 | our calculation; narrower |
| 6 | Curiosity | Why the First-Time Home Buyer Is Now 40 | 39 | surprising fact, partial promise |
| 7 | Hybrid | Why Americans Can't Afford Homes (It's Not One Thing) | 53 | keyword + payoff hint |
| 8 | Hybrid | Who Can Afford a House in 2026? The Math Says Few | 48 | autocomplete phrase + stake |
| 9 | Creative | The Starter Home Is Disappearing. Here's Who Took It | 52 | narrative; "who" = forces |
| 10 | Creative | Priced Out, Rated Out, Zoned Out | 32 | payoff line; weak for search |

## 8. Thumbnail concepts (3)
- **F (default):** original character Maya (young buyer bust) shocked beside a "$416,700" tag; words "CAN'T AFFORD / A HOME".
  Rendered: `youtube-package/thumbnail.png` (= `thumbnail_face.png`), QC pass.
- **A:** padlocked starter house at dusk; "HOMES OUT / OF REACH". Rendered: `thumbnail-alt-A.png`, QC pass.
- **B (not rendered):** the same house with two tags, $1,343/mo at 2.65% vs $2,243/mo at 7.11% (our calc.); "SAME HOUSE / +$900".

## 9. Selected title + 2 backups
**Selected:** #1 "Why Americans Can No Longer Afford a Home" + thumbnail F. Backups: #2 (exact autocomplete phrasing) and
#7. Rationale: the owner's title carries the primary keyword's meaning in natural language, the thumbnail shows the
contradiction (a young buyer and a real median price), and the film's hook and payoff deliver exactly that promise (§10).

## 10. Optimized description
Final text in `youtube-package/description.txt` (and `youtube_package.md`): a 100–160-word opening containing "why
Americans can't afford homes", the questions answered, chapters from the final timeline, related channel videos (titles
only, no URLs: none verified), sources, and the channel blurb.

## 11. Tags and hashtags
Tags: why americans can't afford homes, why are houses so expensive, housing affordability crisis, can't afford a house,
housing affordability index, mortgage rates, mortgage rate lock-in, housing shortage, zoning, first-time home buyer,
starter home, home prices 2026, housing crisis explained, economics explained, The Hidden Economics.
Hashtags (3): #housing #realestate #economics

## 12. Chapter structure (final timestamps after render)
From the final `timeline.json` (706.6 s):
```
0:00 Cold open
1:14 The price tag
2:47 The rate rollercoaster
5:14 The great lock-in
7:02 The homes we never built
8:53 The zoning board
10:20 The basement generation
```

## 13. Shorts (3)
1. **Built:** "The Typical Home Costs $416,700. The Typical Paycheck Can't Keep Up" — hook: record paychecks vs the median
   home; insight: income ≈ $87K vs ≈ $108K needed (our calc.). #housing #realestate #economics
2. **Planned:** "Same House, $900 More a Month" — the 2.65% vs 7.11% payment (our calc.), from Act 2. #mortgage #housing #economics
3. **Planned:** "Why Your Parents Won't Sell Their House" — the lock-in effect (half of mortgages < 4%, JCHS; FHFA estimate). #housing #mortgage #economics

## 14. Evergreen assessment
- **6 months:** strong; the October 2026 numbers stay recent until spring data.
- **12 months:** good; mechanisms hold, but rate and price figures date (a pinned comment can update them).
- **24 months:** moderate; the story (price-to-income, lock-in, underbuilding, zoning) stays valid, numbers will be old.

## 15. SEO & commercial scorecard (editorial estimate, not a probability)
| Criterion | Weight | Score | Why |
|---|---:|---:|---|
| Search demand and keyword relevance | 20 | 18 | title matches a live autocomplete query; no volumes available |
| Browse and Suggested audience appeal | 20 | 17 | universal topic, face thumbnail; crowded niche |
| Title and thumbnail potential | 20 | 17 | clear promise, real number on the thumbnail; title plain rather than intriguing |
| Evergreen demand | 15 | 13 | evergreen mechanisms; dated figures |
| Narrative and retention potential | 15 | 13 | sitcom format, running gag, five discoveries |
| Competitive differentiation | 10 | 8 | all five causes + 2026 data + animation; others cover zoning well |
| **Total** | 100 | **86** | target ≥ 85 |
