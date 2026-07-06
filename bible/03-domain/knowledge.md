# Knowledge

## Definition

Knowledge is a durable, curated, and structured unit of understanding about a Company, an industry, a management team, a competitive dynamic, or an investing principle, distilled from one or more pieces of Evidence and Observations and retained independently of any single Investment Thesis. Where Evidence is a sourced fact bearing on a specific Thesis and an Observation is an unevaluated noted change, Knowledge is the accumulated, refined, and reusable "what we understand to be true" that survives across theses, decisions, and time. It is the institutional memory of the investor.

## Why It Exists

Adaptive Quality Investing depends on compounding understanding, not just capital. Facts arrive as transient Evidence and Observations attached to specific arguments; without a dedicated construct, that understanding is lost when a Thesis is closed or a Holding is exited. Knowledge exists to (1) prevent re-learning the same lessons, (2) let a single understanding inform many theses (e.g., understanding a company's capital-allocation history), (3) provide a searchable, confidence-weighted substrate the system reasons over, and (4) generalize beyond public equity into future capital-allocation domains without redesign.

## Key Attributes

- `id` (identifier): Globally unique, immutable identifier.
- `subject_type` (enum): The kind of subject the Knowledge concerns — `Company`, `Industry`, `Management`, `MacroFactor`, `Principle`.
- `subject_ref` (reference, nullable): Reference to a Company or other canonical subject when `subject_type` is entity-bound; null for general Principles.
- `statement` (text): A concise, declarative assertion of what is understood.
- `confidence` (enum/decimal): Graded conviction — `Tentative`, `Working`, `Established` — optionally with a normalized 0–1 score.
- `derived_from` (reference set): Ordered references to the Evidence and Observation items that support the statement.
- `supersedes` (reference, nullable): Reference to a prior Knowledge unit this one revises or replaces.
- `tags` (string set): Retrieval keys (theme, sector, principle category).
- `status` (enum): `Active`, `Superseded`, `Retired`.
- `created_at`, `updated_at`, `last_reaffirmed_at` (timestamp).

## Invariants

- A Knowledge unit MUST have at least one `derived_from` reference OR be explicitly flagged as an axiomatic Principle authored directly by the investor.
- `confidence` MUST be consistent with the strength and independence of its supporting Evidence; confidence above `Tentative` requires at least one corroborating source.
- A unit in `Superseded` status MUST reference the superseding unit; the superseding unit MUST reference it via `supersedes`. Supersession is append-only — prior Knowledge is never destructively edited.
- `statement` MUST be a standalone assertion that is intelligible without its supporting Evidence loaded.

## Relationships

- Distilled from **Evidence** and **Observation** (many-to-many via `derived_from`).
- Concerns a **Company** (or industry/management context) via `subject_ref`.
- Informs one or more **Investment Thesis** and **Investment Case** constructions but is owned by neither.
- Consumed by **Decision** reasoning and by **Learning Event** synthesis.
- Refined by **Learning Event**, which is a common trigger for creating or superseding Knowledge.

## Lifecycle / State

`Active` on creation. Transitions to `Superseded` when a revised unit replaces it, or to `Retired` when the understanding is no longer relevant (e.g., the underlying business line no longer exists). Transitions are monotonic: `Active → Superseded` and `Active → Retired` are permitted; a `Superseded` or `Retired` unit is immutable and never returns to `Active`. Reaffirmation updates `last_reaffirmed_at` and may raise `confidence` without changing state.

## Aggregate Boundary

Knowledge is an **aggregate root**. It owns its `statement`, `confidence`, `status`, and its supersession chain metadata. It holds *references* to — but does not own — the Evidence and Observation records in its `derived_from` set (those belong to their own aggregates), nor the Company it describes. Consistency guaranteed within the boundary: a Knowledge unit and its confidence/status must be mutated atomically; changes to supporting Evidence are handled by domain events rather than direct cross-aggregate writes.
