# The Hidden Economics: production pipeline

A local-first system that turns a researched topic into an original, sourced, 1920x1080 YouTube
documentary using Python and FFmpeg. Nothing is bought, deployed or published without a person
approving it.

**First deliverable:** a 60–90 second proof of concept, *Why Switzerland Is So Rich*
(`projects/why-switzerland-is-so-rich/`). It renders to an 84.7-second MP4 with an animated map,
a bar chart, kinetic typography, a ring chart, a pictogram and a ranking. Every number comes from the
research dossier.

---

## Principles

1. **No invented facts.** Narration and on-screen numbers are templates such as
   `{{gdppc_che_2023}}`, filled in from the dossier. QC fails the build if anyone types digits into
   the narration.
2. **Verification is a status.** Each claim is marked `data_derived`, `human_verified`,
   `source_located` or `needs_verification`. Only the first two can be published.
3. **Original visuals only.** Every frame is drawn by code from licensed data, using public-domain
   Natural Earth maps, CC BY 4.0 World Bank data and the OFL Inter font. Footage is never used unless
   it is listed in `assets/manifest.yaml` with a licence on the allowlist.
4. **Distinct episodes.** Each project sets its own palette, type pairing and motifs. QC warns when
   a new storyboard's scene sequence is too close to an earlier one.
5. **People make the final call.** `approve` needs a named reviewer, a clean QC report and no
   unverified claims. `publish` only builds an upload folder. It never calls YouTube.
6. **Secrets stay in the environment.** API keys are read from environment variables or `.env`,
   which is git-ignored.

## Architecture

```
config/topic_candidates.yaml ──► research/topics.py ──► output/topics/topics.md   (10 scored topics)

projects/<slug>/
  project.yaml      style, target length          ┐
  sources.yaml      sources + claims + data specs ├─► research/dossier.py ──► dossier.json/.md
  script.yaml       narration templates           │        ▲ research/data_sources.py
  storyboard.yaml   scene per segment             │          World Bank API → licensed mirror → snapshot
                                                  ▼
                       script.py  (placeholder rendering, unsourced-number checks)
                       storyboard.py (params ← dossier values)
                                                  ▼
                       tts/  espeak | piper | elevenlabs* | openai* | silent      (*paid, opt-in)
                         one WAV per segment → exact durations → timeline.json
                                                  ▼
                       render/scenes.py  map · bar_chart · kinetic_text · ring_stat ·
                                         pictogram · ranking · end_card · title_card
                       render/assemble.py  Pillow frames ──pipe──► FFmpeg x264 per scene
                                           concat + loudness-normalised narration ► MP4 + SRT
                                                  ▼
                       thumbnails.py (3 concepts) · metadata.py (titles, description, chapters)
                                                  ▼
                       qc.py  timing · media · sources · licensing · distinctiveness · format
                                                  ▼
                       approval.py  approve (named reviewer, SHA-256 of video) → publish package
costs.py   per-step cost ledger (unknown prices stay "unknown")
logging_setup.py   JSON-lines logs in output/<slug>/logs/run.jsonl
```

Each scene lasts exactly as long as its narration plus a lead-in and a tail, rounded to whole frames,
so the picture and the voice cannot drift apart. In-scene animations are tied to cue phrases
(`cue: "In 1815"`). The time of a cue is estimated from where the phrase sits in the narration
text.

## Project structure

```
hiddeneco/            Python package (python -m hiddeneco ...)
  research/           topics, dossier, data access, number formatting
  tts/                TTS adapter interface + providers
  render/             style, drawing primitives, map projection, scenes, FFmpeg assembly
  script.py storyboard.py thumbnails.py metadata.py qc.py approval.py costs.py pipeline.py cli.py
config/               settings.yaml (video/TTS/pricing/licensing/QC), topic_candidates.yaml
projects/<slug>/      everything editorial for one video (all text, all reviewable in git)
assets/               manifest.yaml (licence register), geo/ (Natural Earth subset)
data/snapshots/       committed data snapshot + PROVENANCE.md, for reproducible offline builds
tests/                pytest suite (offline)
docs/                 ARCHITECTURE.md (decisions, roadmap to the full documentary)
output/               generated (git-ignored)
```

## Setup

Requirements: Python 3.10+, FFmpeg and espeak-ng. Piper is optional and gives a better free voice.

```bash
# 1. System tools
#   Ubuntu/Debian: sudo apt install ffmpeg espeak-ng fonts-inter
#   macOS:         brew install ffmpeg espeak-ng && brew install --cask font-inter
#   Windows:       winget install Gyan.FFmpeg  +  espeak-ng installer from its GitHub releases
#                  + install Inter from https://rsms.me/inter/
#   (Without Inter the renderer falls back to DejaVu Sans or Pillow's built-in font.)

# 2. Python environment
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configuration (optional; only needed for Piper or paid TTS)
cp .env.example .env

# 4. Check
python -m hiddeneco tts-check
python -m pytest -q
```

**Better free voice (recommended):** `pip install piper-tts`, then download a Piper voice: an `.onnx`
file plus its `.onnx.json` (see https://github.com/rhasspy/piper/blob/master/VOICES.md). Check the
voice's MODEL_CARD for its licence. Set `PIPER_VOICE_PATH` in `.env` and build with `--tts piper`.

## Running the proof of concept

```bash
python -m hiddeneco topics                                   # 10 scored topic proposals
python -m hiddeneco estimate why-switzerland-is-so-rich      # cost estimate BEFORE building
python -m hiddeneco research why-switzerland-is-so-rich      # dossier only
python -m hiddeneco build why-switzerland-is-so-rich         # full build (espeak voice, ~2-4 min)
python -m hiddeneco build why-switzerland-is-so-rich --tts piper   # nicer free voice
python -m hiddeneco build why-switzerland-is-so-rich --scenes s03_1815   # re-render one scene
python -m hiddeneco qc why-switzerland-is-so-rich            # re-run QC
python -m hiddeneco approve why-switzerland-is-so-rich --reviewer "Your Name"
python -m hiddeneco publish why-switzerland-is-so-rich       # builds an upload folder, never uploads
python -m hiddeneco data refresh                             # refresh the data snapshot
```

The build writes these files to `output/why-switzerland-is-so-rich/`:

| File | What it is |
|---|---|
| `why-switzerland-is-so-rich.mp4` | 1920x1080, 30 fps, H.264 + AAC, loudness-normalised |
| `subtitles.srt` | Captions |
| `research/dossier.md` | Claims, statuses and sources (URL, published date, access date) |
| `script/script.md` | Rendered script with source notes per segment |
| `storyboard/storyboard.md` | Scene-by-scene plan with sources and assets |
| `thumbnails/thumb_*.png` + `thumbnails.md` | Three 1280x720 thumbnail concepts |
| `youtube_metadata.md` | Five title options, a description with chapters, sources and credits, and tags |
| `qc/qc_report.md` | QC issues plus the claims that block publishing |
| `cost_report.md` | Cost per step |
| `logs/run.jsonl` | Structured logs: one JSON event per line, with timings |

### Clearing the approval gate

The QC report lists claims that are still `source_located`. For each one:

1. Open the URL in the dossier and read the primary source.
2. Edit `projects/<slug>/sources.yaml`. Set `status: human_verified` and `verified_by: <name>`.
   If the source says something different, correct the claim instead, or cut it from the script.
3. Rebuild, then run `approve`.

## Cost estimate

| Item | Proof of concept (~85 s, ~1,200 characters) | Full documentary (8–12 min, ~7–11k characters) |
|---|---|---|
| Research data (World Bank, Natural Earth) | $0 | $0 |
| Rendering (local CPU, ~2.5 min for the POC on 4 cores) | $0 | $0 (roughly 20–35 min of CPU) |
| Voice: espeak-ng or Piper (local) | $0 | $0 |
| Voice: OpenAI `tts-1-hd` (opt-in) | ~$0.04 | ~$0.22–0.32 |
| Voice: ElevenLabs (opt-in) | depends on plan | depends on plan |

Paid prices come from `config/settings.yaml` and are **marked unverified**. Check the vendor's
pricing page and update `verified_on` before you rely on them. Run `python -m hiddeneco estimate
<slug>` to recompute the estimate from the real script length.

## Adding a new video

```bash
cp -r projects/why-switzerland-is-so-rich projects/<new-slug>
# Edit project.yaml (new palette/motifs), sources.yaml, script.yaml, storyboard.yaml
python -m hiddeneco research <new-slug> && python -m hiddeneco build <new-slug>
```

Set `format: documentary` and `target_seconds: {min: 480, max: 720}` for a full episode.

## Known limitations (v0.1)

- espeak-ng sounds robotic. Use it for timing and layout drafts. Use Piper or an approved paid voice
  for anything released.
- Cue timing comes from character position, not forced alignment. It is good to roughly half a
  second.
- The words-per-minute QC check undercounts numerals (one token like "100,000" counts as one word),
  so pace warnings on number-heavy segments are often harmless.
- Topic scores are editorial judgements, not audience data. Adding a YouTube or search-trends
  signal is on the roadmap.
- Script writing is human-authored in YAML. An LLM drafting adapter is on the roadmap, and its
  output would enter as `needs_verification`.
