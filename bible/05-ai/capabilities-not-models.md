# Capabilities, Not Models

## The Frozen Principle

> Never build around a model. Build around capabilities. LLMs are interchangeable. Capabilities are permanent. The system must remain model-agnostic. Never tightly couple architecture to GPT, Claude, Gemini, DeepSeek, or any future provider.

This is the single load-bearing constraint of Volume V. Every design that follows exists to make it true in code, not in slideware. A reader should be able to take any AI-related module in Aegis, swap the underlying provider, and change nothing in the domain layer, the application layer, or any consumer of an AI result. If a proposed design cannot survive that test, it is wrong and must be rebuilt.

## What a Capability Is

A **capability** is a named, stable, provider-independent unit of cognitive work that the platform requires — expressed as a contract over typed domain inputs and typed domain outputs, with no reference to *how* the work is performed. It is the AI-layer analogue of a domain service interface: the system depends on the interface, never on the mechanism behind it.

A capability is defined by four things and only these four:

1. **Intent** — a precise, single-sentence statement of the cognitive task ("extract candidate Evidence items from a filing," "detect whether an Observation contradicts a stated Investment Thesis").
2. **Input contract** — a typed structure composed of canonical domain objects or their projections (an `Observation`, an `Investment Thesis`, a set of `Evidence` references), never raw provider-shaped payloads.
3. **Output contract** — a typed, validated structure the domain understands (a list of `CandidateEvidence` with source references, a `ContradictionAssessment` with confidence and citations), never free-form model text handed to a consumer verbatim.
4. **Invariants and guarantees** — properties that must hold regardless of implementation: every claim carries a source reference, confidence is normalized to 0–1, outputs never assert unsourced facts, the capability never emits a `Decision`.

Nothing in this definition mentions a prompt, a token limit, a temperature setting, a context window, or a vendor. Those are implementation details of an *adapter* that satisfies the contract (see `provider-abstraction.md`). The capability is what survives; the adapter is what is replaced.

## The Canonical Capability Set (V1)

Aegis defines its cognitive surface as a closed, versioned catalog of capabilities. Representative members:

- **`summarize.evidence`** — condense a set of Evidence into a faithful, fully-sourced synopsis.
- **`extract.facts_from_filing`** — turn an unstructured document into typed candidate Evidence with locators back into the source.
- **`assess.thesis_contradiction`** — judge whether an Observation confirms, contradicts, or is neutral to an Investment Thesis, with cited reasoning.
- **`explain.recommendation`** — render the reasoning chain behind a surfaced flag or suggestion, grounded in specific Evidence.
- **`retrieve.relevant_knowledge`** — select the Knowledge units bearing on a reasoning task (see `memory-and-knowledge.md`).
- **`reflect.behavioral_pattern`** — surface an investor's own recurring behavior from their Behavior Profile.

Each is a stable name with a versioned contract. New cognitive needs add new capabilities or new contract versions; they never leak provider concepts into the caller.

## Why Capabilities Are the Unit of Permanence

**Models depreciate; cognitive needs do not.** The requirement to "detect a thesis contradiction" predates every current model and will outlive all of them. If architecture is organized around a model, every model change is a migration. If it is organized around capabilities, a model change is a configuration change behind a stable seam. Aegis chooses the seam that moves least.

**Capabilities are testable independently of any model.** A contract with typed inputs, typed outputs, and stated invariants can be verified against golden fixtures and property checks (see `evaluation-and-guardrails.md`). "Does GPT do this well?" is not a system-level test; "does the `assess.thesis_contradiction` capability satisfy its contract on the evaluation set?" is. The provider becomes one swappable variable in an otherwise fixed harness.

**Capabilities keep AI subordinate to the domain.** Because inputs and outputs are canonical domain objects, the AI layer can never smuggle in a foreign vocabulary or a foreign authority. It cannot return "a decision"; it can only return an `Assessment` that a human turns into a `Decision`. The domain model — Volume III — remains sovereign. AI is a set of services the domain calls, never a layer the domain answers to.

**Capabilities localize risk.** Hallucination, prompt injection, provider outage, cost, and latency are all properties of an implementation. Bounding them at the capability seam means a failure or a swap is contained to one adapter, observable through one set of OpenTelemetry spans, and reversible without touching business logic.

## The Test Every Design Must Pass

For each AI feature in Aegis, ask: *If we deleted the current provider tomorrow and wired in a different one, what code outside the provider adapter would change?* The mandated answer is **none**. Domain code depends on capability interfaces. Application code orchestrates capability calls. Only the adapter — the thing that translates a capability contract into a specific provider's API — knows a vendor exists, and even it is registered, not hard-wired.

This chapter defines the *what*. The remaining chapters define the *how*: the gateway that enforces the seam, the pipeline that composes capabilities into assisted reasoning, the explainability and grounding that make outputs trustworthy, the prompt and evaluation machinery that keeps quality measurable, and the memory model that feeds reasoning without surrendering the investor's judgment. Throughout, the invariant holds: we build around capabilities, and capabilities do not know the name of the model beneath them.
