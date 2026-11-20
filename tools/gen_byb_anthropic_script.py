"""Writes projects/before-you-buy-anthropic-2026-11/deliverables/documentary/script.yaml (Before You Buy: Anthropic, Nov 2026)
and docs/episodes/byb-anthropic-2026-11/narration_plain.txt. Every figure is a {{claim}} from sources.yaml (13 spoken figures,
at most one per segment; check with tools/count_numbers.py). Neutral: never buy/sell, no price target.
Run: python tools/gen_byb_anthropic_script.py   (then python tools/gen_byb_anthropic_storyboard.py)
"""
import yaml
CH = ["The day-one question", "What you actually own", "The price you pay", "The lock-up calendar", "The first report card",
      "Who it depends on", "New-IPO weather", "Who is in charge", "What would change the picture"]
S = []
def seg(id_, ch, text, claims=(), note=None):
    d = {"id": id_, "chapter": CH[ch], "narration": " ".join(text.split()), "claims": list(claims)}
    if note:
        d["analysis"] = True
        d["source_note"] = note
    S.append(d)
def card(id_, ch):
    S.append({"id": id_, "chapter": CH[ch], "narration": "", "claims": []})

seg("h_open", 0, """Maya has had the app open since breakfast. On the screen sits a brand-new ticker, A, N, T. Anthropic, the company behind
the Claude A I models, sold its first shares to the public at {{ipo_price}}. And her thumb is hovering over the buy button.""", ["ipo_price"],
    "Hook. Maya is fictional (a would-be buyer). Offer price per the 424B4 / FWP.")
seg("h_day", 0, """Day one was a roller coaster. The stock opened far above the offer, slid back all afternoon, and closed at {{close_px}}.
Everyone on her feed has an opinion. Maya has a rule instead. Never buy something before you've read the label.""", ["close_px"])
seg("h_maya", 0, """So she grabs a clipboard and writes down the questions a careful buyer asks. What do I actually own? What am I paying? When
can insiders sell? What will the first report show? Who does this company depend on? How wild do new stocks get? And who's really in charge?
Let's go through them with her.""", [], "Promise of the episode: the buyer's checklist.")
seg("h_disclaimer", 0, """A quick note first. This is not investment advice. We won't tell you to buy or sell, and we have no price target.
Everything here comes from Anthropic's prospectus, other public filings and named news reports, with our own math labelled. Our channel uses A I tools, including Claude, to make its videos. Anthropic didn't sponsor or review this one, which is exactly
why we stick to the filings.""", [], "Series disclaimer and production disclosure (neutrality rule).")

card("c1_card", 1)
seg("c1_classes", 1, """First on the list. What do you actually own? Anthropic doesn't have just one kind of stock. It has a whole family. Class A is
what trades on the Nasdaq, with one vote per share. Class N gets the same money, but no vote, and it's held mostly by big strategic partners.
And then come the special classes that carry power, but no money at all.""", [],
    "424B4: Class A one vote; Class N no vote except as required by law, holders primarily strategic business partners; Class T, F and E no economic rights.")
seg("c1_votes", 1, """Here's the twist. A single Class F share, held by a company the co-founders own, carries {{votes}} of the votes at every
shareholder meeting. A single Class T share, held by an independent trust, picks most of the board. So a Class A buyer does get a vote. But the
big decisions are already spoken for.""", ["votes"])
seg("c1_float", 1, """Next, how many shares really exist. The offering put a big block of stock into public hands. But that block is {{float}}
of all the shares outstanding. Most of the company still belongs to early investors, partners and employees. And for now, most of them can't
sell.""", ["float"])
seg("c1_draw", 1, """Let me draw the difference between outstanding and fully diluted. Outstanding shares are the ones that exist today. Now add
the employee stock options, the stock awards still vesting, and the notes Amazon holds that turn into stock. That's the fully diluted count,
{{fd}} shares than today. So when someone quotes a market value, ask which count they used.""", ["fd"])
seg("c1_dilute", 1, """And that count can keep growing. Amazon's notes convert a slice at a time, every few months, up to an ownership cap.
Employee plans add new stock every year. And there's a twist you won't find at most companies. Each time the share price hits a new milestone,
the board may hand extra shares to Anthropic's own public benefit fund. Good for its mission. A slightly smaller slice for everyone
else.""", [], "424B4: Amazon Notes convert at the end of each fiscal quarter up to the ownership cap; 2026 Plan and ESPP annual increases; Public Benefit Issuances of up to 2% more shares each time the price rises 50% above the prior milestone (from the IPO price), at the board's discretion.")
seg("c1_transition", 1, """So that's what you own. Now, what are you paying for it?""", [], "Transition.")

card("c2_card", 2)
seg("c2_ps", 2, """Next on the list. The price. Anthropic barely makes an operating profit yet, so the usual price to earnings ratio doesn't
work. Investors use price to sales instead. Take the latest close, multiply by the shares outstanding, and divide by the last year of revenue.
By our math, that's {{ps_ant}} sales.""", ["ps_ant"])
seg("c2_draw", 2, """Let me put that next to the giants. Here's Nvidia. Here's Microsoft. On the same day's close, with the same math, both
sit at {{ps_megas}} their sales. And here's A, N, T, towering over them. Same yardstick. Very different height.""", ["ps_megas"])
seg("c2_growth", 2, """Is that crazy? Not automatically. The giants grow far more slowly, and Anthropic's revenue so far this year is many
times what it was a year earlier. Measured against its latest monthly pace, stretched over a year, the multiple shrinks a lot. That's the bull
case. The bear case is simple. A price that high only works if fast growth lasts for years, and fast growth rarely lasts forever.""", [],
    "424B4: revenue 9M 2026 $33.2bn vs 9M 2025 $2.5bn (13x, our calc); run rate ≈$81bn (Oct 31) → ≈15.9x outstanding (our calc). Balance: bull and bear in one segment.")
seg("c2_value", 2, """One more label to check. Anthropic holds a big pile of cash from its private rounds, plus the money from this offering,
and very little debt. So its enterprise value, the price of the business itself, is lower than its market value. Our multiple uses market
value. Whatever headline you read, check which one it uses.""", [],
    "424B4: cash $95.6bn + short-term investments $36.3bn (Sep 30, 2026), ≈$104.8bn net proceeds, debt $6.2bn. Equity value vs EV.")

card("c3_card", 3)
seg("c3_waves", 3, """Next question. When can insiders sell? Most new stocks come with a lock-up. Early holders promise not to sell for a
while. Anthropic's isn't one cliff. It's a staircase. Some employee shares could trade from day one. More unlock in steps through December,
January and February. And a bigger wave follows right after the first annual results.""", [],
    "424B4 'Shares Eligible for Future Sale' table: Nov 19, Dec 15, 2026; Jan 5, Jan 19, Feb 2, 2027; FY26 Earnings Release Date + 2 trading days.")
seg("c3_gate", 3, """Then comes the big gate, the one most investors will circle. It opens right after the results for January to March, or
at the very latest on {{lock_may}} next year.""", ["lock_may"])
seg("c3_size", 3, """Behind that gate sit {{lock_big}}, the biggest single step on the whole calendar.""", ["lock_big"])
seg("c3_year", 3, """The co-founders, and investors holding more than a sliver of the company, wait longer. Up to a full year, until the
results for next summer are out, or the following November at the latest.""", [],
    "424B4: co-founders and holders of >0.5% of fully diluted shares: earlier of the Q3 2027 release + 2 trading days or the 365th day (Nov 18, 2027); timed automatic expirations apply.")
seg("c3_meaning", 3, """Unlocked doesn't mean sold. Plenty of holders keep their shares. But more shares that can be sold means more possible
sellers, so Maya writes these dates down. One more detail. The chip and cloud companies that bought shares privately at the offer price aren't
in the lock-up at all. But their shares are restricted, so they can't simply sell them on the market whenever they like.""", [],
    "424B4: concurrent private placement shares are not subject to lock-up but are restricted securities under Rule 144.")

card("c4_card", 4)
seg("c4_when", 4, """Next, the first report card. Anthropic's first results as a public company will cover this full year, and they
should arrive early next year. The date hasn't been announced yet. But it matters twice. It's the first fresh look at the numbers since the
offering. And it's also the trigger for one of those lock-up waves.""", [],
    "424B4: the FY26 Earnings Release Date (results for the year ending Dec 31, 2026) triggers a release step; no date announced as of 2026-11-20.")
seg("c4_draw", 4, """Here's what Maya will look for. First, revenue growth. Is the rocket still climbing? Second, the compute bill. How much do
chips and data centers cost for each dollar of sales? Third, operating cash flow. Is real cash still coming in? And fourth, the commitment
schedule. How much has it promised to spend, and when?""", [], "Watchlist (our analysis), each tied to a 424B4 line item.")
seg("c4_cost", 4, """That compute bill is the one to watch. Last year, it was bigger than the sales it helped earn. So far this year, it's down
to {{compute}} for every dollar of revenue. If that keeps falling, margins open up. If it climbs back, the story gets harder.""", ["compute"])
seg("c4_cash", 4, """And then there are the promises. Anthropic has signed up to spend {{commit}} on computing and data centers over many
years, much of it owed whether customers show up or not. On the other side, it has a large cash cushion, and its operating cash flow turned
positive this year. The report will show whether that cash keeps pace with the bills.""", ["commit"])

card("c5_card", 5)
seg("c5_partners", 5, """Next. Who does Anthropic depend on? Start with Amazon and Google. Both are big shareholders. Both rent it the
computing power it runs on. Both sell Claude to their own cloud customers. And both build A I models of their own. Partner, landlord,
salesman and rival, all at once.""", [],
    "424B4: Amazon 14.6% and Google 13.4% of outstanding capital stock; compute arrangements; CSP marketplaces; risk factor on CSPs that develop their own models.")
seg("c5_draw", 5, """Let me draw how that works. Amazon invests in Anthropic. Anthropic pays Amazon for computing. Amazon's cloud customers buy
Claude, and Amazon keeps a cut. Google sits in a similar triangle. The prospectus itself warns that these ties could create conflicts of
interest and affect its access to computing.""", [],
    "424B4 risk factor (verbatim words 'conflicts of interest'); Amazon 10-Q investments; partner fees recorded as expense.")
seg("c5_chips", 5, """The reassuring part is in the chips. Anthropic trains and runs Claude on chips from Amazon, Google, Nvidia and A M D, so
no single supplier can choke it off. The flip side? Several of those suppliers are also shareholders, and its commitments to them are
huge.""", [], "424B4: multi-chip architecture across AWS Trainium, Google TPUs, NVIDIA GPUs and AMD GPUs; placement buyers incl. Google, NVIDIA, AMD.")
seg("c5_customers", 5, """And the customers? So far this year, no single customer was big enough to be named in the filing. Last year, a couple
were. That's a healthier spread. But a big share of sales still flows through the cloud marketplaces of those same partners. So the web of ties
runs both ways.""", [],
    "424B4: customers ≥10% of revenue: 2025 Customer A 12%, Customer B 12%; 9M 2026 none. CSP marketplaces 44% of 9M 2026 revenue. (Customers are not named in the filing; 'named' = listed as a ≥10% customer.)")

card("c6_card", 6)
seg("c6_fb", 6, """Next. How wild can a new stock get? Look back at Facebook's debut. Within a few months, its shares had fallen to
{{fb}} the offer price, and the first lock-up ended right in the middle of that slide. A year after the offering, it was still below the
offer.""", ["fb"])
seg("c6_arm", 6, """Now the opposite story. Chip designer Arm listed in the fall, popped on day one, then slipped below its offer within weeks.
Months later, a strong quarterly report came out, and the stock jumped by {{arm}} in a single day.""", ["arm"])
seg("c6_lesson", 6, """Same lesson from both. In its first year, a new stock trades on very little history. In both of these cases, some of the
biggest moves came around lock-up dates and earnings reports. Those are exactly the dates on Maya's clipboard.""", [],
    "Analysis of the two cases (AP, Bloomberg, Yahoo Finance closes). Not a forecast for ANT.")

card("c7_card", 7)
seg("c7_pbc", 7, """Last question. Who governs this company? Anthropic is a public benefit corporation. By law, its board must balance
shareholders' money with the interests of people affected by its work, and with a stated mission, the responsible development of advanced A I
for the long-term benefit of humanity.""", [], "424B4: PBC; specific public benefit purpose quoted.")
seg("c7_trust", 7, """On top of that sits the Long-Term Benefit Trust, a small group of trustees with no financial stake in the company.
Through that Class T share, they elect most of the board. That makes Anthropic what Nasdaq calls a controlled company, which may skip some of
the usual governance rules.""", [], "424B4: LTBT of five financially disinterested trustees; Class T elects a majority of the board; controlled company under Nasdaq rules.")
seg("c7_meaning", 7, """What does that mean for a buyer? Supporters say it shields long-term thinking from short-term pressure. The
prospectus itself warns that the trust may have interests that differ from yours, and could use its power in ways you disagree with. Either
way, if you buy, you're joining a company where your vote has limits.""", [], "424B4 risk factor ('may have interests that differ from yours'). Both sides.")

card("c8_card", 8)
seg("c8_bull", 8, """So, what would change the picture? On the bright side, watch for revenue that keeps growing fast, a compute bill that keeps
shrinking for every dollar of sales, cash flow that stays positive, and lock-up waves that pass without a flood of selling.""", [],
    "Bullish signals (our analysis), same weight as the bearish ones.")
seg("c8_bear", 8, """On the dark side, watch for growth that slows sharply, a compute bill that climbs back up, cash that can't keep pace with
the commitments, or big holders heading for the exit when the gates open.""", [], "Bearish signals (our analysis), same weight as the bullish ones.")
seg("c8_close", 8, """Maya pins the clipboard to her fridge. She didn't decide today, and we're not deciding for her. But now she knows what she
would own, what she would pay, and which dates to watch. The prices in this video are from the first day's close, and every figure is sourced in
the description. And once more, this is not investment advice.""", [], "Close. Maya is fictional. Not investment advice.")
seg("teaser", 8, """Next in the series, another giant of the stock market, opened up the same way. This is The Hidden Economics.""", [],
    "Generic teaser (channel rule).")

doc = {"logline": "Maya, a fictional would-be buyer, watches Anthropic's first trading day and works through a buyer's checklist before she touches the buy button: what she would own (share classes, votes, share count, dilution), what she would pay (price to sales vs the megacaps, our calc), when insiders can sell (the lock-up staircase and the big gate on May 17, 2027 or earlier), what the first report should show, who the company depends on, how wild new stocks get (Facebook 2012, Arm 2023), and who governs it (public benefit corporation and Long-Term Benefit Trust). Ends with bullish and bearish signals of equal weight. Not investment advice.",
       "title": "Anthropic Stock Before You Buy: 7 Things to Check (Nov 2026)", "segments": S}
hdr = ("# Before You Buy: Anthropic (ANT), November 2026 edition. Series spec: docs/series/BEFORE_YOU_BUY.md. Built by\n"
       "# tools/gen_byb_anthropic_script.py (edit the generator, not this file). Every number through {{placeholders}}\n"
       "# (sources.yaml); our calculations said as ours. NEUTRAL: never buy/sell, no price target; disclaimer after the hook and at the end.\n")
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
open(ROOT / "projects/before-you-buy-anthropic-2026-11/deliverables/documentary/script.yaml", "w").write(hdr + yaml.safe_dump(doc, sort_keys=False, width=140, allow_unicode=True))
open(ROOT / "docs/episodes/byb-anthropic-2026-11/narration_plain.txt", "w").write("\n\n".join(f"[{s['id']}] {s['narration']}" for s in S if s['narration']) + "\n")
print(len(S), sum(len(s['narration'].split()) for s in S))
