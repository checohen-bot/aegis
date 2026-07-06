# Domain Model: Observation

## Definition

An **Observation** is a raw, uninterpreted, point-in-time record of a fact about the world relevant to investment reasoning — a reported financial figure, a disclosed corporate action, a management statement, a regulatory filing, a market data point, or a news event — captured as it was, with its source and the moment it was observed. An Observation asserts *that something is (or was reported to be) the case*, without asserting what it means for any claim. It is the domain's neutral, factual substrate: the shared ground truth from which interpreted Evidence is later derived. It is deliberately opinion-free so that the same fact can be interpreted differently by different investors and claims without corrupting the record of the fact itself.

## Why It Exists

AQI separates *what happened* from *what it means*, so that reasoning can be audited at both layers and so that facts are not silently entangled with the conclusions drawn from them. The Observation exists to be the immutable, timestamped, sourced record of facts, giving every piece of Evidence a verifiable origin and giving the whole system a reconstructable history of what was known and when. This separation is what makes honest, hindsight-resistant review possible: because Observations record the information available at a point in time, later analysis can distinguish a sound decision made on the facts then available from one that merely got lucky.

## Key Attributes

- `observation_id: identity` — stable unique identifier.
- `subject_company_ref: reference (optional)` — the Company the fact concerns, when applicable; some Observations are macro or market-wide.
- `observation_type: enumeration` — the kind of fact (e.g., financial metric, corporate action, filing, management statement, price/market data, news event).
- `content: structured or text value` — the factual payload as observed.
- `observed_at: timestamp` — the point in time to which the fact pertains (the "as-of" moment).
- `recorded_at: timestamp` — when the Observation entered the system.
- `source_ref: source descriptor` — the origin of the fact (filing, data feed, publication) with enough detail to verify it.
- `source_reliability: ordinal` — an assessment of how trustworthy the source is.
- `status: enumeration` — lifecycle state (see Lifecycle).

An Observation carries no polarity, no strength, and no claim linkage; those belong to Evidence.

## Invariants

- An Observation must record its `source_ref`, `observed_at`, and `recorded_at`; a fact with no verifiable origin or no time reference is not a valid Observation.
- An Observation is immutable once recorded; it is never edited in place. A correction is a new Observation that supersedes the prior one, and a fact later shown to be false is marked `invalidated`, never rewritten.
- An Observation must not contain interpretation, polarity, or conclusions; any judgment about meaning belongs to Evidence.
- `observed_at` must be less than or equal to `recorded_at`; a fact cannot be recorded before the moment it pertains to.
- When `subject_company_ref` is present it must reference an existing Company; a company-specific Observation cannot dangle without its subject.

## Relationships

- **Company** — an Observation may reference the Company it concerns as its subject; market-wide or macro Observations may have no company subject.
- **Evidence** — Evidence is derived from one or more Observations; the Observation is referenced by, but has no knowledge of, the Evidence built upon it. One Observation may underlie many pieces of Evidence across different Theses and investors.
- **Investment Thesis / Investment Case** — Observations reach Theses and Cases only indirectly, through the Evidence that interprets them; they never attach directly to a claim.
- **Knowledge** — patterns recognized across many Observations may contribute to accumulated Knowledge, but the Observation itself remains a raw record.

## Lifecycle / State

An Observation moves through: `captured` (recorded from its source) → `validated` (confirmed as accurately recorded and sourced) → terminal states `superseded` (replaced by a corrected Observation) or `invalidated` (found to be false or spurious). Valid transitions: `captured → validated`, `captured → invalidated`, `validated → superseded`, `validated → invalidated`. As with all immutable records, a transition changes only the status flag; the factual content is never altered.

## Aggregate Boundary

The Observation **is an aggregate root**, modeled as an immutable, append-only ledger entry. Its aggregate owns the factual payload, timing, source, reliability, and status, plus the optional *reference* to its subject Company. It does **not** own Evidence, Theses, or Companies — Evidence references Observations, and the subject Company is separate shared reference data. The Observation is the consistency boundary for a single recorded fact as observed at a point in time, and the neutral foundation on which all interpreted reasoning in the domain is built.
