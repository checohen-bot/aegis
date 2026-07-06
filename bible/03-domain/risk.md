# Risk

## Definition

A Risk is a named, articulated way in which an Investment Thesis could be wrong or a Holding could impair capital — a specific, forward-looking condition whose occurrence would damage the case for holding a position. A Risk is not a price movement and not a probability abstraction; it is a concrete failure mode ("the company's largest customer concentration unwinds," "the regulatory moat is removed") with an assessed likelihood, an assessed impact, and a set of Observations or Catalysts that would confirm or deny its materialization. Risks make the falsifiability of a Thesis operational: they are the enumerated ways the belief could break.

## Why It Exists

Adaptive Quality Investing treats the honest enumeration of what could go wrong as a core competence of decision quality. Investors systematically underweight disconfirming possibilities; a first-class Risk object forces explicit articulation, ongoing monitoring, and structured re-evaluation. Risk exists to (1) make each Thesis auditable against its own failure modes, (2) drive monitoring by linking failure modes to observable signals, (3) feed position sizing and Policy constraints, and (4) create the raw material for Learning Events when a Risk materializes or is proven immaterial.

## Key Attributes

- `id` (identifier): Globally unique, immutable identifier.
- `thesis_ref` (reference): The Investment Thesis this Risk challenges.
- `statement` (text): Concrete description of the failure mode.
- `category` (enum): `Business`, `Financial`, `Competitive`, `Management`, `Regulatory`, `Macro`, `Valuation`, `Behavioral`.
- `likelihood` (enum/decimal): Assessed probability band — `Low`, `Medium`, `High` — optionally a 0–1 estimate.
- `impact` (enum): Severity if it materializes — `Minor`, `Material`, `Severe`, `ThesisBreaking`.
- `severity_score` (derived): Composite of likelihood and impact used for prioritization.
- `monitoring_signals` (reference set): Observations and Catalysts that would evidence movement toward or away from materialization.
- `mitigation` (text, nullable): Actions or conditions that reduce exposure.
- `status` (enum): `Identified`, `Monitored`, `Materialized`, `Mitigated`, `Retired`.
- `identified_at`, `updated_at`, `resolved_at` (timestamp).

## Invariants

- A Risk MUST reference exactly one Investment Thesis.
- `likelihood` and `impact` MUST both be assigned before a Risk transitions out of `Identified`.
- A Risk marked `ThesisBreaking` in `impact` that transitions to `Materialized` MUST emit an event that flags its parent Thesis for invalidation review.
- A Risk MUST NOT be silently deleted once monitored; it transitions to `Retired` with a recorded reason, preserving audit history.

## Relationships

- Challenges an **Investment Thesis** (`thesis_ref`), many Risks to one Thesis.
- Monitored via **Observation** and **Catalyst** references in `monitoring_signals`.
- Substantiated or refuted by **Evidence** attached through Observations.
- Informs **Decision** (sizing, exit) and constrains behavior under **Policy** and **Capital Mission** risk tolerance.
- A materialized or falsified Risk is a primary trigger for a **Learning Event**.

## Lifecycle / State

`Identified` on articulation. `Identified → Monitored` once likelihood/impact are assessed and monitoring signals attached. `Monitored → Materialized` when confirming signals fire; `Monitored → Mitigated` when action or circumstance neutralizes it. Both `Materialized` and `Mitigated` may transition to `Retired` when the Risk is fully resolved or the Holding is exited. Retired Risks are immutable. A Risk never returns from `Materialized` to `Monitored`; a recurrence is a new Risk.

## Aggregate Boundary

Risk is **not an aggregate root**; it is an entity within the **Investment Thesis** aggregate, whose root is the Thesis. Its lifecycle and consistency (especially the ThesisBreaking → invalidation rule) must be governed atomically with the Thesis. It holds references to Observations, Catalysts, and Evidence — all separately rooted aggregates — and coordinates with them via domain events rather than owning them.
