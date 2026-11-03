# Cost report: why-switzerland-is-so-rich / extended_franc

| Kind | Step | Provider | Units | USD | Note |
|---|---|---|---|---|---|
| estimate | tts (pre-build estimate) | openai | 1061 characters | $0.0318 | pricing verified_on: 2026-11-03 via search results (not OpenAI's page) - confirm at https://openai.com/api/pricing |
| actual | render | local_cpu | 0.0278 cpu_hours | $0.0000 | assumed negligible on your own machine |
| actual | tts (characters actually synthesised) | openai | 0 characters | $0.0000 | pricing verified_on: 2026-11-03 via search results (not OpenAI's page) - confirm at https://openai.com/api/pricing; cached sentences are free |
| **actual total** | | | | **$0.0000** | |

## Paid voice actually billed (OpenAI `gpt-4o-mini-tts`, voice `onyx`)

The table above is from the final rebuild, where every sentence came from the audio cache (0 new
characters). The narration was paid for once, in the first build on 2026-11-03:

| Requests | Characters | USD (at $0.030 / 1k chars) |
|---|---|---|
| 17 | 1076 | $0.03228 |

Topic ledger: `output/<slug>/paid_spend.json`. Topic total for all four deliverables plus one
119-character voice test: **9,734 characters, $0.2920**, against the hard cap of $0.50.
