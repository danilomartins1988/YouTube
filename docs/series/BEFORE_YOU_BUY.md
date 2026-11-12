# Series draft: "Before You Buy" (largest U.S. listed companies)

Status: APPROVED by the owner 2026-11-11: produce the 10 largest Nasdaq-listed companies; every episode dated, to be remade each quarter.

## Audience
Viewers who already know the basics of investing. No concept lessons: terms such as revenue, gross/operating margin,
free cash flow, guidance, buybacks, dilution, P/E and backlog are used without being explained.

## Content rule
100% about the company. Every number comes from the company's own filings (10-K, 10-Q, 8-K earnings releases, proxy)
or is our calculation from them (labelled). Analyst views only attributed, never ours. No buy/sell call, no price target
of ours, no return promises. Short disclaimer after the hook and in the description.

## Core question (owner, 2026-11-11)
What is priced into the stock, what has to happen for it to keep rising, what could go wrong, and what opportunities
could add even more value.

## Episode structure (11-13 min)
1. Hook: the gap between the price and today's business (e.g. market value vs this year's profit).
2. The business today, fast: revenue by segment, where the profit is, concentration (only what the rest needs).
3. What is priced in: a simple reverse calculation (our calculation, assumptions on screen: current market cap,
   free cash flow, discount rate, years) giving the growth the price implies; compared with the company's guidance
   and attributed analyst consensus.
4. What has to happen: the 3-4 concrete conditions (e.g. data-center demand, margins holding, a product ramp),
   each tied to a filing number.
5. What could go wrong: company-specific risks (10-K risk factors, regulation, competitors, customers), with the
   money at stake where it is disclosed.
6. Upside the price may not include: opportunities the company itself discloses (new products, markets, contracts),
   sized only from sourced figures; company TAM claims attributed as claims.
7. The scorecard: the 3 numbers to watch next quarter that confirm or break the priced-in story.

## Method rules for "priced in"
- Owner question 2026-11-11: free cash flow alone misleads during an investment boom (Alphabet 178x, Amazon negative).
  Every episode therefore shows the SAME three lenses, then picks the most meaningful base for the implied-growth gauge:
  1. P/E on trailing net income (strip one-off gains when disclosed, e.g. Alphabet equity gains);
  2. FCF yield (FCF / market cap) — what owners actually get today;
  3. Cash before growth spending: operating cash flow yield, plus "what the capex must earn": the annual return the
     trailing capex needs to generate for the price to make sense (our calculation).
  Use enterprise value (market cap + debt - cash) when net cash or debt is material.
  Base for the gauge: FCF when capex is steady (Apple); operating cash flow minus depreciation as a proxy for
  maintenance-adjusted cash when capex is booming (Microsoft, Alphabet, Amazon, Meta), clearly labelled as a proxy;
  revenue/scenario framing when profit is tiny (Tesla).
- Our calculation, labelled every time; inputs and date on screen; a range (two discount rates), not one number.
- Never "fair value", "cheap", "expensive", "buy" or "sell". The episode says what the price assumes, not whether
  the assumption is right.

## Season 1 candidates (verify market-cap order before starting)
Nvidia, Microsoft, Apple, Alphabet, Amazon, Meta, Broadcom, Tesla, Berkshire Hathaway, JPMorgan. Bonus: SpaceX (Ep 51).

## Dating and quarterly refresh (owner, 2026-11-11)
- Title carries the edition: "Before You Buy Nvidia Stock, Watch This (Nov 2026)"; next edition after the next earnings report.
- On screen: a "DATA AS OF <close date> · LATEST REPORT: <quarter>" stamp at the hook, at the priced-in section and at the end.
- Description: the same date line plus "updated every quarter".
- Each project keeps one file of inputs (prices, share count, segment figures, guidance) so a refresh swaps numbers
  and re-renders; scripts read the numbers from sources.yaml placeholders.
- Order: companies that already reported this quarter first; Nvidia after its Nov 2026 report.

## Look and voice (owner, 2026-11-11)
- As animated as possible, retro-futurist sci-fi cartoon comedy feel (same genre-level rules as Ep 52: original
  designs only, never copying any existing show's characters, designs, logos, fonts, catchphrases or music).
  Mostly drawn scenes; charts only where QC requires.
- Series-only voice: younger and more human than the channel's documentary voice. Samples sent 2026-11-11
  (gpt-4o-mini-tts: verse, ballad, coral, echo, alloy, sage, marin, cedar, with a "young creator" instruction);
  the owner picks. Implemented as a per-project TTS override, so the channel default (ash) is unchanged.
- Public-figure caricatures (CEO etc.) appear where the narration names them (owner 2026-11-12); rules in docs/PRODUCTION_STANDARD.md "Real people". Nov 2026 edition: Musk in the Tesla episode; the Amazon script does not name Andy Jassy, so no caricature there.
