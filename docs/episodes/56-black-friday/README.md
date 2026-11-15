# Episode 56: How Black Friday Actually Makes Money (owner request, 2026-11-15)

- Post window: Nov 20-23, 2026 (Black Friday is Nov 27, 2026). Publishing is manual; nothing uploaded.
- Project: `projects/how-black-friday-actually-makes-money`; storyboard generator `tools/gen_blackfriday_storyboard.py` (43 scenes).
- Owner direction: feel like an actual episode of a prime-time animated TV sitcom, at genre level only (all characters, names,
  designs, title card text, captions and sound are original). Built as a TV episode: cold open gag at the 5 a.m. mall ->
  channel intro (the "theme") -> show title card with a typed joke subtitle -> five acts, each opened by a bumper with a rotating
  joke caption and a chase gag -> payoff -> end card -> button joke ("THIS VIDEO: WAS $0 · NOW $0").
- New engine pieces (`remotion/src/animation-engine/CartoonStage/sitcom.tsx`, registered in CartoonStage): the `toon` character rig
  (squash-and-stretch entrances, anticipation hops, double-takes, walk/run cycles with smears, speed lines and dust, blinking,
  lip-flap `talk` windows, faces happy/grin/panic/smug/shock/deadpan/angry/dizzy/worry/dollar/love, held props); recurring cast
  GLORIA (store manager), DASH (deal-hunter), TAGBOT (price-tag printer robot; its ever-growing "WAS" tags are the running gag),
  BUZZ (drone), LIFT (forklift); items `stampede`, `bubble`, `heapcart`, `bigtag`, `feeflow`, `toonwords`; sets `megamall`,
  `storefloor`, `philly61`, `tvfactory`, `quarterhq`, `payrails`, `bnplride`, `adarena`, `returnsmtn`, `titlecard`, `bumper`;
  camera whip-pans with speed lines and directional blur (CartoonStage); a `sitcom` tone (tone.tsx, visual direction, music mood);
  `bigchart` panel option; thumbnail subject `bftag`. Dev preview: `tools/stage_preview.py` + `StagePreview` composition.
- Sources: Adobe Analytics (Dec 2025, Jan 2026, Sep 2026 forecast), NRF (weekend survey; returns report with Happy Returns),
  U.S. Census Bureau (Q4 2025 e-commerce), Best Buy 10-K and Q4 FY26 release, Target 10-K, Amazon 10-K, Federal Reserve
  (Regulation II 2023 data), CFPB (BNPL 2022), Consumer Reports (2018), Abito & Salant (Review of Economic Studies, via Kellogg
  Insight), Which? (UK), History.com, Philadelphia Inquirer. Notes: `RESEARCH_NOTES.md`; checks: `FACT_CHECK.md`.
- Rules: our calculations labelled (Best Buy shares, 81.7% offline); 2026 = forecast; Which? = UK-only; warranty margins = academic
  estimate; no logos, no real people; jokes never change a number.
