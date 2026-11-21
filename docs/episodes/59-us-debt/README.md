# Episode 59: Who Owns America's Debt? It's Not Who You Think (owner request, 2026-11-17)

- Runtime 12:50 (770.2 s), QC 0 errors (90 warnings: licence notes on U.S. government datasets, since fixed in sources.yaml; 15 claims
  awaiting human sign-off; 1 pace and 1 caption-speed note), no freeze > 5 s, no black gaps, -16.2 LUFS; TTS US$0.30
  (gpt-4o-mini-tts, voice ash). Commercial brief: `COMMERCIAL_BRIEF.md` (score 82/100, honest; title crowded).
- **Known issue (fix ready, not re-rendered)**: in the CBO scene (≈ 11:38) the meter rolls to "$2,146B" under "CBO PROJECTION
  (FEB 2026)". That dollar figure is reported by search summaries of CRS but could not be verified on the source page, so the
  storyboard now keeps the meter at the FY2026 actual ($1,052B). A re-render with cached narration ($0) applies the fix. Light copy: `output/usdebt_documentary_light.mp4` (the full master is deleted after the light
  copy is made). Short: `output/shorts/59-us-debt_short.mp4`. Thumbnails: `youtube-package/thumbnail_face.png` (F, default:
  original taxpayer TED + giant IOU, "WHO OWNS US DEBT?") and the standard cinematic IOU concept (A).
- Title: the owner's "Who Actually Owns America's $Trillions in Debt?" with the verified figure: Treasury Debt to the Penny
  **$40,616,678,827,092.07 on Nov 13, 2026** -> "$40 Trillion" (rounded down; the total first passed $40T on Aug 18, 2026).
- Project: `projects/who-actually-owns-americas-debt`; storyboard generator `tools/gen_debt_storyboard.py` (44 scenes).
- **Neutrality rule (owner, "Sem viés político")**: strictly non-partisan. No party, president, administration or member of Congress
  is named, blamed or credited; no politician is drawn; no editorial adjectives; the debt's growth is shown only as sourced
  daily totals; whether the debt is "a problem" is not judged (CBO's projection is reported as a projection; interest is shown
  as both a cost to taxpayers and income to holders). Countries appear only as place cards (no flags). See `FACT_CHECK.md`.
- Owner direction: as animated as possible, like a prime-time TV cartoon sitcom, at genre level only (all characters, names,
  designs, title card text, captions and sound are original). Built as a TV episode: cold open in the IOU vault -> channel intro
  (the "theme") -> show title card ("WHO OWNS THE DEBT?", typed subtitle "Some Assembly, and Interest, Required") -> five acts,
  each opened by a rubber-stamped IOU bumper with a rotating joke caption -> payoff -> end card -> button joke (OWEN, swollen with
  interest, gets stuck in the vault door).
- Running gag: OWEN, a living IOU note, grows every act ($38T -> $39T -> $40T -> $40.6T -> "+ INTEREST").
- Cast (original, generic): TED (taxpayer), RUTH (retiree), the AUCTIONEER, dinner guests labelled only by place cards. No public
  figure is central, so none is drawn (no Treasury Secretary, no Fed Chair).
- New engine pieces: `remotion/src/animation-engine/CartoonStage/debt.tsx` (registered in CartoonStage with one small edit):
  sets `iouvault` (vault door + debt odometer + IOU press), `auctionhouse` (podium, paddle-raising bidder tiers, results board,
  SOLD!), `dinnerparty`, `mainstreet` (holders' street, bonds pop into the windows), `fedwarehouse` (shelves that thin out and
  refill, holdings gauge, bills conveyor), `trustcabinet` (drawer of IOU folders that empties through a tube to the Treasury),
  `meterscale` (interest meter vs a defense balance scale that tips), `debttitle`, `debtbumper`; items `owen`, `feast`,
  `ioustack`, `bondpop`. Thumbnail subject `iou` in `remotion/src/thumbnails/CinematicThumb.tsx`.
- Presenter boards (5): the IOU in two boxes; holdings to scale (bars + area); the savings loop; the trust fund round trip;
  federal outlays FY2026 (bars).
- Sources (primary): Treasury Debt to the Penny, MSPD, auction results, average interest rates and Monthly Treasury Statement
  (Fiscal Data); Treasury TIC Table 5 and history; Federal Reserve H.4.1 and Z.1; CRS reports reproducing the 2026 Social
  Security Trustees Report and CBO's February 2026 baseline (ssa.gov and cbo.gov refused automated access). Notes:
  `RESEARCH_NOTES.md`; checks: `FACT_CHECK.md`.
- Rules: every figure dated; TIC = custody-based (said on screen); shares, per-day figures and the rough ownership split are our
  calculations (labelled); CBO = projection (labelled); fiscal years labelled; jokes never change a number. Publishing is
  manual; nothing uploaded.
