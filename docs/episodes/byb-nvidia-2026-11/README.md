# Before You Buy: Nvidia (Nov 2026 edition)

Series "Before You Buy" (docs/series/BEFORE_YOU_BUY.md). Not a numbered channel episode. Rendered 2026-11-17/18 for
posting on Wed Nov 18, 2026 (upload stays manual).

- Project: `projects/before-you-buy-nvidia-2026-11` (alias `bybnvda`); generator `tools/gen_byb_nvidia_storyboard.py`
  (41 scenes; lint 0; strict cues 0 missing); series helpers `tools/byb_kit.py`. Voice alloy (tts_overrides).
- Result: 12:11 (730.9 s), QC 0 errors (85 warnings, 16 claims awaiting human verification), visual QC pass, no frozen
  picture > 5 s (ffmpeg freezedetect clean after the scorecard-board fix), -16.0 LUFS. Narration $0.32 (OpenAI
  gpt-4o-mini-tts, cached).
- Edition: DATA AS OF the Nov 17, 2026 close (the close BEFORE the results); latest report Q3 FY2027 (Oct 25, 2026). The
  Q3 10-Q is not filed yet: Q3 figures come from the Nov 17 8-K (release, CFO commentary, supplemental information).
- Method: P/E 16.6x (≈ 18.7x ex equity gains), FCF yield 4.0%, OCF yield 4.2%; base = TTM FCF $148.6bn (capex ≈ 6% of
  OCF). Reverse calculation: ≈ 5.6% (8%) to ≈ 10.3% (10%) FCF growth a year for 10 years, then 3%. All our calc.
- Real people: Huang only as the respectful caricature preset in the hook (8-K facts: resignation accepted Nov 11, no
  reason given); the leadership/investigation scene shows an empty chair, never the caricature. Kress and Jones in text.
- Files: COMMERCIAL_BRIEF.md, SEO_PACKAGE.md, FACT_CHECK.md, research notes docs/series/research/nvidia_2026-11.md,
  youtube-package/ (title, description, chapters, tags, thumbnail.png = face F, thumbnail-alt-A.png), youtube-short/.
- Video: output/bybnvda_documentary_light.mp4 (1280x720); full master deleted for disk (re-render: TTS is cached, $0).
  Build note: OMP_NUM_THREADS=1 makes `nproc` report 1 and Remotion refuses concurrency 4; build with a PATH shim
  whose nproc ignores OMP_NUM_THREADS.
