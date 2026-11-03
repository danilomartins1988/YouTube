# QC report: why-switzerland-is-so-rich / short_secrecy (short_9x16)

- Runtime: **46.93 s**
- Video: 1080x1920 @ 30/1 h264, audio aac 48000 Hz, 22.5 MB
- Loudness: -14.4 LUFS integrated, true peak -4.3 dBFS
- Errors: **1**, warnings: **2**
- Technical QC passed: **False**
- Publishable (no unverified claims): **False**

## Issues

- [ERROR] (timing) Runtime 46.9s outside target 30-45s
- [WARNING] (timing) Segment law pace 110 wpm (numerals count as one word)
- [WARNING] (timing) Segment number pace 100 wpm (numerals count as one word)

## Publish blockers - claims needing human verification

- `aeoi_2018` (source_located): In 2018 Switzerland exchanged financial account information automatically with partner states for the first time, covering around 2 million financial accounts (FTA release, 5 October 2018), under the global AEOI standard.  
  Title of the FTA release says 'around 2 million financial accounts'. Partner count differs between sources (36 vs 38) - deliberately not used.
- `banking_act_1934` (source_located): The 1934 Federal Act on Banks and Savings Banks (in force 1 March 1935) made breaching banking secrecy a criminal offence (Article 47); before that, banking secrecy was protected by civil law.  
  Secondary sources (academic chapter + law firm). Ideally confirm against the Act's text on fedlex.admin.ch (Article 47) and cite it.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.
