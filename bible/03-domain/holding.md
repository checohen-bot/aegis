# Domain Model: Holding

## Definition

A **Holding** is a single, currently or formerly held position in one asset within one Portfolio, together with the reasoning that justifies it and the record of how it came to exist and evolve. It represents the intersection of "which Portfolio," "which Company (asset)," and "the live Investment Case that backs owning it." A Holding is the durable, evolving object that ties an investor's committed capital in a specific security to the falsifiable reasoning behind that commitment. It is distinct from a transaction (a discrete buy or sell event) and from a Decision (a recorded act of judgment); a Holding is the *ongoing position and its rationale*, shaped over time by many Decisions.

## Why It Exists

AQI insists that every position be traceable to explicit, testable reasoning and be continuously reconciled against reality. The Holding exists to enforce that traceability: it binds committed capital to an active Investment Case and thereby makes it possible to ask, at any moment, "why do we still own this, and does the original reasoning still hold?" It is the unit at which position-level conviction, sizing rationale, exposure, and thesis health are tracked, and the unit against which Observations and Evidence are continuously evaluated for confirmation or falsification.

## Key Attributes

- `holding_id: identity` — stable unique identifier.
- `portfolio_ref: reference` — the Portfolio this Holding belongs to.
- `company_ref: reference` — the Company (asset) held.
- `investment_case_ref: reference` — the currently governing Investment Case justifying the Holding.
- `status: enumeration` — lifecycle state (see Lifecycle).
- `quantity: quantity` — units currently held (zero when closed).
- `cost_basis: money` — aggregate acquisition cost in the Portfolio's base currency.
- `conviction_level: ordinal` — the investor's current strength of belief in the Case backing this Holding.
- `target_allocation: percentage (optional)` — intended weight within the Portfolio, per sizing rationale.
- `opened_at / closed_at: timestamps` — when the position was first established and finally exited.
- `origin_decision_ref: reference` — the Decision that opened the Holding.

Current market value and unrealized/realized return are **derived** and not authoritative attributes of the entity.

## Invariants

- A Holding must reference exactly one Portfolio and exactly one Company, both immutable for the life of the Holding.
- A Holding must reference exactly one active Investment Case while in any `open` state; a Holding may not be open without justifying reasoning.
- Only one active Holding may exist for a given (Portfolio, Company) pair at a time; re-establishing an exited position after full closure creates a new Holding.
- `quantity` must be zero if and only if `status` is `closed`.
- Every change to `quantity`, `cost_basis`, or the governing Investment Case must be attributable to a Decision.
- A Holding cannot be created except as the result of a Decision (`origin_decision_ref` is required).

## Relationships

- **Portfolio** — a Holding references and is grouped under exactly one Portfolio. The Portfolio is the allocation and governance context.
- **Company** — a Holding references exactly one Company, the asset held. Company is shared reference data, not owned by the Holding.
- **Investment Case** — a Holding references the Investment Case that justifies it; the Case (and the Investment Theses within it) is the falsifiable reasoning under continuous test.
- **Decision** — Decisions act upon a Holding (open, add, trim, hold-review, close). Each mutation of the Holding is caused by a Decision that references it.
- **Observation / Evidence** — Observations about the held Company generate Evidence that bears on the Holding's Investment Case, informing conviction and future Decisions. The Holding does not own these; they reference the Case/Company.

## Lifecycle / State

A Holding progresses through: `proposed` (a Decision to open exists but the position is not yet established) → `open` (capital committed, actively tracked) → `under_review` (a triggering Observation or thesis stress has flagged the Case for re-examination) → `closed` (fully exited, retained as historical record). Valid transitions: `proposed → open`, `open → under_review`, `under_review → open`, `open → closed`, `under_review → closed`, `proposed → closed` (abandoned before establishment). A Holding never leaves `closed`.

## Aggregate Boundary

The Holding **is an aggregate root**. Its aggregate owns its identity, status, position facts (quantity, cost basis), conviction and sizing intent, and the *references* to its Portfolio, Company, and governing Investment Case. It does **not** own the Portfolio, the Company, the Investment Case, or the Decisions that act on it — each is a separate aggregate referenced by identity. The Holding is the consistency boundary for a single position's state and the rationale-linkage that keeps committed capital tethered to falsifiable reasoning.
