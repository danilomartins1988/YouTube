# Story over statistics (owner directive, 2026-11-18, permanent)

Owner: "the content feels dull, too many numbers and percentages, like a scientific research video. We need something
more commercial, fewer numbers, more narrative." This overrides any habit of listing every verified figure.

## Rules for every script
1. **One protagonist, one journey.** Every film follows a character or a concrete situation (a shopper, a factory
   manager, a family, a company founder, an object like one phone or one $100 bill) from the cold open to the payoff.
   The economics is what happens to them.
2. **Number budget:** at most **8–12 spoken numbers in the whole film**, and **never more than one number per scene**.
   Pick the 3–4 numbers that carry the story ("hero numbers") and repeat/visualize them instead of adding new ones.
3. **Prefer images and comparisons to statistics.** "Enough to buy every NFL team twice" beats "$148.6 billion".
   "One in every four" beats "24.7%". Round honestly ("almost half", "about $40 trillion"); keep exact values in
   FACT_CHECK.md and the description.
4. **No percentage chains.** Never stack two percentages in one sentence; never read decimals aloud unless the decimal
   is the punchline.
5. **On screen:** one big number at a time, animated as an event (a stack falling, a meter bursting), never tables or
   multi-bar charts with many labels. Charts get ≤3 labeled values.
6. **Scenes are story beats, not data beats.** Each scene = something happens (a decision, a surprise, a conflict, a
   reveal). If a scene's only job is to deliver a statistic, cut it or turn it into a moment.
7. **Dialogue and action:** characters speak short lines, react, argue, joke; the narrator connects. Every 45–90 s:
   a twist, a reveal or a complication.
8. **Depth moves to the description.** Full figures, sources and caveats live in the description and FACT_CHECK.md;
   accuracy rules are unchanged (verified, USD, estimates labeled), only the amount said out loud shrinks.
9. **Self-check before narration:** count numbers in the narration (`python tools/count_numbers.py <script or text>`);
   over budget → rewrite, don't trim words.

Commercial test for every scene: would a viewer who hates math still want to see what happens next?
