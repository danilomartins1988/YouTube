# Call to action standard: subscribe and like (owner, 2026-11-20, permanent)

**Status: approved by the owner on 2026-11-21** ("Aprovada a vinheta pedindo seguidores"). The narrated subscribe card before the channel intro is now the channel standard for every new film.

The owner's request: "We need to start having a call for the viewer to subscribe to the channel and hit like."
Before this date no film, Short or package asked for it. From now on every film does, in the ways below, and the build
does it for you.

## Principles (current YouTube practice)

- **Ask early, once, and briefly.** One sentence of about 6 to 8 seconds, after the cold-open hook has paid off. Viewers
  who stay past the hook are the ones who subscribe.
- **Tie it to the channel's promise, not to begging.** "If you like finding the hidden money behind the headlines…" is
  better than "please subscribe".
- **Ask for likes and comments at the end with a real question about the episode.** A specific question gets comments.
  A generic "let me know what you think" does not.
- **Show it as well as say it.** The animated SUBSCRIBE / LIKE widget plays while the line is spoken. It never covers key
  figures or captions.
- **No platform logos.** The widget is a generic red rounded pill, a thumbs-up and a bell, drawn in the channel's cartoon
  style. It does not use the YouTube logo or any other trademark.

## 1. Long films (16:9)

Structure: **hook → narrated SUBSCRIBE card → channel intro (vinheta) → documentary → narrated LIKE + COMMENT card →
teaser / end card (→ button joke, if any).**

| Moment | What | Length | How |
|---|---|---|---|
| Right **before** the channel intro | Narrated subscribe ask + full-frame animated card (`cta_card`, kind `subscribe`) | 6–8 s | automatic (`hiddeneco/cta.py`) |
| Right before the teaser / end card | Narrated like + comment ask with the episode question + card (kind `like`) | 5–8 s | automatic |
| Optional, any scene | Small corner widget (4 s, lower corner) over the picture | 4 s | storyboard `params.cta_overlay: {cue: "...", corner: right}` |

### Narrated wording

- **Subscribe (generic, fits every film):**
  > If you like finding the hidden money behind the headlines, hit subscribe and like. It really helps the channel.

  The scriptwriter may adapt it per episode in `project.yaml` (`cta.subscribe_line`). Keep it to one sentence that is tied
  to the story, for example: "If you like seeing who really pays for a deal like this, subscribe. It's free and it helps the
  channel."
- **Like + comment (end):** `If this changed how you see the story, tap like, and tell us in the comments: {question}`.
  Set the episode's question in `project.yaml` as `cta.like_question`, for example "would you pay the toll, or drive
  around it?". The default question is "what hidden business should we open up next?".

```yaml
# project.yaml (all optional)
cta:
  enabled: true
  subscribe_line: "If you like seeing who really pays for a deal like this, subscribe. It's free and it helps the channel."
  like_question: "would you pay the toll, or drive around it?"
  like: true
```

Voices follow the project's TTS settings. The default documentary voice is `ash`; the Before You Buy series uses `alloy`.

### How it is built (no manual work)

- `hiddeneco/cta.py` `insert_cta()` runs in `pipeline.prepare()` right after the channel intro is placed. It inserts the
  `cta_subscribe` segment before `channel_intro` and the `cta_like` segment before the `teaser` / end-card segment.
  Each segment has a `cta_card` scene. Neither is inserted twice. A script that already says "subscribe" or "tap like"
  keeps its own lines. It works with the Remotion renderer only, the same as the intro.
- The card is drawn by `remotion/src/brand/SubscribeCTA.tsx` (`CTACardArt`): the channel mascot, the big widget and two
  lines ("LIKE FINDING THE HIDDEN MONEY?" / "IT'S FREE · IT HELPS THE CHANNEL"). The like card reads "DID THIS CHANGE
  YOUR MIND? / TELL US IN THE COMMENTS".
- The optional corner overlay is the `CTAOverlayLayer` in `Documentary.tsx`, fed from `props.cta` by
  `remotion_bridge.build_props`.
- Storyboard and script generators need no changes. The pipeline adds both segments to every future build, so the
  generators' cue checks are unaffected.

## 2. The reusable channel asset

The widget is a dark rounded plate holding a thumbs-up button, a red SUBSCRIBE pill and a bell. A cartoon glove clicks the
thumb, which fills blue, then clicks the pill, which turns grey with "✓ SUBSCRIBED". The bell then pops in and rings.
Length 4 s, transparent background, readable on a phone.

| File | What |
|---|---|
| `assets/brand/cta/subscribe_cta_1080.webm` | 760×260, VP9 with alpha, for 1920×1080 |
| `assets/brand/cta/subscribe_cta_720.webm` | 506×174, VP9 with alpha, for the 1280×720 lights |
| `assets/brand/cta/subscribe_cta_preview.png` | preview frame |
| `assets/brand/cta/cta_clip_{ash,alloy}_720.mp4`, `cta_voice_*.wav` | narrated splice clips used by the retrofit (MP4 not committed; regenerable) |

Regenerate the assets with `python tools/render_cta_assets.py` (Remotion compositions `SubscribeCTA` and `CTACard`). Use
FFmpeg's `-c:v libvpx-vp9` decoder on the WebM so the alpha channel survives.

## 3. Shorts

- The end card reads FULL STORY ON THE CHANNEL / every figure sourced / **FOLLOW FOR MORE**, with the animated widget
  playing inside the white box (`tools/make_shorts.py`: `end_box()`, `CTA_WIDGET`).
- The description gets the line: "Follow The Hidden Economics for more of the hidden money behind the headlines."
  (`hiddeneco.cta.SHORT_FOLLOW_LINE`).

## 4. Description and pinned comment

- **Description:** add this line before the hashtags. `hiddeneco/metadata.py` and `youtube_thumbnail.package_texts()` add
  it automatically when it fits within 5,000 characters.
  > Subscribe to The Hidden Economics for a new animated documentary about the money behind the headlines. It's free, and it really helps the channel.
- **Pinned comment:** post this and pin it. The build writes it to `pinned_comment.md`.
  > If this one surprised you, tap like and subscribe: it helps more people find the channel.

  Add the episode question, plus the full source list when the description overflows.
- **End screen (Studio):** "Best for viewer" video + Subscribe element, as before.

## 5. Retrofit of finished, unpublished films (2026-11-20)

`tools/cta_retrofit.py` splices the narrated subscribe clip into the light MP4s right before the channel intro. It also
overlays the corner widget about 25 s before the end, in whichever lower corner is less cluttered and has no caption. It then
shifts `subtitles_en.srt` (adding a cue for the line), `chapters.txt`, the description chapters and `youtube_package.md`
by the inserted length. `python tools/cta_retrofit.py shorts <ep>…` swaps the Shorts' end card for the new one.
