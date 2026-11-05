# Quality report - how-nvidia-took-over-the-ai-economy / documentary

| Check | Result | Detail |
|---|---|---|
| File exists | PASS | output/nvidia_documentary.mp4 (176.0 MB) |
| Resolution 1920x1080 | PASS | 1920x1080 |
| H.264 video | PASS | h264 High, yuv420p, 30/1 fps |
| AAC audio | PASS | aac 48000 Hz, 2 ch |
| Duration 10-12 min | PASS | 698.77 s (11:38) |
| English narration | PASS | OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: 0 |
| Caption/voice sync | PASS | 308 cues; median cue-start offset 0.07 s, p90 0.36 s; 100% of speech captioned |
| No black gaps (>1 s) | PASS | none |
| No frozen picture (>5 s) | PASS | none |
| Licensed assets only | PASS | every scene asset is on the licence allowlist (assets/manifest.yaml) |

- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Scenes: 34; types: act_title x6, ai_network x1, big_counter x3, compare x4, cpu_gpu x1, donut x1, fund_flow x2, kinetic_text x3, landscape x1, line_chart x1, map x2, stack x2, stacked_columns x2, supply_chain x2, timeline x1, whiteboard x2
- Average scene length: 20.6 s; act cards are music-only.

## Pipeline QC report

# QC report: how-nvidia-took-over-the-ai-economy / documentary (long_16x9)

- Runtime: **698.77 s**
- Video: 1920x1080 @ 30/1 h264, audio aac 48000 Hz, 176.0 MB
- Loudness: -16.1 LUFS integrated, true peak -4.1 dBFS
- Errors: **0**, warnings: **42**
- Technical QC passed: **True**
- Publishable (no unverified claims): **False**

## Issues

- [WARNING] (timing) Segment open_revenue pace 117 wpm (numerals count as one word)
- [WARNING] (timing) Segment a2_origins pace 111 wpm (numerals count as one word)
- [WARNING] (timing) Segment a3_flywheel pace 116 wpm (numerals count as one word)
- [WARNING] (timing) Segment a4_revenue pace 111 wpm (numerals count as one word)
- [WARNING] (timing) Segment a6_rivals pace 117 wpm (numerals count as one word)
- [WARNING] (timing) Segment a6_amd pace 100 wpm (numerals count as one word)
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'two' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'half' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'six' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'six' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'six' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'quarter' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'six' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'five' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'six' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'twenty' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'one' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (sources) Number word 'three' outside a placeholder - confirm it is not an unsourced statistic.
- [WARNING] (distinctiveness) Scene sequence 88% similar to 'how-nvidia-took-over-the-ai-economy/documentary_presenter'

## Publish blockers - claims needing human verification

- `alexnet` (source_located): In 2012 the AlexNet neural network, trained on two NVIDIA GTX 580 GPUs, won the ImageNet image-recognition competition; training took five to six days.  
  
- `amd_dc_2025` (source_located): AMD's Data Center segment revenue (EPYC CPUs and Instinct GPUs) was $16.6 billion in calendar 2025, up 32%.  
  Calendar 2025 and includes CPUs; not directly comparable with NVIDIA's fiscal-year Data Center figure.
- `arizona` (source_located): In October 2025 NVIDIA and TSMC showed the first Blackwell wafer produced in the United States, at TSMC's Arizona fab; reports say the wafers still go to Taiwan for advanced packaging.  
  
- `aws_trainium` (source_located): In October 2025 AWS activated Project Rainier, a cluster with nearly 500,000 of its own Trainium2 chips, used by Anthropic.  
  
- `capex_2026` (source_located): Trackers of company guidance put 2026 capital spending by Amazon, Microsoft, Alphabet and Meta at roughly $700 billion combined (estimates range from about $690bn to $760bn), much of it for AI data centers.  
  Secondary compilation of company guidance; say "roughly" and "estimates".
- `china_guidance` (source_located): NVIDIA's outlook for Q3 FY2027 (and earlier for Q1 FY2027) assumes no Data Center compute revenue from China.  
  
- `competitors_10k` (source_located): NVIDIA's 10-K lists competitors including AMD, Huawei and Intel, and large cloud companies designing their own AI hardware, such as Alibaba, Alphabet, Amazon, Baidu, Huawei and Microsoft.  
  
- `cuda_2006` (source_located): NVIDIA introduced CUDA in 2006, opening 'the parallel processing capabilities of our GPU to a broad range of compute-intensive applications' (10-K).  
  
- `customers_fy2026` (source_located): In fiscal 2026 sales to one direct customer were 22% of NVIDIA's total revenue and sales to another were 14% (10-K); the customers are not named.  
  
- `dc_fy2026` (source_located): Data Center revenue was $193.7 billion in fiscal 2026 (up 68%), about 90% of total revenue (our calculation: 193.7 / 215.9 = 89.7%); in fiscal 2020 it was $2.98 billion, about 27% (2.98 / 10.92).  
  
- `developers` (source_located): NVIDIA's FY2026 10-K says there are over 7.5 million developers worldwide using CUDA and its other software tools.  
  
- `founded_1993` (source_located): NVIDIA was incorporated in California in April 1993; Jen-Hsun (Jensen) Huang co-founded it and has been CEO since inception.  
  
- `gm_fy2026_reason` (source_located): NVIDIA says fiscal 2026 gross margin fell as its business moved from Hopper HGX systems to Blackwell full-scale datacenter solutions, and because of a $4.5 billion charge for H20 excess inventory and purchase obligations after new US export licence requirements for China (April 2025).  
  
- `google_tpu` (source_located): Google made Ironwood, its seventh-generation TPU, generally available in November 2025; in October 2025 Anthropic said it plans to access up to one million Google TPUs, while continuing to use Amazon Trainium and NVIDIA GPUs.  
  
- `gpu_1999` (source_located): NVIDIA's 10-K says its 'invention of the GPU in 1999 sparked the growth of the PC gaming market and redefined computer graphics'.  
  Company's own description; say "what Nvidia calls the first GPU".
- `gross_margin_series` (source_located): NVIDIA GAAP gross margin by fiscal year (our calculation from 10-K gross profit / revenue, XBRL): FY2016 56.1%; FY2017 58.8%; FY2018 59.9%; FY2019 61.2%; FY2020 62.0%; FY2021 62.3%; FY2022 64.9%; FY2023 56.9%; FY2024 72.7%; FY2025 75.0%; FY2026 71.1%.  
  Years on the chart are fiscal years (FY2016 = year ended Jan 2016). FY2024-26 values match the 10-K reported GAAP margins.
- `market_cap_5tn` (source_located): On 29 October 2025 NVIDIA became the first company to close with a stock market value above $5 trillion.  
  
- `q2fy27` (source_located): For the quarter ended 26 July 2026 (Q2 fiscal 2027) NVIDIA reported revenue of $96.2 billion (up 106% year over year), Data Center revenue of $89.0 billion, a 75.0% gross margin, and guided to about $108 billion for the next quarter, assuming no Data Center compute revenue from China.  
  
- `revenue_fy2023` (source_located): NVIDIA revenue for fiscal 2023 (year ended 29 Jan 2023) was $26.97 billion; fiscal 2026 revenue was about eight times higher (our calculation, 215.9 / 26.97 = 8.0).  
  
- `revenue_fy2026` (source_located): NVIDIA revenue for fiscal 2026 (year ended 25 Jan 2026) was $215.9 billion, up 65% from $130.5 billion in fiscal 2025.  
  
- `revenue_series` (source_located): NVIDIA revenue by fiscal year, US$ billion (10-K / XBRL): FY2016 5.0; FY2017 6.9; FY2018 9.7; FY2019 11.7; FY2020 10.9; FY2021 16.7; FY2022 26.9; FY2023 27.0; FY2024 60.9; FY2025 130.5; FY2026 215.9.  
  
- `rnd_total` (source_located): NVIDIA says it has invested over $76.7 billion in research and development since its inception (FY2026 10-K).  
  
- `rubin` (source_located): In its Q4 FY2026 results NVIDIA said it unveiled the Rubin platform (six new chips) and claimed up to a 10x reduction in inference token cost compared with Blackwell; AWS, Google Cloud, Microsoft Azure and Oracle Cloud are to be among the first to deploy it.  
  Company performance claim; attribute to NVIDIA.
- `segments` (source_located): NVIDIA revenue by market, US$ billion (10-K): FY2020 Data Center 2.98, Gaming 5.52, other 2.42; FY2021 6.70 / 7.76 / 2.22; FY2022 10.61 / 12.46 / 3.84; FY2023 15.01 / 9.07 / 2.90; FY2024 47.53 / 10.45 / 2.95; FY2025 115.19 / 11.35 / 3.96; FY2026 193.74 / 16.04 / 6.16. 'Other' = Professional Visualization + Automotive + OEM and other (our sum).  
  
- `suppliers` (source_located): NVIDIA's 10-K: it uses foundries such as TSMC and Samsung to produce its wafers, buys memory from SK Hynix, Micron and Samsung, uses CoWoS technology for packaging, and uses contract manufacturers such as Hon Hai, Wistron and Fabrinet for assembly, testing and packaging; its supply chain is 'mainly concentrated in Asia' while it expands into the US and Latin America.  
  
- `supply_risk` (source_located): NVIDIA's 10-K warns that 'supply constraints or availability issues with respect to any one component' can have a broader revenue impact because its products are part of a complex data center buildout.  
  
- `tensor_2017` (source_located): NVIDIA introduced its first Tensor Core GPU, built for AI, in 2017 (10-K).  
  

To clear a blocker: read the primary source, then set `status: human_verified` and `verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild.

