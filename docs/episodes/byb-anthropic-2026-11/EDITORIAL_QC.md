# Editorial QC: Anthropic Stock Before You Buy: 7 Things to Check (Nov 2026)

Build: 746.1 s (12:26; series target 11-13 min, deliverable 660-800 s), 1920x1080, -16.1 LUFS, true peak -4.1 dBFS; pipeline QC **0 errors**,
29 warnings (below); ffmpeg freezedetect (n=0.003, d=5 s): **no frozen stretch ≥ 5 s**; visual QC: no near-identical consecutive samples,
no clipping, no silences > 2.5 s. Narration US$0.31 (gpt-4o-mini-tts, voice **alloy**, 10,229 characters; cap US$1); the fix re-render reused
the cached narration (US$0.00).

## Neutrality check (critical: Anthropic makes the AI model used to produce this film)
| Check | Result |
|---|---|
| Sources limited to public filings (424B4, FWP, Amazon 10-Q, peer filings) and named press/data vendors; no insider, "the model knows" or first-person framing | PASS |
| Never buy/sell/hold, no price target, no forecast; "Maya didn't decide today, and we're not deciding for her" | PASS |
| "Not investment advice" on screen at the start (s04 headline + sign) and the end (s44 stamp, end card), spoken at both points, and in the description and Shorts package note | PASS |
| Production disclosure spoken and on screen (s04) and in the description: AI tools including Claude are used; Anthropic did not sponsor or review | PASS (owner may remove; factual) |
| Risks and positives with equal weight: c2_growth (bull and bear in one segment), c4_cost (falls / climbs back), c4_cash (promises vs cash cushion), c5_chips (no choke point / suppliers are shareholders), c5_customers (healthier spread / marketplaces), c6 (Facebook down, Arm up), c7_meaning (risk factor vs supporters), c8 (4 bullish + 4 bearish signals; c8_bull 14.9 s vs c8_bear 11.9 s, same balance shown level at the end) | PASS |
| Superlatives only when sourced; no promotional words ("best", "winner"); governance described in the prospectus's own words, including its risk factor | PASS |
| No accusation of wrongdoing; conflicts of interest quoted as the prospectus's own risk factor | PASS |
| No real people drawn; Maya is fictional and labelled; no logos (ticker ANT) | PASS |
| Ep 72 not repeated: no founding history, no money-loop chapter, no who-got-rich, no bull/base/bear roads; only reused verified facts (offer, close, compute cost, commitments) in a checklist frame | PASS |

## Standard checks
| Check | Result |
|---|---|
| Runtime within target | PASS (746.1 s) |
| Hook first, then channel intro, then disclaimer | PASS (h_open-h_maya 0:00-0:57, intro 0:57-1:02, disclaimer 1:02) |
| Presenter boards ≥ 4 (draw, chart, relationship) | PASS (p09 outstanding vs fully diluted, p14 price/sales bars, p25 report card, p30 partner triangle) |
| Spoken numbers 10-15, ≤ 1 per segment | PASS (13; see FACT_CHECK.md) |
| Story over statistics: one protagonist | PASS (Maya and her clipboard, hook to close) |
| Market cap vs EV; outstanding vs fully diluted; unlocked vs sold; commitment vs debt; run rate vs revenue | PASS (each on screen) |
| Every price dated; our calculations labelled | PASS ("DATA AS OF NOV 19, 2026 CLOSE" stamp at the hook/disclaimer, priced-in scene and end; "OUR CALC" on every multiple) |
| Past IPOs sourced from AP, Reuters, Bloomberg and daily closes; "past patterns don't predict ANT" on screen | PASS |
| Titles without "—"; first 30 characters make sense | PASS ("Anthropic Stock Before You Buy") |
| USD only | PASS |

## Visual review (first render → fixes → second render)
First render reviewed on `visual_qc/sheet_sampled.jpg` and 15 extra frames. Fixed before the final render: elevator floor labels clipped by
the shaft (now short prices + a sign); disclaimer stamp over the signs (moved); vote tower labels dark on dark and the ballot box over the
auction podium (white plaques, studio set, layout inside the Short crop); share grid labels behind desks (office set, grid raised); the
"no customer ≥ 10%" pie did not draw (full-circle arc; now two halves); Maya over the marketplace sign and the lock-up sign (moved); the
"promises vs cash" headline over the bank columns (studio set). Signature sheets: `sheet_s03_list`, `sheet_s06_classes`, `sheet_s18_waves`,
`sheet_s34_fb`, `sheet_s43_bear`.

Known minor issue (accepted, not re-rendered): in the disclaimer scene the edition stamp sits partly behind the "FILINGS" mascot for its last
seconds; the same stamp is fully visible in the price scene (s13) and at the end (s44).

## Shorts and thumbnails
Three Shorts cut from the master before it was deleted; each checked frame by frame in the vertical crop. B (class cards) and C (presenter
board) clipped edge labels in the default 1520-px crop, so they were recut with a 1800-px crop (`CROPS` in `tools/make_shorts.py`); A fits the
default crop. Shorts descriptions add "Not investment advice" and the data date. Thumbnails: three poster concepts, QC pass (scores 0.81 /
0.69 / 0.83); padlock tag and ticker board moved after review so no text touches the art or leaves the frame.

Warnings (accepted): 11 "number word 'one'/'twice'/'third'" notes (not statistics: "one vote", "matters twice", "Third," in a list); 4 pace
notes (h_maya, c7_meaning, c8_bull, c8_bear at 188-204 wpm; alloy's natural pace); caption reading-speed and short-caption notes.
Claims awaiting human verification: 7 (status source_located until a named reviewer signs off).
