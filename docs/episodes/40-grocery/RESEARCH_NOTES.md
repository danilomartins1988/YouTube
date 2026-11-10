# Research Notes: The Hidden Business Behind America's Grocery Prices

Compiled 2026-11-10. Every item below was read on the primary page or file, fetched on 2026-11-10. Some quotes come from a page summarizer rather than a raw text dump; these are marked "(summarizer quote)". Recheck them word for word before putting them on screen. Calculations that are mine and not the agency's are marked **[calc]**.

## 1. USDA ERS Food Dollar Series (latest data year: 2024)

- 2024 farm share: **11.8 cents** per food dollar; marketing share: **88.2 cents**. https://www.ers.usda.gov/data-products/food-dollar/summary-findings (updated 3/10/2026). I also confirmed both figures in the ERS data file, Food Dollar Nominal Data, "Data by year" sheet. https://www.ers.usda.gov/media/7051/food-dollar-nominal-data.xlsx?v=85548 (release March 2026, covers 2007–2024)
- 2024 industry group bill, in cents per domestic food dollar, from the same XLSX ("Industry group bill", Food, All channels):
  - Food services 38.6
  - Food processing 16.1
  - Food retail 13.8
  - Food wholesale 6.3
  - Finance and insurance 4.7
  - Transportation and storage 4.1
  - Energy 3.1
  - Agribusiness 3.0
  - Livestock 3.3
  - Crops 2.5
  - Advertising 2.2
  - Legal and accounting 1.4
  - Forestry, fishing, and ag services 0.9
  - Farm production total (crops + livestock + forestry/fishing/ag services) 6.7, per the summary findings page.
  - Source: https://www.ers.usda.gov/media/7051/food-dollar-nominal-data.xlsx?v=85548
- For comparison, the same file gives 2023: farm share 12.1, food retail 13.8, food services 37.5, food processing 16.3, energy 3.5.
- Summary findings page (2024 vs 2023 value added): food processing +2.1 percent, energy −7.8 percent, transportation −1.5 percent (summarizer). https://www.ers.usda.gov/data-products/food-dollar/summary-findings (3/10/2026)
- Next release: "November 17, 2026" will add the 2025 Food Dollar. The 2024 figures may be superseded a week after this research date. https://www.ers.usda.gov/data-products/food-dollar-series/ (page updated 5/11/2026)
- NOTE: the current series has **no "packaging" industry group**. The 12 groups are listed above. Do not say "packaging is X cents" from this series.

## 2. Food-at-home inflation

- BLS September 2026 CPI (released Oct 14, 2026): "The food at home index rose 1.8 percent over the 12 months ending in September." Also: "The index for food at home decreased 0.1 percent over the month." https://www.bls.gov/news.release/cpi.nr0.htm
- October 2026 CPI: BLS scheduled it for **Tuesday, November 10, 2026, 8:30 a.m. ET**. It had **not** been released when these notes were compiled (about 4:30 a.m. ET). Update this figure before the script is locked. Same URL.
- Cumulative rise: neither BLS nor ERS states one on the pages I checked. ERS Food Price Outlook says it gives no cumulative figure. **[calc]** From BLS series CUUR0000SAF11 (CPI-U food at home, U.S. city average, not seasonally adjusted):
  - Jan 2020 = 243.110; Jan 2021 = 252.107; Sep 2026 = 321.758.
  - Rise since Jan 2020: about **+32.4%**. Rise since Jan 2021: about **+27.6%**.
  - Source: BLS Public Data API, series CUUR0000SAF11 (https://data.bls.gov/timeseries/CUUR0000SAF11). Attribute as "our calculation from BLS data".
- ERS Food Price Outlook, Summary Findings (updated 10/23/2026): https://www.ers.usda.gov/data-products/food-price-outlook/summary-findings
  - "In 2026, food-at-home prices are forecast to increase 2.3 percent, with a forecast interval of 1.9 to 2.7 percent."
  - "Food-at-home prices increased by an average of 2.6 percent per year between 2006 and 2025."
  - "In 2026, prices for all food are forecast to increase 2.8 percent, with a forecast interval of 2.6 to 3.1 percent." The 20-year all-food average is 3.0 percent per year (2006–25).
  - Food away from home: 2026 forecast +3.5 percent (interval 3.4 to 3.7).
- ERS Charting the Essentials, Food Prices and Spending (updated 6/1/2026). https://ers.usda.gov/data-products/ag-and-food-statistics-charting-the-essentials/food-prices-and-spending
  - "The largest change in this index's average annual value occurred in 2022, when the price of food rose by 9.9 percent." (all food)
  - Food at home rose 2.3 percent in 2025, "less than the 20-year historical rate of 2.6 percent per year."
  - Consumers spent "9.7 percent of disposable personal incomes on food" (summarizer).

## 3. Eggs (avian flu) and beef

- ERS: "Retail egg prices increased 32.2 percent in 2022, 1.4 percent in 2023, 8.5 percent in 2024, and 21.9 percent in 2025." https://www.ers.usda.gov/data-products/food-price-outlook/summary-findings (10/23/2026)
- ERS: farm-level egg prices "increased 31.6 percent in 2025, primarily due to the spread of HPAI". The page also refers to "An ongoing outbreak of Highly Pathogenic Avian Influenza (HPAI) that began in 2022" (same URL).
- ERS: "Egg prices are forecast to decrease 29.3 percent in 2026" (interval −31.6 to −26.7). Retail eggs were "20.6 percent lower in September 2026 than in September 2025" (same URL).
- BLS average price, Grade A large eggs, per dozen (series APU0000708111):
  - Jan 2020: $1.461
  - Jan 2023: $4.823 (first spike)
  - **Mar 2025: $6.227** (highest month in 2019–2026)
  - Sep 2026: $2.272
  - Source: https://data.bls.gov/timeseries/APU0000708111 (pulled via the BLS API)
  - October 2025 shows no value ("-"). BLS published no figure for that month.
  - Vivid line, prices nominal: "A dozen eggs went from about $1.46 in January 2020 to $6.23 in March 2025."
- BLS average price, ground beef 100% beef, per lb (series APU0000703112):
  - Jan 2020: $3.886
  - Aug 2026: $6.923 (highest month in the pull)
  - Sep 2026: $6.792
  - Source: https://data.bls.gov/timeseries/APU0000703112
  - **[calc]** Jan 2020 to Sep 2026 is about +75%, nominal.
- ERS: "Beef and veal prices are forecast to increase 8.7 percent in 2026" (interval 7.4 to 10.1). Retail beef and veal "were 3.5 percent higher in September 2026 than in September 2025." https://www.ers.usda.gov/data-products/food-price-outlook/summary-findings (10/23/2026)
- BLS Sept 2026 CPI: "The meats, poultry, fish, and eggs index decreased 0.5 percent over the month, as the beef index fell 1.0 percent." https://www.bls.gov/news.release/cpi.nr0.htm (Oct 14, 2026)

## 4. Retailer margins (latest 10-Ks)

- **Kroger**, FY2025 (ended Jan 31, 2026), 10-K filed 2026-03-31. https://www.sec.gov/Archives/edgar/data/56873/000110465926037723/kr-20260131x10k.htm
  - Total sales: $147,642M in 2025 and $147,123M in 2024.
  - Net earnings attributable to The Kroger Co.: $1,016M in 2025 and $2,665M in 2024.
  - **[calc]** Net margin: about **0.69%** in FY2025 and about **1.81%** in FY2024.
  - FY2025 includes "$2.5 billion of fulfillment network impairment and related charges".
  - Adjusted net earnings were $3,199M, about **2.2%** of sales **[calc]**. This is a company non-GAAP figure.
  - "Our gross margin rates, as a percentage of sales, were 22.9% in 2025 and 22.3% in 2024."
- **Albertsons**, FY2025 (ended Feb 28, 2026; 53 weeks), 10-K filed 2026-04-27. https://www.sec.gov/Archives/edgar/data/1646972/000164697226000032/aci-20260228.htm
  - The company's own table states net income as a percent of sales: "Net income $ 217.4 0.3 % $ 958.6 1.2 % $ 1,296.0 1.6 %" for fiscal 2025, 2024 and 2023.
  - Net sales and other revenue: $83,172.5M. Gross margin: 27.2%.
  - FY2025 net income includes a "$599.8 million charge, net of tax" for the Opioid Settlement Framework. Adjusted net income was $1,209.3M (non-GAAP).
- **Walmart U.S.**, FY2026 (ended Jan 31, 2026), 10-K filed 2026-03-13. https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm
  - Walmart U.S. net sales: $482,975M. Grocery net sales: **$285,482M**, about 59% of Walmart U.S. sales **[calc]**.
  - Walmart U.S. operating income: $25,158M, stated as **5.2%** of net sales. This is an *operating* margin, not a net margin.
  - Walmart does **not** report a grocery-only margin.
- **FMI (industry trade group)**:
  - "The average net profit for food retailers in 2025 is 2.1%." https://www.fmi.org/our-research/food-industry-facts (undated page; it references "As of August 2026")
  - "Food retailer profit margins fell from 2.3% in 2022 to pre- COVID- 19 pandemic levels of 1.6% in 2023". https://www.fmi.org/newsroom/latest-news/view/2024/06/27/new-fmi-research--the-food-industry-increases-strategic-investments-while-tackling-financial-challenges (June 27, 2024)
- **FTC, "Feeding America in a Time of Crisis"** (staff report, March 2024). Report PDF: https://www.ftc.gov/system/files/ftc_gov/pdf/p162318supplychainreport2024.pdf. Press release, March 21, 2024: https://www.ftc.gov/news-events/news/press-releases/2024/03/ftc-releases-report-grocery-supply-chain-disruptions
  - Exact quote from the report's executive summary: "Specifically, food and beverage retailer revenues increased to more than 6 percent over total costs in 2021, higher than their most recent peak, in 2015, of 5.6 percent. In the first three-quarters of 2023, retailer profits rose even more, with revenue reaching 7 percent over total costs. This casts doubt on assertions that rising prices at the grocery store are simply moving in lockstep with retailers' own rising costs."
  - Caveat in the report itself: "This study did not test whether the specific companies that received 6(b) Orders increased their prices by more or less than their input cost increases."
  - Data source: Census Quarterly Financial Report, Food and Beverage Stores (Table 2).
  - Press release, Chair Khan: "...dominant firms used this moment to come out ahead at the expense of their competitors and the communities they serve." (summarizer quote)
- **Where the sources disagree.** The FTC's measure is industry-wide revenue over total costs, from Census QFR data. FMI and the 10-Ks report net profit margins, about 0.3%–2.3%. These are different metrics, so present both and attribute each. I found no direct FMI rebuttal of the FTC report (see Flags).

## 5. Consolidation

- FTC complaint (Feb 26, 2024): "Kroger Company's $24.6 billion acquisition of the Albertsons Companies, Inc." The combined firm would have had "more than 5,000 stores" and "nearly 700,000 employees across 48 states." https://www.ftc.gov/news-events/news/press-releases/2024/02/ftc-challenges-krogers-acquisition-albertsons
- Court ruling, from Kroger's 10-K: "On December 10, 2024, pursuant to a decision of United States District Court for the District of Oregon in the case Federal Trade Commission et al. v. The Kroger Company and Albertsons Companies, Inc. (Case No.: 3:24-cv-00347-AN), the court issued a preliminary injunction enjoining the consummation of the merger." The Washington state court issued a permanent injunction the same day. https://www.sec.gov/Archives/edgar/data/56873/000110465926037723/kr-20260131x10k.htm
- FTC statement (Dec 10, 2024), Bureau of Competition Director Henry Liu: "This historic win protects millions of Americans across the country from higher prices for essential groceries—from milk, to bread, to eggs..." https://www.ftc.gov/news-events/news/press-releases/2024/12/statement-ftc-victory-securing-halt-kroger-albertsons-grocery-merger
- Termination:
  - Albertsons 10-K: it "sent a notice to Kroger on December 10, 2024 terminating the Merger Agreement" and that day sued Kroger in the Delaware Court of Chancery.
  - Kroger 10-K: "On December 11, 2024, the Company delivered a notice to Albertsons terminating the merger agreement". Kroger says it owes no termination fee. Albertsons seeks "$ 600" (million) plus damages. The litigation was ongoing at the time of the 10-K.
  - Sources: https://www.sec.gov/Archives/edgar/data/1646972/000164697226000032/aci-20260228.htm and the Kroger 10-K above.
- Chair Khan statement (Jan 2, 2025): "On December 11, Kroger and Albertsons announced an abandonment of their proposed transaction." It also discusses the "proposed divestiture of 579 stores to C&S Wholesale Grocers". https://www.ftc.gov/system/files/ftc_gov/pdf/2025.01.02-statement-of-chair-lina-m.-khan-in-the-matter-of-the-kroger-company-and-albertsons-companies-inc.-final.pdf
- Meatpacking, USDA ERS Amber Waves, "Concentration in U.S. Meatpacking Industry and How It Affects Competition and Cattle Prices" (James M. MacDonald, Jan 25, 2024). https://www.ers.usda.gov/amber-waves/2024/january/concentration-in-u-s-meatpacking-industry-and-how-it-affects-competition-and-cattle-prices
  - The four largest firms handle "85 percent of all steer and heifer purchases" (summarizer; no year given on the page).
  - 1980: "the four largest beef packers accounted for 36 percent of all purchases of steers and heifers".
  - "By 1995, the largest four firms accounted for 81 percent of steer and heifer purchases."
  - Balance: earlier research found "the impact of higher concentration—reducing prices paid for cattle—was more than offset" by lower costs. The article also finds "in recent years there is evidence of reduced competition in meatpacking, with lower prices for cattle."
  - Wording: this measures the share of fed-cattle (steer and heifer) purchases, not "85% of all beef sold."
- Slotting fees, FTC staff report "Slotting Allowances in the Retail Grocery Industry: Selected Case Studies in Five Product Categories" (Nov 2003; press release Nov 14, 2003). https://www.ftc.gov/sites/default/files/documents/reports/use-slotting-allowances-retail-grocery-industry/slottingallowancerpt031114.pdf and https://www.ftc.gov/news-events/news/press-releases/2003/11/ftc-releases-grocery-industry-slotting-allowance-report
  - Exact: "the average amount of slotting allowances (per item, per retailer, per metropolitan area) for all five categories combined ranged from $2,313 to $21,768, depending on the particular retailer and metropolitan area."
  - Definition: "one-time payments a supplier makes to a retailer" for new product placement (summarizer).
  - Caveat: the study is "based on a small sample of detailed, anonymous case studies" and "may not be representative of all retailers in the United States."
  - The data are from about 2003, in nominal dollars.
- The FTC 2024 report defines "trade promotion" to include "slotting fees, staying fees, display fees, free fill, promotional spend, rebates, and discounts". It gives no slotting dollar figures. https://www.ftc.gov/system/files/ftc_gov/pdf/p162318supplychainreport2024.pdf

## 6. Shrinkflation and the CPI

- BLS Beyond the Numbers, "Getting less for the same price? Explore how the CPI measures 'shrinkflation' and its impact on inflation" (Kari McNair, Feb 2, 2023). https://www.bls.gov/opub/btn/volume-12/measuring-shrinkflation-and-its-impact-on-inflation.htm
  - "An effective price per standard size, usually a price per ounce, is calculated for items where size is reported."
  - Example: a 64 oz ice cream shrinks to 60 oz at the same $5.99. That is a 6.7 percent price increase, and the CPI includes it.
  - Toilet paper: going from 220 to 200 sheets is treated as a 10 percent increase in price per sheet.
  - Overall: "the impact of product downsizing at the all commodity and services level is minimal", about 0.01 percent per year (summarizer).
  - "Snacks experienced the largest number of size changes for food items."
- BLS MLR, "Why is candy so expensive these days?" (Natalie Ho, September 2026). https://www.bls.gov/opub/mlr/2026/article/why-is-candy-so-expensive-these-days.htm
  - Updated research covering January 2019 through October 2023 "showed downsizing led to a 2.1-percent increase for candy and chewing gum prices during this period."
  - "The CPI for candy and chewing gum increased 32.0 percent" (Dec 2019–Nov 2024).
- BLS research series R-CPI-SC (CPI without product size changes) imputes price change "in the month a product size change occurs". https://www.bls.gov/cpi/research-series/r-cpi-sc.htm (last modified Oct 21, 2026)

## 7. Store brands (private label)

- PLMA (trade association; data from Circana Unify+), Jan 20, 2026. https://www.plma.com/article/us-private-label-industry-reached-2828-billion-sales-2025
  - Store brand sales were $282.8B in 2025 (52 weeks ending Dec 28, 2025), all outlets.
  - Dollar share **21.3%** (up from 19.1% in 2021). Unit share 23.5% (up from 21.6%).
  - Attribute as "according to the Private Label Manufacturers Association."

## Flags / not verified

1. **October 2026 CPI was not yet released** at compile time (scheduled 8:30 a.m. ET today, Nov 10). The 1.8% figure is September 2026. Update it.
2. **No official cumulative food-at-home increase since 2020/2021** was found on BLS or ERS pages. The +32.4% (since Jan 2020) and +27.6% (since Jan 2021) are my calculations from the BLS index. Label them that way.
3. **The Food Dollar 2025 update is due Nov 17, 2026.** The 2024 figures (11.8 cents farm share) may change. Recheck before publishing.
4. **No "packaging" industry group exists** in the current ERS Food Dollar industry bill. The older series had one; it was not verified here.
5. **No direct FMI rebuttal to the FTC March 2024 report** was found on fmi.org. Only FMI's own margin figures (1.6% for 2023, 2.1% for 2025) are verified. Present them as a contrasting measure, not as "FMI's rebuttal."
6. **FTC vs. FMI and 10-K margins measure different things.** The FTC uses Census QFR revenue over total costs, industry-wide. The others use company or industry net margins. Do not imply one source "debunks" the other.
7. **The "four firms control 85% of beef packing" claim** is verified only as ERS's "85 percent of all steer and heifer purchases" (no year stated). A USDA press release with an "over 80 percent of the beef market" wording returned HTTP 403 and was not read.
8. **Walmart's grocery margin is not disclosed.** Only the Walmart U.S. segment operating margin (5.2%) is available.
9. **Kroger and Albertsons net margins for FY2025 are depressed by one-time charges:** Kroger's $2.5B impairment and Albertsons' $599.8M opioid settlement. FY2024 margins (Kroger ~1.8% [calc], Albertsons 1.2% stated) may be more representative. Disclose which year you use.
10. **Slotting fee dollar figures date from the 2003 FTC study** and come from a small, non-representative sample. No newer FTC figure was found.
11. **Egg and beef "record" claims:** I checked BLS average prices for 2019–2026, plus partial history (1980s, 2000s). I did not check the full history, so say "the highest in recent years" or "a record high" only after checking the full BLS series. All values are nominal, not inflation-adjusted.
12. **Quotes marked "(summarizer quote)"** were read through a page summarizer rather than raw text. Confirm the exact wording on the page before putting it on screen. Quotes from the 10-Ks, FTC report PDF, FTC slotting PDF and Khan statement were taken from the raw extracted text.
13. **The Kroger and Albertsons termination-fee litigation** was ongoing as of the 10-Ks (Mar/Apr 2026). Its current status was not checked.
