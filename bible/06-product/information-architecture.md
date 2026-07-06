# Information Architecture

The information architecture of Aegis is a direct projection of the domain model. Navigation areas are not invented conveniences; each is the primary surface for one or more canonical objects, and the relationships between areas are the relationships between objects. An investor who understands the domain understands the app, and vice versa. This is deliberate: the structure teaches the method.

## Top-level structure

The web app has five primary navigation areas, presented in a persistent, restrained top-level navigation:

1. **Portfolio** — the state of capital
2. **Companies & Theses** — the workspace of judgment
3. **Library** — the accumulated Evidence and Knowledge
4. **Decisions** — the auditable record
5. **Mission & Settings** — the governing intent and configuration

Everything the investor does begins in one of these five and moves along the relationships between them.

## 1. Portfolio

The Portfolio area is the home surface and the entry point for the core loop. It presents the **Portfolio** object and its **Holdings**, synced from the connected IBKR account.

Portfolio does not lead with price or daily P&L. It leads with **thesis health**: for each Holding, whether an Investment Thesis exists, and if so whether current Evidence confirms it, challenges it, or is neutral. A Holding without a Thesis is surfaced as an open task — the system's standing invitation to make an implicit bet explicit. Positions requiring attention, because an Observation now challenges their Thesis, rise to the top; positions in a steady, confirmed state recede.

From any Holding, the investor descends into that Company's workspace. Portfolio is therefore the map; the Company workspace is the territory.

## 2. Companies & Theses

This is the analytical heart of the product and where the investor spends deliberate time. Each **Company** has a workspace that binds together the objects of judgment:

- The **Investment Thesis** — the investor's explicit hypothesis for holding.
- The **Investment Case** — the structured argument beneath the Thesis: what must be true, what would disprove it.
- **Evidence** and **Observations** — the incoming facts about the Company, each timestamped and sourced, positioned as confirming or challenging the Case.
- **Risks** and **Catalysts** — the identified threats to the Thesis and the events that could resolve it.

The Company workspace is where a Thesis is formed, where Observations are evaluated against it, and where the confirm/challenge framing is presented. A Company may exist in the workspace without being a Holding — Companies under research or on a watchlist — which lets the investor build a Case before committing capital. The relationship is clean: a Holding points to a Company; a Company carries a Thesis; a Thesis is supported by a Case built from Evidence.

## 3. Library

The Library is the cross-portfolio home of **Evidence** and **Knowledge**. Where the Company workspace shows Evidence in the context of a single Thesis, the Library presents the full corpus: everything the investor and the system have gathered, searchable and filterable across Companies.

**Evidence** here is the raw, sourced material — filings, transcripts, the investor's own imported research and notes. **Knowledge** is the distilled, durable understanding that accrues as Evidence is evaluated and Decisions play out: patterns, established facts, and reusable conclusions that outlive any single Thesis. The Library is where the Consolidating Veteran's scattered research becomes one indexed system of record, and where Knowledge compounds into a portfolio-level asset.

The Library relates outward to every Company: a piece of Evidence is always attributable to the Company and Thesis it informs, so the investor can move from a document to the Decision it shaped and back.

## 4. Decisions

The Decisions area is the **Decision** log — the complete, auditable, chronological record of capital-allocation choices and the reasoning captured at the moment each was made. Every Decision links to the Thesis it affected and the Evidence that motivated it, so the record is never a bare transaction; it is a transaction with its rationale attached.

Decisions is also where **Learning Events** originate. As outcomes unfold against recorded reasoning, Decisions generate the Learning Events that feed Knowledge and the **Behavior Profile**. The log therefore reads in two directions: forward as an audit trail, and backward as the source material for self-understanding.

## 5. Mission & Settings

This area holds the governing objects and configuration. The **Capital Mission** is the investor's stated purpose for the portfolio — the intent against which the whole system is oriented. **Policies** encode the investor's own rules and constraints. The **Behavior Profile**, built from Learning Events, lives here as a reflective surface: an honest account of the investor's patterns and tendencies over time.

Settings also governs the IBKR connection, notification cadence, and account configuration. Placing Mission alongside these settings is intentional: the investor's purpose is a setting of the highest order, and every other configuration serves it.

## How the areas relate

The five areas form the core loop as a traversal:

**Portfolio** surfaces a Holding needing attention → the investor enters **Companies & Theses** to evaluate an Observation against the Thesis, drawing on the **Library** for Evidence → the investor records an outcome in **Decisions** → that Decision produces a Learning Event that updates Knowledge in the Library and the Behavior Profile in **Mission & Settings** → which in turn informs how the next cycle through **Portfolio** is framed.

The architecture is a loop, not a hierarchy. No area is a dead end; each hands the investor to the next along a real relationship in the domain. The navigation is stable and shallow — five destinations — while depth lives inside each, disclosed progressively rather than spread across ever-more menu items.
