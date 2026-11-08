# Retroactive thumbnail report

- Deliverables discovered: **21** (15 long-form documentaries, 6 shorts/other)
- Documentaries with older thumbnails kept untouched: **6**
- New thumbnails generated (default + alternative): **13**
- Passed automated QC: **13**; every one still needs a human look (subject, tone, spelling, not misleading)
- Documentary deliverables without a brief (older cuts of the same story): `how-nvidia-took-over-the-ai-economy:documentary`, `why-switzerland-is-so-rich:pilot_horizontal`
- Missing package metadata (title/description/tags): the-day-volkswagen-became-the-most-valuable-company, the-hidden-business-of-formula-1
- Failed generation attempts: 0
- Image generation: none used. Backend `svg-composite` (original vector art rendered locally with Remotion), cost US$0.00. No AI image service is configured for thumbnails and the channel rule is free/open tools only.

## Per episode

| Episode | Default | QC | Design score A / B | Package | Files |
|---|---|---|---|---|---|
| How Dubai Really Makes Money | B | pass | 0.715 / 0.752 | ready | `docs/episodes/02-dubai/youtube-package/` |
| How Nvidia Took Over the AI Economy | A | pass | 0.726 / 0.682 | ready | `docs/episodes/06-nvidia/youtube-package/` |
| The $2 Billion That Never Existed | B | pass | 0.69 / 0.702 | ready | `docs/episodes/12-wirecard/youtube-package/` |
| The Cables at the Bottom of the Ocean That Carry the Internet | A | pass | 0.733 / 0.582 | ready | `docs/episodes/09-cables/youtube-package/` |
| The Day Volkswagen Became the World's Most Valuable Company | B | pass | 0.817 / 0.867 | in production | `docs/episodes/13-volkswagen/youtube-package/` |
| The Hidden Business of Formula 1 | A | pass | 0.721 / 0.634 | not ready | `docs/episodes/03-formula1/youtube-package/` |
| The Tiny Island Getting Rich From AI | A | pass | 0.728 / 0.694 | ready | `docs/episodes/10-anguilla/youtube-package/` |
| The Machine Only One Company on Earth Can Build | B | pass | 0.719 / 0.794 | ready | `docs/episodes/08-asml/youtube-package/` |
| Why Norway Is So Rich — The Secret Behind Its Oil Fortune | A | pass | 0.712 / 0.625 | ready | `docs/episodes/04-norway/youtube-package/` |
| Why Almost Half the World's Ships Fly Three Small Flags | A | pass | 0.695 / 0.616 | ready | `docs/episodes/11-flags/youtube-package/` |
| Why Switzerland Is So Rich | A | pass | 0.882 / 0.704 | ready | `docs/episodes/01-switzerland/youtube-package/` |
| Why Taiwan Matters So Much to the Global Economy (original cut) | B | pass | 0.556 / 0.705 | ready | `docs/episodes/07-taiwan/youtube-package/` |
| Why Taiwan Matters So Much to the Global Economy | A | pass | 0.653 / 0.646 | ready | `docs/episodes/07-taiwan-v2/youtube-package/` |

Contact sheets: `docs/thumbnails/contact_sheet.jpg` (default and alternative per episode) and `docs/thumbnails/contact_sheet_phone.jpg` (all defaults at phone size, to spot repetition).

Design scores are internal (contrast, legibility, clutter, distinctness) and do not predict click-through rate.
