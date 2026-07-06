# Domain Model: Investment Case

## Definition

An **Investment Case** is the complete, structured argument for taking or maintaining a capital-allocation stance on a Company, composed of one or more Investment Theses together with the Risks, Catalysts, valuation reasoning, and body of Evidence that inform it. Where an Investment Thesis is a single falsifiable claim, the Investment Case is the coherent whole an investor actually reasons and decides against: it assembles the constituent claims into a considered position ("here is the full argument for why owning this business, at this size, makes sense — and here is what would change my mind"). It is the object a Decision is justified by and the object a Holding is backed by.

## Why It Exists

AQI holds that capital-allocation decisions should be made against a complete, explicit argument rather than a single slogan or a diffuse feeling. The Investment Case exists to be that argument-of-record: it collects the multiple Theses that jointly justify a position, weighs supporting and contradicting Evidence, incorporates the Risks that could break the case and the Catalysts that could confirm it, and expresses the overall conviction and intended sizing. It gives Decisions a single, reviewable object to reference, and gives Holdings a single governing rationale that can be continuously reconciled against reality and, when the balance of the argument shifts, revised or abandoned deliberately.

## Key Attributes

- `case_id: identity` — stable unique identifier.
- `company_ref: reference` — the single Company the Case concerns.
- `author_ref: reference` — the investor who owns the Case.
- `title: text` — concise label for the argument.
- `summary: text` — the overall argument in brief, tying the constituent Theses together.
- `thesis_refs: ordered set of reference` — the Investment Theses composing the Case, with at least one designated primary.
- `valuation_reasoning: text` — how price relative to worth is being judged (quality-of-decision framing, not price prediction).
- `overall_conviction: ordinal` — the investor's aggregate strength of belief in the Case.
- `sizing_rationale: text` — why the intended position size is appropriate given conviction and risk.
- `risk_refs / catalyst_refs: sets of reference` — the Risks and Catalysts bearing on the Case.
- `status: enumeration` — lifecycle state (see Lifecycle).
- `created_at / last_reviewed_at: timestamps` — provenance and review recency.

## Invariants

- An Investment Case must reference at least one Investment Thesis and must designate exactly one of them as primary.
- All Theses referenced by a Case must concern the same Company as the Case; a Case spans exactly one Company.
- `overall_conviction` must be consistent with the evidential standing of its Theses; a Case cannot claim high conviction while its primary Thesis is under review or contradicted by the weight of Evidence.
- A Case may not be `active` if its primary Thesis is `invalidated`; invalidation of the primary claim forces the Case into review or closure.
- The Case's argument is versioned: material revision of the constituent claims or sizing rationale creates a new version, preserving what was argued at the time each Decision was made against it.

## Relationships

- **Company** — a Case concerns exactly one Company, referenced by identity.
- **Investment Thesis** — a Case composes one or more Theses; Theses are separate aggregates referenced by identity, not owned internally, so they can be evaluated and reused independently.
- **Evidence** — Evidence bears on the Case through its Theses, shaping overall conviction.
- **Risk / Catalyst** — a Case references the Risks and Catalysts relevant to the position.
- **Holding** — a Holding references the Investment Case that justifies it; the Case is the Holding's governing rationale.
- **Decision** — a Decision references the Investment Case it is made against (and, per its own invariant, at least one Thesis within it).

## Lifecycle / State

An Investment Case moves through: `draft` (being assembled) → `active` (the governing argument for a proposed or open Holding) → `under_review` (triggered when a constituent Thesis is stressed, invalidated, or Evidence shifts the balance) → terminal states `superseded` (replaced by a revised Case) or `closed` (abandoned or fully exited). Valid transitions: `draft → active`, `active → under_review`, `under_review → active`, `active/under_review → superseded`, `active/under_review → closed`. Terminal states are immutable.

## Aggregate Boundary

The Investment Case **is an aggregate root**. Its aggregate owns the argument itself — summary, valuation and sizing reasoning, overall conviction, the ordering and primary designation of its Theses, and lifecycle state — plus the *references* to its Company, Theses, Risks, and Catalysts. It does **not** own the Theses, Evidence, Risks, Catalysts, Holdings, or Decisions as internal entities; each is a separate aggregate referenced by identity. The Case is the consistency boundary for one coherent investment argument and the aggregate conviction it expresses.
