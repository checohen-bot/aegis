# Prompt Strategy and the Prompt Library

## Purpose

Prompts are the most dangerous place for provider coupling to leak back into an otherwise model-agnostic architecture. A prompt is intrinsically implementation detail — the vendor-specific phrasing that coaxes one model into satisfying a capability contract — yet teams routinely bury prompts as string literals inside application code, tying business logic to a model's quirks. This chapter specifies how Aegis keeps prompts where they belong: as **versioned, testable artifacts** behind the adapter seam, expressing capability contracts rather than model tricks, organized so that changing a prompt is a data change, not a code change.

## Principle 1 — Capability Contracts, Not Prompt Tricks, Are the Interface

The system's stable interface is the capability contract: typed inputs, typed outputs, stated invariants (see `capabilities-not-models.md`). A prompt is merely one adapter's means of hitting that contract for one provider. Therefore:

- **Callers never see prompts.** Domain and application code invoke capabilities by name; they have no prompt parameter and cannot pass raw text into a model.
- **Prompts render from contracts.** An adapter takes the typed request and renders it through a prompt template; it never concatenates ad hoc strings from business logic.
- **Model-specific coaxing is quarantined.** A trick that a given model needs — a particular delimiter, a chain-of-thought scaffold, a JSON-mode instruction — lives inside that provider's prompt artifact and nowhere else. A different provider's adapter uses a different artifact. Neither leaks upward.

If a "prompt improvement" would require changing a caller, the contract is wrong, not the prompt.

## Principle 2 — Prompts Are Versioned Artifacts

Every prompt is a file, not a literal. The Prompt Library under `/prompts` is the single source of truth, structured by capability and version:

```
/prompts
  /assess.thesis_contradiction
    /1.2.0
      anthropic.system.md
      anthropic.user.md.j2        # Jinja template over the request contract
      openai.system.md
      openai.user.md.j2
      contract.json               # input/output schema this prompt targets
      evals.jsonl                 # golden fixtures for this version
      CHANGELOG.md
    /1.1.0
      ...
  /extract.candidate_evidence
    /...
```

Each capability version directory contains: one prompt set **per provider** (so the same contract version can be served by any adapter), the `contract.json` the prompts must satisfy, the golden evaluation fixtures, and a changelog. The directory *is* the versioned artifact; the adapter references it by capability name, contract version, and provider — never by inlined text.

## Principle 3 — Semantic Versioning of Capability Definitions

Capability contracts and their prompts are versioned together under semantic versioning:

- **Patch** (1.2.0 → 1.2.1) — prompt wording refinement that does not change inputs or outputs. Backward compatible; callers unaffected.
- **Minor** (1.2.x → 1.3.0) — additive contract change (a new optional output field). Callers may adopt at will.
- **Major** (1.x → 2.0.0) — breaking contract change. Old and new versions run side by side; callers migrate deliberately.

The Gateway resolves a capability to a specific version, so multiple versions coexist and a prompt change is releasable, A/B-testable, and reversible independently of application deployments. A regression is a version pin, not a hotfix.

## Principle 4 — Prompts Are Tested Like Code

Because each prompt version ships with `evals.jsonl`, prompts are subject to the evaluation harness (see `evaluation-and-guardrails.md`). No prompt reaches production without passing its capability's evaluation suite against the target provider. Tests assert contract conformance (output parses and validates), grounding (every claim cites an in-input source), and quality (agreement with human-labeled golden cases above a threshold). A prompt edit that lowers eval scores is blocked in CI the same way a failing unit test is. This converts prompt engineering from folklore into a measurable, gated engineering discipline.

## Principle 5 — Templates Render From the Contract Only

Prompt templates are Jinja files whose only inputs are the fields of the typed request contract. A template cannot reach into global state, the database, or arbitrary context; what it may reference is exactly what the contract declares. This guarantees that the prompt is a pure function of validated, scoped input — which in turn makes grounding enforceable (the model is only ever shown sources the Gateway can later verify against; see `explainability.md`) and makes injection surfaces auditable. Retrieved Knowledge and Evidence enter the template as structured, delimited, individually-identified blocks, never as an unbounded context dump (see `memory-and-knowledge.md`).

## Principle 6 — No Prompt Encodes a Decision or a Provider Assumption

Two prohibitions are absolute:

1. **No prompt may instruct the model to decide, trade, or act.** Prompts elicit assessments, extractions, and explanations — never authoritative actions. The human boundary (see `cognitive-pipeline.md`) is upstream of any prompt's authority.
2. **No prompt assumption may bind a caller.** If provider A needs the request framed one way and provider B another, that difference is fully absorbed by having two artifacts under the same version directory. The contract the caller sees is identical.

## Operational Model

At runtime an adapter calls `prompt_library.render(capability, version, provider, request)`. The library loads the pinned artifact, validates that the request matches `contract.json`, renders the template, and returns the provider-shaped prompt for the adapter to send. The library is the one component allowed to know both a capability and a provider, and it knows them only as lookup keys into files — never as branching logic. Prompt artifacts are deployed as versioned, immutable content; a "rollback" restores a prior directory, and production always runs a pinned, evaluated version.

## Why This Preserves Model-Agnosticism

Prompts are the natural leak point for provider coupling, and Aegis seals it by construction: prompts live outside code, keyed by provider so every provider has its own set; the caller's interface is the contract, which is provider-free; and every prompt is gated by evaluation so a provider swap is validated, not hoped. Adding or replacing a model means adding a provider's prompt files under existing version directories and re-running evals — no caller, no contract, no domain object changes. The Prompt Library is how the platform stays model-agnostic *at the exact place most systems accidentally become model-bound*.
