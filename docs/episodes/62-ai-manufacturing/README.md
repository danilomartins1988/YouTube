# Episode 62: Could AI Make American Factories Cheaper Than China's? (arc Episode 2; owner brief 2026-11-18)

Episode 1 of the arc: Ep 60 "Why the World Still Depends on Chinese Factories" (`docs/episodes/60-china-factories`).

- **Runtime and QC:** 11:45 (704.9 s); QC 0 errors, 26 warnings (15 spoken number words in the illustrative model and story
  lines, 7 dataset-licence notes, 2 pace notes, 2 scene-grammar similarity notes); 14 claims awaiting human sign-off. No freeze
  over 5 s, no black gaps, −16.1 LUFS, no clipping.
- **Narration:** gpt-4o-mini-tts, voice ash, American English. Paid total **US$0.87** across three takes (cap $1.00): take 1
  (784.6 s, over the 13-minute target), take 2 (tempo 1.07, 757.4 s), take 3 = the story-over-stats rewrite (final).
- **Story-over-stats:** protagonist Mel (Ep 60's shopper) decides to build her own toaster factory in Ohio; 14 spoken numbers by
  `tools/count_numbers.py` (budget 10-15), at most one per scene; at most three labelled values on screen at a time. Exact
  figures live in `FACT_CHECK.md` and the description.
- **Outputs:** light copy `output/aimfg_documentary_light.mp4` (1280x720; master deleted after packaging). Shorts:
  `output/shorts/62-ai-manufacturing-b_short.mp4` (Short 2, "China Already Has More Factory Robots Than You Think", publish
  first), `62-ai-manufacturing_short.mp4` (Short 1), `62-ai-manufacturing-c_short.mp4` (Short 3); see `SHORTS.md`.
- **Thumbnails** (`youtube-package/`): default **C** "CHEAPER THAN / CHINA?" (`thumbnail.png`; two original factories and a
  question-mark cost meter), alternates `thumbnail-alt-A.png` "CHINA'S END?" and `thumbnail-alt-B.png` "AI FACTORIES / COMING
  BACK?". No logos, no flags, no numbers; distinct from Ep 60.
- **Title:** "Could AI Make American Factories Cheaper Than China's?" (`youtube-package/title.txt`; backup "Could AI End
  China's Manufacturing Dominance?"). **The owner's upload path truncates titles at 30 characters: set the full title in YouTube
  Studio in a desktop browser.**
- **Docs:** `COMMERCIAL_BRIEF.md` (89 → 91 after the rewrite), `SEO_PACKAGE.md` (84 pre-score → 88; gap to 90 documented),
  `RESEARCH_NOTES.md`, `FACT_CHECK.md`, `EDITORIAL_QC.md`, `VISUAL_DIRECTION.md`, `scene_manifest.json`, `visual_qc/`,
  `subtitles_en.srt`, `youtube_package.md`, `autocomplete_2026-11-18.txt`.
- **Engine:** generator `tools/gen_aimfg_storyboard.py` (42 scenes, 6 presenter boards); new kit
  `remotion/src/animation-engine/CartoonStage/automation.tsx` (ohiobot us/cn, billbox, toastlab, robotrace, chainweb,
  moneyriver, aititle, aibumper; items torq, humanoid, pricemeter), registered in `CartoonStage.tsx`; thumbnail subjects
  `robofactory`, `megafactory`, `costmeter` in `CinematicThumb.tsx`.
- **Brief vs standing rules (flagged):** (1) thumbnail B's words "FACTORIES COMING BACK?" became "AI FACTORIES COMING BACK?"
  because the standing rule requires CHINA or AI on the thumbnail; (2) the hook runs about 35 s (brief: 20-30 s) because it
  introduces Mel and the Episode 1 link before the title question; (3) the coordinator's title upgrade replaced the brief's
  primary title, which is kept as the backup.
- **Limitations:** IEA rare-earth figure reused from Ep 60 (read from a PDF copy; re-check on iea.org); Japan's 38% robot-
  production share is the IFR's July 2025 preliminary figure (no newer one located); China's robot density uses a new IFR
  employment base, so no comparison with older editions is made; the Census payroll share is from 2021, the last ASM year; a
  few on-screen captions sit close to the factory board in the Act 2 recap. Publishing is manual; nothing was uploaded.
