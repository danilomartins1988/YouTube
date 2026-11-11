SLUG = "before-you-buy-meta-2026-11"
GEN = "tools/gen_byb_meta_storyboard.py"
CLAIMS = '''
  - id: geo
    text: "Our calc. from the 10-K FY2025 and 10-Qs, TTM revenue by user geography: U.S. and Canada $95.2bn (39.4%), Europe $55.5bn (23.0%), Asia-Pacific $63.9bn (26.5%), Rest of World $27.0bn (11.2%). Q3 press release: headcount 66,775 (-15% year over year). 10-Q: 'In the nine months ended September 30, 2026, 89% of our total costs and expenses were recognized in FoA and 11% were recognized in RL.'"
    spoken: about thirty-nine percent
    display: "TTM revenue: U.S.&Canada 39% · Europe 23% · Asia-Pacific 27% · RoW 11% (our calc.)"
    fields: {eu_spoken: twenty-three percent, apac_spoken: about twenty-seven percent, row_spoken: eleven percent, staff_spoken: about sixty-seven thousand, staff_drop_spoken: fifteen percent, foa_cost_spoken: eighty-nine percent}
    source_ids: [tenq, rel]
    status: source_located

  - id: commit
    text: "10-Q: non-cancelable contractual commitments '$454.52 billion … with approximately $45.85 billion and $121.41 billion due in 2026 and 2027'. Sep 30, 2026: cash, equivalents and marketable securities $82,449M; debt (face) $84,000M. Shares outstanding 2,529,555,464 (Jan 23, 2026) to 2,556,241,253 (Oct 16, 2026), +1.05% (our calc.) with no buybacks."
    spoken: about four hundred and fifty-five billion dollars
    display: "$454.5bn of commitments; $121.4bn due in 2027 (10-Q)"
    fields: {due26_spoken: about forty-six billion dollars, due27_spoken: about one hundred and twenty-one billion dollars, cash_spoken: about eighty-two billion dollars, debt_spoken: about eighty-four billion dollars, shares_spoken: about one percent}
    source_ids: [tenq]
    status: source_located

  - id: youth
    text: "10-Q: settlement with state attorneys general, 'Approximately $12.7 billion … payable … in annual installments over a 10-year period'; about $5.3bn is contingent (payable only if peers adopt similar protections) and not accrued. 'counsel for over two hundred thousand individual claimants have sent mass arbitration demands'; next school-district bellwether February 2027; the DC Attorney General is 'seeking up to $1.7 billion in civil penalties'. Plaintiffs have said damages sought 'have at times in certain cases amounted to more than a trillion dollars' (a plaintiffs' claim, not an estimate)."
    spoken: about twelve point seven billion dollars
    display: "Youth cases: $12.7bn over 10 years · 200,000+ arbitration claimants · DC up to $1.7bn (10-Q)"
    fields: {contingent_spoken: about five point three billion dollars, claimants_spoken: more than two hundred thousand, dc_spoken: up to one point seven billion dollars}
    source_ids: [tenq]
    status: source_located
'''
SEGS = [
 dict(after="m1_ads", id="m1_geo", chapter="The machine", claims=["geo"],
      narration="Where does that money come from? The United States and Canada bring in {{geo}} of revenue. Europe, {{geo.eu_spoken}}. Asia Pacific, {{geo.apac_spoken}}. The rest of the world, {{geo.row_spoken}}. And the machine is getting leaner. Meta's headcount is down {{geo.staff_drop_spoken}} from a year ago, to {{geo.staff_spoken}} people. Almost all the spending, {{geo.foa_cost_spoken}} of costs, goes into the apps, and the rest into the headsets and glasses lab.",
      scene='''
stage("s09b_geo", "m1_geo", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("And the machine"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="WHERE THE AD MONEY COMES FROM", at=0.2, size=52, color="gold"),
              it("sign", x=500, y=250, text="U.S. & CANADA 39%", at=C("The United States"), color="#BBDEFB", size=30),
              it("sign", x=850, y=330, text="EUROPE 23%", at=C("Europe,"), color="#C8E6C9", size=30),
              it("sign", x=1200, y=250, text="ASIA-PACIFIC 27%", at=C("Asia Pacific"), color="#FFE0B2", size=30),
              it("sign", x=1550, y=330, text="REST OF WORLD 11%", at=C("The rest of the world"), color="#F5F5F5", size=30),
              it("sign", x=1000, y=480, text="HEADCOUNT 66,775 (−15%)", at=C("Meta's headcount"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=590, text="89% OF COSTS: THE APPS", at=C("Almost all the spending"), color="#FFF8E1", size=28),
              buddy(1750, 860, at=0.3, mood="happy", label="META", color="#FF4FD8", hop=14)]},
    sources=["tenq", "rel"])
'''),
 dict(after="m2_capital", id="m2_commit", chapter="The cash", claims=["commit"],
      narration="And the bills are already signed. Meta lists {{commit}} of non cancelable contractual commitments. About {{commit.due26_spoken}} is due this year, and {{commit.due27_spoken}} next year. At the end of September, it held {{commit.cash_spoken}} of cash and securities, against {{commit.debt_spoken}} of debt. So for the first time in years, the balance sheet is roughly even, and with no buybacks, the share count rose about {{commit.shares_spoken}} in nine months.",
      scene='''
stage("s15b_commit", "m2_commit", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("At the end of September"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE BILLS ARE ALREADY SIGNED", at=0.2, size=54, color="gold"),
              it("counter", x=760, y=270, at=C("Meta lists"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "non cancelable"}, 454.5]], text="COMMITMENTS (10-Q)"),
              it("sign", x=1400, y=230, text="DUE 2026: $45.9BN", at=C("due this year"), color="#FFE0B2", size=30),
              it("sign", x=1400, y=330, text="DUE 2027: $121.4BN", at=C("next year"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=500, text="CASH $82.4BN  ·  DEBT $84.0BN", at=C("At the end of September"), color="#BBDEFB", size=30),
              it("sign", x=1000, y=610, text="SHARES +1% IN 9 MONTHS", at=C("the share count rose"), color="#F5F5F5", size=28),
              buddy(1750, 860, at=0.3, mood="worry", label="CASH", color="#23995A", hop=12)]},
    sources=["tenq"])
'''),
 dict(after="m5_courts", id="m5_youth", chapter="Risks and upside", claims=["youth"],
      narration="And the youth safety cases aren't over. The settlement with the states is paid over ten years, with {{youth}} in installments, plus about {{youth.contingent_spoken}} more that only comes due if rivals like YouTube and TikTok adopt similar protections. Lawyers for {{youth.claimants_spoken}} people have sent mass arbitration demands. The next school district trial is set for February. And the District of Columbia is seeking {{youth.dc_spoken}} in penalties. Plaintiffs have claimed damages above a trillion dollars in some cases, but that's their number, not an estimate.",
      scene='''
stage("s32b_youth", "m5_youth", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Lawyers for"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="NOT OVER YET", at=0.2, size=60, color="gold"),
              it("sign", x=600, y=250, text="$12.7BN OVER 10 YEARS", at=C("paid over ten years"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=250, text="+$5.3BN IF RIVALS FOLLOW", at=C("only comes due"), color="#FFE0B2", size=28),
              it("sign", x=600, y=380, text="200,000+ ARBITRATION CLAIMANTS", at=C("Lawyers for"), color="#FFCDD2", size=28),
              it("sign", x=1350, y=380, text="NEXT TRIAL: FEB 2027", at=C("school district trial"), color="#BBDEFB", size=30),
              it("sign", x=1000, y=510, text="DC: UP TO $1.7BN", at=C("District of Columbia"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=630, text="'$1 TRILLION+' = PLAINTIFFS' CLAIM", at=C("Plaintiffs have claimed"), color="#F5F5F5", size=26),
              buddy(1750, 860, at=0.4, mood="worry", label="META", color="#FF4FD8", hop=12)]},
    sources=["tenq"])
'''),
]
