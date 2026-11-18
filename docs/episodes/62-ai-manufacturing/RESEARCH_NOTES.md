# Ep 62 research dossier: Could AI Make American Factories Cheaper Than China's?

Arc Episode 2 (Episode 1 = Ep 60, "Why the World Still Depends on Chinese Factories"). All new sources read on 2026-11-18;
machine-readable claims in `projects/could-ai-end-chinas-manufacturing-dominance/sources.yaml`. US dollars only.

## 1. Robots: IFR World Robotics 2026 (primary)
- **Executive Summary WR 2026, Industrial Robots** (IFR, published Sep 24, 2026; data year 2025; units = industrial robots
  installed per year). Read from the PDF text:
  - 603,307 units installed worldwide in 2025 (+11%); previous record 552,946 (2022). Forecast 655,000 (2026), 806,000 (2029):
    IFR forecasts, **not used as facts in the film**.
  - Operational stock 5,079,078 (+9%). Market value US$18.6bn.
  - China 354,226 (+20%); Asia 457,315 (76% of the world); Europe 73,054 (−14%); Americas 57,044; US 38,428 (+12%).
  - Chinese domestic suppliers: "around 30% from 2019 to 2021 ... Since 2024, more than half of the Chinese installations are
    from Chinese brands."
  - AI maturity: "Machine vision for detection and robot guidance is already established and industry-grade. Predictive
    maintenance, process optimization and AI-based inspection are also increasingly used in industry. General-purpose Physical
    AI systems and learning from simulation and experience, are not yet industry-grade."
  - Humanoids: "Most humanoids remain prototypes or pilot-stage technologies rather than industrial-grade products. At the
    current stage of technology, industrial robots are economically superior for industrial production tasks."
- **IFR press release, Sep 24, 2026** ("Five Million Robots now Operate in Factories Globally"): China 354,000 (59%); US almost
  38,500 (+12%, now 2nd); Japan 36,219 (−19%); Korea 30,000 (−1%); Germany fewer than 25,000; India almost 10,500.
- **IFR China release, Sep 24, 2026**: domestic suppliers +15%, 55% of installations (57% in 2024 per the global release);
  labor shortage "due to demographic change"; 15th Five-Year Plan (2026–2030) aims AI research at "physical applications".
- **IFR density release, Nov 12, 2026** (data year 2025; robots per 10,000 manufacturing employees): Korea 1,066; Singapore
  873; Germany 469; Japan 452; US 323 (8th); EU 240; world 152; China 193 (19th), "based on employment data of the National
  Economic Census", +147% 2020–2025. **Caution:** the IFR changed China's employment base between editions (the April 2026
  release, data 2024, gave China 166, 22nd; earlier editions gave much higher figures on another base). The film makes no
  cross-edition comparison for China.
- **IFR, Jul 15, 2025**: "Japan is the world's predominant robot manufacturing country representing 38% of global robot
  production" (preliminary 2024 data; no newer production share located).

## 2. US factories: cost structure, output, jobs
- **Census 2021 Annual Survey of Manufactures** (last ASM year; replaced by AIES): shipments $6.1T (21 subsectors sum
  $6,079.6bn); cost of materials sum $3,340.8bn → 55% (our calculation). Census "Manufacturing in America" infographic: 11.7M
  employees, annual payroll $785.2bn → 12.9% of shipments (our calculation; wages and salaries before benefits).
- **Fed G.17 IPMAN** (index 2017=100): June 1979 47.61 → Oct 2026 99.72 = ×2.09 (our calculation). **BLS MANEMP**: June 1979
  19,553k (all-time peak) → Oct 2026 12,681k (−35%). Interpretation in the film: "automation is a big part of that story"
  (not the only cause; trade and composition also matter).
- Reused from Ep 60 (still current): BLS CES3000000008 2025 average $29.05/hour; NBS 2025 production workers (larger firms)
  ¥80,739 ≈ $11,200 at Fed G.5A 7.1875 (our conversion); "roughly a fifth" per hour is a rough comparison (hours and
  definitions differ; our calculation). World Bank WDI: China 27.4% of world MVA, 2025 (our calculation). IEA GCMO 2026: China
  85% of magnet rare-earth refining (2025).

## 3. Companies (only what the documents say)
- **Foxconn / NVIDIA** (NVIDIA blog, Jun 2, 2024): digital twin of a new Guadalajara factory; engineers define processes and
  train robots in the virtual environment. A planning/simulation example, **not** a claim of an autonomous factory.
- Not used (insufficient primary evidence for this film's claims or not needed): "lights-out" factory claims (FANUC, Xiaomi
  and others), Tesla Optimus deployment statements, Chinese robot makers' individual filings (Estun, Inovance, Siasun). The
  Chinese-brand share comes from the IFR instead. Siemens/ABB/Rockwell named nowhere; Germany and Switzerland are described
  only as "home to big automation suppliers" (analysis).

## 4. Jobs research
- **Acemoglu & Restrepo, "Robots and Jobs", JPE 128(6), 2020**: US commuting zones 1990–2007; one more robot per thousand
  workers reduces the employment-to-population ratio by 0.2 percentage points and wages by 0.42%.

## 5. The $100 three-factory experiment (ILLUSTRATIVE MODEL, our assumptions)
Units: dollars per toaster delivered to a US warehouse. No real company's costs. Materials ≈ 60% echoes the Census materials share
(55% of shipments) only loosely; every other line is an assumption chosen to show mechanisms.

| Line | 1 Conventional China | 2 Automated Ohio | 3 Automated China |
|---|---:|---:|---:|
| Materials & parts | 61 | 64 (imported parts) | 59 (cluster) |
| Labor | 11 | 13 (¾ fewer hours, higher pay) | 3 |
| Machines (depreciation of robots, software, vision) | 5 | 14 | 11 (cheaper domestic robots, assumed) |
| Energy | 3 | 3 | 3 |
| Upkeep | 2 | 4 | 3 |
| Defects | 3 | 2 | 2 |
| Shipping | 6 | 2 | 6 |
| Tariff (≈10%, assumption) | 9 | 0 | 8 |
| **Total** | **100** | **102** | **95** |

Switches: tariff 25% → F1 112, F3 107, Ohio 102 wins; tariff 0 → F1 91, F3 87; Ohio robots idle half the time → machines
14 → 28, Ohio 116; imported-parts premium and robot prices move Ohio's materials/machines lines.

## 6. Autocomplete (SEO)
`tools/yt_autocomplete.py --expand`, collected 2026-11-18 08:41 UTC (US, en): raw output in `autocomplete_2026-11-18.txt`.
