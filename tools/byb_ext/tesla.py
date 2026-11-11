SLUG = "before-you-buy-tesla-2026-11"
GEN = "tools/gen_byb_tesla_storyboard.py"
CLAIMS = '''
  - id: geo
    text: "Our calc. from the 10-K FY2025 and 10-Q, TTM revenue: U.S. $47.3bn (45.6%), China $20.8bn (20.1%), other international $35.5bn (34.3%). Q3 2026 (10-Q): U.S. $12.5bn (-14% year over year), other international $10.3bn (+32%). Q3 2026 Update: active FSD subscriptions 1.74 million (Q3 2025: 1.04 million); services and other revenue $16.3bn TTM (our calc.), gross profit 'a record $734M' in Q3."
    spoken: about forty-six percent
    display: "TTM revenue: U.S. 46% · China 20% · other 34% (our calc.)"
    fields: {china_spoken: about twenty percent, other_spoken: about thirty-four percent, us_q3_spoken: fourteen percent, intl_q3_spoken: thirty-two percent, fsd_spoken: one point seven four million, fsd_prior_spoken: one point oh four million, svc_spoken: about sixteen billion dollars}
    source_ids: [tenq, deck]
    status: source_located

  - id: stake
    text: "10-Q: Tesla invested $2.00bn in SpaceX stock (originally xAI preferred) on Mar 12, 2026; fair value $2.865bn at Sep 30, 2026; IPO lock-up 'expire[s] in December 2026'. SpaceX bought $626M of Megapacks in 9M 2026 (related party). Q3 2026 net income included a $142M loss on the SpaceX investment and a $288M bitcoin gain. 9M capex $13.01bn vs $6.13bn in 9M 2025."
    spoken: two billion dollars
    display: "SpaceX stake: $2.0bn in → $2.865bn fair value (10-Q)"
    fields: {fv_spoken: about two point nine billion dollars, mp_spoken: about six hundred and twenty-six million dollars, sx_loss_spoken: about one hundred and forty million dollars, btc_spoken: about two hundred and ninety million dollars, capex9_spoken: about thirteen billion dollars, capex9_prior_spoken: about six billion dollars}
    source_ids: [tenq]
    status: source_located

  - id: squeeze
    text: "Q3 2026 Update and 10-Q: TTM income from operations $3,466M on revenue $103,570M = 3.3% operating margin (our calc.). Operating expenses $4.78bn in Q3 2026 vs $3.43bn a year earlier, driven by 'SI and other R&D projects, SBC (including 2025 CEO Performance Award)'. Securities class action over Autopilot, FSD and Robotaxi claims (W.D. Tex., filed Aug 4, 2025); motion to dismiss fully briefed."
    spoken: three point three percent
    display: "TTM operating margin 3.3% · Q3 opex $4.78bn vs $3.43bn (deck; our calc.)"
    fields: {opex_spoken: about four point eight billion dollars, opex_prior_spoken: about three point four billion dollars}
    source_ids: [deck, tenq]
    status: source_located
'''
SEGS = [
 dict(after="m1_energy", id="m1_geo", chapter="The machine", claims=["geo"],
      narration="Where are the customers? Over the last twelve months, the United States brought in {{geo}} of revenue, China {{geo.china_spoken}}, and everywhere else {{geo.other_spoken}}. And the map is moving. Last quarter, U S revenue fell {{geo.us_q3_spoken}}, while other international markets grew {{geo.intl_q3_spoken}}. Software is creeping in too. Active Full Self Driving subscriptions reached {{geo.fsd_spoken}}, up from {{geo.fsd_prior_spoken}} a year earlier. And services, from repairs to charging, now bring in {{geo.svc_spoken}} a year.",
      scene='''
stage("s09b_geo", "m1_geo", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Software is creeping"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="WHERE THE CUSTOMERS ARE", at=0.2, size=56, color="gold"),
              it("sign", x=550, y=250, text="U.S. 46%", at=C("the United States brought"), color="#BBDEFB", size=32),
              it("sign", x=1000, y=250, text="CHINA 20%", at=C("China"), color="#FFE0B2", size=32),
              it("sign", x=1450, y=250, text="REST 34%", at=C("everywhere else"), color="#C8E6C9", size=32),
              it("sign", x=650, y=380, text="Q3: U.S. −14%", at=C("U S revenue fell"), color="#FFCDD2", size=30),
              it("sign", x=1350, y=380, text="Q3: OTHER INTL +32%", at=C("other international markets"), color="#C8E6C9", size=30),
              it("sign", x=1000, y=510, text="FSD SUBSCRIPTIONS 1.04M → 1.74M", at=C("Active Full Self Driving"), color="#BBDEFB", size=28),
              it("sign", x=1000, y=620, text="SERVICES ≈ $16.3BN / YEAR", at=C("And services"), color="#F5F5F5", size=28),
              buddy(1750, 860, at=0.3, mood="happy", label="TSLA", color="#E53935", hop=14)]},
    sources=["tenq", "deck"])
'''),
 dict(after="m2_returns", id="m2_stake", chapter="The cash", claims=["stake"],
      narration="Tesla also owns a piece of the Musk universe. In March it put {{stake}} into what is now SpaceX stock. By the end of September that stake was marked at {{stake.fv_spoken}}, and the lock up after the SpaceX listing ends in December. The flow goes both ways. SpaceX bought {{stake.mp_spoken}} of Tesla's Megapack batteries this year. These marks move the profit line. Last quarter, net income included a loss of {{stake.sx_loss_spoken}} on SpaceX and a gain of {{stake.btc_spoken}} on bitcoin. Meanwhile, capex in the first nine months more than doubled, to {{stake.capex9_spoken}} from {{stake.capex9_prior_spoken}}.",
      scene='''
stage("s16b_stake", "m2_stake", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("These marks"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="A PIECE OF THE MUSK UNIVERSE", at=0.2, size=54, color="gold"),
              it("sign", x=650, y=250, text="SPACEX STAKE: $2.0BN → $2.865BN", at=C("put"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=250, text="LOCK-UP ENDS DECEMBER", at=C("the lock up"), color="#F5F5F5", size=28),
              it("sign", x=1000, y=370, text="SPACEX BOUGHT $626M OF MEGAPACKS", at=C("SpaceX bought"), color="#FFE0B2", size=28),
              it("sign", x=650, y=490, text="Q3: SPACEX −$142M", at=C("a loss of"), color="#FFCDD2", size=28),
              it("sign", x=1350, y=490, text="Q3: BITCOIN +$288M", at=C("on bitcoin"), color="#C8E6C9", size=28),
              it("sign", x=1000, y=610, text="9M CAPEX $6.1BN → $13.0BN", at=C("capex in the first nine months"), color="#FFE0B2", size=28),
              buddy(1750, 860, at=0.3, mood="worry", label="TSLA", color="#E53935", hop=12)]},
    sources=["tenq"])
'''),
 dict(after="m5_demand", id="m5_squeeze", chapter="Risks and upside", claims=["squeeze"],
      narration="And the margin is already thin. Over the last twelve months, Tesla's operating margin was {{squeeze}}. Operating expenses last quarter were {{squeeze.opex_spoken}}, up from {{squeeze.opex_prior_spoken}} a year earlier, which Tesla puts down to its super intelligence and other research projects, and to stock pay, including the C E O's award. A securities class action over its Autopilot, self driving and Robotaxi claims is also pending. So the costs of the bet arrive before the revenue does.",
      scene='''
stage("s34b_squeeze", "m5_squeeze", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("A securities class action"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="A THIN MARGIN", at=0.2, size=60, color="gold"),
              it("sign", x=1000, y=250, text="TTM OPERATING MARGIN 3.3%", at=C("operating margin was"), color="#FFCDD2", size=32),
              it("sign", x=1000, y=370, text="Q3 OPEX $3.43BN → $4.78BN", at=C("Operating expenses"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=490, text="SI + R&D + STOCK PAY (INCL. CEO AWARD)", at=C("super intelligence"), color="#F5F5F5", size=28),
              it("sign", x=1000, y=610, text="SECURITIES CLASS ACTION PENDING", at=C("A securities class action"), color="#FFCDD2", size=28),
              buddy(1750, 860, at=0.4, mood="worry", label="TSLA", color="#E53935", hop=12)]},
    sources=["deck", "tenq"])
'''),
]
