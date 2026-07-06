# V1 Scope: Narrow by Design

V1 of Aegis does exactly one thing: it makes an individual investor demonstrably better at long-term public equity investing. This document fixes that boundary precisely — what is in, what is out, and why the narrowness is a strategic decision rather than a resource constraint. When scope pressure arrives, and it will, this page is the line.

## What V1 is

**Long-term public equity investing, only.** V1 supports the full Adaptive Quality Investing loop — thesis formation, evidence gathering, investment cases, decision recording, risk and catalyst tracking, outcome reconciliation, and learning over time — applied exclusively to publicly traded equities held on a multi-year horizon. Common stock of listed companies. That is the entire asset universe of V1.

**Interactive Brokers as the sole broker integration.** IBKR gives us a serious, globally capable brokerage with real APIs, and its user base skews toward exactly our customer: self-directed, internationally minded, cost-conscious, serious. One deep, reliable integration that ingests real positions and real transactions is worth ten shallow ones. Portfolio truth comes from IBKR; reasoning truth comes from Aegis. Users without IBKR can follow the same discipline with manually maintained holdings, but the first-class, automated experience is IBKR, and V1 builds no second integration.

**Web-first.** Thesis writing, evidence review, and decision-making are sit-down, full-attention activities — the work happens with a keyboard, a large screen, and time to think. V1 is a web application, excellent on desktop, responsive enough to be readable anywhere. There is no native mobile app in V1, and this is philosophy as much as sequencing: mobile-first design optimizes for glanceable, interrupt-driven use, which is the exact behavior pattern Aegis exists to break. If we ever ship mobile surfaces, they will serve capture and calm review — never twitch.

**Hybrid business model.** Aegis is paid software with a free tier that is genuinely useful, not a crippled demo. The free tier lets an investor experience the core discipline — connect a portfolio, articulate theses, feel the difference. Paid tiers unlock the full depth of the intelligence layer: evidence automation, deep analysis, full history and learning analytics. What we will never monetize: order flow, user data, attention, or activity. Our revenue must come from the same place our value does — better decisions — so that our incentives and our users' incentives never diverge. Subscription-based revenue with depth-based tiers is the only model that survives that constraint.

## Explicitly out of scope for V1

Named individually, so that no ambiguity survives:

- **Options and derivatives.** No options chains, no covered-call tooling, no derivative analytics. Even "conservative" options strategies drag the product toward price-and-volatility thinking and away from business-quality thinking.
- **Day trading and short-term speculation.** No real-time streaming quotes as a centerpiece, no intraday charts, no momentum signals, no order-entry optimization. Aegis is not a trading front-end; V1 is not where you execute fast, it is where you decide well.
- **Other asset classes.** No bonds, no crypto, no commodities, no funds-analysis tooling, no private assets. (ETFs may appear as holdings ingested from IBKR, but the analytical machinery targets individual companies.)
- **Private equity, venture capital, real estate, corporate capital allocation, strategic procurement.** These are real horizons — see *extensibility-horizons.md* — and exactly zero lines of V1 code are written for them.
- **Mobile-first experience.** No native apps, no push-notification-driven engagement loops.
- **Additional broker integrations.** IBKR only, done properly.
- **Social features.** No feeds, no copy-trading, no leaderboards. Possibly ever.

## Why this scope

**Public equities are the proving ground for the methodology.** AQI's claim — that structured theses, evidence discipline, and closed learning loops improve decision quality — must be proven somewhere before it is generalized anywhere. Public equities are the best-instrumented capital-allocation domain on earth: standardized disclosures, audited financials, long history, liquid prices that eventually render verdicts. If decision-quality improvement can be demonstrated anywhere, it is here; if we cannot demonstrate it here, we have no business expanding anywhere else. V1 is the controlled experiment that earns the right to every later horizon.

**Narrowness is how depth gets built.** Apple-level simplicity and Palantir-level depth are both expensive. Every additional asset class multiplies the ontology's edge cases, the data integrations, and the interface's surface area — and divides the team's attention. A product that is profound about one thing beats a product that is shallow about five, in every market that matters to us.

**The customer is narrow too.** Our customer's self-directed conviction lives overwhelmingly in public equities. Meeting them exactly where they are, with more depth than anyone has ever offered them, is better than meeting them everywhere at half strength.

## The nuance that must not be lost

V1 is narrow **by design, not by limitation**. The domain model underneath — Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy — is deliberately more general than V1's surface, because it describes capital allocation itself, not stock-picking in particular. We build only the public-equity expression of that model in V1, but we design the model so that later expressions require extension, not rewrite. The scope boundary constrains what we *build*; it must never be allowed to silently constrain what the foundations *can become*. Holding both truths at once — build narrow, design general — is the central engineering discipline of V1.
