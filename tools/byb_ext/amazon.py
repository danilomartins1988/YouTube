SLUG = "before-you-buy-amazon-2026-11"
GEN = "tools/gen_byb_amazon_storyboard.py"
CLAIMS = '''
  - id: streams
    text: "Q3 2026 release supplemental, trailing twelve months (sums our calc.): third-party seller services $187,666M; advertising services $78,006M; subscription services $54,285M. AWS growth year over year excluding FX: 24% (Q4 2025), 28% (Q1 2026), 37% (Q2), 39% (Q3). Release: Prime Day moved to Q2 in 2026; 'Excluding this shift, third quarter year-over-year growth would have been approximately 400 basis points higher.'"
    spoken: about one hundred and eighty-eight billion dollars
    display: "TTM: seller services $187.7bn · ads $78.0bn · subscriptions $54.3bn (our calc.)"
    fields: {subs_spoken: about fifty-four billion dollars, g1_spoken: twenty-four, g2_spoken: twenty-eight, g3_spoken: thirty-seven, g4_spoken: thirty-nine percent, shift_spoken: about four percentage points}
    source_ids: [rel]
    status: source_located

  - id: bsheet
    text: "10-Q, Sep 30, 2026: cash and equivalents plus marketable securities $55,783M + $58,443M = $114,226M (sum our calc.); total face value of long-term debt $180,887M, including a $17.5bn term loan drawn in September 2026; long-term lease liabilities $98,824M; leases not yet commenced $164.9bn."
    spoken: about one hundred and fourteen billion dollars
    display: "Cash $114.2bn vs debt $180.9bn + leases $98.8bn (10-Q)"
    fields: {debt_spoken: about one hundred and eighty-one billion dollars, loan_spoken: seventeen and a half billion dollars, lease_spoken: about ninety-nine billion dollars, notyet_spoken: about one hundred and sixty-five billion dollars}
    source_ids: [tenq]
    status: source_located

  - id: chips
    text: "10-Q risk factor: 'we rely on a limited group of suppliers for semiconductor products, including products related to artificial intelligence infrastructure such as graphics processing units'; guidance cites 'resource and supply volatility, including for memory chips'. Xockets ITC patent case against AWS servers, seeking injunctive relief. Unrecognized tax contingencies about $7.3bn (10-Q)."
    spoken: about seven point three billion dollars
    display: "Chip suppliers · patent case vs AWS servers · tax contingencies ≈ $7.3bn (10-Q)"
    fields: {}
    source_ids: [tenq, rel]
    status: source_located
'''
SEGS = [
 dict(after="m1_backlog", id="m1_streams", chapter="The machine", claims=["streams"],
      narration="Behind the stores there are quieter money streams too. Fees from outside sellers who use Amazon's marketplace and warehouses brought in {{streams}} over the year. Advertising, about seventy eight billion. Prime and other subscriptions, {{streams.subs_spoken}}. And the cloud is speeding up, not slowing down. A W S growth went from {{streams.g1_spoken}}, to {{streams.g2_spoken}}, to {{streams.g3_spoken}}, to {{streams.g4_spoken}} over the last four quarters, ignoring currency moves. One caution for the stores. Prime Day moved to an earlier quarter this year, which Amazon says cut the latest quarter's growth by {{streams.shift_spoken}}.",
      scene='''
stage("s09b_streams", "m1_streams", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("And the cloud is speeding up"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE QUIETER STREAMS", at=0.2, size=58, color="gold"),
              it("sign", x=550, y=250, text="SELLER SERVICES $187.7BN", at=C("Fees from outside sellers"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=330, text="ADS $78.0BN", at=C("Advertising, about"), color="#FFE0B2", size=28),
              it("sign", x=1450, y=250, text="SUBSCRIPTIONS $54.3BN", at=C("Prime and other"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=470, text="AWS GROWTH: 24% → 28% → 37% → 39%", at=C("A W S growth went"), color="#C8E6C9", size=30),
              it("sign", x=1000, y=590, text="PRIME DAY SHIFT: ≈ −4 PTS IN Q3", at=C("Prime Day moved"), color="#F5F5F5", size=28),
              buddy(1750, 860, at=0.3, mood="happy", label="AWS", color="#FF9F1C", hop=14)]},
    sources=["rel"])
'''),
 dict(after="m2_stakes", id="m2_bsheet", chapter="The cash", claims=["bsheet"],
      narration="Put the balance sheet together and it has flipped. At the end of September, Amazon held {{bsheet}} of cash and securities. It owed {{bsheet.debt_spoken}} in long term debt, including a {{bsheet.loan_spoken}} term loan taken in September. On top of that, lease liabilities add {{bsheet.lease_spoken}}, and another {{bsheet.notyet_spoken}} of leases are signed but haven't started yet. That's the price of building data centers faster than the cash comes in.",
      scene='''
stage("s15b_bsheet", "m2_bsheet", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("On top of that"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE BALANCE SHEET FLIPPED", at=0.2, size=56, color="gold"),
              it("sign", x=650, y=250, text="CASH + SECURITIES $114.2BN", at=C("Amazon held"), color="#C8E6C9", size=30),
              it("sign", x=1350, y=250, text="LONG-TERM DEBT $180.9BN", at=C("It owed"), color="#FFCDD2", size=30),
              it("sign", x=1350, y=360, text="INCL. $17.5BN TERM LOAN (SEPT)", at=C("term loan"), color="#FFCDD2", size=26),
              it("sign", x=1000, y=480, text="LEASE LIABILITIES $98.8BN", at=C("lease liabilities"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=590, text="+$164.9BN OF LEASES NOT YET STARTED", at=C("signed but haven't"), color="#FFE0B2", size=28),
              buddy(1750, 860, at=0.3, mood="worry", label="CASH", color="#23995A", hop=12)]},
    sources=["tenq"])
'''),
 dict(after="m5_legal", id="m5_chips", chapter="Risks and upside", claims=["chips"],
      narration="And then there's supply. Amazon says it relies on a limited group of suppliers for chips, including the graphics processors behind A I, and its own guidance flags supply swings in memory chips. A patent case at the International Trade Commission is seeking to block some A W S servers. And Amazon carries about {{chips}} of uncertain tax positions. None of these is sized as a loss, but each one could slow the build out.",
      scene='''
stage("s34b_chips", "m5_chips", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("A patent case"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 4 · SUPPLY", at=0.2, size=60, color="gold"),
              it("sign", x=650, y=260, text="'A LIMITED GROUP OF SUPPLIERS'", at=C("relies on a limited"), color="#FFE0B2", size=28),
              it("sign", x=1350, y=260, text="MEMORY CHIP SWINGS", at=C("memory chips"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=390, text="PATENT CASE VS AWS SERVERS (ITC)", at=C("A patent case"), color="#FFCDD2", size=28),
              it("sign", x=1000, y=510, text="TAX POSITIONS ≈ $7.3BN", at=C("uncertain tax"), color="#F5F5F5", size=30),
              buddy(1750, 860, at=0.4, mood="worry", label="AWS", color="#FF9F1C", hop=12)]},
    sources=["tenq"])
'''),
]
