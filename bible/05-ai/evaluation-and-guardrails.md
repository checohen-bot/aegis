# Evaluation and Guardrails

## Purpose

A model-agnostic architecture is only trustworthy if the quality and safety of its cognitive outputs are *measured and constrained independently of the model producing them*. This chapter specifies the two mechanisms that do so: **guardrails** — runtime constraints that block unsafe or ungrounded outputs before they reach a user — and the **evaluation harness** — the continuous measurement that tracks capability quality over time and gates every model or prompt change. Both live above the adapter seam, so they hold regardless of which provider is installed and become the objective test a swap must pass.

## The Non-Negotiable Constraint

> AI must never autonomously execute a trade or record a Decision.

This is the top-level guardrail and it is enforced structurally, not by prompt. No capability output contract is or contains a `Decision` or an order. No pipeline stage holds a write handle to the `Decision` aggregate or to any brokerage integration. The domain rejects any `Decision` whose actor is a system principal. Even a fully compromised or hallucinating model has no code path to act — it can only produce assessments that a human must adjudicate (see `cognitive-pipeline.md`). Safety here is a property of the wiring, not of the model's compliance.

## Guardrails: Runtime Constraints

Guardrails run in the Capability Gateway as pre- and post-invocation checks. They are provider-agnostic and apply to every capability call.

### Pre-Invocation

- **Input scoping** — the request is validated against the contract and confirmed to reference only domain objects within the invoking investor's authorization scope. A capability cannot be handed data it may not see.
- **PII redaction** — data leaving the boundary to a provider is redacted per policy; identifiers are tokenized so the provider never receives raw account identity.
- **Injection isolation** — untrusted content (Observation text, filing bodies) is passed only as clearly delimited, non-instructional data blocks, never merged into the instruction channel. Prompt-injection attempts in source documents are treated as data, not commands.

### Post-Invocation

- **Contract validation** — the output must parse and satisfy its typed schema, or it is rejected (never returned as raw text).
- **Grounding check** — every factual claim must cite a source that (a) resolves to a real domain object and (b) was actually in the input set. Claims citing invented or out-of-scope sources are stripped; if stripping empties the result, the call fails. This is the primary defense against **hallucinated evidence** (see `explainability.md`).
- **Confidence consistency** — a claim's confidence must be consistent with the number and independence of its sources; inconsistent confidence is a violation.
- **Factual-grounding cross-check** — for high-stakes capabilities (contradiction assessment, fact extraction), a second, independent verification pass confirms each claim is entailed by its cited source. Because this pass is itself a capability, it can be served by a *different* provider than the one that produced the claim, giving cross-model corroboration without any hard-coded vendor.

A guardrail failure is a first-class, observable event (OpenTelemetry span attribute `ai.guardrail.outcome`), feeding both fallback logic and the quality metrics below.

## The Evaluation Harness

Guardrails catch failures per-call; evaluation measures capability *quality over time* and is the gate through which every model, adapter, or prompt change must pass.

### Golden Datasets

Each capability version ships a curated evaluation set (`evals.jsonl`, see `prompt-strategy.md`): representative inputs paired with human-labeled expected outcomes — e.g., Observation/Thesis pairs labeled confirm/contradict/neutral by an expert, filings with the correct extracted Evidence and locators. These datasets are versioned with the capability contract and grow as production edge cases are triaged in.

### Metrics

The harness scores each capability, per provider, on:

- **Contract conformance** — fraction of outputs that parse and validate.
- **Grounding fidelity** — fraction of claims with valid, in-input sources.
- **Faithfulness** — fraction of claims actually entailed by their cited sources (adjudicated by the cross-check capability plus human spot audit).
- **Task accuracy** — agreement with golden labels (e.g., contradiction classification F1).
- **Calibration** — whether stated confidence matches empirical correctness.
- **Cost and latency** — operational quality per provider.

### Gating

Evaluation is wired into CI and release. A prompt edit, a contract change, or a new provider adapter cannot ship unless it meets or exceeds the current version's thresholds on the golden set. **A provider swap is not an act of faith; it is a diff that must pass the same evaluation suite.** This is the operational teeth of the frozen principle: the harness is the fixed instrument, and the model is the variable it measures.

### Continuous Monitoring

Beyond release gating, the harness runs against sampled production traffic (with human labels backfilled) to detect drift — a provider silently changing behavior, or a capability degrading on a shifting input distribution. Drift breaching a threshold raises an alert and can trigger automatic fallback to a known-good adapter via the Gateway's routing policy.

## Human Adjudication as Ground Truth

The ultimate evaluator is the investor. Every disposition at the human boundary — a rejected candidate Evidence, a dismissed contradiction flag, an accepted assessment — is captured as a labeled outcome and flows back into the golden datasets. Over time the system's evaluation basis is grounded in the platform's own expert users, not a static benchmark, and this labeled corpus is itself provider-independent — it evaluates *any* model equally.

## Model-Agnosticism of Evaluation and Guardrails

Guardrails execute in the Gateway; evaluation runs against contracts and golden data. Neither imports a provider SDK; both treat the provider as a swappable variable under test. The consequence is decisive: quality and safety are not claims about a chosen model — they are continuously measured properties of the architecture that any candidate model must satisfy before it is trusted, and must keep satisfying to remain in service. The model can change; the standard it is held to does not.
