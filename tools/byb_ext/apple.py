SLUG = "before-you-buy-apple-2026-11"
GEN = "tools/gen_byb_apple_storyboard.py"
CLAIMS = '''
  - id: qtr
    text: "10-Qs and Q4 release, net sales by category ($M): Q1 FY26 (Dec quarter) total 143,756, iPhone 85,269; FY2026 total 478,834, so the Dec quarter was 30.0% of the year (our calc.). Q4 FY26 (Sep quarter) year over year (our calc.): iPhone +17.5%, Mac +23.7%, iPad -10.4%, Wearables, Home and Accessories -7.9%."
    spoken: about one hundred and forty-four billion dollars
    display: "Dec quarter $143.8bn = 30% of FY2026 sales (10-Q; our calc.)"
    fields: {dec_share_spoken: thirty percent, dec_iphone_spoken: about eighty-five billion dollars, iph_spoken: seventeen and a half percent, mac_spoken: almost twenty-four percent, ipad_spoken: about ten percent, wear_spoken: about eight percent}
    source_ids: [tenk, q4]
    status: source_located

  - id: ocfq
    text: "10-K cash-flow statement: operating cash flow $111,482M (FY2025) and $145,097M (FY2026), +30% (our calc.); 'Other current and non-current liabilities' +$13.7bn in FY2026 vs -$11.1bn in FY2025; inventories $5.7bn to $14.5bn. 8-K: $7.5bn of notes issued Nov 9, 2026 (seven tranches, 2028-2036; sum our calc.)."
    spoken: about one hundred and eleven billion dollars
    display: "Operating cash $111.5bn → $145.1bn (+30%); timing items inside (10-K)"
    fields: {jump_spoken: thirty percent, liab_spoken: about fourteen billion dollars, liab_prior_spoken: about eleven billion dollars, inv0_spoken: about six billion dollars, inv1_spoken: about fourteen and a half billion dollars, notes_spoken: seven and a half billion dollars}
    source_ids: [tenk]
    status: source_located

  - id: conc
    text: "10-K: 'Substantially all of the Company's hardware products are manufactured by outsourcing partners'; two vendors accounted for 45% and 27% of vendor non-trade receivables; one customer accounted for 13% of total trade receivables; cellular network carriers accounted for 33% of trade receivables. Names not disclosed."
    spoken: forty-five percent
    display: "Two vendors: 45% and 27% of vendor receivables; carriers 33% of trade receivables (10-K)"
    fields: {v2_spoken: twenty-seven percent, carriers_spoken: a third, one_spoken: thirteen percent}
    source_ids: [tenk]
    status: source_located
'''
SEGS = [
 dict(after="m1_where", id="m1_rhythm", chapter="The machine", claims=["qtr"],
      narration="Apple's year also has a very uneven rhythm. The December quarter alone brought in {{qtr}}, about {{qtr.dec_share_spoken}} of the whole year, with {{qtr.dec_iphone_spoken}} from the iPhone in just those three months. Now look at the September quarter, the one just reported. The iPhone grew {{qtr.iph_spoken}} and the Mac {{qtr.mac_spoken}}, while the iPad fell {{qtr.ipad_spoken}} and wearables slipped {{qtr.wear_spoken}}. So two product lines carried the growth, and two of them shrank.",
      scene='''
stage("s09b_rhythm", "m1_rhythm", {
    "zones": [Z("shop")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Now look at"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="ONE GIANT QUARTER", at=0.2, until=C("Now look at"), size=60, color="gold"),
              it("counter", x=800, y=280, at=C("The December quarter"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "brought in"}, 143.8]], text="DEC QUARTER = 30% OF THE YEAR", until=C("Now look at")),
              it("letters", x=1000, y=100, text="SEP QUARTER, YEAR OVER YEAR", at=C("Now look at"), size=52, color="gold"),
              it("sign", x=600, y=260, text="IPHONE +17.5%", at=C("The iPhone grew"), color="#C8E6C9", size=32),
              it("sign", x=1000, y=260, text="MAC +23.7%", at=C("and the Mac"), color="#C8E6C9", size=32),
              it("sign", x=1400, y=260, text="IPAD −10.4%", at=C("the iPad fell"), color="#FFCDD2", size=32),
              it("sign", x=1750, y=360, text="WEARABLES −7.9%", at=C("wearables slipped"), color="#FFCDD2", size=30),
              buddy(450, 860, at=0.3, mood="happy", label="AAPL", hop=14)]},
    sources=["tenk", "q4"])
'''),
 dict(after="m2_ai", id="m2_quality", chapter="The cash", claims=["ocfq", "lenses", "cap"],
      narration="Now, one honest footnote on all that cash. Operating cash flow jumped from {{ocfq}} to {{lenses.ocf_spoken}}, about {{ocfq.jump_spoken}} in a single year. Part of that was timing. A swing in other liabilities added {{ocfq.liab_spoken}} this year, after taking away {{ocfq.liab_prior_spoken}} the year before. And inventories climbed from {{ocfq.inv0_spoken}} to {{ocfq.inv1_spoken}}. So this year's cash was strong, but not all of it is a new normal. And the day before our data date, Apple still sold {{ocfq.notes_spoken}} of new bonds, even with net cash of {{cap.netcash_spoken}}.",
      scene='''
stage("s15b_quality", "m2_quality", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Part of that"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}, {"at": C("And the day before"), "x": 1000, "y": 520, "zoom": 1.05, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="A FOOTNOTE ON THE CASH", at=0.2, size=58, color="gold"),
              it("counter", x=750, y=270, at=C("Operating cash flow"), prefix="$", suffix="BN", decimals=1, steps=[[0, 111.5], [{"cue": "jumped"}, 145.1]], text="OPERATING CASH FLOW (+30%)"),
              it("sign", x=1400, y=250, text="OTHER LIABILITIES: +$13.7BN (VS −$11.1BN)", at=C("A swing in"), color="#FFE0B2", size=28),
              it("sign", x=1400, y=360, text="INVENTORIES $5.7BN → $14.5BN", at=C("And inventories"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=520, text="NOV 9: $7.5BN OF NEW BONDS (8-K)", at=C("Apple still sold"), color="#BBDEFB", size=30),
              buddy(1750, 860, at=0.3, mood="worry", label="CASH", color="#23995A", hop=12)]},
    sources=["tenk"])
'''),
 dict(after="m5_tariffs", id="m5_partners", chapter="Risks and upside", claims=["conc"],
      narration="And there's a quieter concentration risk. Almost all of Apple's hardware is built by outsourcing partners, and just two suppliers account for {{conc}} and {{conc.v2_spoken}} of the money vendors owe Apple. On the selling side, phone carriers make up {{conc.carriers_spoken}} of what customers owe Apple, and one single customer alone is {{conc.one_spoken}}. Apple doesn't name any of them. But if one big partner stumbles, on either end of the chain, it shows up in Apple's numbers.",
      scene='''
stage("s34b_partners", "m5_partners", {
    "zones": [Z("port")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("On the selling side"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="RISK 4 · A FEW BIG PARTNERS", at=0.2, size=52, color="gold"),
              it("sign", x=600, y=250, text="2 SUPPLIERS: 45% + 27%", at=C("just two suppliers"), color="#FFE0B2", size=32),
              it("sign", x=1350, y=250, text="CARRIERS: 33% OF RECEIVABLES", at=C("phone carriers"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=360, text="ONE CUSTOMER: 13%", at=C("one single customer"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=520, text="NAMES NOT DISCLOSED (10-K)", at=C("doesn't name"), color="#F5F5F5", size=28),
              ship(kind="cargo", x=[[0, 200], [12, 1400]], y=760, scale=0.7),
              buddy(1750, 860, at=0.4, mood="worry", label="AAPL", hop=12)]},
    sources=["tenk"])
'''),
]
