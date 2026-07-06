# Explainability and Structural Grounding

## Purpose

In an Investment Intelligence Platform, an unsourced claim is worse than no claim: it manufactures false conviction, the exact failure mode Adaptive Quality Investing exists to prevent. This chapter specifies explainability as an **architectural invariant**, not a presentation feature. Every AI-generated output in Aegis — every summary, flag, suggestion, and assessment — must be traceable to the specific Evidence and Observations that produced it, and the system must make it *structurally impossible* to present an unsourced claim as fact. Explainability is enforced in the type system and the Gateway, so it holds no matter which model is behind the capability.

## The Core Requirement: Grounded Outputs Only

Aegis distinguishes two kinds of content in any AI output:

- **Grounded claims** — assertions backed by a resolvable reference to a source domain object (an `Evidence` id with a locator, an `Observation` id, a `Knowledge` id).
- **Ungrounded prose** — connective language, hedges, and framing that assert no fact.

The invariant: **every factual claim must be a grounded claim.** Ungrounded prose may exist only where it asserts nothing. This is not a stylistic preference enforced by prompt wording (which no model can be trusted to obey reliably); it is enforced by the output contract's shape.

## Structural Enforcement

### 1. Claims Are Typed, Not Free Text

Capability output contracts do not return a blob of model text. They return structured claims, each of which *requires* a source:

```python
class GroundedClaim(BaseModel):
    statement: str
    sources: conlist(SourceRef, min_length=1)     # cannot be empty
    confidence: confloat(ge=0.0, le=1.0)

class SourceRef(BaseModel):
    kind: Literal["evidence", "observation", "knowledge"]
    ref_id: str
    locator: str | None            # span / section within the source
```

Because `sources` has `min_length=1`, a claim with no source **cannot be constructed** — it fails contract validation at the Gateway before any consumer sees it. The impossibility is in the type, not in a reviewer's diligence.

### 2. Source Verification at the Gateway

Contract validation guarantees a source *field* is present; the Gateway's grounding post-check guarantees the source is *real and relevant*. For each `SourceRef` it verifies: the `ref_id` resolves to an existing domain object in this investor's scope; the referenced object was actually part of the capability's input set (a model cannot cite a source it was never given — that would be a fabricated citation); and, where a locator is present, the locator resolves within the source. Any claim failing these checks is stripped, and if stripping empties the output, the invocation fails rather than returning an unsourced result. This closes the "plausible but invented citation" failure mode common to LLMs.

### 3. The Citation Graph

Every surfaced output carries a **citation graph**: a persisted, queryable structure linking each claim to its sources, and transitively to the Evidence's own provenance and the Observations behind it. This graph is a first-class record, stored alongside the output and emitted on the OpenTelemetry span. It enables three things: the UI can render any claim with its sources one click away; an auditor can reconstruct *why* the system said what it said, months later; and the evaluation harness can measure grounding fidelity over time (see `evaluation-and-guardrails.md`).

### 4. No Consumer Reads Raw Model Text

By boundary rule, no domain, application, or UI consumer ever receives a provider's raw completion. They receive the validated, grounded output contract. The raw text exists only transiently inside the adapter, where it is parsed into the contract and then discarded. This means there is no path by which ungrounded model prose can reach a user — the only surface a user sees is the grounded contract.

## Confidence Must Be Honest

Grounded does not mean certain. Each claim carries a normalized confidence, and the UI is required to render it. A single-source claim, a claim from a Tentative Knowledge unit, or an assessment the model itself flagged as low-confidence must be visibly distinguished from a well-corroborated one. Explainability includes *epistemic honesty about strength*, not merely *presence of a source*. Confidence that is inconsistent with the number and independence of sources is a contract violation, mirroring the Knowledge domain's invariant.

## Explaining Recommendations

The `explain.recommendation` capability exists so that any flag or suggestion can be expanded into its reasoning chain on demand. Critically, it does not *generate* a post-hoc rationalization; it *renders the already-recorded citation graph* into readable form. The explanation is a view over the grounding that produced the output, so the explanation and the output can never diverge — a system cannot claim one reason while having acted on another. This distinction (rendering recorded provenance vs. generating a fresh justification) is what separates genuine explainability from plausible-sounding fabrication.

## What This Prevents

- **Hallucinated evidence** — a claim without a resolvable, in-input source cannot survive the Gateway.
- **Citation fabrication** — sources are verified against the actual input set, not merely against existence.
- **Unfalsifiable conviction** — because every claim resolves to Evidence, the investor can inspect and challenge the underlying fact, keeping theses falsifiable.
- **Reasoning drift** — the explanation is the recorded graph, so stated reasons match actual provenance.

## Model-Agnosticism

None of this depends on a provider. The output contract, the grounding post-check, the citation graph, and the source-verification rules live in the Gateway and the domain, above the adapter seam. A weaker or stronger model changes *how often* outputs pass the grounding check — a quality metric tracked by evaluation — but never changes *whether the invariant is enforced*. Swap the model, and unsourced claims remain structurally impossible to surface. Explainability is a property of the architecture, not of the model that happens to be installed.
