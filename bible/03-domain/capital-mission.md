# Capital Mission

## Definition

A Capital Mission is the declared purpose, objective, and constraint set that governs a pool of capital — the investor's explicit statement of what a Portfolio is *for*, over what horizon, under what risk tolerance, and against what definition of success. It is the top-level intent object from which allocation Policies, acceptable Risks, and the evaluation of Decisions ultimately derive. A Capital Mission answers "why is this capital deployed and what would constitute doing right by it," as distinct from the Portfolio, which is merely the collection of Holdings that operationalizes the mission.

## Why It Exists

Decision quality can only be assessed relative to intent. Two investors making the identical trade may be acting well or badly depending on the mission the capital serves — retirement preservation versus long-horizon compounding versus a speculative sleeve. Aegis's methodology (improving decision quality, not predicting prices) requires an explicit, first-class objective against which every Decision, Policy, and Risk is judged. The Capital Mission exists to anchor suitability, to make constraints enforceable rather than implicit, and to generalize the platform to arbitrary future capital-allocation domains — each new domain is a new Mission type, not a redesign.

## Key Attributes

- `id` (identifier): Globally unique, immutable identifier.
- `name` (string): Human-readable label (e.g., "Long-Horizon Compounding Core").
- `objective` (enum): Primary aim — `Growth`, `Preservation`, `Income`, `Balanced`.
- `time_horizon` (duration/enum): Intended holding horizon — anchors the "long-term" framing of V1.
- `risk_tolerance` (enum): `Conservative`, `Moderate`, `Aggressive`, decomposable into drawdown tolerance and volatility tolerance.
- `success_definition` (structured): The metric(s) and benchmark against which the mission judges itself — process-quality metrics prioritized over price outcomes.
- `constraints` (structured set): Hard boundaries (e.g., excluded sectors, concentration ceilings, liquidity minimums) that Policies must respect.
- `capital_scope` (reference): The Portfolio(s) this Mission governs.
- `status` (enum): `Draft`, `Active`, `Suspended`, `Retired`.
- `created_at`, `activated_at`, `updated_at` (timestamp).

## Invariants

- A Capital Mission MUST define at least one `objective`, one `time_horizon`, and one `risk_tolerance` before it can transition to `Active`.
- Every governing **Policy** MUST be consistent with the Mission's `constraints`; a Policy that violates a Mission constraint is invalid.
- A Portfolio MAY be governed by at most one `Active` Capital Mission at a time.
- `success_definition` MUST be measurable and MUST NOT reduce solely to realized price return, consistent with AQI principles.

## Relationships

- Governs one or more **Portfolio** (`capital_scope`), one-to-many.
- Parents one or more **Policy**, which translate the Mission into enforceable allocation and behavior rules.
- Provides the evaluation frame for every **Decision** taken within its scope.
- Bounds the acceptable set of **Risk** the investor is willing to hold.
- Informs the interpretation of **Behavior Profile**, since deviation is judged relative to mission intent.

## Lifecycle / State

`Draft` while being defined. Transitions to `Active` once mandatory attributes are complete and at least one governing Policy exists. `Active → Suspended` temporarily halts new allocation under the mission while preserving Holdings. `Suspended → Active` resumes it. `Active → Retired` (or `Suspended → Retired`) permanently closes the mission; retirement requires that governed Portfolios be reassigned or wound down. Retired missions are immutable historical records.

## Aggregate Boundary

Capital Mission is an **aggregate root**. It owns its `objective`, `time_horizon`, `risk_tolerance`, `success_definition`, and `constraints`. It owns the *parenting relationship* to its Policies but not the Policy aggregates themselves, which are separately rooted for independent evolution. It references — and does not own — the Portfolios it governs; a Portfolio is its own aggregate. Cross-aggregate consistency (e.g., ensuring Policies honor Mission constraints) is enforced through domain events and validation at Policy creation, not through direct nested writes.
