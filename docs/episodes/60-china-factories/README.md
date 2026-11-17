# Episode 60: Why the World Still Depends on Chinese Factories (owner request, 2026-11-17)

- **Runtime and QC:**
  - Runtime 11:53 (712.9 s).
  - QC 0 errors. There are 87 warnings: 63 are claims awaiting human sign-off, and the rest cover licensing notes, caption
    speed, presenter board p30 at 31.7 s and the sitcom-format similarity.
  - No freeze over 5 s; full decode is clean.
  - Loudness −16.1 LUFS.
- **Narration:** US$0.29 (gpt-4o-mini-tts, voice ash).
- **Outputs:**
  - Light copy: `output/chinafactories_documentary_light.mp4`. The full master was deleted after QC.
  - Short: `output/shorts/60-china-factories_short.mp4` (49 s).
  - Thumbnails: `youtube-package/thumbnail.png` = `thumbnail_face.png` (F, Mel + 27% tag, "MADE IN CHINA. STILL.");
    `thumbnail-alt-A.png` (parcels).
- **Docs:**
  - Package: `youtube-package/` (title, description, chapters, tags), `SEO_PACKAGE.md`, `COMMERCIAL_BRIEF.md`.
  - Facts: `RESEARCH_NOTES.md`, `FACT_CHECK.md`.
  - Generator: `tools/gen_chinafactories_storyboard.py` (37 scenes).
- **Format:** an Ep 56-style sitcom episode.
  - Cold open: Mel's toaster dies, and every appliance shows "Made in China".
  - The channel intro, then a title card ("STILL MADE IN CHINA").
  - Four act bumpers, in each of which a drone delivers the next toaster part ("FROM: DOWN THE STREET"; the running gag).
  - Boxes on legs that keep walking back home.
  - Button joke: the plug's tag.
- **Presenter boards:**
  - p08: world manufacturing bar;
  - p14: supplier cluster;
  - p25: who pays a tariff;
  - p30: import shares.
- **Post-render fix:** QC flagged a ¥ amount on screen in s11, which breaks the USD-only rule. Scene s11 was re-rendered with
  the same props and spliced into the master (video only, audio untouched), then QC was re-run.
- **Limitations:**
  - The IEA reports were read from full PDF copies because iea.org blocks automated access; a reviewer should re-check them.
  - The 2025/2026 import shares use the seasonally adjusted world total (labelled as our calculation).
  - The tariff rates are as of November 2026.
  - In s26 the chart panel is empty for about 2 s before its bars grow.
  - Publishing is manual; nothing was uploaded.
