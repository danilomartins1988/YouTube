# The Hidden Economics: YouTube SEO, Discovery & Organic Growth — Master Directive

Owner directive, 2026-11-17. **Permanent; applies automatically to every future video.** Works together with
`docs/COMMERCIAL_DIRECTIVE.md` and `docs/PRODUCTION_STANDARD.md`. Never sacrifice accuracy, originality or viewer
satisfaction for clicks. Primary audience: United States; secondary: other English-speaking markets.

## Operational summary

- **Before scripting**, save `docs/episodes/<ep>/SEO_PACKAGE.md` (template: `docs/templates/SEO_PACKAGE.md`) with the
  15 required items (§14). It can share evidence with `COMMERCIAL_BRIEF.md`; both are required.
- **Data access in this pipeline (be honest about it):**
  - YouTube autocomplete (US, en): **available** via `python tools/yt_autocomplete.py "<seed>" [--expand]`; record the
    collection timestamp. It shows what people type, **not volumes**.
  - Google Trends: **not available** programmatically here (API refuses automated requests). Demand history is a
    labeled **qualitative** assessment unless the owner supplies a Trends export.
  - YouTube search results / competitors: use web search or public pages when reachable; public view counts and dates
    only. Never infer competitors' CTR, retention or revenue.
  - YouTube Analytics / vidIQ: **not available** unless the owner exports data. Log real data in `docs/ANALYTICS_LOG.md`.
- **Never invent** keyword volumes, Trends scores, competitor metrics, chapters, sources or video links. Related-video
  links only with verified published URLs (otherwise list the episode title as "coming soon"/omit).
- **After rendering:** regenerate chapters from the final timeline, finalize description/tags, update the SEO package.
- **Alignment rule (§10):** primary keyword, title, thumbnail, opening hook and film carry the same promise.
- **Never** publish or modify live YouTube videos without authorization.

## SEO & Commercial Scorecard (pre-production, target ≥85; editorial estimate, not a probability)

| Criterion | Weight |
|---|---:|
| Search demand and keyword relevance | 20 |
| Browse and Suggested audience appeal | 20 |
| Title and thumbnail potential | 20 |
| Evergreen demand | 15 |
| Narrative and retention potential | 15 |
| Competitive differentiation | 10 |
| **Total** | **100** |

---

## Full directive (owner's text, condensed only in formatting)

**Role:** Senior YouTube Growth Strategist, SEO Specialist, Audience Researcher and Packaging Director. Maximize:
qualified organic impressions; CTR; retention and watch time; Search traffic; Browse and Suggested traffic; evergreen
views over 6–24 months; returning viewers and subscribers; sustainable monetization potential.

### 1. Research search demand before production
Investigate YouTube autocomplete; Google Trends (12 months and 5 years); Google Search trends; YouTube search results;
comparable documentaries; competitor titles and thumbnails; recurring viewer questions; related terms; channel
analytics when available. Prioritize US demand. Distinguish **evergreen** (recurring for years), **emerging** (growing
long-term) and **trending** (temporary spike). Prefer evergreen and emerging for most production; don't mistake a
short spike for durable demand. If reliable volume data is unavailable, label the assessment qualitative. Never
invent keyword volumes or Trends scores.

### 2. Keyword research
One primary keyword; five secondary; ten long-tail; five audience questions; related entities (companies, products,
countries, concepts); search intent for each. Relevance to the actual film first; no stuffing; natural American
English. Select by relevance, intent and evidence, not by how popular it sounds.

### 3. Title optimization
Ten candidates: three search-oriented, three curiosity-driven, two hybrid SEO+curiosity, two alternative creative.
Evaluate search relevance, clarity, curiosity, emotional stakes, broad appeal, distinctiveness, accuracy, evergreen
potential. Prefer recognizable subjects + compelling questions (weak: "The Economics of Chinese Electric Vehicle
Manufacturing"; better: "Why Are Chinese Cars So Cheap — And So Advanced?"). No misleading exaggeration; never claim a
CTR. Select one primary and two backups. Around 45–65 characters when practical (not a rigid rule).

### 4. Thumbnail optimization
Three concepts per film: one clear idea, readable on mobile, curious but not misleading, complements (doesn't repeat)
the title, recognizable subjects where appropriate, channel identity, minimal text/clutter. Compare with competing
thumbnails without copying compositions. Prepare alternatives for YouTube's thumbnail test when available. Don't
assume complexity raises CTR.

### 5. SEO-optimized description
Natural American English. (a) Opening paragraph ~100–160 words with the primary keyword near the start; (b) the major
questions addressed, with secondary keywords without repetition; (c) chapters matching the final render; (d) related
videos from the channel, verified published URLs only; (e) credible sources; (f) a concise channel description. No
keyword lists disguised as prose; never fabricate sources, chapters or links.

### 6. Tags and hashtags
Primary topic, recognizable companies, industry terms, close search variations, useful alternative spellings. Tags
play a limited role (YouTube); don't rely on them. Up to three highly relevant hashtags in the description.

### 7. Optimize for recommendations
Serve browsers, not only searchers: broad curiosity, strong title-thumbnail pair, deliver the promise early, no
unnecessary intro, narrative progression, discoveries throughout, natural pacing, satisfying conclusion. Keywords must
never make narration unnatural; the film must work for someone who knows nothing about the subject.

### 8. Evergreen strategy
Prioritize how major companies make money; why industries are dominated by a few; hidden business models; economic
paradoxes; global supply chains; financial crises and mechanisms; economics of technology; why countries get rich or
poor; consumer prices and incentives. Don't rely on news cycles. Assess relevance at 6, 12 and 24 months; date
time-specific figures without making the whole film obsolete.

### 9. Competitor analysis
5–10 competing videos when accessible: titles, thumbnails, dates, durations, public view counts, positioning,
questions answered, gaps. Don't infer private metrics. Win with more audience value, not copying.

### 10. Search intent and content alignment
Primary keyword, title, thumbnail, hook and film share one promise (e.g. keyword "why are chinese cars so cheap" →
title "Why Are Chinese Cars So Cheap — And So Advanced?" → hook on the price/tech contradiction → investigation of
subsidies, efficiency, batteries, integration, margins, cash burn → conclusion weighing the mechanisms). Never optimize
metadata for subjects the film doesn't meaningfully cover.

### 11. Shorts discovery
Three Shorts per film, each a distinct question or insight: strong hook, concise standalone narrative, accurate
curious title, description, relevant hashtags, natural link to the full film. Not random cuts; independently
understandable and entertaining.

### 12. Post-publication optimization
When analytics are accessible: 48 h, 7, 30, 90, 180 days — impressions, CTR by traffic source, average view duration,
retention, search terms, Browse and Suggested, returning viewers, subscribers, long-tail daily views. Compare with the
channel's baseline and similar videos. A 48-hour impressions drop is not automatically an SEO problem: diagnose topic
demand vs packaging vs audience fit vs retention vs normal distribution. Recommend changes only when supported by data;
don't churn metadata without a clear hypothesis.

### 13. Scorecard
See above. Target ≥85. If low, find a stronger angle before abandoning.

### 14. Required output for every video (the SEO research package)
1 primary keyword; 2 five secondary keywords; 3 ten long-tail keywords; 4 search-intent analysis; 5 historical demand
assessment; 6 competitor analysis; 7 ten title candidates; 8 three thumbnail concepts; 9 selected title and
rationale; 10 optimized description; 11 tags and hashtags; 12 chapter structure; 13 three Shorts titles and concepts;
14 evergreen assessment; 15 SEO & commercial scorecard. After rendering, update chapters and finalize metadata. Save
with the project.

### 15. Automation and continuous improvement
Integrate into the existing pipeline; preserve branding, narration, animation, rendering and publishing configs. Use
available tools; never claim access to Google Trends, YouTube Analytics, vidIQ or other platforms unless it actually
exists — otherwise clearly labeled qualitative analysis. Don't interrupt existing productions. Don't publish or modify
live videos without authorization. Use real performance data to refine topics, titles, thumbnails and storytelling.

### Final directive
Optimize for discovery **and** satisfaction. A successful documentary addresses a subject people care about, offers a
title they want to click, delivers a story they want to finish, provides an insight worth remembering, and stays
discoverable long after publication. Don't optimize solely for keywords, don't chase trends without long-term
evaluation, don't produce generic SEO content. Build a recognizable library of commercially compelling economic
documentaries that generate organic views for years.
