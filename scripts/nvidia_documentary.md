# How Nvidia Took Over the AI Economy

_A graphics-card company became the main supplier of the AI boom by combining parallel chips, a software ecosystem and a global supply chain. Here is how it makes money, and what could break its grip._

## open_network - The supplier

Every time you ask an AI chatbot a question, a machine somewhere does the math. Behind the apps are the AI labs. Behind the labs are the cloud companies and the data centers. And behind almost all of them, there is one supplier.

> `customers_fy2026` [source_located] In fiscal 2026 sales to one direct customer were 22% of NVIDIA's total revenue and sales to another were 14% (10-K); the customers are not named. (sources: nvda_10k_fy2026)  
> Contains editorial interpretation (marked analysis).  
> "Behind almost all of them" is our characterisation, supported by Nvidia's scale and customer list in the 10-K.  

## open_value - The supplier

In October twenty twenty-five, that supplier, Nvidia, became the first company in history to be worth more than 5 trillion dollars.

> `market_cap_5tn` [source_located] On 29 October 2025 NVIDIA became the first company to close with a stock market value above $5 trillion. (sources: ap_5tn)  

## open_revenue - The supplier

In its last full fiscal year, it sold 215.9 billion dollars worth of products, about eight times what it sold just three years earlier.

> `revenue_fy2026` [source_located] NVIDIA revenue for fiscal 2026 (year ended 25 Jan 2026) was $215.9 billion, up 65% from $130.5 billion in fiscal 2025. (sources: nvda_q4fy26, nvda_10k_fy2026)  
> `revenue_fy2023` [source_located] NVIDIA revenue for fiscal 2023 (year ended 29 Jan 2023) was $26.97 billion; fiscal 2026 revenue was about eight times higher (our calculation, 215.9 / 26.97 = 8.0). (sources: nvda_10k_fy2025, nvda_xbrl)  

## open_question - The supplier

For most of its life, Nvidia was known for video game graphics cards. So how did a gaming company end up at the center of the AI economy? And can it stay there? This is The Hidden Economics.

> Contains editorial interpretation (marked analysis).  
> Framing questions, answered in the acts that follow.  

## a2_card - From gaming to AI




## a2_origins - From gaming to AI

Nvidia was founded in 1993 in California by Jensen Huang and two fellow engineers, to make chips for computer graphics. In 1999, it launched what it calls the first GPU, a graphics processing unit. Its business was drawing video games, fast.

> `founded_1993` [source_located] NVIDIA was incorporated in California in April 1993; Jen-Hsun (Jensen) Huang co-founded it and has been CEO since inception. (sources: nvda_10k_fy2026)  
> `gpu_1999` [source_located] NVIDIA's 10-K says its 'invention of the GPU in 1999 sparked the growth of the PC gaming market and redefined computer graphics'. (sources: nvda_10k_fy2026)  
> "Two fellow engineers" refers to Nvidia's other co-founders; "what it calls the first GPU" attributes the claim to Nvidia.  

## a2_sketch - From gaming to AI

Here is the key idea. To draw one frame of a game, a chip has to color millions of pixels, and each pixel can be worked out on its own. So instead of a few very fast workers, a graphics chip uses a huge number of simpler ones, all working at the same time.

> Contains editorial interpretation (marked analysis).  
> General explanation of parallel graphics processing; no figures.  

## a2_cpu_gpu - From gaming to AI

Give both kinds of chip the same job: a pile of small tasks that don't depend on each other. The CPU's few powerful cores work through them in rounds. The GPU gives one to each of its many cores, and finishes in a few steps. But flip the problem. In a step-by-step job, where each step needs the result of the last one, the CPU's faster cores win. Real performance always depends on the workload.

> Contains editorial interpretation (marked analysis).  
> Conceptual illustration of serial versus parallel work; the animation is labelled as not a benchmark.  

## a2_alexnet - From gaming to AI

And training a neural network turns out to look a lot like graphics: enormous piles of multiplications that can run side by side. In 2012, a network called AlexNet, trained on two Nvidia gaming cards, won a famous image recognition contest. Researchers took notice, and so did Nvidia. In 2017, it launched its first chip with Tensor Cores, built from the ground up for AI.

> `alexnet` [source_located] In 2012 the AlexNet neural network, trained on two NVIDIA GTX 580 GPUs, won the ImageNet image-recognition competition; training took five to six days. (sources: alexnet_2012, nvda_10k_fy2026)  
> `tensor_2017` [source_located] NVIDIA introduced its first Tensor Core GPU, built for AI, in 2017 (10-K). (sources: nvda_10k_fy2026)  

## a3_card - The CUDA advantage




## a3_stack - The CUDA advantage

But the chip was only half the story. Years before AI took off, in 2006, Nvidia released CUDA, software that let programmers use its graphics chips for general computing. On top of it, Nvidia built libraries for math, for neural networks and for linking chips together. The popular AI frameworks plugged into those libraries. Developers learned them. And applications were built on top. Today Nvidia says more than 7.5 million developers use CUDA and its other tools.

> `cuda_2006` [source_located] NVIDIA introduced CUDA in 2006, opening 'the parallel processing capabilities of our GPU to a broad range of compute-intensive applications' (10-K). (sources: nvda_10k_fy2026)  
> `developers` [source_located] NVIDIA's FY2026 10-K says there are over 7.5 million developers worldwide using CUDA and its other software tools. (sources: nvda_10k_fy2026)  
> Layer names (cuDNN, cuBLAS, NCCL; PyTorch, TensorFlow, JAX) are examples of the libraries and frameworks described.  

## a3_switch - The CUDA advantage

That creates what economists call switching costs. A company can move to another chip, but first it may have to port and retest its code, tune its performance again, change its tools, and retrain its teams. None of this is impossible. Other chips run AI every day. But every step costs time and money, and that friction is valuable to Nvidia.

> Contains editorial interpretation (marked analysis).  
> Economic explanation of switching costs; it does not claim rivals cannot run AI workloads.  

## a3_flywheel - The CUDA advantage

It is also a network effect. More developers write more software for Nvidia chips. More software attracts more customers. More customers bring in more money for new chips and new tools, which attract even more developers. The wheel feeds itself.

> Contains editorial interpretation (marked analysis).  
> Our description of the network effect; Nvidia's 10-K says its developer base "strengthens our ecosystem".  

## a4_card - How Nvidia makes money




## a4_revenue - How Nvidia makes money

Now, the money. Nvidia's year ends in late January, so its fiscal twenty twenty-six is mostly calendar twenty twenty-five. For a decade, revenue grew steadily. Then it exploded: from 27 billion dollars in fiscal twenty twenty-three, to 215.9 billion dollars in fiscal twenty twenty-six.

> `revenue_series` [source_located] NVIDIA revenue by fiscal year, US$ billion (10-K / XBRL): FY2016 5.0; FY2017 6.9; FY2018 9.7; FY2019 11.7; FY2020 10.9; FY2021 16.7; FY2022 26.9; FY2023 27.0; FY2024 60.9; FY2025 130.5; FY2026 215.9. (sources: nvda_xbrl)  
> `revenue_fy2023` [source_located] NVIDIA revenue for fiscal 2023 (year ended 29 Jan 2023) was $26.97 billion; fiscal 2026 revenue was about eight times higher (our calculation, 215.9 / 26.97 = 8.0). (sources: nvda_10k_fy2025, nvda_xbrl)  
> `revenue_fy2026` [source_located] NVIDIA revenue for fiscal 2026 (year ended 25 Jan 2026) was $215.9 billion, up 65% from $130.5 billion in fiscal 2025. (sources: nvda_q4fy26, nvda_10k_fy2026)  

## a4_mix - How Nvidia makes money

What changed is who buys. In fiscal twenty twenty, gaming was the biggest business, and data center sales were about a quarter of the total. By fiscal twenty twenty-six, data center revenue had reached 193.7 billion dollars. That is about 90 percent of everything Nvidia sold.

> `segments` [source_located] NVIDIA revenue by market, US$ billion (10-K): FY2020 Data Center 2.98, Gaming 5.52, other 2.42; FY2021 6.70 / 7.76 / 2.22; FY2022 10.61 / 12.46 / 3.84; FY2023 15.01 / 9.07 / 2.90; FY2024 47.53 / 10.45 / 2.95; FY2025 115.19 / 11.35 / 3.96; FY2026 193.74 / 16.04 / 6.16. 'Other' = Professional Visualization + Automotive + OEM and other (our sum). (sources: nvda_10k_fy2022, nvda_10k_fy2025, nvda_10k_fy2026)  
> `dc_fy2026` [source_located] Data Center revenue was $193.7 billion in fiscal 2026 (up 68%), about 90% of total revenue (our calculation: 193.7 / 215.9 = 89.7%); in fiscal 2020 it was $2.98 billion, about 27% (2.98 / 10.92). (sources: nvda_10k_fy2026, nvda_10k_fy2022)  

## a4_customers - How Nvidia makes money

Those buyers are cloud giants, AI labs and large companies building what Nvidia calls AI factories. And they are concentrated. In fiscal twenty twenty-six, one direct customer accounted for 22 percent of Nvidia's revenue, and another for 14 percent.

> `customers_fy2026` [source_located] In fiscal 2026 sales to one direct customer were 22% of NVIDIA's total revenue and sales to another were 14% (10-K); the customers are not named. (sources: nvda_10k_fy2026)  

## a4_margin - How Nvidia makes money

Then look at the margin. Gross margin is what is left from each dollar of sales after the cost of making the product. Nvidia's rose from about 57 percent in fiscal twenty twenty-three to 75 percent in fiscal twenty twenty-five. Last year it slipped to 71 percent, partly because of a 4.5 billion dollar charge on chips it could no longer sell to China.

> `gross_margin_series` [source_located] NVIDIA GAAP gross margin by fiscal year (our calculation from 10-K gross profit / revenue, XBRL): FY2016 56.1%; FY2017 58.8%; FY2018 59.9%; FY2019 61.2%; FY2020 62.0%; FY2021 62.3%; FY2022 64.9%; FY2023 56.9%; FY2024 72.7%; FY2025 75.0%; FY2026 71.1%. (sources: nvda_xbrl, nvda_10k_fy2026)  
> `gm_fy2026_reason` [source_located] NVIDIA says fiscal 2026 gross margin fell as its business moved from Hopper HGX systems to Blackwell full-scale datacenter solutions, and because of a $4.5 billion charge for H20 excess inventory and purchase obligations after new US export licence requirements for China (April 2025). (sources: nvda_10k_fy2026)  

## a4_why - How Nvidia makes money

Why so profitable? Demand ran far ahead of supply. The product was hard to replace. And customers were not just buying chips, but whole systems: processors, networking and software that work together. Networking alone brought in 31 billion dollars last fiscal year. And Nvidia keeps reinvesting: it says it has spent more than 76 billion dollars on research and development since it was founded.

> `dc_fy2026` [source_located] Data Center revenue was $193.7 billion in fiscal 2026 (up 68%), about 90% of total revenue (our calculation: 193.7 / 215.9 = 89.7%); in fiscal 2020 it was $2.98 billion, about 27% (2.98 / 10.92). (sources: nvda_10k_fy2026, nvda_10k_fy2022)  
> `supply_risk` [source_located] NVIDIA's 10-K warns that 'supply constraints or availability issues with respect to any one component' can have a broader revenue impact because its products are part of a complex data center buildout. (sources: nvda_10k_fy2026)  
> `rnd_total` [source_located] NVIDIA says it has invested over $76.7 billion in research and development since its inception (FY2026 10-K). (sources: nvda_10k_fy2026)  
> Contains editorial interpretation (marked analysis).  
> Our reading of the drivers; networking revenue is from the FY2026 10-K.  

## a4_latest - How Nvidia makes money

And it is still growing. In the quarter that ended in July twenty twenty-six, Nvidia brought in 96.2 billion dollars, up 106 percent from a year earlier, and it expected about 108 billion dollars in the quarter after that.

> `q2fy27` [source_located] For the quarter ended 26 July 2026 (Q2 fiscal 2027) NVIDIA reported revenue of $96.2 billion (up 106% year over year), Data Center revenue of $89.0 billion, a 75.0% gross margin, and guided to about $108 billion for the next quarter, assuming no Data Center compute revenue from China. (sources: nvda_q2fy27)  

## a5_card - The global supply chain




## a5_chain - The global supply chain

Here is the surprising part. Nvidia designs its chips, but it does not make them. Its engineers in California send the designs to TSMC in Taiwan, which prints them onto silicon wafers. The chips are then joined with stacks of high bandwidth memory from SK Hynix, Micron and Samsung, using an advanced packaging technique called CoWoS. Contract manufacturers assemble them into servers, and the servers ship to data centers around the world.

> `suppliers` [source_located] NVIDIA's 10-K: it uses foundries such as TSMC and Samsung to produce its wafers, buys memory from SK Hynix, Micron and Samsung, uses CoWoS technology for packaging, and uses contract manufacturers such as Hon Hai, Wistron and Fabrinet for assembly, testing and packaging; its supply chain is 'mainly concentrated in Asia' while it expands into the US and Latin America. (sources: nvda_10k_fy2026)  

## a5_bottleneck - The global supply chain

A chain like this is only as fast as its slowest link. Nvidia's own annual report warns that a shortage of any one component can hold back its sales. When advanced packaging or memory runs short, everything downstream has to wait.

> `supply_risk` [source_located] NVIDIA's 10-K warns that 'supply constraints or availability issues with respect to any one component' can have a broader revenue impact because its products are part of a complex data center buildout. (sources: nvda_10k_fy2026)  

## a5_arizona - The global supply chain

Most of this chain is concentrated in Asia, above all in Taiwan. Nvidia is trying to spread it out. In October twenty twenty-five, it showed the first Blackwell wafer made in the United States, at TSMC's factory in Arizona. But reports say those wafers still travel back to Taiwan to be packaged.

> `arizona` [source_located] In October 2025 NVIDIA and TSMC showed the first Blackwell wafer produced in the United States, at TSMC's Arizona fab; reports say the wafers still go to Taiwan for advanced packaging. (sources: arizona_wafer)  
> `suppliers` [source_located] NVIDIA's 10-K: it uses foundries such as TSMC and Samsung to produce its wafers, buys memory from SK Hynix, Micron and Samsung, uses CoWoS technology for packaging, and uses contract manufacturers such as Hon Hai, Wistron and Fabrinet for assembly, testing and packaging; its supply chain is 'mainly concentrated in Asia' while it expands into the US and Latin America. (sources: nvda_10k_fy2026)  

## a6_card - The competition




## a6_rivals - The competition

So who could challenge Nvidia? Its annual report names them: chipmakers like AMD, Intel and Huawei, and also some of its own biggest customers. Google, Amazon and Microsoft all design AI chips of their own.

> `competitors_10k` [source_located] NVIDIA's 10-K lists competitors including AMD, Huawei and Intel, and large cloud companies designing their own AI hardware, such as Alibaba, Alphabet, Amazon, Baidu, Huawei and Microsoft. (sources: nvda_10k_fy2026)  

## a6_amd - The competition

AMD sells data center GPUs too, with its own open software platform, called ROCm. In calendar twenty twenty-five, AMD's whole data center business, including its server processors, brought in 16.6 billion dollars. Nvidia's data center revenue in its latest fiscal year was 193.7 billion dollars.

> `amd_dc_2025` [source_located] AMD's Data Center segment revenue (EPYC CPUs and Instinct GPUs) was $16.6 billion in calendar 2025, up 32%. (sources: amd_fy2025)  
> `dc_fy2026` [source_located] Data Center revenue was $193.7 billion in fiscal 2026 (up 68%), about 90% of total revenue (our calculation: 193.7 / 215.9 = 89.7%); in fiscal 2020 it was $2.98 billion, about 27% (2.98 / 10.92). (sources: nvda_10k_fy2026, nvda_10k_fy2022)  
> Different fiscal periods and scopes; labelled on screen.  

## a6_custom - The competition

Then there are custom chips. Google builds its own TPUs, now in their seventh-generation. Amazon builds Trainium, and its Project Rainier cluster runs nearly half a million of them. In late twenty twenty-five, the AI lab Anthropic said it plans to use up to one million Google TPUs, while still using Amazon's chips and Nvidia's GPUs.

> `google_tpu` [source_located] Google made Ironwood, its seventh-generation TPU, generally available in November 2025; in October 2025 Anthropic said it plans to access up to one million Google TPUs, while continuing to use Amazon Trainium and NVIDIA GPUs. (sources: google_ironwood, anthropic_tpu)  
> `aws_trainium` [source_located] In October 2025 AWS activated Project Rainier, a cluster with nearly 500,000 of its own Trainium2 chips, used by Anthropic. (sources: aws_rainier)  

## a6_landscape - The competition

Why build your own chip? Economics. A general-purpose GPU can run almost any AI workload, has the widest software support, and can be rented from many clouds. A custom accelerator is designed around one company's own workloads. At enormous scale it can be cheaper to run, but it is mostly available inside that company's cloud, and software has to be adapted to it. Different jobs favor different chips. There is no single winner.

> `competitors_10k` [source_located] NVIDIA's 10-K lists competitors including AMD, Huawei and Intel, and large cloud companies designing their own AI hardware, such as Alibaba, Alphabet, Amazon, Baidu, Huawei and Microsoft. (sources: nvda_10k_fy2026)  
> `google_tpu` [source_located] Google made Ironwood, its seventh-generation TPU, generally available in November 2025; in October 2025 Anthropic said it plans to access up to one million Google TPUs, while continuing to use Amazon Trainium and NVIDIA GPUs. (sources: google_ironwood, anthropic_tpu)  
> `aws_trainium` [source_located] In October 2025 AWS activated Project Rainier, a cluster with nearly 500,000 of its own Trainium2 chips, used by Anthropic. (sources: aws_rainier)  
> Contains editorial interpretation (marked analysis).  
> Qualitative comparison of general-purpose GPUs and custom accelerators; no benchmarks or rankings are implied.  

## a7_card - The future of Nvidia




## a7_capex - The future of Nvidia

The whole boom rests on one thing: customers spending. Trackers estimate that Amazon, Microsoft, Alphabet and Meta plan to spend roughly 700 billion dollars on capital projects in twenty twenty-six, much of it on AI data centers.

> `capex_2026` [source_located] Trackers of company guidance put 2026 capital spending by Amazon, Microsoft, Alphabet and Meta at roughly $700 billion combined (estimates range from about $690bn to $760bn), much of it for AI data centers. (sources: capex_tracker)  

## a7_risks - The future of Nvidia

That is also the risk. If that spending slows, so does Nvidia. Its biggest customers are building rival chips. And when a customer that large pauses its orders, it shows up directly in Nvidia's revenue. Its supply chain runs through a handful of factories in Asia. And export rules have shut much of the China market: Nvidia's latest forecast assumes no data center compute sales there at all.

> `china_guidance` [source_located] NVIDIA's outlook for Q3 FY2027 (and earlier for Q1 FY2027) assumes no Data Center compute revenue from China. (sources: nvda_q2fy27, nvda_q4fy26)  
> `customers_fy2026` [source_located] In fiscal 2026 sales to one direct customer were 22% of NVIDIA's total revenue and sales to another were 14% (10-K); the customers are not named. (sources: nvda_10k_fy2026)  
> `suppliers` [source_located] NVIDIA's 10-K: it uses foundries such as TSMC and Samsung to produce its wafers, buys memory from SK Hynix, Micron and Samsung, uses CoWoS technology for packaging, and uses contract manufacturers such as Hon Hai, Wistron and Fabrinet for assembly, testing and packaging; its supply chain is 'mainly concentrated in Asia' while it expands into the US and Latin America. (sources: nvda_10k_fy2026)  
> Contains editorial interpretation (marked analysis).  
> Risk summary drawn from Nvidia's 10-K risk factors and guidance.  

## a7_inference - The future of Nvidia

The market is shifting, too. A model is trained once, but it runs every time someone uses it. That second part is called inference, and as it grows, the cost of each answer matters more. That is exactly where custom chips compete. Nvidia's response is to keep moving, with new systems every year, like its next platform, Rubin, which it says will cut the cost of inference again.

> `rubin` [source_located] In its Q4 FY2026 results NVIDIA said it unveiled the Rubin platform (six new chips) and claimed up to a 10x reduction in inference token cost compared with Blackwell; AWS, Google Cloud, Microsoft Azure and Oracle Cloud are to be among the first to deploy it. (sources: nvda_q4fy26)  
> Contains editorial interpretation (marked analysis).  
> Training versus inference explained generally; the Rubin cost claim is Nvidia's own.  

## outro - The future of Nvidia

Nvidia's real advantage was never one chip. It was a stack: hardware, software, developers and suppliers, built over three decades. In an economy hungry for computing power, whoever controls the bottleneck captures the profit. And one of the biggest bottlenecks of all sits on a single island. Next time: why Taiwan matters so much to the global economy. This was The Hidden Economics.

> `suppliers` [source_located] NVIDIA's 10-K: it uses foundries such as TSMC and Samsung to produce its wafers, buys memory from SK Hynix, Micron and Samsung, uses CoWoS technology for packaging, and uses contract manufacturers such as Hon Hai, Wistron and Fabrinet for assembly, testing and packaging; its supply chain is 'mainly concentrated in Asia' while it expands into the US and Latin America. (sources: nvda_10k_fy2026)  
> Contains editorial interpretation (marked analysis).  
> Concluding interpretation and next-episode teaser.  
