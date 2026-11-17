# Ep 59 research notes: Who Actually Owns America's $40 Trillion in Debt? (read 2026-11-17)

Primary sources only (Treasury, Federal Reserve, CRS reproducing the Trustees and CBO). Raw pulls are reproducible with the URLs below.

## Treasury, Debt to the Penny (Fiscal Data API `v2/accounting/od/debt_to_penny`)
- Nov 13, 2026 (latest record): total $40,616,678,827,092.07; held by the public $32,825,322,014,326.67; intragovernmental $7,791,356,812,765.40.
- Nov 13, 2025: total $38,150,716,416,656.92 -> +$2.466T in a year (≈ $6.76bn/day, our calc.).
- Sep 30, 2026 (end of FY2026): total $40,171.8bn; Aug 31, 2026: total $40,175.6bn, public $32,415.0bn; Dec 31, 2025: intragov $7,667.3bn.
- First record at/above: $38T Oct 21, 2025; $39T Mar 17, 2026 (dipped below and re-crossed in March and May); $40T Aug 18, 2026.

## Treasury, MSPD Table I (Oct 31, 2026)
- Marketable held by public $32,129.4bn: bills 7,381.3; notes 16,333.5; bonds 5,549.9; TIPS 2,156.8; FRNs 707.9. Savings bonds 145.2.

## Treasury auctions (Fiscal Data `v1/accounting/od/auctions_query`)
- Auctions dated Oct 1, 2025 - Sep 30, 2026: 436 (328 bills, 82 notes, 26 bonds); total accepted ≈ $32.9T (includes SOMA add-ons).
- 10-year note Aug 12, 2026 (91282CRF0): offering $42.0bn; competitive tendered $106.16bn, accepted $41.82bn; bid-to-cover 2.53;
  high yield 4.683%; indirect $32.09bn, direct $6.14bn, primary dealers $3.60bn; SOMA add-on $10.62bn (not part of the offering).
- The dataset's latest complete results when read: Oct 15, 2026.

## TIC (Treasury International Capital)
- Table 5 (`slt_table5.txt`), August 2026, $bn: Japan 1,068.3; UK 1,009.5; China 590.7; Belgium 490.5; Canada 464.6; Cayman 463.0;
  Luxembourg 448.2; France 363.4; Ireland 352.1; Taiwan 298.4; Switzerland 285.8; Singapore 277.9; Hong Kong 261.5; India 219.7;
  Norway 214.0 ... Grand total 9,331.7; foreign official 3,755.6.
- Note on the table: data come from U.S.-based custodians and broker-dealers; overseas custody "may not be attributed to the actual owners".
- Historical (`mfhhis01.txt`): China peak $1,316.7bn (Nov 2013).

## Federal Reserve
- H.4.1 (released Nov 12, 2026): Treasury securities held outright Wednesday Nov 11, 2026 $4,586,607m (bills $580,660m;
  nominal notes/bonds $3,620,738m; TIPS $277,656m; inflation comp. $107,554m). Week-average change vs Nov 12, 2025: total +$390,388m,
  bills +$382,036m.
- TREAST (H.4.1 series via FRED): peak $5,771,393m on Jun 8, 2022.
- Z.1 (Sep 11, 2026), Treasury securities levels, 2026:Q2 ($bn): liabilities 30,878.3 (face); holders (market value) total 29,013.6:
  households 2,831.1; nonfinancial corporate 218.6; noncorporate 94.8; state & local govts 1,647.6; central bank 4,082.7;
  U.S.-chartered banks 1,799.1; foreign banking offices 140.0; banks in U.S.-affiliated areas 28.2; credit unions 73.6; P&C 380.2;
  life 229.2; private pensions 590.2 (DB 280.3, DC 310.0); federal pensions 23.3; state & local pensions 561.6; MMFs 3,281.6;
  mutual funds 1,741.2; closed-end 2.0; ETFs 807.6; hedge funds 123.5; GSEs 274.2; ABS 18.6; broker-dealers 566.7; holding cos 129.4;
  other financial 99.3; rest of world 9,269.2; discrepancy 1,864.7.
- Note: the old `releases/z1/current/html/l210.htm` URL no longer exists; the table is now `F3_2_s.htm`.

## Monthly Treasury Statement, Table 9 (FY2026 through Sep 30, 2026; $bn)
- Net interest 1,051.8 (FY2025 970.4); national defense 965.2 (916.6); Social Security 1,667.1; Medicare 1,072.6; health 1,025.6;
  total outlays 7,395.8 (7,010.0); total receipts 5,403.3 (5,234.6) -> deficit ≈ 1,992.5 (our calc.).

## Average interest rates (Fiscal Data `v2/accounting/od/avg_interest_rates`)
- Total marketable: 1.455% (Oct 31, 2021), 3.393% (Oct 31, 2025), 3.570% (Oct 31, 2026). Bills 4.014% (Oct 31, 2026).

## Social Security (CRS IF13256, Jun 25, 2026, from the 2026 Trustees Report)
- Reserves start 2025 $2,721.5bn; end 2025 $2,561.3bn; revenue $1,449.3bn; costs $1,609.5bn; change -$160.2bn.
- OASI depleted Q4 2032; combined OASDI Q3 2034; ≈ 83% of scheduled benefits payable in 2034 (≈ 65% by 2100).
- ssa.gov returned HTTP 403 to automated access.

## CBO (via CRS R44383, updated Nov 5, 2026; and R49408, Sep 30, 2026)
- February 2026 baseline: FY2026 net interest projected $1.039T (3.3% of GDP); FY2036 4.6% of GDP; previous high since FY1940:
  3.2% (FY1991). cbo.gov returned HTTP 403 to automated access (the FY2026 Monthly Budget Review could not be read directly).
