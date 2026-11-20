# Before You Buy: Anthropic (Nov 2026 edition)

Series "Before You Buy" (docs/series/BEFORE_YOU_BUY.md). Not a numbered channel episode. A practical buyer's checklist on Anthropic
(Nasdaq: ANT) the day after its IPO; deliberately NOT a repeat of Ep 72 (`docs/episodes/72-anthropic-ipo`, the IPO documentary).

> **Owner, please read: disclosure line.** Anthropic makes the AI model used to produce this film. As in Ep 72, the film says so (spoken
> and on screen in the disclaimer scene) and the description carries: "Disclosure: AI tools, including Anthropic's Claude, are used in
> producing this channel. This video relies only on public filings and named press reports; Anthropic did not sponsor, review or approve
> it." It is factual; remove or edit it if you prefer (the spoken line would need a re-render, TTS cached except that segment).

> **Title.** "Anthropic Stock Before You Buy: 7 Things to Check (Nov 2026)" (60 characters, no em dash). The app's 30-character cut reads
> "Anthropic Stock Before You Buy". Paste from `youtube-package/title.txt`.

- Project `projects/before-you-buy-anthropic-2026-11` (alias `bybant`); script generator `tools/gen_byb_anthropic_script.py`; storyboard
  generator `tools/gen_byb_anthropic_storyboard.py` (45 scenes, cue check built in); new CartoonStage items in
  `remotion/src/animation-engine/CartoonStage/bybant.tsx` (checklist, classcards, floodgates, ipopath, govtower); new poster heroes
  `padlock` and `clipboard` (PosterThumb.tsx). Voice **alloy** (tts_overrides).
- Result: **12:26 (746.1 s)**, target 660-800 s (series 11-13 min); QC 0 errors (29 warnings), no frozen picture ≥ 5 s, no silence > 2.5 s,
  -16.1 LUFS. Narration **US$0.31** (gpt-4o-mini-tts, 10,229 characters); the fix re-render cost $0.
- Edition: DATA AS OF the Nov 19, 2026 close (first trading day; the Nov 20 session had not closed); latest filing the 424B4 dated Nov 18, 2026.
- Story: Maya (fictional would-be buyer) and her clipboard of seven questions. **13 spoken figures**, at most one per segment (FACT_CHECK.md).
- Light copy: `output/bybant_documentary_light.mp4` (1280x720, 29 MB). **Master deleted** after the light copy and Shorts (disk); rebuild at
  no TTS cost with `OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m hiddeneco build before-you-buy-anthropic-2026-11 -d documentary --tts openai --allow-paid` (≈35 min).
- Shorts (`SHORTS.md`): `output/shorts/byb-anthropic-2026-11_short.mp4` (44 s, lock-up), `..._-b_short.mp4` (47 s, votes),
  `..._-c_short.mp4` (44 s, first report card). B and C use a wider centre crop (new `CROPS` override in `tools/make_shorts.py`) so the class
  cards and the presenter board stay in frame.
- Thumbnails (`youtube-package/`): default P `thumbnail.png` = `thumbnail_poster.png` "BEFORE YOU / BUY ANTHROPIC"; A `thumbnail_poster_A.png`
  "THE BIG / UNLOCK" (padlock, MAY 17); B `thumbnail_poster_B.png` "7 THINGS / TO CHECK"; contact sheet `thumbnail_contact_sheet.jpg`. No logos.
- Package: `title.txt`, `description.txt` (≈4,980 characters, "NOT INVESTMENT ADVICE", date line, disclosure, sources, 3 hashtags),
  `chapters.txt` (from the final timeline), `tags.txt`.
- Docs: `COMMERCIAL_BRIEF.md` (87), `SEO_PACKAGE.md` (85), `FACT_CHECK.md`, `EDITORIAL_QC.md` (neutrality check), `SHORTS.md`,
  `scene_manifest.json`, `visual_qc/`, `subtitles_en.srt`, `narration_plain.txt`, `autocomplete_2026-11-20.txt`; research notes
  `docs/series/research/anthropic_2026-11.md`.
- Claims awaiting human verification: 7 (`source_located`); clear them in `sources.yaml` after a named review.
- Publishing is manual; nothing uploaded.
