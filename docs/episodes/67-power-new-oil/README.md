# Episode 67: Could Cheap Electricity Become the New Oil? (series "Who Wins and Who Loses in the AI Economy" #1)

> **Owner, set the title in YouTube Studio in a desktop browser.** The usual upload path truncates titles at 30 characters; the title
> "Could Cheap Electricity Become the New Oil?" is 43 characters (no em dash). Paste it from `youtube-package/title.txt`.

- Runtime 12:16 (736.2 s), QC 0 errors (30 warnings: 14 claims awaiting human sign-off, number-word notes, 2 caption-speed, 7 dataset
  licence notes, 5 scene-sequence similarity), no freeze > 5 s, no black gaps, -16.2 LUFS. Narration US$0.27 (gpt-4o-mini-tts, voice
  ash, one take, 9,035 characters). Commercial score 89 (honest; target 90); SEO score 87.
- Light copy: `output/powernewoil_documentary_light.mp4` (master deleted). Shorts: `output/shorts/67-power-new-oil_short.mp4`,
  `67-power-new-oil-b_short.mp4`, `67-power-new-oil-c_short.mp4` (scripts in `SHORTS.md`).
- Thumbnails (`youtube-package/`): default F face "POWER: THE NEW OIL?" (Nia + a giant plug drawn like an oil barrel, `thumbnail.png` /
  `thumbnail_face.png`), A "CHEAP POWER / NEW OIL?" (`thumbnail-alt-A.png`), B "AI FOLLOWS / CHEAP POWER" (`thumbnail-alt-B.png`).
  Package: `title.txt`, `description.txt` (sources, key figures, chapters from the final timeline, related episodes by title),
  `chapters.txt`, `tags.txt`; 3 hashtags.
- Story: one protagonist, NIA (fictional site scout), with CUBBY (the walking scale model of the campus); 11 spoken statistics
  (docs/STORY_OVER_STATS.md); exact figures in `FACT_CHECK.md` and the description.
- The answer: cheap power already decides where the next giant industry lands, as it did for aluminum smelters; but electricity can't
  be shipped, so the "new oil" is power you can plug into now, in big blocks, that a country is willing to share.
- Project: `projects/could-cheap-electricity-become-the-new-oil`; generator `tools/gen_powernewoil_storyboard.py` (35 scenes, cue check
  built in); new kit `remotion/src/animation-engine/CartoonStage/powermap.tsx` (sets pmoffice, pmmap, pmoil, pmsmelter, pmnorth, pmsun,
  pmtropic, pmqueue, pmscore, pmtitle, pmbumper; items pmtag, cubby), registered in CartoonStage.tsx; thumbnail face prop `plug` in
  `remotion/src/thumbnails/FaceThumb.tsx`.
- Presenter sequences: p07 (why the factory goes to the energy), p24 (the real price of a plug), p30 (oil's one market vs power's many).
- Overlaps: Ep 65 "Why AI Could Make Your Electricity Bill Explode" and Ep 04 "Why Norway Is So Rich" linked by title only; Ep 63's
  Brazil beat not repeated.
- Docs: `COMMERCIAL_BRIEF.md`, `SEO_PACKAGE.md`, `RESEARCH_NOTES.md`, `FACT_CHECK.md`, `EDITORIAL_QC.md`, `SHORTS.md`,
  `VISUAL_DIRECTION.md`, `scene_manifest.json`, `visual_qc/`, `subtitles_en.srt`, `autocomplete_2026-11-18.txt`.
- Publishing is manual; nothing uploaded.
