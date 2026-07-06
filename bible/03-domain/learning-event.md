# Learning Event

## Definition

A Learning Event is a recorded moment of structured reflection in which the investor compares what was expected against what actually happened and extracts a durable lesson about their own judgment, process, or understanding. It is triggered by a meaningful reality check — a Thesis invalidated, a Risk materialized, a Catalyst that resolved against expectation, a Decision whose outcome diverged from its rationale — and it produces or refines Knowledge and updates the Behavior Profile. The Learning Event is the primary mechanism by which Adaptive Quality Investing "adapts": it closes the loop between prediction and outcome and converts experience into improved future decision quality.

## Why It Exists

The central thesis of AQI is that decision quality can be systematically improved through deliberate feedback. Without a first-class construct, learning stays implicit, unmeasured, and vulnerable to hindsight and self-serving bias. The Learning Event exists to (1) force explicit comparison of pre-registered expectations to outcomes, (2) attribute results to skill versus luck versus process, (3) generate reusable Knowledge and calibrate the Behavior Profile, and (4) build an auditable record of how the investor's judgment evolves over time.

## Key Attributes

- `id` (identifier): Globally unique, immutable identifier.
- `trigger_type` (enum): What prompted reflection — `ThesisInvalidated`, `RiskMaterialized`, `CatalystResolved`, `DecisionOutcome`, `PeriodicReview`.
- `trigger_ref` (reference): The source object (Thesis, Risk, Catalyst, or Decision).
- `expectation` (text): What was believed or predicted beforehand, drawn from the pre-registered record.
- `outcome` (text): What actually occurred.
- `variance_analysis` (text): The reasoned account of why expectation and outcome diverged (or converged).
- `attribution` (enum): `Skill`, `Luck`, `ProcessGap`, `KnowledgeGap`, `BehavioralError`, `CorrectProcessBadOutcome`.
- `lesson` (text): The distilled, forward-applicable takeaway.
- `resulting_knowledge_refs` (reference set, nullable): Knowledge units created or superseded.
- `behavior_profile_impact` (structured, nullable): Adjustments propagated to the Behavior Profile.
- `status` (enum): `Captured`, `Synthesized`, `Applied`.
- `occurred_at`, `captured_at`, `synthesized_at` (timestamp).

## Invariants

- A Learning Event MUST reference exactly one `trigger_ref` consistent with its `trigger_type`.
- Both `expectation` and `outcome` MUST be populated before an `attribution` may be assigned; attribution without both sides of the comparison is invalid.
- `attribution` MUST distinguish outcome quality from process quality — a good outcome from a poor process, or a poor outcome from a sound process, must be representable (`CorrectProcessBadOutcome`).
- A Learning Event is append-only once `Synthesized`; corrections are made by recording a new Learning Event, never by editing the record.

## Relationships

- Triggered by **Investment Thesis** (invalidation), **Risk** (materialization), **Catalyst** (resolution), or **Decision** (outcome divergence) via `trigger_ref`.
- Produces or supersedes **Knowledge** (`resulting_knowledge_refs`).
- Updates the **Behavior Profile** (`behavior_profile_impact`).
- May prompt revision of a **Policy** when a recurring `BehavioralError` or `ProcessGap` warrants a new guardrail.
- Draws on **Evidence** and **Observation** as the factual basis for the outcome side of the comparison.

## Lifecycle / State

`Captured` when the trigger fires and the expectation/outcome pair is recorded. `Captured → Synthesized` once variance analysis, attribution, and lesson are complete. `Synthesized → Applied` once its outputs (Knowledge, Behavior Profile updates, or Policy proposals) have been propagated. States advance monotonically; a Learning Event is never reopened, preserving an honest historical record of what was understood at each point.

## Aggregate Boundary

Learning Event is an **aggregate root**. It owns its comparison record — `expectation`, `outcome`, `variance_analysis`, `attribution`, and `lesson` — which must be internally consistent and mutated atomically. It references but does not own its trigger source, the Knowledge it generates, or the Behavior Profile it influences; those are separate aggregates updated through domain events (`LearningCaptured`, and downstream Knowledge/Behavior updates). This keeps reflection immutable and independently queryable as the system's learning ledger.
