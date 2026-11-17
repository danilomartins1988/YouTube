# Episode 61: Why Are Chinese Cars So Cheap — And So Advanced? (owner PRIORITY brief, 2026-11-17)

- Runtime 12:09 (728.6 s), QC 0 errors (63 warnings: 55 claims awaiting human sign-off, 4 caption speed, 3 pace, 1 sequence
  similarity), no freeze > 5 s, no black gaps, −16.1 LUFS. TTS US$0.60 total (gpt-4o-mini-tts, voice ash; two takes: the first ran
  747 s of voice, so 45 words were trimmed and a 1.08 atempo added; one 183-char re-take for the USD-only hook). Commercial score 92.
- Light copy: `output/chinesecars_documentary_light.mp4` (master deleted). Shorts: `output/shorts/61-chinese-cars_short.mp4` (54 s),
  `61-chinese-cars-b_short.mp4` (53 s), `61-chinese-cars-c_short.mp4` (48 s); scripts in `SHORTS.md`.
- Thumbnails (`youtube-package/`): A default "$9,900? CHINESE EV" (`thumbnail.png`), B split "$9.9K vs $56K", C "WHO PAYS FOR IT?",
  F face (Wang Chuanfu bust) `thumbnail_face.png`. Package: title/description (key sources)/chapters/tags.
- Project: `projects/why-are-chinese-cars-so-cheap`; generator `tools/gen_chinesecars_storyboard.py` (55 scenes); engine kit
  `remotion/src/animation-engine/CartoonStage/cars.tsx` (generic original cars; sets evshow, costlab, gigaline, cellplant,
  chainvalley, cashworks, pricestreet, carport, tariffgate, c61title, c61bumper; items evcar, suspects, cellbot, coinrain); busts
  `wangcf`, `leijun`; thumbnail subject `evhatch`.
- Docs: `COMMERCIAL_BRIEF.md`, `RESEARCH_NOTES.md` (dossier), `FACT_CHECK.md`, `EDITORIAL_QC.md`, `VISUAL_DIRECTION.md`,
  `scene_manifest.json`, `visual_qc/`, `subtitles_en.srt`.
- Production note: the render's audio-mix step stalled for hours when two builds ran in parallel (numpy convolutions with
  multi-threaded BLAS oversubscribed the 4 cores). It was finished with `OPENBLAS_NUM_THREADS=1` (4 min). The USD-only fix re-rendered
  only the 7 changed scenes and spliced them frame-exactly into the earlier silent render (21,859 frames).
- Publishing is manual; nothing uploaded. Limitations: see `RESEARCH_NOTES.md` (IEA mirror PDF, Ford/VW via secondary pages, BYD Q3
  2026 via press, SNE via CnEVPost).
