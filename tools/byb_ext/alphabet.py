SLUG = "before-you-buy-alphabet-2026-11"
GEN = "tools/gen_byb_alphabet_storyboard.py"
CLAIMS = '''
  - id: geo
    text: "10-Q, Q3 2026: United States 53% of revenue ($67.7bn, +39% year over year); EMEA 26%; APAC 16%; Other Americas 5%; FY2025 U.S. share 48% (10-K). Advertising $82,012M of $127,577M = 64% of Q3 revenue (our calc.); 10-K: 'more than 70% of total revenues from online advertising in 2025'. Network impressions -14% (10-Q). Pichai (Q3 release): 'now on a half-trillion dollar revenue run rate' (company claim)."
    spoken: fifty-three percent
    display: "Q3 2026: U.S. 53% of revenue (+39%) · ads 64% (10-Q; our calc.)"
    fields: {us_growth_spoken: thirty-nine percent, us_prior_spoken: forty-eight percent, ads_spoken: about sixty-four percent, net_spoken: fourteen percent}
    source_ids: [tenq, rel]
    status: source_located

  - id: stakes
    text: "10-Q, Sep 30, 2026: marketable equity includes $75.2bn of SpaceX shares 'subject to short-term restrictions on the ability to sell'; non-marketable securities $135.2bn, of which about $128.2bn is 'primarily … our investment in one private company' (not named). Together ≈ 5.8% of market value (our calc.). Q3 other income and expense -$8.2bn, 'net unrealized losses in our marketable equity securities largely from SpaceX'. June 2026 offering price '$355.1982 per share' (Class A); Nov 10 close $287.38 is 19% below (our calc.)."
    spoken: about seventy-five billion dollars
    display: "SpaceX stake $75.2bn + one private company ≈ $128.2bn (10-Q)"
    fields: {private_spoken: about one hundred and twenty-eight billion dollars, mcshare_spoken: about six percent, q3loss_spoken: about eight billion dollars, offer_spoken: about three hundred and fifty-five dollars, below_spoken: nineteen percent}
    source_ids: [tenq, px]
    status: source_located

  - id: fines
    text: "10-Q Note 10: European Commission ad tech fine recorded as a $3.5bn charge, under appeal; EU DMA decisions (Play and Search) recorded as a $1.0bn charge in Q3 2026, under appeal; PriceRunner (Stockholm) 'approximately $2.1 billion … in principal damages plus accrued interest', under appeal; DOJ ad tech: a Texas state AG trial follows; 'We cannot estimate a possible loss.'"
    spoken: three and a half billion dollars
    display: "EU ad tech $3.5bn charge · DMA $1.0bn · PriceRunner ≈ $2.1bn (10-Q)"
    fields: {dma_spoken: one billion dollars, pr_spoken: about two point one billion dollars}
    source_ids: [tenq]
    status: source_located
'''
SEGS = [
 dict(after="m1_cloud", id="m1_geo", chapter="The machine", claims=["geo"],
      narration="That shift shows up on the map too. In the September quarter, the United States made up {{geo}} of revenue, growing {{geo.us_growth_spoken}}, up from {{geo.us_prior_spoken}} of the total last year, in line with that American cloud and chip demand. And advertising fell to {{geo.ads_spoken}} of quarterly revenue, from more than seventy percent last year. Impressions on partner sites dropped {{geo.net_spoken}}. Sundar Pichai says the company is now on a half trillion dollar revenue run rate. That's his framing, but the math roughly checks out.",
      scene='''
stage("s09b_geo", "m1_geo", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("And advertising fell"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE MIX IS SHIFTING", at=0.2, size=60, color="gold"),
              it("sign", x=650, y=250, text="U.S. 53% OF REVENUE (+39%)", at=C("the United States"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=250, text="WAS 48% LAST YEAR", at=C("up from"), color="#F5F5F5", size=30),
              it("sign", x=650, y=380, text="ADS: 64% OF THE QUARTER", at=C("And advertising fell"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=380, text="PARTNER IMPRESSIONS −14%", at=C("Impressions on partner"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=520, text="'HALF-TRILLION RUN RATE' (CEO CLAIM)", at=C("Sundar Pichai"), color="#C8E6C9", size=28),
              buddy(1750, 860, at=0.3, mood="happy", label="GOOG", color="#3DF5FF", hop=14)]},
    sources=["tenq", "rel"])
'''),
 dict(after="m2_returns", id="m2_stakes", chapter="The cash", claims=["stakes", "cap"],
      narration="There's also a strange pile of investments on the balance sheet. Alphabet holds {{stakes}} of SpaceX shares, which it can't sell right away, and one unnamed private company carried at {{stakes.private_spoken}}. Together, by our math, that's about {{stakes.mcshare_spoken}} of Alphabet's own market value. Those are marks, not cash, and they swing. In the September quarter, mostly SpaceX, they cost about {{stakes.q3loss_spoken}} on paper. And the new shares sold in June went out at about {{stakes.offer_spoken}} each. Today's price is {{stakes.below_spoken}} lower.",
      scene='''
stage("s16b_stakes", "m2_stakes", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Those are marks"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="A PILE OF STAKES", at=0.2, size=60, color="gold"),
              it("sign", x=650, y=250, text="SPACEX SHARES $75.2BN (RESTRICTED)", at=C("of SpaceX shares"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=250, text="ONE PRIVATE CO. ≈ $128.2BN", at=C("one unnamed private"), color="#BBDEFB", size=28),
              it("sign", x=1000, y=370, text="≈ 6% OF MARKET VALUE (OUR CALC.)", at=C("Together, by our math"), color="#FFF8E1", size=28),
              it("sign", x=1000, y=480, text="Q3: −$8.2BN ON PAPER", at=C("they cost"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=590, text="JUNE OFFER $355.20 → NOV 10 CLOSE $287.38", at=C("the new shares"), color="#FFE0B2", size=28),
              buddy(1750, 860, at=0.3, mood="worry", label="GOOG", color="#3DF5FF", hop=12)]},
    sources=["tenq", "px"])
'''),
 dict(after="m5_legal", id="m5_fines", chapter="Risks and upside", claims=["fines"],
      narration="And the bills from Europe keep coming. The European ad tech fine was booked as a {{fines}} charge, and the two digital markets decisions added another {{fines.dma_spoken}} last quarter, all under appeal. A Swedish price comparison site won about {{fines.pr_spoken}} in damages, also under appeal. A Texas trial on ad tech is still ahead, and for that one Alphabet says it can't estimate a possible loss.",
      scene='''
stage("s34b_fines", "m5_fines", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("A Swedish"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE BILLS FROM EUROPE", at=0.2, size=60, color="gold"),
              it("sign", x=650, y=260, text="EU AD TECH: $3.5BN CHARGE", at=C("The European ad tech"), color="#FFCDD2", size=30),
              it("sign", x=1350, y=260, text="DMA: +$1.0BN (Q3)", at=C("digital markets"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=390, text="PRICERUNNER ≈ $2.1BN (APPEAL)", at=C("A Swedish"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=520, text="TEXAS AD TECH TRIAL: 'CANNOT ESTIMATE'", at=C("A Texas trial"), color="#F5F5F5", size=28),
              buddy(1750, 860, at=0.4, mood="worry", label="GOOG", color="#3DF5FF", hop=12)]},
    sources=["tenq"])
'''),
]
