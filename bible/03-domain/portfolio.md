# Domain Model: Portfolio

## Definition

A **Portfolio** is a bounded collection of capital deployed by a single investor toward a defined set of objectives, together with the governing intent, constraints, and policies that shape how capital is allocated within it. It is the top-level organizing context under which an investor holds positions, records decisions, and evaluates outcomes. A Portfolio is not merely a list of positions; it is the accounting and governance boundary that gives those positions meaning — it answers the questions "whose capital is this, toward what mission, under what rules, and how is it performing as a whole?" In V1 a Portfolio contains only long-term public equity positions, but the concept is asset-class agnostic and must accommodate future capital-allocation domains without redesign.

## Why It Exists

Adaptive Quality Investing evaluates decision quality against explicit intent. A Portfolio exists to supply that intent and the aggregate context against which individual Holdings and Decisions are judged. It anchors a **Capital Mission** (the purpose and objectives of the capital), enforces **Policy** (allocation limits, concentration rules, exclusions), and provides the denominator for portfolio-level risk, diversification, and performance measurement. Without a Portfolio, Holdings and Decisions would be isolated facts with no allocation context, no constraint framework, and no way to assess whether the whole is coherent with its stated purpose.

## Key Attributes

- `portfolio_id: identity` — stable unique identifier for the Portfolio.
- `owner_id: reference` — the investor (account principal) who owns this Portfolio.
- `name: text` — human-readable label chosen by the owner.
- `base_currency: currency code` — the currency in which aggregate value and performance are denominated.
- `capital_mission_ref: reference` — the governing Capital Mission expressing objectives, time horizon, and constraints.
- `policy_refs: set of reference` — the Policies currently binding this Portfolio (concentration limits, exclusions, allocation targets).
- `status: enumeration` — lifecycle state (see Lifecycle).
- `inception_date: date` — when the Portfolio began holding or was funded.
- `benchmark_ref: reference (optional)` — a comparison standard used for decision-quality context, not price prediction.
- `created_at / closed_at: timestamps` — provenance of the Portfolio record.

Monetary aggregates (total value, invested capital, cash balance) are **derived** from the Portfolio's Holdings and cash movements and are not authoritative attributes of the Portfolio entity itself.

## Invariants

- A Portfolio must reference exactly one Capital Mission at all times while in an active state.
- A Portfolio must have exactly one owner; ownership is immutable for the life of the Portfolio.
- `base_currency` is immutable once the Portfolio holds any position.
- Every Holding attributed to the Portfolio must reference this Portfolio's identity; a Holding cannot exist in more than one Portfolio.
- All active Policies referenced by the Portfolio must be mutually satisfiable; a Policy set that is self-contradictory is invalid.
- A Portfolio may not transition to `closed` while it references any open Holding.

## Relationships

- **Capital Mission** — a Portfolio references one Capital Mission; the Mission is a distinct aggregate that expresses purpose and constraints and may inform Policy.
- **Policy** — a Portfolio references a set of Policies that constrain Decisions made within it. Policies are separate aggregates referenced by identity.
- **Holding** — a Portfolio is the context for many Holdings. Each Holding references its Portfolio by identity; Holdings are their own aggregate roots (not contained inside the Portfolio aggregate) to keep the aggregate small and independently loadable.
- **Decision** — Decisions are made within the scope of a Portfolio and reference it by identity.
- **Behavior Profile** — the owner's Behavior Profile provides cross-portfolio behavioral context; it is not owned by the Portfolio.

## Lifecycle / State

A Portfolio moves through: `draft` (created, mission and policy being defined, may hold no positions) → `active` (funded and eligible to acquire Holdings and record Decisions) → `dormant` (temporarily inactive; retains Holdings but discourages new Decisions) → `closed` (no open Holdings, retained for historical record). Valid transitions: `draft → active`, `active → dormant`, `dormant → active`, `active → closed`, `dormant → closed`. A Portfolio cannot return from `closed`.

## Aggregate Boundary

The Portfolio **is an aggregate root**. Its aggregate owns the Portfolio's identity, name, base currency, status, and the *references* to its Capital Mission and Policies. It does **not** own Holdings, Decisions, Capital Mission, or Policy as internal entities — each of those is a separate aggregate referenced by identity. The Portfolio is the consistency boundary for portfolio-level governance state (which Mission and Policies apply and the Portfolio's own lifecycle), and it is the correlation key through which its Holdings and Decisions are grouped and aggregated.
