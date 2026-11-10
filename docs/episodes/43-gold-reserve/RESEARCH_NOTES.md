# Ep. 43: "America's $1 Trillion of Gold Is Booked at $11 Billion": Research Notes

Fact-check compiled 2026-11-10. All amounts in US dollars. Every bullet below was read on the primary page or document. Search snippets were used only to find documents. "Computed" means our own arithmetic from the cited figures.

## 1. Holdings and book value (Treasury Fiscal Data)

- **Total and book value, Oct 31, 2026.** The 8 line items on the Fiscal Data API for record_date 2026-10-31 sum to **261,498,926.241 fine troy oz** and a **book value of $11,041,059,957.90** (computed sum). That is $42.2222/oz, which confirms the ~$11.04bn figure. Dataset page: "the total number of troy ounces multiplied by a value established by law ($42.222), set in 1973." Page: https://fiscaldata.treasury.gov/datasets/status-report-government-gold-reserve/ ; API: https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/gold_reserve?filter=record_date:eq:2026-10-31 . Record date 2026-10-31.
- **Line items, Oct 31, 2026** (same API):
  - Fort Knox, KY, Mint deep storage: 147,341,858.382 oz, $6,221,097,412.78 (56.3%, computed)
  - West Point, NY, Mint deep storage: 54,067,331.379 oz, $2,282,841,677.17 (20.7%)
  - Denver, CO, Mint deep storage: 43,853,707.279 oz, $1,851,599,995.81 (16.8%)
  - Mint working stock ("Coins, blanks, miscellaneous"): 2,783,218.656 oz, $117,513,614.74 (1.1%)
  - Federal Reserve Banks, NY vault, bullion: 13,376,987.724 oz, $564,805,851.07
  - Federal Reserve Banks, NY vault, coins: 73,452.066 oz
  - Federal Reserve Banks, display, bullion and coins: 1,993.321 oz and 377.434 oz
  - FRB total: 13,452,810.545 oz (5.1%, computed)
- **Unchanged since at least 2010.** GAO testimony gave the total as 261,498,900 oz as of Sept 30, 2010. https://gao.gov/assets/a126524.html (GAO-11-768T, June 23, 2011)
- **Tonnage (computed).** 261,498,926 oz × 31.1034768 g = **≈8,133.5 metric tonnes**.

## 2. Legal basis of $42.2222 and the price history

- **Statute.** 31 U.S.C. 5117(b): outstanding gold certificates may be "not more than the value (for the purpose of issuing those certificates, of 42 and two-ninths dollars a fine troy ounce) of the gold held against gold certificates." 42 2/9 = $42.2222. https://www.law.cornell.edu/uscode/text/31/5117 (current code)
- **1973 act.** Pub. L. 93-110 (H.R. 6912), approved **Sept 21, 1973**, 87 Stat. 352, "An Act To amend the Par Value Modification Act." It struck "one thirty-eighth of a fine troy ounce of gold" and inserted "0.828948 Special Drawing Right or, the equivalent in terms of gold, of forty-two and two-ninths dollars per fine troy ounce of gold." The same act (Sec. 3) repealed Sections 3 and 4 of the Gold Reserve Act of 1934 on private ownership, effective on a later presidential finding. https://www.govinfo.gov/content/pkg/STATUTE-87/pdf/STATUTE-87-Pg352.pdf
- **1972 act ($38).** Pub. L. 92-268 (S. 3160), approved **March 31, 1972**, 86 Stat. 116, "Par Value Modification Act": "a new par value of the dollar of $1 equals one thirty-eighth of a fine troy ounce of gold." https://www.govinfo.gov/content/pkg/STATUTE-86/pdf/STATUTE-86-Pg116.pdf
- **1934 ($20.67 to $35).** Federal Reserve History: "individuals and institutions received currency at a rate of $35 per ounce of gold. This rate reduced the gold value of the dollar to 59 percent of the value set by the Gold Act of 1900, which equaled $20.67 per ounce." The essay also says "Section 2 of the act transferred ownership of all monetary gold in the United States to the US Treasury." The Gold Reserve Act was signed Jan 30, 1934. https://www.federalreservehistory.org/essays/gold-reserve-act (Richardson, Komai & Gou, written as of Nov 22, 2013)
- **Accounting rate used by Treasury and OIG.** "reported in these schedules at the values stated in 31 U.S.C. §5116 and §5117 (statutory rates) which are $42.2222 per fine troy ounce." https://oig.treasury.gov/system/files/2025-12/OIG-26-002-%28locked%29.pdf (OIG-26-002, Dec 12, 2025, Note 2)

## 3. Gold certificates: Treasury and the Fed

- **H.4.1, week ended Nov 4, 2026** (released Nov 5, 2026): "Gold stock" = **$11,041 million** (Table 1). "Gold certificate account" = **$11,037 million** (Table 5). https://www.federalreserve.gov/releases/h41/current/ (as fetched 2026-11-10; dated archive: https://www.federalreserve.gov/releases/h41/20261105/)
- **The Fed owns no gold.** Fed FAQ: "The Federal Reserve does not own gold." "The Gold Reserve Act of 1934 required the Federal Reserve System to transfer ownership of all of its gold" to Treasury, and the Fed received gold certificates in return. "Gold certificates are denominated in U.S. dollars." The certificates carry no right to redeem for gold. https://www.federalreserve.gov/faqs/does-the-federal-reserve-own-or-hold-gold.htm (last updated Nov 5, 2024)
- **Custody split.** Same Fed FAQ: about 5% of Treasury gold is held by the Reserve Banks, mostly at the NY Fed, and the remaining 95% "is held in custody for the Treasury by the U.S. Mint." The Oct 31, 2026 data match this: 5.1% FRB.
- **How monetization works.** CRS IF13109: Treasury "monetized the gold by issuing gold certificates to the Fed," and the Fed "credited the Treasury's General Account held at the Fed." Certificates must be "less than or equal to the book value" of the gold stock. CRS gives certificates at $11.037bn against a statutory gold value of about $11.041bn. "Monetization or demonetization would also take place if the statutory value of the gold were changed." https://www.everycrsreport.com/reports/IF13109.html (Sept 23, 2025)
- **Gap (computed).** $11.041bn minus $11.037bn is about $4m of gold not monetized. This fits the statutory cap.

## 4. Where the gold sits

- **Locations.** Mint deep storage at Fort Knox, West Point and Denver, Mint working stock, and the FRB NY vault plus a display. Source: Fiscal Data API line items above and the CRS IF13109 Table 1 (as of Aug 31, 2025: 261,498,926.24 oz, $11,041,059,957.90).
- **NY Fed share.** "The Federal Reserve Bank of New York holds 99.98% of the total United States-owned gold bars and coins held by FRBs within its vault." https://oig.treasury.gov/system/files/2026-01/OIG-26-004-%28secured%2C-508%29.pdf (OIG-26-004, Dec 19, 2025, Note 2)
- **Deep storage.** "Deep storage is defined as that portion of the Treasury-owned gold and silver bullion reserves which the Mint secures in sealed vaults." "The Mint did not use deep storage gold or silver reserves to produce coins in fiscal years 2025 and 2024." Reserves "are not assets of the Mint, but are assets of Treasury." OIG-26-002 (Dec 12, 2025), Note 1.
- **GAO description of sites (2011).** "the United States Bullion Depository at Fort Knox, Kentucky," "the Mint at Denver, Colorado," "the Mint at West Point, New York," and the "Federal Reserve Bank of New York." GAO-11-768T. https://gao.gov/assets/a126524.html

## 5. Audits

- **Treasury OIG, FY2025, Mint deep storage.** OIG-26-002, "Audit of the United States Mint's Schedules of Custodial Deep Storage Gold and Silver Reserves as of September 30, 2025 and 2024," Dec 12, 2025. Clean opinion: schedules "are presented fairly, in all material respects"; "no material weaknesses"; "no reportable noncompliance." Deep storage gold: **245,262,897.04 oz**, statutory value **$10,355,539,091**, market value **$938,204,160,047** at Sept 30, 2025. https://oig.treasury.gov/system/files/2025-12/OIG-26-002-%28locked%29.pdf
- **Treasury OIG, FY2025, FRB-held gold.** OIG-26-004, Dec 19, 2025. Clean opinion. **13,452,810.532 oz** (bars 13,378,981.032 and coins 73,829.500), statutory value **$568,007,257**, market value **$51,461,036,128** at Sept 30, 2025. https://oig.treasury.gov/system/files/2026-01/OIG-26-004-%28secured%2C-508%29.pdf
- **Audit history (GAO, 2011).** GAO-11-768T (June 23, 2011, Gary T. Engel):
  - 1974: "In 1974, in response to congressional interest and in conjunction with the Mint, GAO assisted in the planning" of an audit. GAO audited 3 of 13 Fort Knox compartments and reported no differences.
  - 1975: Treasury then established the "Committee for Continuing Audits of United States Government-owned Gold."
  - By Sept 30, 1986, "about 92 percent" of the gold had been audited.
  - Since 1995, "the Treasury OIG has annually audited the deep storage gold reserves." The OIG inspects joint seals on all 42 compartments each year.
  - Source: https://gao.gov/assets/a126524.html
- **GAO Review article.** "Yes There Is Gold at Fort Knox," GAO Review, Summer 1975. The catalog page has no text. https://www.gao.gov/products/091066
- **2017 Mnuchin visit.** Treasury OIG memo, Oct 4, 2017 (Rich Delmar to IG Thorson), "Inquiry Re Use of Government Aircraft by Secretary Mnuchin":
  - It concerns Mnuchin's use, "on August 21, of a government aircraft for a trip to the Mint's Bullion Depository in Kentucky."
  - It describes an "official event with Senate Majority Leader McConnell and other officials and visit to Mint's Bullion Depository at Ft. Knox."
  - "There is no indication that the date was chosen to coincide with the solar eclipse."
  - An Air Force C-37B was used "at a stated cost of $26,900.25."
  - Source: https://oig.treasury.gov/system/files/Audit_Reports_and_Testimonies/Treasury-OIG-Travel-Inquiry-To-Inspector-General-Thorson.pdf

## 6. Market value

- **Official dated price.** Treasury OIG notes, both reports: "At September 30, 2025 and 2024, the market values of gold per the LBMA Gold Price (PM) were $3,825.30 and $2,629.95 per FTO respectively." OIG-26-002 and OIG-26-004 (Dec 2025).
- **Total at that price (computed).** 261,498,926 oz × $3,825.30 = **≈$1.0003 trillion**, which supports the "$1 trillion" headline. Using OIG's own figures, deep storage ($938.2bn) plus FRB ($51.5bn) = $989.7bn. Mint working stock is excluded from that sum (2.78m oz, ≈$10.6bn at $3,825.30, computed).
- **Market-to-book ratio (computed).** $3,825.30 / $42.2222 ≈ 90.6×. Book value is about 1.1% of market value.
- **CRS figure.** "the market value of that gold has risen to over $900 billion as of September 11, 2025." CRS IF13109.

## 7. "Revalue the gold" debate (all PROPOSALS, none enacted as far as we could confirm)

- **CRS mechanism.** Any change to the statutory value would monetize or demonetize gold through the certificate account (quotes in Section 3). CRS IF13109, Sept 23, 2025.
- **S. 954, BITCOIN Act of 2025 (PROPOSAL).** Sen. Lummis, with Sens. Justice, Tuberville, Moreno, Marshall and Blackburn. Introduced March 11, 2025. Sec. 9(c) would make Reserve Banks tender gold certificates within 180 days, and the Secretary would "issue new gold certificates to the Federal reserve banks that reflect the fair market value price" of the gold. The aim is to offset the cost of a Strategic Bitcoin Reserve. CRS says it was referred to Senate Banking. https://www.govinfo.gov/content/pkg/BILLS-119s954is/html/BILLS-119s954is.htm
- **H.R. 3795, Gold Reserve Transparency Act of 2025 (PROPOSAL, audit only, no revaluation).** Rep. Massie, with Reps. Davidson, McDowell and Nehls. Introduced June 6, 2025. It would require "a full assay, inventory, and audit of all gold reserves" by an independent auditor within 9 months and every 5 years after, including "encumbrances, including those due to lease, swap, or similar transactions." https://www.govinfo.gov/content/pkg/BILLS-119hr3795ih/html/BILLS-119hr3795ih.htm

## 8. International comparison

- **U.S. tonnage.** Treasury data put the U.S. at ≈8,133.5 t (computed, Section 1).
- **WGC data source.** WGC's reserves page says the data come from IMF IFS: "IFS data are two months in arrears, so holdings are as of September 2026 for most countries." Dashboard "Data as of 30 September, 2026"; header dated Nov 4, 2026. https://www.gold.org/goldhub/data/gold-reserves-by-country
- **WGC monthly stats** (data to Aug 31, 2026; source "IMF, respective central banks, World Gold Council"):
  - China "around 2,387t" (9% of reserves)
  - Russia "2,271t"
  - Poland bought 98t year to date
  - Central banks bought about 170t year to date in total
  - Source: https://www.gold.org/download/file/21213/CB_Blog_Post_Oct26.pdf (Marissa Salim, WGC, created Oct 14, 2026)
- **Comparison (computed).** U.S. ≈8,133 t is about 3.4× China's ~2,387 t and about 3.6× Russia's ~2,271 t.

## Flags / not verified

1. **No current (Nov 2026) spot price verified.** LBMA price tables now need a licence on the MyLBMA portal, and the CME settlements page returned 503. The only official dated price we found is the LBMA PM of $3,825.30 on Sept 30, 2025, as cited by Treasury OIG. **The ~$1.0tn figure is a Sept 30, 2025 valuation.** Get a licensed LBMA PM quote, or cite "as of Sept 30, 2025", before publishing. If gold has moved since, the headline number changes.
2. **Not verified on primary: Germany, Italy, France and IMF tonnages, and U.S. % of reserves.** The WGC country spreadsheet (World_official_gold_holdings_as_of_Nov2026_IFS.xlsx) returned 403. Figures like Germany ~3,350 t and the U.S. "8,133.5 t" in WGC tables come only from secondary sites. Our U.S. tonnage is computed from Treasury ounces.
3. **1974 congressional visit details not verified on a primary page.**
   - Verified: Mint Director Mary Brooks led congressmen and journalists into Fort Knox on Sept 23, 1974. This appears in secondary sources only; the usmint.gov pages, including the "Inspection of Gold at Fort Knox" historical document, returned 403.
   - Disputed: the delegation leader (Rep. Philip Crane vs. Rep. John Conlan) and headcount.
   - Verified on primary: GAO's 1974 partial audit (3 of 13 compartments), from GAO-11-768T.
4. **Mint Fort Knox page not read.** usmint.gov returned 403, so claims such as "first gold arrived 1937" and "about half of Treasury gold" were not read on the primary page. Fiscal Data shows Fort Knox at 56.3%.
5. **Mnuchin "first Treasury Secretary since 1948 (John Snyder)" not verified.** It comes from a tweet quoted in news coverage. The OIG memo confirms only the visit and its date.
6. **Bill status not confirmed.** congress.gov returned 403, so S. 954 and H.R. 3795 latest actions were not checked. CRS (Sept 2025) says they were referred to committee. We found no 2026 bill. Do not say any revaluation bill passed.
7. **Precision of the statutory price.** Statute: "42 and two-ninths dollars" ($42.2222...). Fiscal Data and CRS print $42.222; OIG prints $42.2222. Use "$42.22" on screen.
8. **31 U.S.C. 5117 vs. the 1973 act.** The current text of 5117(b) comes from the 1982 recodification (Pub. L. 97-258). The $42 2/9 figure originates in Pub. L. 93-110 (1973). The Cornell notes do not name the 1973 act; the link was made through the 1973 statute text itself.
9. **No official Fed or Treasury statement on revaluation reviewed.** Bessent's February 2025 remarks ("audit every year", "monetize the asset side") appear in search snippets only. GAO-26-109081 (Sept 2026) does not discuss gold.
10. **H.4.1 date.** We used the "current" release (Nov 5, 2026, week ended Nov 4). Archive the dated URL before publishing.
