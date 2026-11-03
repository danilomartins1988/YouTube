# Research dossier: Why Switzerland Is So Rich

Generated 2026-11-03T00:31:22+00:00.

## Claims

| ID | Claim | Status | Sources |
|---|---|---|---|
| `geo_landlocked` | Switzerland is a landlocked, mountainous country. | **source_located** | natural_earth |
| `neutrality_1815` | Europe's great powers formally recognised Swiss neutrality in 1815 (Congress of Vienna and the Second Treaty of Paris). | **source_located** | admin_neutrality, eda_neutrality |
| `pharma_share_2024` | Chemical and pharmaceutical products accounted for 52.7% of Swiss exports in 2024 (CHF 149,058 million). | **source_located** | bazg_trade_2024, kmu_pharma_exports |
| `vet_share` | About two-thirds of young people in Switzerland enter vocational education and training (VET); the most common form is dual-track VET combining classroom instruction with workplace training. | **source_located** | seri_vet |
| `gii_2025_rank` | In the Global Innovation Index 2025, WIPO ranked Switzerland first of 139 economies. | **source_located** | wipo_gii_2025, ige_gii_2025 |
| `gii_2025_top5` | GII 2025 top five: Switzerland, Sweden, United States, Republic of Korea, Singapore. | **source_located** | wipo_gii_2025 |
| `pop_che_2023` | Switzerland's population in 2023 was 8,888,822. | **data_derived** | wb_pop_mirror |
| `gdppc_che_2023` | Switzerland's GDP per capita in 2023 was $99,557 (current US$). | **data_derived** | wb_gdppc_indicator, wb_gdp_mirror, wb_pop_mirror |
| `ratio_che_deu_2023` | In 2023, Switzerland's GDP per capita was 1.86 times that of Germany ($99,557 vs $53,503). | **data_derived** | wb_gdppc_indicator, wb_gdp_mirror, wb_pop_mirror |
| `ratio_che_euu_2023` | In 2023, Switzerland's GDP per capita was 2.44 times that of European Union ($99,557 vs $40,877). | **data_derived** | wb_gdppc_indicator, wb_gdp_mirror, wb_pop_mirror |
| `gdppc_chart_2023` | GDP per capita (current US$), 2023: Switzerland $99,557; United States $81,249; Austria $56,510; Germany $53,503; United Kingdom $48,741; France $44,329; EU average $40,877; Italy $38,228 | **data_derived** | wb_gdppc_indicator, wb_gdp_mirror, wb_pop_mirror |

## Claims that require verification before publishing

- `geo_landlocked` (source_located): Switzerland is a landlocked, mountainous country.  
  _Note:_ Landlocked status is visible in the Natural Earth boundaries. 'Mountainous' needs a citation (e.g. Swiss Federal Statistical Office land-use statistics) or should be cut.
- `neutrality_1815` (source_located): Europe's great powers formally recognised Swiss neutrality in 1815 (Congress of Vienna and the Second Treaty of Paris).  
  _Note:_ admin.ch dates the recognition to 1815 via the Congress of Vienna and the Treaty of Paris. Check exact wording on both pages.
- `pharma_share_2024` (source_located): Chemical and pharmaceutical products accounted for 52.7% of Swiss exports in 2024 (CHF 149,058 million).  
  _Note:_ Figure taken from a search summary of the FOCBS 2024 annual report. Confirm the 52.7% and which export total it refers to (FOCBS 'Total 1' business-cycle total excludes gold and other precious metals) and word the on-screen label accordingly.
- `vet_share` (source_located): About two-thirds of young people in Switzerland enter vocational education and training (VET); the most common form is dual-track VET combining classroom instruction with workplace training.  
  _Note:_ SERI states that two-thirds of young people benefit from VET. Confirm exact phrasing; do not conflate with annual 'Transition Barometer' interest percentages.
- `gii_2025_rank` (source_located): In the Global Innovation Index 2025, WIPO ranked Switzerland first of 139 economies.  
  _Note:_ Confirm 139 economies and rank in WIPO's press release. Secondary sources disagree on the length of the streak (14th vs 15th year), so the script deliberately does not mention it.
- `gii_2025_top5` (source_located): GII 2025 top five: Switzerland, Sweden, United States, Republic of Korea, Singapore.  
  _Note:_ Confirm order in WIPO's ranking table.

## Sources

| ID | Title | Publisher | Published | Accessed | Kind | URL |
|---|---|---|---|---|---|---|
| `wb_gdp_mirror` | GDP (current US$) - World Bank WDI, normalised CSV (datasets/gdp) | World Bank (via Datahub datasets/gdp) | 2026-04-08 (datapackage last_updated) | 2026-11-03 | dataset | https://github.com/datasets/gdp |
| `wb_pop_mirror` | Population, total - World Bank WDI, normalised CSV (datasets/population) | World Bank (via Datahub datasets/population) | n/a | 2026-11-03 | dataset | https://github.com/datasets/population |
| `wb_gdppc_indicator` | GDP per capita (current US$), indicator NY.GDP.PCAP.CD | World Bank | n/a | 2026-11-03 | dataset | https://data.worldbank.org/indicator/NY.GDP.PCAP.CD |
| `natural_earth` | Natural Earth 1:50m Cultural Vectors - Admin 0 Countries | Natural Earth | n/a | 2026-11-03 | dataset | https://www.naturalearthdata.com/downloads/50m-cultural-vectors/ |
| `admin_neutrality` | Switzerland's policy of neutrality | Swiss Federal Administration (admin.ch) | n/a | 2026-11-03 | primary | https://www.admin.ch/en/switzerlands-policy-of-neutrality |
| `eda_neutrality` | Neutrality (About Switzerland) | Federal Department of Foreign Affairs (FDFA) | n/a | 2026-11-03 | primary | https://www.aboutswitzerland.eda.admin.ch/en/neutrality |
| `bazg_trade_2024` | Swiss Foreign Trade 2024 - annual report (912.5-02) | Federal Office for Customs and Border Security (FOCBS / BAZG) | 2025 | 2026-11-03 | primary | https://www.bazg.admin.ch/dam/en/sd-web/1TnZbTRz4WOh/912.5-02_jb_2024_1.1_en.pdf |
| `kmu_pharma_exports` | Record exports driven by chemicals and pharmaceuticals | State Secretariat for Economic Affairs SECO (kmu.admin.ch) | n/a | 2026-11-03 | secondary | https://www.kmu.admin.ch/en/record-exports-driven-by-chemicals-and-pharmaceuticals |
| `seri_vet` | Vocational education and training (VET) | State Secretariat for Education, Research and Innovation (SERI / SBFI) | n/a | 2026-11-03 | primary | https://www.sbfi.admin.ch/en/vocational-education-and-training-vet |
| `wipo_gii_2025` | Global Innovation Index 2025 press release | World Intellectual Property Organization (WIPO) | 2025-09-16 | 2026-11-03 | primary | https://www.wipo.int/pressroom/en/articles/2025/article_0009.html |
| `ige_gii_2025` | Global Innovation Index 2025: Switzerland retains top position | Swiss Federal Institute of Intellectual Property (IGE/IPI) | n/a | 2026-11-03 | secondary | https://www.ige.ch/en/services/newsroom/news/news-details/global-innovation-index-2025-schweiz-behauptet-den-spitzenplatz |

## Open research questions

- For the full documentary - role of banking secrecy and its erosion (1934 Banking Act, automatic exchange of information). Needs primary legal sources.
- Swiss franc and the Swiss National Bank's balance sheet - SNB annual reports.
- Counterpoints - cost of living, inequality measures, dependence on a few large firms. Needs balanced sources.
- Is GDP per capita the right lens? Compare GNI per capita and PPP-adjusted measures (World Bank NY.GNP.PCAP.CD, NY.GDP.PCAP.PP.CD).
