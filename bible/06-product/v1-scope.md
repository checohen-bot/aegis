# V1 Scope

This document defines the precise product surface of Aegis at launch. V1 serves one investor doing one thing: a long-term, self-directed investor allocating capital across public equities held at Interactive Brokers. Everything in scope exists to make the core loop real and complete for that investor. Everything deferred is deferred deliberately, so that what we ship is coherent rather than broad.

The test for V1 inclusion is singular: does this feature complete the core loop — connect, form a Thesis, track Evidence, surface change against the Thesis, record an auditable Decision, produce a Learning Event? If yes, it ships. If it is adjacent, aspirational, or serves a different investor, it waits.

## In scope at launch

### Portfolio sync via IBKR
- Read-only connection to a single Interactive Brokers account.
- Synced **Portfolio** and **Holdings**, each linked to a **Company**.
- The Portfolio view leads with thesis health, not price or P&L, and surfaces Holdings that lack a Thesis or whose Thesis is under challenge.
- Trade execution remains in IBKR; Aegis records Decisions but does not execute them.

### Thesis workspace
- A **Company** workspace supporting the full formation of an **Investment Thesis** and the structured **Investment Case** beneath it, including the disconfirming conditions.
- Recording of **Risks** and **Catalysts** per Thesis.
- Guided Thesis formation — the scaffolding that helps a less experienced investor build a real Case.
- Companies may exist for research without being Holdings (a basic watchlist capability), so a Case can be built before capital is committed.

### Evidence tracking
- A **Library** of **Evidence**, sourced and dated, attributable to the Company and Thesis it informs.
- Import of the investor's own research and notes into the Library.
- **Observations** surfaced against existing Theses, framed as confirm-or-challenge, with explicit provenance and logical connection to the affected element of the Case.
- Notifications limited to genuine, thesis-relevant change, delivered at a cadence matched to significance.

### Decision log
- A complete, auditable, chronological log of **Decisions**, each capturing the reasoning recorded at the moment of choice and linked to its Thesis and motivating Evidence.
- No path to record a Decision without its basis attached.

### Basic Learning and Knowledge views
- **Learning Events** generated from Decisions as outcomes unfold against recorded reasoning.
- A **Knowledge** surface where distilled, durable understanding accrues in the Library.
- A first-generation **Behavior Profile** — an honest, reflective view of the investor's patterns over time. In V1 this is observational: it shows the investor their tendencies. It does not yet coach.

### Governing objects
- **Capital Mission** — the investor's stated purpose for the portfolio.
- Basic **Policies** — the investor's own rules and constraints.
- Account, connection, and notification-cadence settings.

### Platform
- Web-first, responsive for desktop-class browsers, designed for deliberate sessions rather than glances.

## Explicitly deferred post-V1

These are not gaps or oversights. Each is a considered decision to protect the coherence of the launch product.

### Social and sharing features
No sharing of Theses, portfolios, or performance; no following other investors; no community, feeds, or commentary. Social mechanics invite comparison and imitation, which corrode independent judgment — the opposite of what Aegis builds. Deferred, and gated behind a high bar for ever being introduced.

### Native mobile apps
V1 is web-first. A glance-optimized mobile app risks pulling the investor toward the frequent, reactive checking our horizon-respecting design exists to prevent. Mobile access, if built, will be shaped to preserve the deliberate tempo, and that shaping is post-V1 work.

### Multi-asset-class support
V1 is public equities only. Fixed income, options, funds, private assets, and crypto each carry distinct thesis structures, evidence types, and risk models. Supporting them well requires domain work we are not doing at launch. Equities first, done properly.

### Advanced Behavior Profile coaching
V1 shows the investor their patterns; it does not yet intervene, prescribe, or actively coach against identified biases. Coaching that changes behavior demands a maturity of the Behavior Profile — and a level of trust and evidence — we will not have on day one. Turning reflection into guidance is a distinct, later phase.

### Multiple and non-IBKR brokerage connections
V1 supports a single IBKR account. Additional accounts, account aggregation, and other brokers are deferred. IBKR is the V1 broker; breadth of connectivity comes later.

### Automated or agentic action
Aegis never executes Decisions in V1, and any form of automated allocation, rebalancing, or agentic trading is out of scope indefinitely. The investor is the decision-maker; that is architectural, not a phase.

## The shape of V1

Read together, the scope describes one thing done completely: a web-based intelligence layer that turns an IBKR equity portfolio into a set of explicit, evidence-backed Theses, watches them honestly, and builds an auditable record of reasoning that compounds into Knowledge and self-understanding over time. It is narrow on purpose. A coherent tool that does the core loop with full integrity is worth more to our investor than a broad one that does everything partially — and it is the only foundation on which the deferred capabilities could ever responsibly be built.
