# Episode 02 - "How Dubai Really Makes Money": production, QC and cost report

Built 2026-11-03 with the existing pipeline (`python -m hiddeneco build how-dubai-really-makes-money
-d documentary yt_short ig_reel tiktok --tts openai --allow-paid`). Nothing was published.

## Deliverables (confirmed with ffprobe)

| File | Format | Duration | Target | Video / audio | Loudness | QC |
|---|---|---|---|---|---|---|
| `output/dubai_documentary.mp4` | 1920x1080, 16:9 | 690.1 s (11:30) | 600-720 s | H.264 / AAC 48 kHz | -16.2 LUFS | 0 errors, 21 warnings |
| `output/dubai_youtube_short.mp4` | 1080x1920, 9:16 | 44.3 s | 30-45 s | H.264 / AAC | -14.6 LUFS | 0 errors, 1 warning |
| `output/dubai_instagram_reel.mp4` | 1080x1920, 9:16 | 44.1 s | 30-45 s | H.264 / AAC | -14.6 LUFS | 0 errors, 3 warnings |
| `output/dubai_tiktok.mp4` | 1080x1920, 9:16 | 89.0 s | 65-90 s | H.264 / AAC | -14.7 LUFS | 0 errors, 5 warnings |

Each `output/dubai_*.mp4` is byte-identical to `output/how-dubai-really-makes-money/<id>/how-dubai-really-makes-money--<id>.mp4`.
Warnings are pace notes (numerals count as one word) and two number words ("one", "half") that are not statistics.

**Fixes made during production:** the reel (47.4 s) and the TikTok (92.1 s) first came out over their
limits with the slower `ash` voice; their closing call-to-action lines were shortened (no content
added, no speed-up). A timeline label collision (1979/1991) and a map label touching the chapter tag
were fixed and those two scenes re-rendered.

## Caption synchronisation

Measured against the narration-only track (per-segment voice audio placed on the timeline), not the music mix:

| Deliverable | Caption cues | Speech covered by captions | Median offset cue start vs voice onset | 90th percentile |
|---|---|---|---|---|
| documentary (SRT sidecar) | 294 | 100% | 0.05 s | 0.36 s |
| yt_short (burned-in + SRT) | 20 | 100% | 0.01 s | 0.29 s |
| ig_reel (burned-in + SRT) | 17 | 100% | 0.02 s | 0.18 s |
| tiktok (burned-in + SRT) | 37 | 100% | 0.03 s | 0.27 s |

Word timing inside a sentence is estimated (syllable-weighted); sentence boundaries are snapped to real
pauses in the paragraph audio.

## Thumbnails (original illustration, no photos, no logos)

| File | Size | Headline |
|---|---|---|
| `documentary_thumb_1_not_oil.png` | 1280x720 | NOT OIL? (footer: "95%+ of GDP is non-oil · Government of Dubai") |
| `documentary_thumb_2_the_real_money.png` | 1280x720 | THE REAL MONEY (port · airport · skyline) |
| `documentary_thumb_3_dubais_secret.png` | 1280x720 | DUBAI'S SECRET (bars = sourced GDP shares, H1 2026) |
| `*_thumb_cover.png` | 1080x1920 | Covers for the three verticals |

The tower is a generic stylised supertall, not a replica of Burj Khalifa (Emaar holds trademarks on its name and image).

## Cost

| Item | Provider | Units | USD |
|---|---|---|---|
| Narration - documentary | OpenAI `gpt-4o-mini-tts`, voice `ash` | 8,531 chars (39 requests) | $0.2559 |
| Narration - YouTube Short | same | 531 chars (5) | $0.0159 |
| Narration - Instagram Reel (incl. re-voiced trimmed lines) | same | 736 chars (7) | $0.0221 |
| Narration - TikTok (incl. re-voiced trimmed line) | same | 1,191 chars (8) | $0.0357 |
| **Total paid** | | **10,989 chars** | **$0.3297** of the approved **$0.60** cap |
| Rendering, maps, illustrations, music, SFX, fonts | local / original / public domain / OFL | | $0 |

Priced at the configured $0.030 per 1,000 characters (from search results, not OpenAI's page - confirm
on https://openai.com/api/pricing). Ledger: `output/how-dubai-really-makes-money/paid_spend.json`.
Per-deliverable `cost_report.md` files show 0 characters for the last run because every sentence came
from the audio cache; the table above is reconstructed from the ledger.

## Publishing status: BLOCKED (by design)

All 54 claims are `source_located` (found by web research; several primary pages returned 403 to
automated access). QC lists them as publish blockers: documentary 53, short 4, reel 7, TikTok 8.
A named reviewer must read each source, then set `status: human_verified` and `verified_by` in
`projects/how-dubai-really-makes-money/sources.yaml` and rebuild. Priority checks:

1. `sectors_h1_2026` and `gdp_h1_2026` - read the DDSE table (revised 2026 series).
2. `non_oil_share` - exact dubai.ae wording.
3. `war_2026` - attribution of the H1 2026 contraction (press reporting).
4. `reserves_split` - find a current UAE primary source (current one is US ITA citing a 2019 report).
5. `jafza_port_gdp` (government estimate, 36%) - attributed on screen.
6. `no_pit` - official UAE statement (currently PwC).
7. URLs marked "reconstructed" or "truncated" in `sources.yaml` notes (Gulf News Jebel Ali, WAM population).

## Package contents in this folder

`plan.md` (approved outline) · `dossier.md` (all sources and claims with status) · `script_*.md`
(full narration with the claim behind every number) · `metadata_*.md` (titles, description with
chapters, tags, platform captions) · `pinned_comment_documentary.md` (full source list; the description
uses a compact list to stay under YouTube's 5,000-character limit) · `qc_*.md` · `subtitles_*.srt` ·
thumbnails · contact sheets.

## Retrieving the files from the cloud environment

The MP4s are not in git (`output/` is ignored). They live only in this session's container:

- They were sent as file attachments in the chat. The documentary is also available as a lighter
  re-encode, `output/downloads/dubai_documentary_1080p_light.mp4` (1920x1080, 25.7 MB, same content),
  because the 355 MB master exceeds the attachment size the app shows a download button for.
- To regenerate them anywhere: clone the repo, `pip install -r requirements.txt`, install FFmpeg and
  run the build command above (narration cache is not in git, so a rebuild pays for narration again,
  about $0.33, and the cap still applies).
- The container is reclaimed after inactivity: download the files before ending the session.
