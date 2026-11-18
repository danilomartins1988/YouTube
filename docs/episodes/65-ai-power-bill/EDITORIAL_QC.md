# Ep 65 editorial QC

| Check | Result |
|---|---|
| Runtime 660–800 s | 741.0 s ✓ |
| Pipeline QC | 0 errors; 29 warnings (14 claims awaiting human sign-off; number-word notes on "one/three/double/triple/third" used as words, not statistics; 5 caption-speed; c6_maya 191 wpm, c5_gs5 120 wpm; scene-sequence similarity 81–86% with five films, expected for the shared engine grammar; dataset licence notes for EIA public-domain data) |
| Freeze > 5 s / black gaps | none / none (post.sh freezedetect + visual_qc) |
| Loudness | −16.2 LUFS |
| Hook first, then channel intro | intro at 33.8 s after the hook ✓ |
| Presenter draws ≥3 substantial explanations | 4 boards (p04, p06, p17, p23) ✓ |
| Story over statistics | one protagonist (Maya) from cold open to payoff; ~13 spoken statistics (count_numbers.py reports 16, over-counting "three dials", "Three Mile Island", ordinals); ≤1 per segment; on screen one big number at a time, charts ≤3 labels |
| "could" vs "is" | title and forecasts use "could"/"forecast"; every forecast has a FORECAST pill; our calculations labelled OUR CALC; Market Monitor figures labelled ESTIMATE |
| Neutral tone | both sides: cost-shift risk and counterpoints (tech deals, tariffs, load growth lowering prices, new supply, PJM trimming its forecast); verdict is a three-dial framework, no advocacy |
| Real people / logos | no real person drawn (regulators and executives are silhouettes); companies named in narration only; no logos; generic buildings |
| USD only | ✓ |
| Overlap with Ep 35 | linked by title; no Ep 35 figure repeated in narration (Ep 35 used the 2025/26 jump and 4.4%→6.7–12% shares) |
| Title rules | no em dash; README tells the owner to set the 47-character title in YouTube Studio on desktop |
| Thumbnail | ≤4 words naming the subject (AI, bill); QC pass |
| Known cosmetic notes | brief overlap of two captions at the start of s28 (dials) and some static backgrounds in the hearing-room scenes (characters and props still move); accepted to avoid a second full render on a tight disk |
