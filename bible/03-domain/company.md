# Domain Model: Company

## Definition

A **Company** is the canonical representation of a real-world business enterprise that can be the subject of investment reasoning and, where publicly traded, the underlying asset of a Holding. It is the shared, investor-independent reference entity that identifies "which business" an Investment Thesis makes claims about, which Observations describe, and which a Holding is a position in. A Company captures the enduring identity and descriptive facts of the enterprise itself — not any one investor's opinion of it, and not the tradable security instrument as a market object. In V1 the Company is the equity issuer; the abstraction is deliberately named to generalize later to other capital-allocation subjects (a private business, a property, a fund) without renaming.

## Why It Exists

Every other reasoning object in the domain needs a stable, shared referent for the thing being analyzed. The Company exists to be that single source of identity so that Theses, Cases, Evidence, Observations, Holdings, and Decisions across all Portfolios and all investors point to the *same* enterprise consistently. It decouples investor-specific reasoning (Thesis, Case, conviction) from investor-independent facts (what the business is, its identifiers, its classification), preventing duplication and enabling cross-investor learning and aggregation while keeping opinion out of shared reference data.

## Key Attributes

- `company_id: identity` — stable internal unique identifier, independent of any external ticker or registrar.
- `legal_name: text` — the registered legal name of the enterprise.
- `display_name: text` — common/brand name used in the interface.
- `identifiers: set of external identifier` — durable external keys (e.g., ticker + exchange, ISIN, LEI, registration number) each with a scheme and value.
- `domicile: country` — jurisdiction of incorporation or principal establishment.
- `classification: set of taxonomy references` — sector/industry classifications used for grouping and diversification context.
- `listing_status: enumeration` — whether the enterprise is publicly listed, private, delisted, or acquired.
- `asset_class: enumeration` — the capital-allocation domain (public equity in V1), enabling future generalization.
- `description: text` — a factual, non-opinionated summary of what the business does.
- `created_at / updated_at: timestamps` — provenance of the reference record.

Prices, fundamentals, and time-series metrics are **not** attributes of the Company entity; they enter the domain as Observations that reference the Company.

## Invariants

- A Company must have at least one external identifier while its `listing_status` is `listed`.
- Each external identifier scheme+value pair must map to at most one Company (no duplicate identity for the same real-world key).
- `company_id` and `asset_class` are immutable once created; a change of asset class or a corporate reorganization that changes identity produces a new Company with recorded lineage rather than an in-place mutation.
- A Company carries no investor-specific opinion, conviction, or valuation; such content belongs to Investment Thesis, Investment Case, or Evidence.
- `legal_name` and `domicile` must be present for any Company that is the subject of an active Holding.

## Relationships

- **Holding** — many Holdings (across Portfolios and investors) reference one Company as the asset held. The Company does not know about individual Holdings.
- **Investment Thesis** — a Thesis makes falsifiable claims about exactly one Company; the Thesis references the Company by identity.
- **Investment Case** — a Case is organized around one Company (via its Theses) and references it.
- **Observation** — Observations that describe facts about a business reference the Company as their subject.
- **Evidence / Knowledge** — Evidence interpreting Observations about a Company, and accumulated Knowledge, reference the Company as subject context.

## Lifecycle / State

`listing_status` expresses the enterprise's market state: `private`, `listed`, `delisted`, `acquired`, `defunct`. Typical transitions: `private → listed` (IPO), `listed → delisted`, `listed → acquired`, `listed → defunct`. Corporate actions that dissolve or merge identity (full acquisition, dissolution) move the Company to a terminal state and record lineage to any successor Company. The Company reference record is never hard-deleted while any historical Holding, Thesis, or Observation references it.

## Aggregate Boundary

The Company **is an aggregate root** and functions as canonical shared reference data. Its aggregate owns its identity, names, external identifiers, classification, domicile, listing and asset-class facts, and description. It does **not** own Holdings, Theses, Cases, Observations, or market data — all of those reference the Company by identity but live in their own aggregates. The Company is the consistency boundary for the stable identity and descriptive facts of a single business enterprise, and the shared anchor that keeps all reasoning about that business pointed at one referent.
