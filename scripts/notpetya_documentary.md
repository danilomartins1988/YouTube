# The $10 Billion Cyberattack That Froze the World's Biggest Shipping Company

_In June twenty seventeen, a piece of code hidden in a Ukrainian tax program froze the world's biggest shipping company, wiped thousands of computers, and caused more than ten billion dollars in damage. How it spread, how Maersk came back, and who ended up paying._

## h_question - The ten-billion-dollar morning

How does a small update for an accounting program in Ukraine end up stopping trucks at a port in New Jersey, shutting down drug production at one of the world's biggest drug makers, and costing the world more than ten billion dollars?

> `total` [source_located] WIRED (Aug 2018): NotPetya caused more than $10 billion in total damages, according to a White House assessment confirmed to WIRED by former Homeland Security adviser Tom Bossert. White House (15 Feb 2018): 'the most destructive and costly cyber-attack in history', 'causing billions of dollars in damage across Europe, Asia, and the Americas'. (sources: wired, wh_2018)  
> `terminals` [source_located] WIRED: the same scene played out at 17 of Maersk's 76 terminals, from Los Angeles to Algeciras, Rotterdam and Mumbai; gates down, cranes frozen. At Elizabeth, New Jersey, about 3,000 trucks arrive on a good day; hundreds of trucks backed up for miles and the Port Authority said the terminal would be closed for the rest of the day. SiliconANGLE: the attack did not stop any of Maersk's ships. (sources: wired, maersk_q2)  
> Contains editorial interpretation (marked analysis).  
> Hook question built from the sourced claims (M.E.Doc update, Elizabeth NJ terminal, Merck, White House total).  

## h_stakes - The ten-billion-dollar morning

The code was called NotPetya, and the White House later put its damage at more than ten billion dollars. One victim was Maersk, the world's largest shipping conglomerate. Within half an hour, its staff were running down the hallways, shouting at colleagues to unplug their computers. And what saved it in the end was a single server in Africa that happened to be offline.

> `total` [source_located] WIRED (Aug 2018): NotPetya caused more than $10 billion in total damages, according to a White House assessment confirmed to WIRED by former Homeland Security adviser Tom Bossert. White House (15 Feb 2018): 'the most destructive and costly cyber-attack in history', 'causing billions of dollars in damage across Europe, Asia, and the Americas'. (sources: wired, wh_2018)  
> `fleet` [source_located] WIRED: Maersk, 'the world's largest shipping conglomerate', was responsible for 76 ports and nearly 800 seafaring vessels, representing close to a fifth of the entire world's shipping capacity. (sources: wired)  
> `rebuild` [source_located] WIRED: Maersk's 150 or so domain controllers synced with each other and all were wiped; backups of almost all individual servers existed, but not of the domain controllers; one lone surviving domain controller was found in Ghana, untouched thanks to a power outage; no Ghana staffer had a British visa, so the drive went by relay via Nigeria, then on a six-and-a-half-hour flight to Heathrow; the recovery centre in Maidenhead was managed by Deloitte. Chair Jim Hagemann Snabe (Davos): it took just 10 days to rebuild 4,000 servers and 45,000 PCs; full recovery took close to two months. (sources: wired)  

## m1_card - The update




## m1_question - The update

How do you hit an entire country at once?

> Contains editorial interpretation (marked analysis).  
> Part question.  

## m1_mdoc - The update

You go through software everybody trusts. A small family-run company in Kyiv, Linkos Group, made an accounting program called M.E.Doc, used by Ukrainian businesses to file their taxes. Like most software, it updated itself. In the spring of twenty seventeen, according to American prosecutors, Russian military hackers took over its update servers and slipped their own code into the updates.

> `mdoc` [source_located] WIRED: Linkos Group, a small, family-run Ukrainian software business, makes M.E.Doc accounting software; in spring 2017 Russian military hackers hijacked its update servers; in June 2017 they used that back door to release NotPetya. Lawfare (DOJ indictment): M.E.Doc is a popular Ukrainian accounting program used to send tax information to the government; malicious code was added to updates on three dates in April, May and June. (sources: wired, lawfare_doj)  

## m1_launch - The update

On June twenty-seventh, the day before a national holiday in Ukraine, they used that back door. The malware spread with terrifying speed. A Ukrainian security firm watched it bring down the network of a large bank in forty-five seconds. Part of a major transit hub was fully infected in sixteen seconds.

> `mdoc` [source_located] WIRED: Linkos Group, a small, family-run Ukrainian software business, makes M.E.Doc accounting software; in spring 2017 Russian military hackers hijacked its update servers; in June 2017 they used that back door to release NotPetya. Lawfare (DOJ indictment): M.E.Doc is a popular Ukrainian accounting program used to send tax information to the government; malicious code was added to updates on three dates in April, May and June. (sources: wired, lawfare_doj)  
> `speed` [source_located] WIRED (ISSP): it took 45 seconds to bring down the network of a large Ukrainian bank; a portion of a major Ukrainian transit hub was fully infected in 16 seconds; the attack came the day before Ukraine's Constitution Day. (sources: wired)  

## m1_weapons - The update

It had two weapons. The first was EternalBlue, a hacking tool built by America's own National Security Agency, which had leaked earlier that year. It broke into Windows computers that had not installed a security fix. The second, Mimikatz, pulled passwords out of memory, and those passwords opened the machines that had been fixed.

> `exploits` [source_located] WIRED: NotPetya combined EternalBlue, a penetration tool created by the US National Security Agency and leaked earlier in 2017, with Mimikatz, which pulls passwords out of memory; together they could infect unpatched computers and then use stolen passwords to infect patched ones. The Register: EternalBlue was leaked from the NSA. (sources: wired, reg_2018)  

## m1_draw - The update

Let me draw how one computer becomes thousands. One infected machine finds a neighbor that missed the security fix, and breaks in. There, it reads the passwords stored in memory. Those passwords open a third machine, even a fully updated one. Every victim becomes a new attacker. And inside a big company, where every computer trusts the others, there is no wall to stop it.

> `exploits` [source_located] WIRED: NotPetya combined EternalBlue, a penetration tool created by the US National Security Agency and leaked earlier in 2017, with Mimikatz, which pulls passwords out of memory; together they could infect unpatched computers and then use stolen passwords to infect patched ones. The Register: EternalBlue was leaked from the NSA. (sources: wired, reg_2018)  
> Contains editorial interpretation (marked analysis).  
> Explanation of the EternalBlue plus Mimikatz combination described by WIRED.  

## m1_ransom - The update

Then the screens changed. Some said the computer was repairing its file system. Others said, oops, your important files are encrypted, and asked for three hundred dollars in bitcoin. But it was a disguise. According to the charges, the files were scrambled in a way that not even the hackers could undo. Paying changed nothing. This was not a ransom. It was a wiper.

> `ransom` [source_located] WIRED: screens read 'oops, your important files are encrypted' and demanded $300 worth of bitcoin; the ransom messages were only a ruse. Lawfare (DOJ): unlike Petya, NotPetya irreversibly encrypted computers so that not even the hackers could restore the contents. (sources: wired, lawfare_doj)  

## m1_ukraine - The update

In Ukraine, it hit hospitals, six power companies, two airports, more than twenty-two banks, cash machines, and practically every government agency. It even shut down the computers at the Chernobyl clean-up site. One senior official estimated that ten percent of all the computers in the country were wiped.

> `ukraine` [source_located] WIRED: NotPetya hit at least four hospitals in Kiev alone, six power companies, two airports, more than 22 Ukrainian banks, ATMs and card payment systems, and practically every federal agency; one senior Ukrainian official estimated that 10 percent of all computers in the country were wiped; it shut down computers at the Chernobyl cleanup site. (sources: wired)  

## m1_transition - The update

But the code did not stay in Ukraine. It got on a plane, so to speak, inside the networks of global companies.


## m2_card - Copenhagen goes dark




## m2_question - Copenhagen goes dark

What happens when the company behind a fifth of world shipping loses its computers?

> Contains editorial interpretation (marked analysis).  
> Part question.  

## m2_door - Copenhagen goes dark

Maersk's door was a single computer. A finance executive at its office in Ukraine had asked for M.E.Doc to be installed on one machine. That was enough. Through Maersk's global network, the malware reached its headquarters in Copenhagen on a sunny summer afternoon, and from there, the rest of the company.

> `mdoc` [source_located] WIRED: Linkos Group, a small, family-run Ukrainian software business, makes M.E.Doc accounting software; in spring 2017 Russian military hackers hijacked its update servers; in June 2017 they used that back door to release NotPetya. Lawfare (DOJ indictment): M.E.Doc is a popular Ukrainian accounting program used to send tax information to the government; malicious code was added to updates on three dates in April, May and June. (sources: wired, lawfare_doj)  

## m2_scale - Copenhagen goes dark

This was the world's largest shipping conglomerate, with seventy-six port terminals, nearly eight hundred vessels, and close to a fifth of the world's shipping capacity. Every container is tracked, booked and cleared by computers. And the computers were gone.

> `fleet` [source_located] WIRED: Maersk, 'the world's largest shipping conglomerate', was responsible for 76 ports and nearly 800 seafaring vessels, representing close to a fifth of the entire world's shipping capacity. (sources: wired)  

## m2_port - Copenhagen goes dark

At the terminal in Elizabeth, New Jersey, about three thousand trucks arrive on a good day. That day, the gates stopped working. Hundreds of trucks backed up for miles, and the terminal was closed for the rest of the day. The same thing happened at seventeen of Maersk's seventy-six terminals, from Los Angeles to Rotterdam and Mumbai. Gates down. Cranes frozen.

> `terminals` [source_located] WIRED: the same scene played out at 17 of Maersk's 76 terminals, from Los Angeles to Algeciras, Rotterdam and Mumbai; gates down, cranes frozen. At Elizabeth, New Jersey, about 3,000 trucks arrive on a good day; hundreds of trucks backed up for miles and the Port Authority said the terminal would be closed for the rest of the day. SiliconANGLE: the attack did not stop any of Maersk's ships. (sources: wired, maersk_q2)  
> `fleet` [source_located] WIRED: Maersk, 'the world's largest shipping conglomerate', was responsible for 76 ports and nearly 800 seafaring vessels, representing close to a fifth of the entire world's shipping capacity. (sources: wired)  

## m2_ships - Copenhagen goes dark

The ships themselves kept sailing. But without the systems that say which box goes where, a port becomes a parking lot. Staff fell back on personal email, spreadsheets and WhatsApp. One customer remembered booking five hundred shipping containers through a messaging app.

> `terminals` [source_located] WIRED: the same scene played out at 17 of Maersk's 76 terminals, from Los Angeles to Algeciras, Rotterdam and Mumbai; gates down, cranes frozen. At Elizabeth, New Jersey, about 3,000 trucks arrive on a good day; hundreds of trucks backed up for miles and the Port Authority said the terminal would be closed for the rest of the day. SiliconANGLE: the attack did not stop any of Maersk's ships. (sources: wired, maersk_q2)  
> `whatsapp` [source_located] WIRED: Maersk staffers took orders via personal Gmail accounts, WhatsApp and Excel spreadsheets; a customer: 'booking 500 shipping containers via WhatsApp'. Maersk CEO Soren Skou (Q2 2017 report): business volumes were negatively affected for a couple of weeks in July. (sources: wired, maersk_q2)  

## m2_transition - Copenhagen goes dark

To come back, Maersk had to rebuild everything. And for that, it needed one thing it could not find.


## m3_card - The search for one server




## m3_question - The search for one server

What do you rebuild first when everything is gone?

> Contains editorial interpretation (marked analysis).  
> Part question.  

## m3_maidenhead - The search for one server

Maersk turned an office building in Maidenhead, a town west of London, into a recovery center run with the consultancy Deloitte. Staff kept arriving from all over the world, luggage in hand. The good news was that there were backups of almost all of the company's servers.

> `rebuild` [source_located] WIRED: Maersk's 150 or so domain controllers synced with each other and all were wiped; backups of almost all individual servers existed, but not of the domain controllers; one lone surviving domain controller was found in Ghana, untouched thanks to a power outage; no Ghana staffer had a British visa, so the drive went by relay via Nigeria, then on a six-and-a-half-hour flight to Heathrow; the recovery centre in Maidenhead was managed by Deloitte. Chair Jim Hagemann Snabe (Davos): it took just 10 days to rebuild 4,000 servers and 45,000 PCs; full recovery took close to two months. (sources: wired)  

## m3_map - The search for one server

The bad news was the map. A network like Maersk's runs on special servers called domain controllers, the master list of who may log in to what. Maersk had about a hundred and fifty, copying each other so that any one could replace the others. That design covered every disaster except one. All of them wiped at once. And there was no separate backup.

> `rebuild` [source_located] WIRED: Maersk's 150 or so domain controllers synced with each other and all were wiped; backups of almost all individual servers existed, but not of the domain controllers; one lone surviving domain controller was found in Ghana, untouched thanks to a power outage; no Ghana staffer had a British visa, so the drive went by relay via Nigeria, then on a six-and-a-half-hour flight to Heathrow; the recovery centre in Maidenhead was managed by Deloitte. Chair Jim Hagemann Snabe (Davos): it took just 10 days to rebuild 4,000 servers and 45,000 PCs; full recovery took close to two months. (sources: wired)  

## m3_draw - The search for one server

Let me draw the trap. Here are the servers, each one a box, all connected to the master list. Normally, if one copy dies, the others fill in. But the malware reached every copy at the same time. No healthy copy was left. And without the master list, the backups of all the other servers were useless, because nobody could log in to restore them.

> `rebuild` [source_located] WIRED: Maersk's 150 or so domain controllers synced with each other and all were wiped; backups of almost all individual servers existed, but not of the domain controllers; one lone surviving domain controller was found in Ghana, untouched thanks to a power outage; no Ghana staffer had a British visa, so the drive went by relay via Nigeria, then on a six-and-a-half-hour flight to Heathrow; the recovery centre in Maidenhead was managed by Deloitte. Chair Jim Hagemann Snabe (Davos): it took just 10 days to rebuild 4,000 servers and 45,000 PCs; full recovery took close to two months. (sources: wired)  
> Contains editorial interpretation (marked analysis).  
> Explanation of the domain-controller problem described by WIRED.  

## m3_ghana - The search for one server

After calling hundreds of administrators around the world, they found one survivor. A single domain controller in an office in Ghana. A power cut had knocked it offline, and the malware never touched it. A blackout had saved the company.

> `rebuild` [source_located] WIRED: Maersk's 150 or so domain controllers synced with each other and all were wiped; backups of almost all individual servers existed, but not of the domain controllers; one lone surviving domain controller was found in Ghana, untouched thanks to a power outage; no Ghana staffer had a British visa, so the drive went by relay via Nigeria, then on a six-and-a-half-hour flight to Heathrow; the recovery centre in Maidenhead was managed by Deloitte. Chair Jim Hagemann Snabe (Davos): it took just 10 days to rebuild 4,000 servers and 45,000 PCs; full recovery took close to two months. (sources: wired)  

## m3_relay - The search for one server

But the connection in Ghana was so slow that sending the data would take days. So they decided to fly it. Nobody in the Ghana office had a British visa, so it became a relay race. One employee flew the hard drive to Nigeria and handed it over at the airport to a colleague, who carried it on a six and a half hours flight to London.

> `rebuild` [source_located] WIRED: Maersk's 150 or so domain controllers synced with each other and all were wiped; backups of almost all individual servers existed, but not of the domain controllers; one lone surviving domain controller was found in Ghana, untouched thanks to a power outage; no Ghana staffer had a British visa, so the drive went by relay via Nigeria, then on a six-and-a-half-hour flight to Heathrow; the recovery centre in Maidenhead was managed by Deloitte. Chair Jim Hagemann Snabe (Davos): it took just 10 days to rebuild 4,000 servers and 45,000 PCs; full recovery took close to two months. (sources: wired)  

## m3_rebuilt - The search for one server

With that drive, Maidenhead could start bringing the company back. According to Maersk's chairman, it took ten days to rebuild a network of four thousand servers and forty-five thousand PCs. Full recovery took close to two months.

> `rebuild` [source_located] WIRED: Maersk's 150 or so domain controllers synced with each other and all were wiped; backups of almost all individual servers existed, but not of the domain controllers; one lone surviving domain controller was found in Ghana, untouched thanks to a power outage; no Ghana staffer had a British visa, so the drive went by relay via Nigeria, then on a six-and-a-half-hour flight to Heathrow; the recovery centre in Maidenhead was managed by Deloitte. Chair Jim Hagemann Snabe (Davos): it took just 10 days to rebuild 4,000 servers and 45,000 PCs; full recovery took close to two months. (sources: wired)  

## m3_transition - The search for one server

Then came the bill. And Maersk was only one of the victims.


## m4_card - The bill




## m4_question - The bill

How much can a few lines of code cost?

> Contains editorial interpretation (marked analysis).  
> Part question.  

## m4_maersk - The bill

In August, Maersk told investors the attack would cut its results by two hundred to three hundred million dollars. Its chairman later put it between two hundred and fifty and three hundred million dollars. Some of the company's own staff privately suspected even that was too low.

> `maersk_cost` [source_located] Maersk interim report Q2 2017 (via SiliconANGLE), CEO Soren Skou: 'We expect that the cyber-attack will impact results negatively by USD 200-300m.' WIRED: Snabe estimated at Davos that NotPetya cost Maersk between $250 million and $300 million; staffers privately suspected the figure was low-balled. Fortune (Feb 2018): up to $300 million replacing tens of thousands of PCs and servers. (sources: maersk_q2, wired, fortune_2018)  

## m4_victims - The bill

And the list kept growing. The drug maker Merck, whose ability to manufacture some medicines was temporarily shut down, reported a loss of eight hundred and seventy million dollars. FedEx, through its European arm TNT Express, four hundred million dollars. Saint-Gobain, the French building giant, three hundred and eighty-four million dollars. The snack maker Mondelez, one hundred and eighty-eight million dollars.

> `victims` [source_located] WIRED (approximate damages reported by the biggest victims): Merck $870 million; FedEx, through TNT Express, $400 million; Saint-Gobain $384 million; Maersk $300 million; Mondelēz $188 million; Reckitt Benckiser $129 million. Merck's ability to manufacture some drugs was temporarily shut down. (sources: wired)  

## m4_draw - The bill

Let me draw the scale. Here is a typical ransomware attack that paralyzed the city of Atlanta, costing up to ten million dollars. Next to it, Maersk. Then FedEx. Then Merck. And then the total. The White House estimate of more than ten billion dollars. Next to that bar, the Atlanta attack is barely a line. It is about a tenth of one percent.

> `atlanta` [source_located] WIRED: the ransomware attack that paralyzed Atlanta's city government in March 2018 cost up to $10 million, a tenth of a percent of NotPetya's price. (sources: wired)  
> `victims` [source_located] WIRED (approximate damages reported by the biggest victims): Merck $870 million; FedEx, through TNT Express, $400 million; Saint-Gobain $384 million; Maersk $300 million; Mondelēz $188 million; Reckitt Benckiser $129 million. Merck's ability to manufacture some drugs was temporarily shut down. (sources: wired)  
> `total` [source_located] WIRED (Aug 2018): NotPetya caused more than $10 billion in total damages, according to a White House assessment confirmed to WIRED by former Homeland Security adviser Tom Bossert. White House (15 Feb 2018): 'the most destructive and costly cyber-attack in history', 'causing billions of dollars in damage across Europe, Asia, and the Americas'. (sources: wired, wh_2018)  
> Contains editorial interpretation (marked analysis).  
> Bar comparison of sourced figures; 'a tenth of a percent' is WIRED's comparison.  

## m4_hospitals - The bill

Not all the damage was measured in money. In Pennsylvania, NotPetya hit the Heritage Valley Health System, two hospitals and seventy-eight other medical facilities. For more than a week, staff could not reach the computer systems they used for cardiology, nuclear medicine, radiology and surgery.

> `doj` [source_located] Lawfare (Oct 2020): federal prosecutors indicted six officers in Unit 74455 of Russia's GRU; systems attacked by NotPetya included two hospitals and 78 other medical facilities in the Heritage Valley Health System in Pennsylvania, which lost access to systems for cardiology, nuclear medicine, radiology and surgery; FedEx spent about $400 million and a large US pharmaceutical manufacturer over $500 million. Infosecurity Magazine: the DoJ said $1 billion was lost from just three of the many victim organizations; the unit is also known as Sandworm. (sources: lawfare_doj, infosec_doj)  

## m4_transition - The bill

Somebody had launched it. And somebody would have to pay for it.


## m5_card - Who pays




## m5_question - Who pays

Who is responsible for a weapon that does not stay where it was aimed?

> Contains editorial interpretation (marked analysis).  
> Part question.  

## m5_blame - Who pays

In February twenty eighteen, Britain's National Cyber Security Centre concluded that the Russian military was almost certainly responsible. The White House called it the most destructive and costly cyber attack in history, and said it was part of the Kremlin's effort to destabilize Ukraine. Russia's government rejected the accusations as groundless.

> `blame` [source_located] The Register (15 Feb 2018): the UK National Cyber Security Centre concluded 'the Russian military was almost certainly responsible'. White House (15 Feb 2018): 'In June 2017, the Russian military launched the most destructive and costly cyber-attack in history.' Fortune (16 Feb 2018): Kremlin spokesman Dmitry Peskov: 'We categorically reject such accusations. We consider them unsubstantiated and groundless.' (sources: reg_2018, wh_2018, fortune_2018)  

## m5_doj - Who pays

In October twenty twenty, American prosecutors charged six officers of a Russian military intelligence unit, known to researchers as Sandworm. They said just three American victims had lost close to a billion dollars. These are accusations, not convictions.

> `doj` [source_located] Lawfare (Oct 2020): federal prosecutors indicted six officers in Unit 74455 of Russia's GRU; systems attacked by NotPetya included two hospitals and 78 other medical facilities in the Heritage Valley Health System in Pennsylvania, which lost access to systems for cardiology, nuclear medicine, radiology and surgery; FedEx spent about $400 million and a large US pharmaceutical manufacturer over $500 million. Infosecurity Magazine: the DoJ said $1 billion was lost from just three of the many victim organizations; the unit is also known as Sandworm. (sources: lawfare_doj, infosec_doj)  

## m5_insurance - Who pays

So the victims turned to their insurers. And the insurers pointed to an old clause excluding hostile or warlike acts. If a government's military launched the attack, they argued, it was war, and they did not have to pay. Merck's fight was over more than one point four billion dollars in losses.

> `merck_ins` [source_located] McGuireWoods (Feb 2024): Merck reached a settlement with its 'all risk' property insurers in a dispute involving over $1.4 billion in losses from NotPetya; the insurers argued a 'hostile/warlike' exclusion applied; the New Jersey trial court found the exclusion did not apply to malware and cyberattacks but only to physical acts of warfare, and the state appeals court affirmed; the settlement came days before the New Jersey Supreme Court was set to hear arguments; terms were not disclosed. (sources: mcg_merck)  

## m5_court - Who pays

A New Jersey court disagreed. The war exclusion, it found, was written for physical acts of warfare between armies, not for malware. An appeals court agreed. In early twenty twenty-four, days before the state's supreme court was due to hear the case, Merck settled with its insurers. The terms were never disclosed.

> `merck_ins` [source_located] McGuireWoods (Feb 2024): Merck reached a settlement with its 'all risk' property insurers in a dispute involving over $1.4 billion in losses from NotPetya; the insurers argued a 'hostile/warlike' exclusion applied; the New Jersey trial court found the exclusion did not apply to malware and cyberattacks but only to physical acts of warfare, and the state appeals court affirmed; the settlement came days before the New Jersey Supreme Court was set to hear arguments; terms were not disclosed. (sources: mcg_merck)  

## payoff - The lesson

So what did NotPetya teach the world economy? That the attack does not have to be aimed at you. Maersk was not the target. It was in the way. One computer running one tax program was enough to stop terminals on three continents. Networks where everything trusts everything else are efficient. They are also fragile. And in the end, the world's biggest shipping company was rescued not by a plan, but by a power cut in Ghana.

> `rebuild` [source_located] WIRED: Maersk's 150 or so domain controllers synced with each other and all were wiped; backups of almost all individual servers existed, but not of the domain controllers; one lone surviving domain controller was found in Ghana, untouched thanks to a power outage; no Ghana staffer had a British visa, so the drive went by relay via Nigeria, then on a six-and-a-half-hour flight to Heathrow; the recovery centre in Maidenhead was managed by Deloitte. Chair Jim Hagemann Snabe (Davos): it took just 10 days to rebuild 4,000 servers and 45,000 PCs; full recovery took close to two months. (sources: wired)  
> `terminals` [source_located] WIRED: the same scene played out at 17 of Maersk's 76 terminals, from Los Angeles to Algeciras, Rotterdam and Mumbai; gates down, cranes frozen. At Elizabeth, New Jersey, about 3,000 trucks arrive on a good day; hundreds of trucks backed up for miles and the Port Authority said the terminal would be closed for the rest of the day. SiliconANGLE: the attack did not stop any of Maersk's ships. (sources: wired, maersk_q2)  
> Contains editorial interpretation (marked analysis).  
> Conclusion drawn from the sourced parts.  

## teaser - The lesson

Next time on The Hidden Economics, we follow the money behind another hidden link of the world economy. This is The Hidden Economics.

> Contains editorial interpretation (marked analysis).  
> Generic teaser (channel rule).  
