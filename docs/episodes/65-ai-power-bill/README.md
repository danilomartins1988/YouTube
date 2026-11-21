# Episode 65: AI Data Centers and Your Bill: Why Your Power Bill Could Explode (series "Who Wins and Who Loses in the AI Economy" #5)

> **Owner, set the title in YouTube Studio in a desktop browser.** The usual upload path truncates titles at 30 characters; the title
> "AI Data Centers and Your Bill: Why Your Power Bill Could Explode" is 47 characters (no em dash). Paste it from `youtube-package/title.txt`.

- Runtime 12:21 (741.0 s), QC 0 errors (29 warnings: 14 claims awaiting human sign-off, number-word notes, 5 caption-speed, 2 pace, 5
  scene-sequence similarity, 5 dataset licence notes), no freeze > 5 s, no black gaps, −16.2 LUFS. Narration US$0.28 (gpt-4o-mini-tts,
  voice ash, one take, 9,459 characters). Commercial score 90 (re-scored after the story-over-statistics rewrite); SEO score 88.
- Light copy: `output/aipowerbill_documentary_light.mp4` (master deleted). Shorts: `output/shorts/65-ai-power-bill_short.mp4`,
  `65-ai-power-bill-b_short.mp4`, `65-ai-power-bill-c_short.mp4` (scripts in `SHORTS.md`).
- Thumbnails (`youtube-package/`): default B "AI'S POWER BILL" (house beside an AI campus, `thumbnail.png`), A "AI VS YOUR BILL"
  (`thumbnail-alt-A.png`), C "WHO PAYS FOR AI?" (`thumbnail-alt-C.png`). Package: `title.txt`, `description.txt` (sources, key figures,
  chapters from the final timeline, related episodes by title), `chapters.txt`, `tags.txt`; 3 hashtags.
- Story: one protagonist, MAYA (fictional Virginia homeowner), follows her ~$150 bill; DEV (fictional lineworker) is the second voice.
  About 13 spoken statistics (docs/STORY_OVER_STATS.md); exact figures in `FACT_CHECK.md` and the description.
- Project: `projects/why-ai-could-make-your-electricity-bill-explode`; generator `tools/gen_aipowerbill_storyboard.py` (37 scenes, cue
  check built in); new kit `remotion/src/animation-engine/CartoonStage/powerbill.tsx` (sets pbtown, bigbill, auction, gridbuild, hearing,
  plantdeal, gaugeroom, pbtitle, pbbumper; items pbtag, billpaper, sparky), registered in CartoonStage.tsx.
- Presenter sequences: p04 (a new country of homes), p06 (follow the $150 bill), p17 (how building more becomes your bill), p23 (the
  line built for a data center that never comes).
- Differs from Ep 35 ("Why America's Electricity Bills Are Rising", linked by title): newer data (PJM 2028/29 auction, Market Monitor July
  2026, PJM 2026 forecast, Nov 2026 STEO) and new angles (large-load tariffs in Ohio and Virginia, the SCC cost study, 10-K capex, Big
  Tech's nuclear deals, LBNL/Brattle counterpoint).
- Docs: `COMMERCIAL_BRIEF.md`, `SEO_PACKAGE.md`, `RESEARCH_NOTES.md`, `FACT_CHECK.md`, `EDITORIAL_QC.md`, `SHORTS.md`,
  `VISUAL_DIRECTION.md`, `scene_manifest.json`, `visual_qc/`, `subtitles_en.srt`, `autocomplete_2026-11-18.txt`.
- Publishing is manual; nothing uploaded. Limitations: LBNL PDFs and Talen's release returned 403 (read via DOE, Brattle and APPA pages);
  the SCC order was read from an NPR-hosted copy with the SCC stamp.
