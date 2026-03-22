# Problem Statement

---

## The problem every seller faces right now

Never before has more been expected of enterprise sellers. The platforms we sell have never been more capable — capability improvements that would have seemed impossible five years ago are shipping quarterly. The competitive landscape shifts faster than any team can track. The strategy evolves constantly. The toolset to do the job grows every year.

And then there is the information problem.

LLMs like Claude, Gemini, and ChatGPT have put more intelligence at our fingertips than any generation of sellers has ever had. News, signals, executive statements, earnings releases, competitor moves — it is all there, instantly, in extraordinary volume.

But volume is not the answer.

More information does not produce better conversations. It produces overwhelmed sellers who skim rather than synthesise, who paste rather than think, who arrive at a first meeting having done the research but lacking the conviction to deliver it.

The best POVs I have ever delivered were the ones I wrote myself. Not because I wrote them well — but because I understood them completely. I had sat with the problem. I had challenged my own hypothesis. I had found the customer's language and made it mine. I walked into the room knowing what I believed and why.

That process used to take days. Sometimes hours if I pushed it. The depth was there because the time was there.

We are being asked to move faster. And moving faster without depth produces a specific kind of failure — polished outputs delivered without conviction. The customer can feel it. The conversation does not go where it should. The follow-up does not land. The deal stalls.

More information is not the antidote. We need to create outputs we can understand and deliver with conviction.

---

## What I built

I built a personal AI sales agent that solves the preparation problem without sacrificing conviction.

The agent does not replace the seller's judgment. It removes the preparation tax that prevents sellers from exercising it consistently.

It researches. It finds the signals — leadership changes, financial announcements, strategic moves, competitive dynamics. It scores them for quality, timeliness, and personal relevance. It surfaces the ones worth building around and discards the noise.

It drafts. It builds a Point of View from a documented methodology — provocative question first, customer's world first, gaps framed as opportunities not failures, ending with aspiration not ask. It runs a red team pass on its own output. It flags what is weak before the seller sees it.

It learns. Every time I edit an output, that edit is a signal. Every time I reject something, that rejection is a training example. The agent that runs Ralph Loop 10 will be better than the one that ran Ralph Loop 1 — not because I tuned it, but because it accumulated evidence of what I would and would not send.

The seller reviews, refines, and delivers. The judgment stays human. The groundwork is automated.

---

## The conviction problem — solved

The difference between this and pasting a ChatGPT output into an email is the methodology layer.

The agent operates from a 414-line identity document — my sales approach, my communication principles, my qualification filters, my POV structure, my discovery methodology, my calibrated scepticism. It is not a generic assistant. It is an agent trained to think the way I think about selling.

When it produces a POV, I recognise it as mine. Not because I wrote every word — but because it was built from my principles, challenged by my Critic, and refined by my rejections. I can stand in front of an executive and deliver it with conviction because I understand why every element is there.

That is the problem worth solving. Not how to produce more outputs faster. How to produce fewer, better outputs that the seller can own completely.

---

## What this looks like at scale

I built this for one seller. The question it is designed to start:

**What would this look like for every seller in the business?**

Every AE arrives at a first meeting with a research brief built from six signal types, scored for quality, produced in minutes — not hours.

Every POV is generated from a shared methodology, reviewed by an automated Critic, edited by the seller, and tracked through a pipeline board that captures every human intervention as a training signal.

Every outreach is written in the prospect's language, with the product introduced after the problem is established — because that is how the best sellers in this organisation already do it.

Every research run feeds a signal quality dataset that improves over time. Every rejection teaches the Critic what this organisation would never send.

The event log across all sellers becomes a training corpus. What did great sellers do differently, at which stage, with which prospects? That question becomes answerable — not from surveying sellers about their process, but from reading the data their agent generated while they were doing the work.

---

## The infrastructure

This runs on a two-node homelab — a local inference server and a sales agent host — connected to Slack, the Anthropic API, and Exa AI for semantic prospect research. The total hardware investment is under $3,000 AUD. The methodology investment — documenting how a senior enterprise seller actually thinks — is what made it work.

The technical stack is in the repository. The methodology is not. What is here is enough to understand what was built, how it works, and what it would take to build it at organisational scale.

---

## The conversation this is designed to start

- How would the methodology layer be governed at scale — centralised or per team?
- Which agents would be deployed first for the highest return?
- How does the signal quality framework integrate with CRM data?
- What does the path from homelab to production infrastructure look like?
- What does a Salesforce-scale version of this change about how we develop and retain sellers?


