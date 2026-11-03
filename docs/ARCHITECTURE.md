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
| Pillow renders frames and pipes raw RGB into FFmpeg | No GUI editor, no proprietary renderer. Deterministic, testable and fast enough (about 2.5x real time on 4 cores). |
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

## Roadmap to the full 8–12 minute documentary

**Before production (editorial)**
- Clear the six `source_located` claims in the POC by reading the primary documents.
- Expand the dossier with the open questions in `sources.yaml`: banking secrecy and its erosion,
  the Swiss franc and the SNB, counter-arguments (cost of living, inequality, concentration in a few
  firms), and GDP versus GNI versus PPP measures.
- Write an approximately 1,500-word script in five or six acts, with a cold open and a counterpoint
  act so the episode is analysis, not promotion.

**Engineering (in priority order)**
1. Piper as the default local voice, with a per-project voice choice. Optional paid voice after the
   cost estimate and approval.
2. Forced alignment (for example aeneas or whisper timestamps) for word-accurate cues and captions.
3. New scene types: timeline, line chart over time (the snapshot already holds 2000–2023), flow or
   Sankey for trade, map with animated routes, and a document-quote card for primary-source excerpts
   with their citation.
4. Original music bed: generated locally or taken from a licensed library recorded in the manifest,
   with ducking under narration.
5. Optional LLM drafting adapters for topic ideation and first-draft scripts. Their output enters as
   `needs_verification` and never bypasses the claim system.
6. A storyboard linter that suggests variation when consecutive scenes share a type, plus a visual
   diff of episodes for the distinctiveness check.
7. Optional YouTube Data API upload behind `check_approved()`, uploaded as *private* by default.

**Estimated cost of the full documentary**: $0 with local voices. With a paid voice, it is the
per-character price times about 9,000 characters (see `python -m hiddeneco estimate`). No cloud
infrastructure is needed.
