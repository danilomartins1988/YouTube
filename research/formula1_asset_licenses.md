# Asset licences: "The Hidden Business Behind Formula 1" (Episode 05)

Checked 2026-11-05. This covers every visual and audio element in `output/formula1_documentary.mp4`.

## Summary

| Element | What it is | Origin | Licence / rights |
|---|---|---|---|
| Race cars (side view) | Generic open-wheel car, `remotion/src/components/RaceCar.tsx` | Drawn in code by this project | Original work, owned by the channel |
| Trackside scene (grandstand, crowd, kerbs, skyline) | `remotion/src/scenes/RaceScenes.tsx` (`RaceTrack`) | Drawn in code | Original work |
| Circuit layout | Fictional track path `CIRCUIT` (not a real circuit) | Drawn in code | Original work |
| Sponsor boards | Placeholder text only ("YOUR BRAND", "SPONSOR", "PARTNER", "PADDOCK CLUB", …) | Drawn in code | Original work; **no real logos** |
| Whiteboard hand and marker | `Hand` in `remotion/src/scenes/Whiteboard.tsx` | Drawn in code | Original work |
| Whiteboard drawings (car, revenue model, circuit) | Strokes traced progressively by the hand | Drawn in code | Original work |
| Charts, counters, timelines, diagrams, icons (TV, flag, sponsor card, "F1" circle) | `remotion/src/scenes/*.tsx` | Drawn in code | Original work. The red "F1" circle is a plain label, not the official F1 logo. |
| World map (expansion scene) | Natural Earth 1:50m Admin 0 Countries, pre-projected (`assets/geo/remotion_world.json`) | naturalearthdata.com | Public domain |
| Typeface | Inter / Inter Display (Rasmus Andersson) | rsms.me/inter, system install | SIL Open Font License 1.1 |
| Handwriting font fallback | 'Comic Neue' / 'Segoe Print' are requested; neither is installed in the render environment, so Inter is used | — | OFL-1.1 (Inter) |
| Music bed and sound effects | Synthesised in code by the pipeline (`hiddeneco/audio.py`; manifest entry `audio:original_sound_design`) | Generated locally | Original work |
| Narration | OpenAI `gpt-4o-mini-tts`, voice `ash` | OpenAI API (paid, within the USD 1.00 cap) | Output owned by the user under OpenAI's terms. The video should disclose that the voice is AI-generated. |
| Rendering software | Remotion 4.0.535 | remotion.dev | Remotion licence. The free tier allows commercial video for individuals and companies with up to 3 employees; a larger company would need a Company Licence. |
| FFmpeg (encode and mux) | ffmpeg | ffmpeg.org | LGPL/GPL tool; the output video is not covered by its licence |

## What was not used, and why

- **No photographs, broadcast footage or press images.** There is no licensed stock library or authorised image source in this repository. Images found through web search are not assumed to be free to use, and copyrighted F1 broadcasts were not scraped.
- **No AI image generation.** The project has no authorised image-generation integration. The OpenAI key is authorised for voice only, so creating images would have been an unauthorised paid call.
- **No official marks.** No F1 / FOM logo, team logos, liveries, sponsor logos, real car designs, real circuit layouts or imitations of F1 broadcast graphics. Team and company names appear only as plain text in factual statements.
- **No paid music, footage or APIs.** Total non-voice spend is USD 0.

## Third-party names

The film names Formula 1, the FIA, Liberty Media, MotoGP, Netflix, Apple, ESPN, LVMH, Aramco, Mercedes, Red Bull Racing, Ferrari, Cadillac, CVC and Forbes as factual references (nominative use). The video is independent and does not suggest any affiliation or endorsement.

## Data and text sources

All figures and their sources are listed in `research/formula1_sources.md`, which is generated from `projects/the-hidden-business-of-formula-1/sources.yaml`. Currency conversions use the US Federal Reserve H.10 series (public domain, US government work).
