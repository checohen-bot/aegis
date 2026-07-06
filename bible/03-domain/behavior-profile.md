# Behavior Profile

## Definition

A Behavior Profile is the evolving, evidence-based model of a single investor's decision-making tendencies, biases, and process patterns as revealed by their accumulated Decisions, Learning Events, and adherence to Policy. It captures traits such as tendency to sell winners early, reluctance to invalidate a Thesis, overconcentration under conviction, or chasing Catalysts, together with calibration statistics (how well predictions match outcomes). The Behavior Profile is descriptive and diagnostic, not prescriptive: it tells the investor and the system *how this person actually behaves* so that Policies and prompts can be tailored to protect decision quality.

## Why It Exists

Improving decision quality requires knowing the specific investor whose decisions are being improved. Generic advice is weak; targeted intervention against a person's demonstrated failure modes is strong. The Behavior Profile exists to (1) surface behavioral patterns the investor cannot see in themselves, (2) personalize Policies and system nudges to the individual's real weaknesses, (3) measure whether decision quality is improving over time, and (4) provide the interpretive context that distinguishes a disciplined action from a characteristic mistake. It is the mechanism through which the platform becomes *adaptive to the person*, complementing Learning Events that adapt to the market.

## Key Attributes

- `id` (identifier): Globally unique, immutable identifier.
- `investor_ref` (reference): The individual investor the profile describes (one-to-one).
- `traits` (structured set): Named behavioral tendencies, each with a strength/confidence score and supporting evidence count (e.g., `LossAversion: 0.7`, `DispositionEffect: 0.5`).
- `calibration` (structured): Aggregate prediction-versus-outcome statistics derived from Catalysts and Decisions (e.g., Brier-style score, over/underconfidence bias).
- `discipline_metrics` (structured): Rates of Policy adherence, thesis-review timeliness, and Decision documentation completeness.
- `evidence_basis` (reference set): The Learning Events and Decisions from which traits are inferred.
- `last_recomputed_at` (timestamp): When the profile was last regenerated from source data.
- `version` (integer): Monotonic version, since the profile is a periodically recomputed projection.

## Invariants

- Exactly one active Behavior Profile exists per investor.
- Every `trait` MUST cite an `evidence_basis` of at least a minimum count of Decisions or Learning Events before it is surfaced as actionable — no trait is asserted from a single data point.
- The Behavior Profile MUST be reproducible: recomputing from the same underlying Decisions and Learning Events MUST yield the same profile (it is a deterministic projection, not an editable record).
- The profile MUST NOT be directly edited by users; it changes only by recomputation from source aggregates.

## Relationships

- Describes one **Investor** (the account owner), one-to-one.
- Inferred from **Decision** history and **Learning Event** records (its `evidence_basis`).
- Calibrated using **Catalyst** prediction outcomes and **Risk** assessment accuracy.
- Personalizes **Policy**: guardrails may be strengthened or added in response to demonstrated traits.
- Interpreted relative to **Capital Mission** intent, since the same behavior may be appropriate under one mission and harmful under another.

## Lifecycle / State

The Behavior Profile is a long-lived, continuously updated **projection** rather than a state-machine entity. It is created (`version 1`) when an investor has accumulated the minimum required Decision and Learning Event history, then `Recomputed` on a schedule and on significant triggers (a new Learning Event with behavioral attribution, a Policy breach). Each recomputation increments `version` and updates `last_recomputed_at`. There is no terminal "closed" state while the investor is active; on account closure the profile is archived immutably.

## Aggregate Boundary

Behavior Profile is an **aggregate root**, but a read-oriented, derived one: it owns its `traits`, `calibration`, and `discipline_metrics`, all computed from — not authored alongside — the Decision and Learning Event aggregates it references. Because it is a deterministic projection, its consistency guarantee is *reproducibility from source events* rather than transactional co-editing. It subscribes to `DecisionMade`, `LearningCaptured`, and `PolicyBreached` domain events to know when to recompute, and never writes back into those aggregates.
