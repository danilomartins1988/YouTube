# Episode 58: Why Americans Can No Longer Afford a Home (owner request, 2026-11-17; supersedes Ep 31)

- Runtime 11:47 (706.6 s), QC 0 errors (95 warnings: claims awaiting human sign-off, number words, 2 distinctiveness notes on
  the shared sitcom scene sequence), no freeze > 5 s, no black gaps; TTS US$0.31 total (gpt-4o-mini-tts, voice ash).
  Light copy: `output/housing_v2_documentary_light.mp4` (master deleted); Short: `output/shorts/58-housing-v2_short.mp4` (49 s).
  Thumbnails: `youtube-package/thumbnail.png` (F, face: Maya + $416,700 tag, "CAN'T AFFORD A HOME"), `thumbnail-alt-A.png`
  (padlocked house, "HOMES OUT OF REACH"), `thumbnail_face.png`.
- Gate docs: `COMMERCIAL_BRIEF.md` (score 88), `SEO_PACKAGE.md` (scorecard 86). Facts: `RESEARCH_NOTES.md`, `FACT_CHECK.md`.
- Project: `projects/why-americans-can-no-longer-afford-a-home`; storyboard generator `tools/gen_housing_v2_storyboard.py` (34 scenes).
- Format (Ep 56 sitcom model, genre level only, all original): cold open at an open house with a bidding war → channel intro →
  title card "STARTER HOME" → five acts with bumpers (running gag: the shrinking starter home) → the basement → end card →
  button joke. Fictional cast: Maya, Rex, DeeDee. No real people, no logos.
- New engine kit: `remotion/src/animation-engine/CartoonStage/housing.tsx` (sets openhouse, ratecoaster [track = Freddie Mac
  weekly data], lockstreet, shrinker, emptylot, zoningboard, basement; items minihome, placard, paddles, padlock, savejar,
  incomebars), registered in CartoonStage.tsx.
- Ep 31 files untouched. Publishing is manual; nothing uploaded.
