# Domain Model: Decision

## Definition

A **Decision** is the immutable record of a deliberate capital-allocation judgment made within a Portfolio at a point in time, grounded in explicit falsifiable reasoning and expressing an intended action toward a Holding — to open, add to, trim, hold, close, or to pass on or watch a candidate. A Decision captures not only *what* was decided but *why*: the Investment Theses and Investment Case it rests on, the conviction and expectations at the moment of choice, and the information then available. It is the primary unit of decision quality in Adaptive Quality Investing — the object whose *quality*, independent of subsequent price outcome, the platform exists to help the investor improve.

## Why It Exists

AQI's entire purpose is to raise the quality of capital-allocation decisions rather than to predict prices. The Decision exists to make each such judgment an explicit, reasoned, and reviewable act of record: by binding every material action to the reasoning behind it and freezing the context in which it was made, the Decision enables honest, hindsight-resistant review — separating sound process from lucky or unlucky outcome. It is the anchor for accountability (every change to a Holding traces to a Decision), for behavioral insight (Decisions across time reveal patterns captured in the Behavior Profile), and for learning (resolved reasoning produces Learning Events).

## Key Attributes

- `decision_id: identity` — stable unique identifier.
- `portfolio_ref: reference` — the Portfolio within whose context the Decision is made.
- `company_ref: reference` — the Company the Decision concerns.
- `holding_ref: reference (conditional)` — the Holding acted upon; absent for a `pass` and set for the resulting Holding on an `open`.
- `decision_type: enumeration` — `open`, `add`, `trim`, `hold`, `close`, `pass`, or `watch`.
- `investment_case_ref: reference` — the Investment Case the Decision is made against.
- `thesis_refs: set of reference` — the Investment Theses relied upon (at least one required).
- `rationale: text` — the reasoning for the action at the time of the Decision.
- `conviction_at_decision: ordinal` — strength of belief when the Decision was made.
- `expected_outcome: text` — what the investor expected to happen and by when.
- `intended_quantity / intended_size: quantity or percentage (conditional)` — the sizing intent for actions that change a position.
- `policy_check_result: structured` — the outcome of evaluating the Decision against the Portfolio's Policies.
- `decided_at: timestamp` — the moment of the Decision.
- `decided_by_ref: reference` — the investor who made it.
- `status: enumeration` — lifecycle state (see Lifecycle).

## Invariants

- A Decision must reference at least one Investment Thesis; no capital-allocation judgment may be recorded without explicit falsifiable reasoning behind it.
- A Decision must reference exactly one Portfolio and exactly one Company, and its referenced Theses and Investment Case must all concern that same Company.
- A Decision is immutable once committed; it is a historical event and may never be edited. A change of mind is a new Decision, not a revision of the old one.
- Any Decision of type `open`, `add`, `trim`, or `close` must resolve to exactly one Holding within the referenced Portfolio; a `pass` must reference no Holding.
- A committed Decision must record its `policy_check_result`; a Decision that violates a binding Policy may only be committed as an explicit, flagged override, never silently.
- `conviction_at_decision` and `expected_outcome` are frozen at commit time and preserved to enable outcome-independent review.

## Relationships

- **Portfolio** — a Decision is made within, and references, exactly one Portfolio; Policies of that Portfolio constrain it.
- **Company** — a Decision concerns exactly one Company, referenced by identity.
- **Investment Case / Investment Thesis** — a Decision references the Investment Case it is made against and at least one Investment Thesis within it, grounding the action in reasoning.
- **Holding** — a Decision is the cause of every Holding mutation; the Holding references its opening Decision, and each Decision references the Holding it acts upon (except `pass`).
- **Policy** — Policies are evaluated against the Decision, producing the recorded policy-check result and any override flag.
- **Behavior Profile** — the stream of Decisions feeds the owner's Behavior Profile, revealing behavioral patterns.
- **Learning Event** — when the reasoning a Decision rested on is later confirmed or invalidated, the reconciliation produces Learning Events.

## Lifecycle / State

A Decision moves through: `proposed` (formulated, reasoning attached, not yet acted on) → `committed` (finalized as the authoritative judgment and, for position-changing types, applied to its Holding) → `executed` (the intended action has been reflected in the position, where execution is distinct from decision) → optionally `reviewed` (revisited against later outcomes, without mutating the original record). A `proposed` Decision may instead be `abandoned`. Valid transitions: `proposed → committed`, `proposed → abandoned`, `committed → executed`, `committed/executed → reviewed`. Once `committed`, the Decision's content is immutable; only its review status may advance.

## Aggregate Boundary

The Decision **is an aggregate root**, modeled as an immutable domain event once committed. Its aggregate owns the judgment record — type, rationale, conviction and expectation at decision time, sizing intent, policy-check result, and lifecycle status — plus the *references* to its Portfolio, Company, Investment Case, Theses, and Holding. It does **not** own any of those referenced aggregates; it records and links them. The Decision is the consistency boundary for a single reasoned act of capital allocation and the frozen context that makes its quality reviewable independent of outcome.
