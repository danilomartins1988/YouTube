# Analysis: hooks, thumbnails and visual diversity (2026-11-09)

Based on 27 episodes, 26 Shorts and the 30 thumbnail briefs in the repo. Measured on the storyboards and timelines.

## 1. The first 30 seconds (hooks)

What the data shows:
- 15 of 26 openings start with "What if…" (or "What happens when…"). The pattern is now predictable.
- The hook is two scenes: a 7–10 s question, then ONE 30–36 s stakes scene in one world with 2–3 callouts. That is slow for the moment when most viewers decide whether to stay.
- The strongest number arrives late. In oil, −$37.63 comes at ~25 s; in nickel, $101,365 at ~25 s.
- Then come ~20 s with little information: the channel intro (5 s), the act card (5.4 s) and the part question (9 s), around 40–63 s. In nickel the channel intro even interrupts the hook at 9 s.

Improvements (rules for the next scripts):
1. **Cold open with the image and the number in the first 3 s**, then the question. Example: "On April 20, 2020, a barrel of oil cost minus $37.63." (image: the screen crossing zero), and only then "How?".
2. **Rotate 6 hook types** (never two episodes in a row with the same one): shocking number; scene in motion (in medias res); contradiction ("Dubai isn't rich because of oil"); a real quote; "the mistake" (someone did X and lost Y); a challenge to the viewer ("Guess…").
3. **Hook = 5–7 cuts in 30 s** (one idea every 4–6 s) instead of one 30 s scene.
4. **An explicit promise by 20 s**: say what the viewer will understand by the end ("…and why the same thing can happen again").
5. **Channel intro: move it to after the first act (~1:30) or shorten it to 2 s**, and never inside the hook. The first part's card + question should become a single 4 s cut.
6. Shorts: hook text stays on screen for the whole Short (already the case); add a "loop" ending that sends viewers back to the start.

## 2. Thumbnails

What the data shows:
- All of them use the same composition: 2 lines of text on the left, one object on the right with a radial glow, and the "THE HIDDEN ECONOMICS" tag at the top.
- 17 of 30 use an empty background ("void"). 8 reuse the `crash` line, 9 reuse `bignum`.
- Concepts A and B differ almost only in colour and text, so the A/B test tests little.
- There is no human face or emotion, even though the channel has its own character (the presenter).

Improvements:
1. **6 layout archetypes**, with A and B always from different archetypes:
   - (a) a giant number filling 60% of the frame;
   - (b) before → after (split screen);
   - (c) the presenter with a strong reaction plus the object (original character, no real person);
   - (d) a zoom/map with a red circle and arrow on the detail;
   - (e) an object in danger (cracking, burning, sinking);
   - (f) an absurd comparison (scale, size).
2. Subject at 55–70% of the area, cut off by the frame edge (closeness), not floating small in the middle.
3. At most 3 words, and they must never repeat the title. The title and the thumbnail complement each other.
4. Remove the brand tag from the corner (it takes space and reads as noise at 160 px). Use a coloured edge per series instead.
5. A real background for the scene (a city, the sea, a factory) instead of "void" in most cases.
6. New automatic QC: block reused support items (crash/bignum) from the last 5 episodes, and require A and B to have different archetypes.

## 3. Visual diversity (the "videos look alike" problem)

What the data shows:
- **Identical skeleton in every episode:**
  - 5 act cards, 4 kinetic transitions, 3–5 boards and ~25 cartoon scenes;
  - every part opens with the same "question" scene (zoom 1.25 → 1.0, gold balloon at the top).
- **Text:** 40–66 pill-shaped callouts per episode, almost all centred at the bottom of the screen, in the same format.
- **Same visual vocabulary:** the same flat style and generic `person` (14–26 per episode), plus `letters`, `calendar` and `counter` in every episode.
- **Same camera:** "start close → pan to the side".

Improvements (in order of impact):
1. **Rotating scene "languages", 2–3 per episode, never the same combination twice in a row:**
   - maps with routes and zoom (MapScene already exists);
   - a full-screen chart (the line growing with its own camera);
   - an evidence board (documents, photos, red string), for fraud and scandals;
   - a split screen (two sides at the same moment);
   - an animated generic interface (inspired by apps and terminals, never a real UI);
   - isometric/miniature (a city or factory seen from above);
   - paper cut-out/collage (texture, shadows);
   - big typography (full-screen kinetic numbers).
2. **Text where it belongs:**
   - speech balloons coming out of the characters;
   - labels attached to the objects;
   - occasional lower thirds;
   - giant numbers integrated into the scene.
   Callouts at the bottom: at most 1 in 3 scenes.
3. **Skeleton variation:** the part's question doesn't always need its own scene (use it as a voice-over over action). Use different act cards per episode (newspaper, file folder, map, screen).
4. **Camera:** a library of 8 moves (whip pan, dolly-in, tilt-down, orbit, tracking with a character, push to a detail, rack focus, still shot with movement inside the frame), with a QC rule that no move repeats in consecutive scenes.
5. **Cast:** 3–4 recurring characters with their own silhouettes (trader, worker, regulator, consumer) instead of the same generic person.
6. **Presenter (done now):**
   - anatomical arms (sleeve, cuff, hand, at most 6% stretch);
   - a telescopic marker/pointer when the drawing is out of reach;
   - he steps aside during pauses and at the end, so the diagram is visible.
   Next: 2 more poses (sitting on the edge of the board, walking into the scene) and a "walk into the scene" between the board and the cartoon.

## 4. Suggested order of work
1. Hook rules + rotation of hook types in the script template (immediate, $0).
2. Thumbnails: archetypes (a)–(f) in `CinematicThumb` plus the new QC (1–2 days of work, $0).
3. Visual diversity: evidence board + full-screen chart + split screen as new scene types, plus a camera rule in QC.
4. Short endings with a loop.
