# Phased Roadmap

*Volume IX — Execution Playbook · Chapter 3*

This is a **sequencing document, not a dated plan.** It states the order in which Aegis is built and the reasoning behind that order. It deliberately commits to *no dates* and to *no Gantt chart*. Dates at this stage would be fiction; sequence is the real commitment. Each phase has an entry condition (what must be true to begin), a goal, and an exit condition (what must be true to move on). A phase is not "in progress" until its predecessor's exit condition is met.

The governing logic is floor-before-ceiling: pour a foundation strong enough that everything above it is cheap and safe, prove the architecture with the thinnest possible real slice, then broaden along the core investment loop, then deepen into knowledge and learning, and only then monetize. Breadth is never bought at the cost of the foundation.

## Phase 0 — Engineering Foundation (Current)

**Entry:** the company exists and the mission is declared.
**Goal:** establish the engineering foundation *before any application code*: the Engineering Bible (all volumes, including this one), the baseline ADRs, the coding and repository standards, the CI/CD pipeline, and the operating documents (README, CLAUDE.md, FOUNDER.md, the founder manifesto). This is the phase that makes every later phase governable.
**Exit:** the Bible is complete and reviewed; the domain objects are defined; architectural principles and the baseline ADRs are accepted; standards are written; CI/CD runs green on an empty-but-real repository; and the operating model, lifecycle, Definition of Done, and onboarding path are documented. In short — the rules of construction exist and are enforceable before construction begins.

## Phase 1 — Walking Skeleton

**Entry:** Phase 0 exit conditions met.
**Goal:** prove the architecture is buildable with the thinnest possible *real* end-to-end slice — one canonical domain object, one API, one test, one CI run — taken through the full RFC → ADR → Domain Model → Implementation → Tests → Docs → Review → Release lifecycle. In parallel, a **read-only IBKR sync proof of concept**: establish a real sandbox connection to Interactive Brokers and pull a single account's positions read-only, proving the broker adapter boundary is real and replaceable.
**Exit:** one domain object lives end-to-end (persisted, exposed, tested, documented, released) and passes CI; a real IBKR sandbox connection has returned real position data through an adapter that touches no domain logic. The architecture is now demonstrated, not asserted.

## Phase 2 — Core V1 Loop

**Entry:** the walking skeleton is proven and the IBKR read path works.
**Goal:** build the core V1 investment loop for long-term public equity investing:
- **Portfolio / Holding sync** — real Portfolios composed of Holdings, synced read-only from IBKR, mapped to Company.
- **Thesis formation** — the investor forms an Investment Thesis for a Holding or candidate Company, with its Investment Case.
- **Evidence tracking** — Observations and Evidence are captured and bound to Theses, with provenance.
- **Decision recording** — the investor records Decisions with reasoning, referenced Evidence, and the Capital Mission they serve, explainable after the fact.
**Exit:** an investor can connect IBKR, see their real Portfolio and Holdings, form a Thesis backed by tracked Evidence, and record explainable Decisions against a Capital Mission — the minimum loop that makes Aegis useful as an investment-intelligence tool.

## Phase 3 — Knowledge & Learning Loop

**Entry:** the core loop is live and generating real Theses, Evidence, and Decisions.
**Goal:** turn accumulated inputs into compounding understanding and self-knowledge:
- **Knowledge / Learning loop** — Learning Events synthesize Observations, Evidence, and resolved Theses into durable, confidence-graded Knowledge with supersession chains.
- **Behavior Profile** — the platform builds an explainable profile of how the investor actually decides, judged relative to their Capital Mission's intent, surfacing deviation and pattern.
**Exit:** Aegis no longer merely records the investment process; it learns from it — accumulating institutional memory and reflecting the investor's behavior back to them, both explainably.

## Phase 4 — Hybrid Business Model Monetization

**Entry:** the platform demonstrably improves decision quality through the knowledge and learning loops.
**Goal:** build the monetization features supporting the hybrid business model, layered onto a product that already delivers real value. Monetization is deliberately last: we do not charge for a promise, we charge for a proven loop.
**Exit:** the hybrid model is operational atop a mature, explainable, learning product.

## A Standing Constraint

Phases are ordered by dependency, not appetite. The exit conditions above are the real gates; a later phase does not begin because a date arrived or a stakeholder is impatient, but because its predecessor is genuinely done to the company's Definition of Done. This document will be amended when sequence changes — never quietly reordered under schedule pressure.
