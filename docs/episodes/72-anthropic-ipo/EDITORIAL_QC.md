# Editorial QC: Anthropic's $1.5 Trillion IPO: The AI Gold Rush or the Next Bubble? (Ep 72)

Build: 821.2 s (13:41), 1920x1080, -16.2 LUFS, true peak -4.0 dBFS; pipeline QC **0 errors**, 27 warnings (below); visual QC: no near-identical
consecutive samples, no clipping, no silences > 2.5 s; ffmpeg freezedetect (d = 5 s): **no frozen stretch ≥ 5 s**; blackdetect (≥ 1 s): none.
Narration US$0.30 (gpt-4o-mini-tts, voice ash, 10,115 characters; cap US$1); the second (fix) render reused the cached narration (US$0.00).

## Neutrality check (critical for this episode)
Anthropic makes the AI model that produced this episode. Checked line by line:

| Check | Result |
|---|---|
| Sources limited to public filings (424B4, pricing FWP, Amazon and Alphabet 10-Qs) and named press; no insider, "the model knows" or first-person framing | PASS (no statement relies on anything but cited public documents) |
| No promotional tone: no superlatives beyond sourced facts ("biggest offering on record" = CNBC / The National; "fastest-growing companies ever measured" stated as the optimists' reading next to the bills) | PASS |
| Bear case given full weight: the skeptics' chart (≈$900bn of commitments, mostly non-cancelable), "the risk is the promise", the dark road (cheaper models, thin profits, more money needed, dilution), lock-up waves, "a lot to assume on day one" | PASS (screen time: bull road 19 s vs dark road 17 s + commitments 25 s + promise board 29 s) |
| Circular-financing criticism presented fairly and in full, attributed (Reuters; Axios, reported; Tech Policy Press, opinion; the prospectus's own "conflicts of interest" risk factor) before the other side | PASS (c4_critics 31.6 s vs c4_defense 31.7 s) |
| No unsupported accusation: nothing called fraudulent, inflated or improper; "No wrongdoing is alleged" in the description; the money loop drawn only from disclosed flows | PASS |
| Not investment advice: no buy/sell/hold, no price target, no scenario probabilities; "June hasn't decided"; "NOT investment advice" line in the description and the Shorts; claim pill "NOT INVESTMENT ADVICE" on the verdict | PASS |
| Disclosure: description states AI tools including Claude are used by the channel and that Anthropic did not sponsor, review or approve the film | PASS (owner may remove; factual) |
| Public figures (Dario and Daniela Amodei, Andy Jassy, Sundar Pichai) only as respectful caricatures with name tags, doing only what the narration documents (standing, talking at founding; standing at their company) | PASS |
| Private individuals: silhouettes (crowds, prospectors, the hypothetical investor, the lock-up queue); June is fictional and labelled | PASS |

## Standard checks
| Check | Result |
|---|---|
| Runtime 720-840 s (owner override) | PASS (821.2 s) |
| Hook first, then channel intro | PASS (co_hook 0:00-0:39, intro 0:39-0:44) |
| Presenter draws ≥ 4 explanatory boards | PASS (p05 price tags, p11 scoreboards, p17 four words, p33 what the price assumes) |
| Spoken numbers 10-15, ≤ 1 per segment | PASS (14; counter reports 15, double-counting "eighty-one billion" and reading "and a" as a number) |
| Story over statistics: one protagonist | PASS (June and her one share, every chapter) |
| Proceeds vs market cap; paper vs realized; EV vs equity; commitment vs debt; run rate vs revenue | PASS (each explained or labelled on screen) |
| Primary vs secondary split verified | PASS (956,351,354 vs 23,648,646, FWP / 424B4) |
| Latest close labelled with date | PASS ("CLOSE NOV 19, 2026 (LATEST AVAILABLE ON NOV 20)") |
| Estimates, hypotheticals, our calculations labelled | PASS (claim pills: OUR CALC, HYPOTHETICAL, REPORTED, OPINION, ILLUSTRATIVE SCENARIO) |
| No logos; company shown by ticker ANT and plain plaques | PASS (thumbnail deviation documented in README) |
| Titles without "—" | PASS (film, Shorts) |
| Day scenes, bespoke worlds, human characters | PASS (14 new sets; the critics' corkboard is lit as a thriller interior; the dark road has a storm by design) |
| USD only | PASS |

Warnings (accepted): 13 "number word 'one'" notes (not statistics); 8 distinctiveness notes (scene-type sequence similar to other
all-cartoon episodes; sets and content are new); p05 lasts 34.6 s (target 10-25 s; it carries the valuation reconciliation); c2_origin and
c4_twist pace 120 wpm (list of names); two caption timing notes; "picture static > 4 s from 82.4 s" (the board before drawing starts; under 5 s).
The manifest lists one unresolved cue (end card brand cue "This is The Hidden Economics"); the renderer's fallback places it, checked on frames.
Review fix after the first render: punchline words in the kitchen and money-loop sets moved above the busy area, loop camera widened,
caricature name tags lifted into frame (re-render with cached narration).
Claims awaiting human verification: 9 (status source_located / data_derived until a named reviewer signs off).

## Could not verify (handled)
CNN live page (HTTP 451) and a Reuters close story (not found): the ≈$1.76-1.77tn figures are not used. Forbes and Axios pages blocked
automated reading: values cross-checked with CNBC / The National, or used only as attributed reports. Nov 20 close not available at lock.
