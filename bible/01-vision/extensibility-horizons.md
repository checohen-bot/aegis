# Extensibility Horizons: The Larger Ambition

Aegis V1 is a product for long-term public equity investors. Aegis, the company, is a bet on something larger: that *capital allocation is one discipline*, appearing in different costumes across different domains, and that a platform which truly captures its structure in one domain can extend to the others. This document names those horizons, explains why the extension is credible, and — just as importantly — draws the line on what this vision does and does not license us to build today.

## The horizons

Five domains, in no committed order, form the long-term map:

**Private equity.** Buying whole companies rather than shares of them. Longer diligence, deeper information access, illiquid holdings, value creation through active ownership. The thesis is richer and the feedback loop slower — which makes disciplined reasoning *more* valuable, not less.

**Venture capital.** Capital allocated against radical uncertainty. Theses rest on founders, markets that don't yet exist, and power-law outcomes. Evidence is scarce and soft; the temptation to narrate rather than reason is overwhelming. A domain starving for exactly the evidence discipline and post-hoc reconciliation Aegis institutionalizes.

**Real estate.** Income-producing property as a capital mission: theses about locations, demographics, and cash flows; evidence from rent rolls, comparables, and local knowledge; catalysts in zoning, rates, and development.

**Corporate capital allocation.** The CFO's question — build, buy, return, or hold? — is the investor's question wearing a different badge. Internal projects compete for capital exactly as stocks compete for a portfolio, and are approved today with less rigor than a good Aegis user applies to a single equity purchase.

**Strategic procurement.** The furthest horizon, and the test of the thesis's generality: committing significant capital to suppliers and long-term contracts is capital allocation under uncertainty, with theses about vendors, evidence about performance, risks, alternatives, and switching costs. If the model reaches here, the model is truly about decisions, not securities.

## Why the domain model generalizes

The claim is not that these domains are similar on the surface — they are wildly different in liquidity, information access, time horizon, and actors. The claim is that they share a *deep structure*, and that Aegis's canonical domain model is written at the level of that deep structure.

Every one of these domains reduces to the same skeleton. A **capital mission**: a pool of capital with a purpose, a horizon, and constraints — a retirement portfolio, a fund, a corporate budget, a procurement program. A **thesis**: a falsifiable belief about why a particular commitment of capital will serve that mission — this business will compound, this founder will win, this property will yield, this supplier will deliver. **Evidence and observations**: information gathered and weighed for and against the thesis, with sources and reliability. A **decision**: capital committed, held, or withdrawn, with reasoning recorded at the moment of commitment. **Risks and catalysts**: named ways the thesis dies, named events that confirm or accelerate it. **Learning events**: outcomes reconciled against the original reasoning, feeding a behavior profile and evolving policies.

Notice what this skeleton never mentions: tickers, share prices, market hours, brokers. Those belong to the public-equity *expression* of the model, not to the model itself. A Holding is a position in an instrument today; the concept — capital committed to a specific opportunity within a mission — describes a portfolio company, a building, or a supplier contract just as faithfully. The entities that carry the intelligence — Thesis, Evidence, Decision, Risk, Catalyst, Learning Event — are domain-agnostic by construction. This is the deliberate design behind the abstraction: we are building a decision-quality engine that currently speaks fluent public equities, not a stock tool we hope to stretch later.

There is also a compounding asset hiding in this generality: the learning loop. A platform that has captured years of a user's theses, decisions, and reconciled outcomes in one domain holds a model of their judgment that transfers. The behavioral patterns — overconfidence after wins, thesis drift, loss aversion — are properties of the *allocator*, not the asset class.

## What this vision licenses — and what it forbids

Now the discipline, stated as bluntly as we can state it.

**No code for these horizons is to be written now.** Not a PE module behind a flag, not a "future asset types" enum stuffed with speculation, not schema fields reserved for real estate. Zero. Speculative generality is how platforms die young: abstractions built for imagined requirements are always wrong, and their wrongness taxes every present-day feature. V1 earns the future by winning the present.

**But no V1 decision may foreclose these horizons.** This is the binding constraint, and it is architectural, not feature-level. Concretely: core entities must not acquire public-equity assumptions that belong in an expression layer — nothing in the heart of the model should require that an asset has a ticker, a real-time price, or a market. Identity, relationships, and lifecycles of the canonical entities must be defined in capital-allocation terms. Public-equity specifics live at the edges, clearly marked as the first expression of a general model, so that the second expression is an *addition*, not a rewrite.

The test for any V1 design review is a single question: *if we added private equity in three years, would this decision require us to rebuild, or merely to extend?* Rebuild answers get redesigned now. Extension answers ship.

Held together, these two rules define our posture toward the future: we do not build for it, and we do not betray it. The horizons are why the foundations must be honest. The foundations are why the horizons are more than a slide.
