# Episode 57: How Costco Really Makes Money Selling Almost Nothing (owner request, 2026-11-17)

- Supersedes Ep 32 ("How Costco Makes Money Selling Things Cheap", left untouched). Runtime 12:01 (721.0 s), QC 0 errors
  (73 warnings: number-word reminders and 14 claims awaiting human sign-off), no freeze > 5 s, no black gaps, -16.1 LUFS.
  TTS US$0.28 (gpt-4o-mini-tts, voice ash). Light copy: `output/costco_v2_documentary_light.mp4` (master deleted after packaging).
  Short: `output/shorts/57-costco-v2_short.mp4` (59 s). Thumbnails: `youtube-package/thumbnail_face.png` (default, Ron Vachris
  bust), `thumbnail-alt-A.png`, `thumbnail-alt-B.png`. Publishing is manual; nothing uploaded.
- Project: `projects/how-costco-makes-billions-selling-almost-nothing`; storyboard generator `tools/gen_costco_v2_storyboard.py`
  (41 scenes + intro). Research `RESEARCH_NOTES.md`, checks `FACT_CHECK.md`, commercial gate `COMMERCIAL_BRIEF.md` (score 87),
  look `VISUAL_DIRECTION.md`.
- Format (owner): prime-time animated TV sitcom at genre level only. Cold open → channel intro as the theme → title card "THE
  CLUB" → five acts with bumpers → button. Running gag: the $1.50 hot-dog board nobody manages to change.
- New engine: `remotion/src/animation-engine/CartoonStage/costco.tsx` (sets clubfloor, memberdesk, foodcourt, housebrand,
  treasureaisle, loadingdock, gasbar, seattle83, cashvault, clubtitle, clubbumper; items cardie, membercard, combo,
  palletstack, receipt); toon cast BEV, HANK, PEARL, SKIP (sitcom.tsx); caricature/bust presets `vachris`, `sinegal`;
  thumbnail subject `hotdog`.
- Pipeline fix found here: the audio mix's `np.convolve` moving averages were O(N·w) and took hours on a loaded machine; now an
  O(N) cumulative-sum boxcar with identical output (`hiddeneco/audio.py`). Opt-in `HIDDENECO_REUSE_RENDER=1` reuses an
  identical Remotion picture (`hiddeneco/pipeline.py`).
- Limitations: hot-dog "since 1985" and both hot-dog quotes are secondary (CNN) and attributed; Kirkland ≈ $90B is a company
  statement; the FY2026 annual-report letter is not out yet. Claims await a named human reviewer.
