SLUG = "before-you-buy-microsoft-2026-11"
GEN = "tools/gen_byb_microsoft_storyboard.py"
CLAIMS = '''
  - id: lines
    text: "10-Q, revenue by product line, Q1 FY27 vs Q1 FY26 ($M; growth our calc.): Microsoft 365 cloud 27,778 (+17%); Search and advertising 6,554 (+10%); Productivity and server licensing 8,407 (-3%); XBOX 5,379 (-2%); Windows OEM and devices 3,551 (-22%). Devices and Consumer segment revenue $15,484M (-3%); Agents and Infra operating margin 52.8% (our calc.). CFO: 'Inventory levels remain elevated' (PCs)."
    spoken: about twenty-eight billion dollars
    display: "Q1 FY27: M365 cloud $27.8bn +17% · Windows OEM −22% (10-Q)"
    fields: {m365_growth_spoken: seventeen percent, search_spoken: ten percent, win_spoken: twenty-two percent, xbox_spoken: two percent, lic_spoken: three percent, margin_spoken: almost fifty-three percent}
    source_ids: [tenq, call]
    status: source_located

  - id: oai
    text: "10-Q: Microsoft holds 'an approximate 24% interest on an as-converted basis' in OpenAI (equity method); receivables from OpenAI $7.2bn; funding commitments $13.0bn, of which $12.0bn funded. FY2026 revenue from OpenAI arrangements $24.1bn = 7.3% of revenue (our calc.). Risk factor: 'If an arrangement fails to adequately anticipate changing circumstances and interests of a party, it may result in early termination or renegotiation'. Market value of the stake not disclosed."
    spoken: about twenty-four percent
    display: "OpenAI: ≈24% stake · $7.2bn receivable · $12.0bn of $13.0bn funded (10-Q)"
    fields: {recv_spoken: about seven billion dollars, commit_spoken: thirteen billion dollars, funded_spoken: twelve billion, fy_spoken: about twenty-four billion dollars, fyshare_spoken: about seven percent}
    source_ids: [tenq]
    status: source_located
'''
SEGS = [
 dict(after="m1_openai", id="m1_lines", chapter="The machine", claims=["lines"],
      narration="Under the hood, the product lines are moving at very different speeds. Microsoft 365 cloud, the Office subscriptions, made {{lines}} in the quarter, up {{lines.m365_growth_spoken}}. Search and advertising grew {{lines.search_spoken}}. But the older businesses are shrinking. Windows sales to PC makers fell {{lines.win_spoken}}, Xbox slipped {{lines.xbox_spoken}}, and classic software licenses dropped {{lines.lic_spoken}}. So the cloud engine runs at an operating margin of {{lines.margin_spoken}}, while the consumer side is going backwards.",
      scene='''
stage("s09b_lines", "m1_lines", {
    "zones": [Z("cloudport")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("But the older businesses"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="DIFFERENT SPEEDS", at=0.2, size=60, color="gold"),
              it("sign", x=600, y=250, text="M365 CLOUD +17%", at=C("Microsoft 365 cloud"), color="#C8E6C9", size=32),
              it("sign", x=1000, y=250, text="SEARCH & ADS +10%", at=C("Search and advertising"), color="#C8E6C9", size=32),
              it("sign", x=600, y=380, text="WINDOWS OEM −22%", at=C("Windows sales"), color="#FFCDD2", size=32),
              it("sign", x=1000, y=380, text="XBOX −2%", at=C("Xbox slipped"), color="#FFCDD2", size=32),
              it("sign", x=1400, y=380, text="LICENSES −3%", at=C("classic software"), color="#FFCDD2", size=32),
              it("sign", x=1000, y=520, text="CLOUD ENGINE MARGIN ≈ 53%", at=C("So the cloud engine"), color="#BBDEFB", size=30),
              buddy(1750, 860, at=0.3, mood="happy", label="AZURE", hop=14)]},
    sources=["tenq"])
'''),
 dict(after="m5_partner", id="m5_stake", chapter="Risks and upside", claims=["oai"],
      narration="And the OpenAI tie runs deeper than revenue. Microsoft owns {{oai}} of OpenAI on an as-converted basis. OpenAI owes it {{oai.recv_spoken}}. And Microsoft has committed {{oai.commit_spoken}} of funding, with {{oai.funded_spoken}} of that already paid in. Last fiscal year, OpenAI brought in {{oai.fy_spoken}} of revenue, {{oai.fyshare_spoken}} of the total. Microsoft's own filing warns that a partnership that fails to anticipate changing circumstances may end early or be renegotiated. It doesn't put a market value on the stake, and neither will we.",
      scene='''
stage("s34b_stake", "m5_stake", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Last fiscal year"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE OPENAI TIE", at=0.2, size=60, color="gold"),
              it("sign", x=600, y=250, text="STAKE ≈ 24% (AS-CONVERTED)", at=C("Microsoft owns"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=250, text="OPENAI OWES $7.2BN", at=C("OpenAI owes it"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=370, text="FUNDING: $12.0BN OF $13.0BN PAID IN", at=C("has committed"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=490, text="FY2026: $24.1BN = 7.3% OF REVENUE", at=C("Last fiscal year"), color="#C8E6C9", size=30),
              it("sign", x=1000, y=610, text="'MAY RESULT IN EARLY TERMINATION OR RENEGOTIATION'", at=C("Microsoft's own filing"), color="#FFCDD2", size=26),
              buddy(1750, 860, at=0.4, mood="worry", label="MSFT", hop=12)]},
    sources=["tenq"])
'''),
]
