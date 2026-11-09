# Episode 29: Why Americans Pay So Much for Healthcare (US batch #01)

- Project: `projects/why-americans-pay-so-much-for-healthcare`; storyboard generator `tools/gen_healthcare_storyboard.py` (37 scenes).
- New rules applied (see `docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md`):
  - Cold open on $28,303 with an itemized bill unrolling.
  - Four hook beats and a promise.
  - Channel intro after part 1.
  - One visual language per part: bill; data charts; hospital corridor; two patients; pharmacy; evidence board.
- New engine pieces:
  - `hospital` set;
  - `medbill` item (itemized bill);
  - `pills` item (pill bottle with price tag).
- Thumbnails: A = split (others vs USA), B = bignum ($28,303).
- Sources: CMS NHE, Peterson-KFF, RAND (hospital prices round 5.1; drug prices 2022), JAMA 2018, KFF EHBS 2026.
  - CMS and OECD-basis figures are never mixed in one sentence.
  - The employer share on screen ($20,832) is computed as $28,303 − $7,471.
