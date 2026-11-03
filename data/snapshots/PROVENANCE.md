# Data snapshot provenance

`worldbank_gdp_population.csv` is a subset (18 economies/aggregates, 2000-2023) of:

| Series | Mirror URL | Upstream |
|---|---|---|
| GDP, current US$ (World Bank `NY.GDP.MKTP.CD`) | https://raw.githubusercontent.com/datasets/gdp/main/data/gdp.csv (datapackage `last_updated` 2026-04-08) | World Bank World Development Indicators |
| Population, total (World Bank `SP.POP.TOTL`) | https://raw.githubusercontent.com/datasets/population/main/data/population.csv | World Bank World Development Indicators |

- Retrieved: 2026-11-03.
- Licence: CC BY 4.0 (World Bank open data terms; mirror datapackage declares CC-BY-4.0).
- GDP per capita is **derived** as GDP / population. It can differ slightly from the
  World Bank's published `NY.GDP.PCAP.CD`. The pipeline tries the official indicator via
  the World Bank API first and only falls back to this derivation when the API is unreachable;
  the dossier records which path was used.
- The snapshot exists so builds are reproducible offline. Refresh with
  `python -m hiddeneco data refresh`.
