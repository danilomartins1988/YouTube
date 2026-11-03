# QC report: why-switzerland-is-so-rich / extended_franc (extended_9x16)

- Runtime: **68.67 s**
- Video: 1080x1920 @ 30/1 h264, audio aac 48000 Hz, 35.4 MB
- Loudness: -14.5 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **2**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.

## Publish blockers - claims needing human verification

- `snb_floor_2011` (source_located): On 6 September 2011 the Swiss National Bank set a minimum exchange rate of CHF 1.20 per euro, saying it would no longer tolerate a EUR/CHF rate below it.  
  The ECB statement of 6 Sep 2011 quotes the SNB decision. Locate and cite the SNB's own press release of that date if possible.
- `snb_floor_end_2015` (source_located): On 15 January 2015 the Swiss National Bank discontinued the minimum exchange rate of CHF 1.20 per euro with immediate effect and ceased the associated foreign currency purchases; the franc appreciated sharply and markets were surprised.  
  Decision wording from SNB press-conference text (BIS). 'Appreciated sharply / surprise' is press coverage - keep it qualitative, no magnitude.
- `snb_floor_interventions` (source_located): According to the SNB (April 2015), the minimum exchange rate could only have been enforced through permanent currency interventions of rapidly increasing magnitude.  
  Confirm wording in the SNB speech of 24 April 2015.

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.
