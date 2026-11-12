# Episode 53: Nvidia's CEO crisis (follow-up to Ep 52)

- Owner request 2026-11-12: a NEW video after the second NYT report and the board meeting, instead of editing Ep 52.
- Project: `projects/nvidia-ceo-crisis-second-report`; generator `tools/gen_nvceo_storyboard.py` (37 scenes; lint 0; strict cues 0 missing).
- Facts: `docs/episodes/52-nvidia-probe/RESEARCH_NOTES.md` (all sections incl. "Update 2026-11-12"). Voice: channel default (ash).
- Status: storyboard validated, style previews in `style_preview/`. **Not rendered** — renders after the Nov 12 US close or a board
  decision, whichever comes first.

## Before rendering (TO UPDATE)
1. `projects/nvidia-ceo-crisis-second-report/sources.yaml`, claim `cum`: spoken / display / fields (`asof_spoken`, `price_spoken`,
   `pct_spoken`) with the Nov 12 close or the decision-time price. Default = premarket Nov 12, 7:03 a.m. ET, $160.27, ≈ -$636bn.
2. `tools/gen_nvceo_storyboard.py`: `CUM_BN`, `LATEST`, `ASOF` (same numbers; drive the counters, the bar board and labels).
3. `project.yaml` → `ending: pending | stays | out`. For `stays`/`out`, first replace every `[TO UPDATE ...]` in
   `endings.yaml` with sourced facts and add the source to claim `oust`; the generator refuses unfinished text and copies the
   chosen ending into `script.yaml` (segment `m_end`).
4. Re-check the board/8-K/newsroom status, Huang statements, and the House deadline outcome; then
   `python tools/gen_nvceo_storyboard.py`, lint, strictcue, validation, and queue the slug.
5. Pick the final title (see `$SP/nvceo_titles.txt`) and run thumbnails/package as usual.

## Rules applied
- The second person is never named, drawn or described beyond "an Nvidia vice president who reports to him"; on screen: "we don't
  name her · she is not accused of anything".
- The first woman: silhouette only, "unnamed · per press reports"; spy claim alleged; China denies; nobody charged.
- Board ouster = WSJ/Semafor reporting; meeting confirmed by CNBC; interim CEO + search firm = Bloomberg report; Colette Kress only as
  Semafor's report (text, not drawn); never "fired".
- Huang caricature (respectful), lawmakers in text only; their calls labelled opinions.
- Market values: our estimate, price × 24.1bn shares, with the time of the price; after-hours/premarket labelled.
