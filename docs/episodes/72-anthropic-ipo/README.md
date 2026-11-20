# Episode 72: Anthropic's $1.5 Trillion IPO: The AI Gold Rush or the Next Bubble? (owner brief, 2026-11-20)

> **Owner, set the title in YouTube Studio in a desktop browser.** The usual upload path truncates titles at 30 characters; the title is
> 67 characters (no em dash; its first 30 characters read "Anthropic's $1.5 Trillion IPO:"). Paste it from `youtube-package/title.txt`.

> **Logo deviation (please read).** The brief asked for the Anthropic logo in the centre of the primary thumbnail. The channel rule is no
> company logos, so the primary thumbnail uses a stylized golden ticker board reading **ANT** instead (and the film shows the company only
> by its ticker and plain-text plaques). If you want the official logo, add it yourself on top of `youtube-package/thumbnail.png` (the
> board sits right of centre, at about x 1150-1730, y 250-620 in the 1920x1080 master; the 1280x720 PNG scales by 2/3).

> **Neutrality.** Anthropic makes the AI model used to produce this episode. The film relies only on SEC filings (424B4, pricing FWP,
> Amazon and Alphabet 10-Qs) and named press reports, gives the bear case and the circular-financing criticism full weight, accuses no one
> of wrongdoing, and is not investment advice. The description carries a "not investment advice" line and a short production disclosure
> (remove the disclosure if you prefer; it is factual). See `EDITORIAL_QC.md`.

- STATUS_LINE
- Story: JUNE, a fictional nurse from Ohio, gets ONE SHARE at the $83 offer price; the share (a golden ticket with a face) is followed
  through the first day, the business, the compute bills, the money loop, who got rich, and the fork in the road. 14 spoken figures (≤1 per
  segment); all other figures on screen with claim pills and in the description.
- The answer: a share of one of the fastest-growing companies ever measured (revenue $41m in 2023 → $33.2bn in Jan-Sep 2026; operating cash
  flow positive), attached to ≈$900bn of compute promises and to partners on every side, priced at ≈20x its sales pace (our calc): neither a
  bubble by definition nor a sure thing. "Importance and investment returns are two different things."
- Key verified figures: offer $83 (range $70-78); 980m shares, $81.34bn, 97.6% primary / 2.4% sold by the seven co-founders; $26.0bn
  concurrent placement (total ≈$107.3bn); close $97.17 on Nov 19, 2026 (open $111.50); ≈$1.5tn fully diluted at $83, ≈$1.75-1.8tn at the
  close, ≈$1.27tn on outstanding shares (13.22bn shares; our check ≈$1.28tn). See `RESEARCH_NOTES.md` §3 for the reconciliation.
- Project: `projects/anthropics-1-5-trillion-ipo`; generator `tools/gen_antipo_storyboard.py` (43 scenes, cue check); new kit
  `remotion/src/animation-engine/CartoonStage/antipo.tsx` (14 sets + the `share` item), registered in CartoonStage.tsx; caricature presets
  `dario` and `daniela` (new `curly` and `long` hair); new poster heroes `tickerboard`, `warnchart`, `bubble`, `loop` in PosterThumb.tsx.
- Presenter sequences: p05 several price tags, p11 five scoreboards, p17 four words, p33 what the price assumes.
- Signature animations: the first-day screen, the revenue rocket, the dollar machine, the contract scroll, THE MONEY LOOP (s20-s23), the
  round table of investor-suppliers (s24), THE FORK of bright, middle and dark roads (s34-s37), the shovel shop (s39).
- Library: Ep 68 "The Countries That Could Win the AI Economy Without Building AI", Ep 28 "How Big Tech Really Makes Money From AI" (by
  title).
- Docs: `PRODUCTION_PROMPT.md`, `COMMERCIAL_BRIEF.md`, `SEO_PACKAGE.md`, `RESEARCH_NOTES.md`, `FACT_CHECK.md`, `EDITORIAL_QC.md`, `SHORTS.md`,
  `VISUAL_DIRECTION.md`, `scene_manifest.json`, `visual_qc/`, `subtitles_en.srt`, `narration_plain.txt`, `autocomplete_2026-11-20.txt`.
- Publishing is manual; nothing uploaded.
