# Retroactive thumbnail report

- Deliverables discovered: **21** (15 long-form documentaries, 6 shorts/other)
- Documentaries with older thumbnails kept untouched: **6**
- New thumbnails generated (default + alternative): **13**
- Passed automated QC: **13**; every one still needs a human look (subject, tone, spelling, not misleading)
- Documentary deliverables without a brief (older cuts of the same story): `how-nvidia-took-over-the-ai-economy:documentary`, `why-switzerland-is-so-rich:pilot_horizontal`
- Missing package metadata (title/description/tags): the-hidden-business-of-formula-1
- Failed generation attempts: 0
- Image generation: none used. Backend `svg-composite` (original vector art rendered locally with Remotion), cost US$0.00. No AI image service is configured for thumbnails and the channel rule is free/open tools only.

## Per episode

| Episode | Default | QC | Design score A / B | Package | Files |
|---|---|---|---|---|---|
| Dubai Isn't Rich Because of Oil. Here's What Pays the Bills | B | pass | 0.715 / 0.791 | ready | `docs/episodes/02-dubai/youtube-package/` |
| From Video Games to AI: How Nvidia Became a $5 Trillion Company | A | pass | 0.691 / 0.618 | ready | `docs/episodes/06-nvidia/youtube-package/` |
| The $2 Billion That Never Existed | B | pass | 0.69 / 0.702 | ready | `docs/episodes/12-wirecard/youtube-package/` |
| The Cables at the Bottom of the Ocean That Carry the Internet | A | pass | 0.733 / 0.582 | ready | `docs/episodes/09-cables/youtube-package/` |
| The Day Volkswagen Became the World's Most Valuable Company | D | pass | 0.798 / 0.74 / 0.843 / 0.776 | ready | `docs/episodes/13-volkswagen/youtube-package/` |
| Who Really Makes Money From Formula 1? | B | pass | 0.72 / 0.634 | not ready | `docs/episodes/03-formula1/youtube-package/` |
| The Tiny Island Getting Rich From AI | A | pass | 0.728 / 0.694 | ready | `docs/episodes/10-anguilla/youtube-package/` |
| The $250 Million Machine Every Advanced Chip Depends On | A | pass | 0.719 / 0.794 | ready | `docs/episodes/08-asml/youtube-package/` |
| How Norway Turned Oil Into a $2 Trillion Fortune | C | pass | 0.676 / 0.579 / 0.691 | ready | `docs/episodes/04-norway/youtube-package/` |
| Why Almost Half the World's Ships Fly Three Small Flags | A | pass | 0.695 / 0.616 | ready | `docs/episodes/11-flags/youtube-package/` |
| The Hidden Formula Behind Switzerland's Wealth | C | pass | 0.882 / 0.704 / 0.785 | ready | `docs/episodes/01-switzerland/youtube-package/` |
| Why Taiwan Matters So Much to the Global Economy (original cut) | B | pass | 0.556 / 0.705 | ready | `docs/episodes/07-taiwan/youtube-package/` |
| The Small Island the Whole World Economy Depends On | B | pass | 0.641 / 0.646 | ready | `docs/episodes/07-taiwan-v2/youtube-package/` |

Contact sheets: `docs/thumbnails/contact_sheet.jpg` (default and alternative per episode) and `docs/thumbnails/contact_sheet_phone.jpg` (all defaults at phone size, to spot repetition).

Design scores are internal (contrast, legibility, clutter, distinctness) and do not predict click-through rate.
