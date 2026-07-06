# Domain Model: Investment Thesis

## Definition

An **Investment Thesis** is a single, explicit, falsifiable claim about a Company that, if true, supports a capital-allocation stance, and that states in advance the conditions under which it would be considered wrong. It is the atomic unit of reasoning in Adaptive Quality Investing: a bounded proposition — such as "this business will sustain returns on capital above its cost of capital because of a durable structural advantage" — paired with the assumptions it rests on and the observable conditions that would falsify it. A Thesis is not a summary of an entire investment argument (that is the Investment Case) and not a decision (that is a Decision); it is one testable belief that can be independently confirmed, weakened, or refuted by evidence over time.

## Why It Exists

The core AQI principle is that decision quality improves when reasoning is made explicit and falsifiable rather than left as vague intuition. The Investment Thesis exists to force each claim underlying a position to be stated as a proposition that reality can contradict. This makes conviction auditable, enables Evidence to be attached for or against a specific claim, and allows the system to detect when a stance has been invalidated by events rather than by price movement. Without falsifiable Theses, positions could not be honestly reviewed, and Learning Events could not be derived from being demonstrably right or wrong.

## Key Attributes

- `thesis_id: identity` — stable unique identifier.
- `company_ref: reference` — the single Company this Thesis makes claims about.
- `author_ref: reference` — the investor who authored the Thesis.
- `thesis_statement: text` — the falsifiable claim being made, stated as a proposition.
- `rationale: text` — the reasoning and mechanism behind why the claim should hold.
- `key_assumptions: list of text` — the explicit assumptions the claim depends on.
- `falsification_conditions: list of condition` — the observable conditions under which the Thesis would be considered wrong (required).
- `time_horizon: duration` — the period over which the claim is expected to play out.
- `conviction_level: ordinal` — the author's current strength of belief given available evidence.
- `status: enumeration` — lifecycle state (see Lifecycle).
- `created_at / last_reviewed_at: timestamps` — provenance and review recency.

## Invariants

- A Thesis must state at least one falsification condition; a claim with no condition under which it could be wrong is invalid and cannot be persisted as a Thesis.
- The `thesis_statement` must be a claim, not a question, instruction, or neutral fact.
- A Thesis references exactly one Company; a proposition spanning multiple companies must be decomposed into separate Theses.
- `conviction_level` must be justifiable by the current balance of Evidence linked to the Thesis; conviction is not an arbitrary free variable divorced from evidence.
- Once a falsification condition is met and confirmed by Evidence, the Thesis must transition to `invalidated`; it may not remain `active` while known to be refuted.
- The `thesis_statement` and `falsification_conditions` are versioned: material change constitutes a new version rather than silent in-place editing, preserving the historical record of what was claimed and when.

## Relationships

- **Company** — a Thesis makes falsifiable claims about exactly one Company, referenced by identity.
- **Investment Case** — one or more Theses are composed into an Investment Case; the Case is the higher-order argument, the Thesis is a component claim. A Thesis may be referenced by more than one Case.
- **Evidence** — Evidence attaches to a Thesis with a polarity (supporting or contradicting) and updates the Thesis's evidential standing and conviction.
- **Decision** — a Decision must reference at least one Investment Thesis, grounding the act of capital allocation in explicit falsifiable reasoning.
- **Risk / Catalyst** — Risks (what could break the claim) and Catalysts (what could confirm or accelerate it) relate to a Thesis as separate aggregates.
- **Learning Event** — the confirmation or invalidation of a Thesis is a primary source of Learning Events.

## Lifecycle / State

A Thesis moves through: `draft` (being formulated) → `active` (asserted and under continuous test) → `under_review` (a falsification condition or contradicting Evidence has triggered re-examination) → terminal states `confirmed` (played out as claimed within horizon), `invalidated` (a falsification condition met and confirmed), or `retired` (superseded or abandoned without resolution). Valid transitions: `draft → active`, `active → under_review`, `under_review → active`, `active/under_review → confirmed`, `active/under_review → invalidated`, `active/under_review → retired`. Terminal states are immutable; further reasoning requires a new Thesis version.

## Aggregate Boundary

The Investment Thesis **is an aggregate root**. Its aggregate owns the claim, rationale, assumptions, falsification conditions, horizon, conviction, and lifecycle state, plus the *reference* to its Company. It does **not** own Evidence, Investment Cases, Risks, Catalysts, or Decisions — each is a separate aggregate that references the Thesis by identity. The Thesis is the consistency boundary for one falsifiable claim and its evidential standing over time.
