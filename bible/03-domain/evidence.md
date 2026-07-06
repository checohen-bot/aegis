# Domain Model: Evidence

## Definition

**Evidence** is an interpreted, decision-relevant unit of reasoning that bears on a specific Investment Thesis, derived from one or more Observations and assessed as either supporting or contradicting the claim. Where an Observation is a raw, uninterpreted fact about the world, Evidence is what that fact *means* for a particular claim: it carries a judgment ("this quarter's gross-margin expansion supports the durable-advantage thesis" or "management's guidance cut contradicts it"), a polarity, a strength, and the reasoning that connects observation to claim. Evidence is the bridge between neutral facts and falsifiable reasoning; it is the mechanism by which reality is allowed to confirm or refute a Thesis.

## Why It Exists

AQI requires that conviction be earned and revised against evidence rather than asserted. Evidence exists to make the link between fact and belief explicit and auditable: it records which Observations were interpreted, how they were interpreted, against which claim, and with what weight and direction. This enables a Thesis's evidential standing to be computed rather than guessed, allows contradicting facts to visibly accumulate until a falsification condition is met, and preserves the interpretive reasoning so that later review (and Learning Events) can judge not only whether the conclusion was right but whether the interpretation was sound.

## Key Attributes

- `evidence_id: identity` — stable unique identifier.
- `thesis_ref: reference` — the Investment Thesis this Evidence bears on.
- `observation_refs: set of reference` — the one or more Observations from which this Evidence is derived.
- `company_ref: reference` — the Company the underlying facts concern (subject context, consistent with the referenced Thesis).
- `polarity: enumeration` — whether the Evidence `supports`, `contradicts`, or is `mixed` relative to the claim.
- `strength: ordinal` — how much weight this Evidence should carry.
- `interpretation: text` — the reasoning connecting the Observations to the claim.
- `assessor_ref: reference` — who made the interpretation (investor or system component).
- `confidence: ordinal` — how reliable the interpreter judges this Evidence to be.
- `knowledge_refs: set of reference (optional)` — accumulated Knowledge or heuristics informing the interpretation.
- `status: enumeration` — lifecycle state (see Lifecycle).
- `created_at: timestamp` — when the interpretation was recorded.

## Invariants

- Evidence must reference at least one Observation; an interpretation with no underlying observed fact is opinion, not Evidence, and is invalid.
- Evidence must reference exactly one Investment Thesis; the same interpretive act against a different claim is separate Evidence.
- The `company_ref` of the Evidence must match the `company_ref` of the referenced Thesis and of its Observations; Evidence may not connect facts about one Company to a claim about another.
- `polarity` and `strength` are required; Evidence with no direction or no weight cannot influence a Thesis and is invalid.
- Evidence is append-only and immutable once recorded; correction or reinterpretation is expressed by superseding it with new Evidence and marking the prior as `superseded`, never by silent edit, preserving the interpretive audit trail.

## Relationships

- **Observation** — Evidence is derived from one or more Observations, which it references by identity; Observations are raw and shared, Evidence is the interpretation layered on top.
- **Investment Thesis** — Evidence attaches to exactly one Thesis and updates its evidential standing and conviction according to polarity and strength.
- **Investment Case** — through its Thesis, Evidence contributes to the overall conviction of any Investment Case that composes that Thesis.
- **Company** — Evidence references the Company its facts concern, kept consistent with the Thesis and Observations.
- **Knowledge** — Evidence may draw on prior Knowledge to inform its interpretation and, when notable, may itself feed back into Knowledge.
- **Learning Event** — when Evidence meets a Thesis's falsification condition or confirms it, that resolution is a source of Learning Events.

## Lifecycle / State

Evidence moves through: `recorded` (interpretation captured and linked) → `active` (currently counting toward its Thesis's standing) → terminal states `superseded` (replaced by a corrected or updated interpretation) or `withdrawn` (retracted as erroneous, e.g., the underlying Observation was found invalid). Valid transitions: `recorded → active`, `active → superseded`, `active → withdrawn`. Because Evidence is immutable, "transition" changes only its status flag; the content is never rewritten.

## Aggregate Boundary

Evidence **is an aggregate root**, modeled as an immutable, append-only record. Its aggregate owns the interpretation, polarity, strength, confidence, and status, plus the *references* to its Observations, Thesis, Company, and any Knowledge. It does **not** own the Observations (raw shared facts), the Thesis, or the Company — each is a separate aggregate referenced by identity. Evidence is the consistency boundary for a single interpretive judgment linking observed fact to a falsifiable claim.
