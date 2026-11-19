# Thumbnail model chosen by the owner (2026-11-19, permanent)

Reference images (owner-made): `docs/thumbnails/owner_reference/` (09-cables, 10-anguilla, 11-flags, 07-taiwan-v2).
The owner's files are also stored in each episode as `youtube-package/thumbnail_owner.jpg` (1280×720, upload-ready) and
`thumbnail_owner_original.png`, and are the **default thumbnail** for those four episodes.

## The model (every new thumbnail follows it)
1. **Cinematic, high-saturation scene, not flat:** deep night-blue background with a glowing world map / network arcs
   or a dramatic real-world setting (ocean, coastline at sunset, skyline at dusk). Strong warm-vs-cool contrast
   (orange/gold light vs electric blue), glow, light rays, sparks, particles, bubbles, motion.
2. **One hero object, big, on the right half, breaking the frame:** the cable being cut, the ship with three flags,
   the chip + wafer + glowing island, the data center by the beach. It is the story's subject, lit dramatically.
3. **Text on the left, 2–3 words, huge:** heavy **italic** condensed caps (Inter Display Black Italic in our system),
   white with a thick black outline/shadow; one line sits on a **rough brush-stroke banner** in **red** or **yellow**
   (black text on yellow, black/white on red). A question mark is common ("CUT THESE CABLES?", "WHY THESE FLAGS?").
   Text and banner may tilt slightly; text fills ~45–55% of the width.
4. **A tension cue:** something about to happen (pliers on the cable, rising arrow/bars, glowing connections).
5. **Recognizable symbols are allowed and encouraged** when they ARE the subject (national flags, a country's
   outline in its flag colors, a famous skyline landmark). Respectful, never mocking. No company logos.
6. **Mobile test:** readable at 320×180; at most 4 words; the picture must tell the story without the title.

## How our pipeline implements it
- New archetype **`poster`** in the thumbnail system (see `hiddeneco/youtube_thumbnail.py` and
  `remotion/src/thumbnails/`): cinematic backdrop (night map with arcs / sunset coast / dusk skyline / deep ocean),
  hero object with rim light and glow, sparks/particles, BlackItalic text with brush banners (red or yellow).
- `poster` is the **default concept** for new episodes; `face` (character bust) stays available as an alternative
  when a person is central. Our art is illustrated/painted, not photographic: never imitate a real photo or a
  real company's imagery, and never fabricate a realistic image of a real person.
