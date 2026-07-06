# The Cognitive Pipeline

## Purpose

The Cognitive Pipeline is the composed, end-to-end flow through which Aegis turns raw investor inputs into *decision-ready reasoning* — and stops. It ingests Observations, extracts candidate Evidence, relates that Evidence to a standing Investment Thesis, judges confirmation or contradiction, and surfaces the result to the investor with its full reasoning trail. It never makes the Decision. The pipeline is a choreography of capabilities (defined in `capabilities-not-models.md`), each invoked through the Capability Gateway; it composes cognition without ever depending on a model.

## The Human-in-the-Loop Invariant

> AI assists reasoning. It never autonomously decides.

Every stage below produces *candidates*, *assessments*, and *surfaced flags* — never state changes to authoritative domain objects. The only actor that can create or transition a `Decision`, promote a `CandidateEvidence` into authoritative `Evidence`, or alter an `Investment Thesis` is the investor. The pipeline's terminal act is always to *present*, and to wait. This is enforced structurally: no pipeline stage holds a write handle to the `Decision` aggregate, and the domain rejects any Decision whose actor is a system principal.

## Stage Flow

The pipeline is event-driven. Each stage consumes a domain event, invokes one or more capabilities, and emits a new event. Stages are independently deployable, individually observable via OpenTelemetry spans, and idempotent on their input event id.

```
Observation recorded
      │  event: ObservationRecorded
      ▼
[1] Normalize & scope        → resolve subject Company / Thesis context
      │  event: ObservationScoped
      ▼
[2] extract.facts_from_filing / extract.candidate_evidence
      │  → CandidateEvidence[] (each with source locator)
      │  event: CandidateEvidenceExtracted
      ▼
[3] retrieve.relevant_knowledge + link to Thesis
      │  → relates candidates to standing Investment Thesis / Case
      │  event: EvidenceRelated
      ▼
[4] assess.thesis_contradiction
      │  → ContradictionAssessment (confirm | contradict | neutral, cited)
      │  event: ThesisSignalAssessed
      ▼
[5] Surface to investor       → ReasoningBundle in the review queue
      │  event: ReasoningSurfaced
      ▼
   ┌─────────── HUMAN BOUNDARY ───────────┐
   │  Investor reviews, edits, accepts or │
   │  rejects. Investor records Decision. │
   └──────────────────────────────────────┘
```

### Stage 1 — Normalize & Scope

An incoming Observation is unstructured and unevaluated. This stage resolves its subject (which `Company`, which `Holding`) and identifies the candidate `Investment Thesis` and `Investment Case` contexts it may bear on. No AI judgment is committed here beyond scoping; ambiguous scope produces multiple candidate contexts, all carried forward.

### Stage 2 — Extract Candidate Evidence

The `extract.candidate_evidence` capability converts the Observation (and any attached source document, via `extract.facts_from_filing`) into typed `CandidateEvidence`. Every candidate carries a **source locator** — a reference back to the exact span, filing section, or Observation id it came from. A candidate without a locator is invalid and dropped by the Gateway's grounding post-check (see `evaluation-and-guardrails.md` and `explainability.md`). Candidates are *not* Evidence yet; they are proposals awaiting human confirmation.

### Stage 3 — Relate to Thesis and Retrieve Knowledge

The pipeline pulls the standing Investment Thesis's claims and, via `retrieve.relevant_knowledge`, the accumulated Knowledge units bearing on this subject (see `memory-and-knowledge.md`). It relates each candidate to specific Thesis claims — "this candidate speaks to the claim *margins are structurally expanding*." Relationships are explicit, typed edges, not prose. This is where prior institutional memory enters the reasoning without full-context stuffing.

### Stage 4 — Assess Signal

`assess.thesis_contradiction` produces a `ContradictionAssessment` per related claim: a classification of confirm / contradict / neutral, a normalized confidence, and a **cited reasoning chain** naming the exact Evidence candidates and Knowledge units it relied on. The assessment asserts nothing it cannot cite. A contradiction is the highest-value output of the whole system: it is the machine telling the investor "the thing you believe may be under threat — look."

### Stage 5 — Surface

The pipeline assembles a `ReasoningBundle`: the candidates, their sources, the related Thesis claims, the assessments, and the citation graph. It places the bundle in the investor's review queue and emits `ReasoningSurfaced`. The pipeline's work is now complete. It has changed no authoritative state.

## The Human Boundary

At the boundary the investor does real work, and the system supports it:

- **Confirm or reject candidate Evidence.** Confirmed candidates become authoritative `Evidence` attached to the Thesis; rejected ones are discarded with a reason (which itself becomes signal for evaluation).
- **Accept, revise, or dismiss assessments.** The investor may disagree with a contradiction flag; their disposition is recorded.
- **Record a Decision.** Only here can a `Decision` come into being — authored by the investor, referencing the Evidence and assessments that informed it, under the Portfolio's Policy constraints.
- **Trigger a Learning Event.** Where the reasoning revised understanding, the investor promotes it into Knowledge.

## Model-Agnosticism of the Pipeline

The pipeline is defined entirely in terms of capability names and domain events. It contains no provider SDK import, no model id, no prompt. Swapping the model behind any stage is an adapter change (see `provider-abstraction.md`) with zero pipeline edits; the event contracts and capability interfaces are the fixed points. Because stages communicate through durable events, a provider outage degrades gracefully — the affected stage retries or falls back at the Gateway while upstream and downstream stages are unaffected, and the human boundary is never bypassed to compensate.

## What the Pipeline Must Never Do

It must never execute a trade, transition a Decision, mutate a Thesis, promote its own candidates to authoritative Evidence, or present an assessment as fact. Its charter is to *prepare the investor to decide well* — to raise contradictions early, ground every claim, and hand a clean, cited reasoning bundle to the one actor allowed to act on it.
