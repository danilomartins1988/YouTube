# Architecture and implementation plan

## Goals and constraints

- Produce an original, engaging 8–12 minute documentary from a selected topic with minimal human
  editing. The human work goes into editorial judgement, not timeline fiddling.
- Run locally with free, open-source parts. Paid services are optional adapters that stay off by
  default.
- Make factual integrity something the pipeline enforces, not just a guideline.

## Key design decisions

| Decision | Why |
|---|---|
| Editorial content lives in plain YAML per project (`sources`, `script`, `storyboard`) | Diffable and reviewable in git. A person can see exactly what changed between versions. |
| Numbers are placeholders resolved from the dossier | Unsourced statistics become a build error instead of a review burden. |
| Claim status ladder (`data_derived` → `human_verified` → `source_located` → `needs_verification`) | Says honestly what has been checked. Web-search hits never count as verified on their own. |
| Data: official API → licensed mirror → committed snapshot | Builds stay reproducible offline. The dossier records which route produced each value. |
| One TTS file per segment, scene length derived from audio | Picture and voice stay in sync by construction. Changing the voice re-times the whole film. |
| Pillow renders frames and pipes raw RGB into FFmpeg | No GUI editor, no proprietary renderer. Deterministic, testable and fast enough (about 2.5-3x real time on 4 cores). |
| One topic, several deliverables, each with its own script | A vertical video tells its own story instead of being a crop of the long one. They share the dossier, so facts stay consistent. |
| Layouts adapt to the format; vertical layouts respect UI safe zones | One component library serves 16:9 and 9:16. Captions and key content avoid the areas platform UI covers. |
| Sentence-level TTS with a cache | Sentence timing is exact, and editing one line only re-voices that sentence (cost control for paid voices). |
| Music and sound effects synthesised in code | No licence risk and no library fees. Every episode can use its own progression or palette. |
| Scene types are classes; a project's look comes from its `style` block | New grammar (timelines, flows, route maps) slots in without touching other scenes. Each episode gets its own identity. |
| QC splits technical errors (block approval) from publish blockers (unverified claims) | You can preview a draft before research is finished, but you can't publish one. |
| Approval stores the video's SHA-256 | If anyone edits the video after approval, publishing is refused. |
| No upload code | Prevents accidental publishing. YouTube API upload can be added later behind the same approval check. |

## Stage contracts

1. **Topics**: `config/topic_candidates.yaml` → ranked `topics.md`. The weights are explicit. Scores
   are judgements with written reasons.
2. **Dossier**: `sources.yaml` → `dossier.json`. It is validated before anything else runs: unique
   ids, a URL on every source, a known source on every claim, and a reviewer name on every
   `human_verified` claim.
3. **Script**: `script.yaml` plus the dossier → rendered text. Typed digits are an error and number
   words are a warning. Each placeholder must be declared in its segment's claims list.
4. **Storyboard**: one scene per segment, with params resolved from the dossier. Each scene lists
   its sources (shown on screen as credits) and its assets (checked against the licence manifest).
5. **TTS**: `TTSProvider.synthesize(text, wav)`, normalised to 48 kHz mono with silence trimmed.
   Results are cached by text, provider and options.
6. **Render**: one MP4 per scene, then concat, then mux with loudness-normalised narration
   (−16 LUFS). SRT captions are written alongside.
7. **Packaging**: three thumbnail concepts, title options and a description with chapters (checked
   against YouTube's chapter rules), sources, licence credits and a synthetic-voice disclosure.
8. **QC → approval → publish package.**

## Roadmap

### Phase 1: working pilot (done)
Horizontal 16:9 film (82 s) and vertical 9:16 short (33 s) with burned-in captions, from one
dossier. Includes QC, export drafts, a cost report, a build manifest and 39 tests.

**Open items before anything is published:**
- Verify the 6 `source_located` claims by reading the primary pages.
- Optionally switch the voice to Kokoro.

### Phase 2: reusable production engine
1. **Full documentary.** Five or six acts, 8-12 minutes, with a cold open and a counterpoint act.
   It reuses the deliverable structure (`format: long_16x9`, `target_seconds: {min: 480, max: 720}`).
2. **Three vertical videos per topic.** Two 30-45 s shorts and one 65-90 s `extended_9x16` for
   TikTok, each with its own hook and story.
3. **Forced alignment** (for example a local whisper.cpp model) for word-exact captions and cues.
4. **New scenes:** line chart over time (the snapshot already holds 2000-2023), flow or Sankey for
   trade, route map, document-quote card for primary-source excerpts, comparison split-screen.
5. **Research assistant.** Optional LLM drafting for topic ideas and script first drafts. Its
   output enters as `needs_verification` and can never bypass the claim gate. It runs only behind
   an explicit cost approval.
6. **Topic discovery signals.** Use official APIs only (YouTube Data API search results,
   Google Trends where permitted), stored with timestamps. Without them, the report keeps saying
   "editorial judgement", never invented numbers.

### Phase 3: web dashboard
FastAPI + HTMX + SQLite, running locally or on one small server. Features:
- topic picker
- deliverable selection
- dossier and script review with claim-level verify buttons (named reviewer)
- start or rebuild jobs (a background worker running the same CLI)
- live job status and the cost ledger
- in-browser preview
- approve or reject with notes
- downloads of export packages

### Phase 4: distribution and analytics
- Optional uploads through official APIs (YouTube Data API; TikTok and Instagram content-publishing
  APIs where the account qualifies). Uploads go out as private or draft by default and run only
  after `check_approved()`.
- Analytics module: impressions, CTR, retention, watch time, subscribers and revenue, pulled only
  from connected official analytics APIs and joined with the cost ledger per video. If no data is
  connected, it shows nothing rather than estimates.

## Budget guardrails (initial budget BRL 10,000)
- Phases 1-3 can run at $0 in recurring cost: local CPU, open-source tools, local voices.
- First likely spends, each needing approval: a premium voice once the format proves itself,
  optionally a small VPS for the dashboard, and the domain or branding.
- Every paid call is preceded by `estimate` and requires `--allow-paid`; actual usage is logged
  per video.
