# Memory, Knowledge, and Behavior

## Purpose

The AI layer reasons well only when it has the right prior understanding in front of it and none of the wrong. This chapter specifies how the cognitive layer interacts with two domain objects that constitute the investor's memory: **Knowledge** (institutional memory — what is understood to be true) and **Behavior Profile** (behavioral memory — how this investor tends to act). Two disciplines govern this interaction: Knowledge is *retrieved*, never naively stuffed; and the Behavior Profile is used to *reflect biases back to the investor*, never to steer them. Both are model-agnostic: retrieval and reflection are capabilities over domain objects, indifferent to the provider beneath.

## Part I — Knowledge as Retrieved Memory

### Why Not Full-Context Stuffing

The naive approach — concatenate everything the investor knows into the model's context — fails on every axis that matters here. It is provider-coupling by the back door (it tunes behavior to one model's context window and attention profile), it degrades reasoning quality (relevant Knowledge is diluted by noise), it destroys grounding (the model cannot cleanly cite which unit it used), and it is unbounded in cost and latency. Aegis rejects it. Knowledge enters reasoning through **deliberate retrieval**, not bulk injection.

### The `retrieve.relevant_knowledge` Capability

Retrieval is itself a capability with a typed contract: given a reasoning task (a subject Company, a Thesis claim, an Observation), it returns a *ranked, bounded, cited* set of Knowledge units relevant to that task. Its implementation is provider-swappable like any other:

- **Structured pre-filtering first.** Before any semantic step, retrieval narrows by domain structure: `subject_ref` matching the Company, `status = Active` (never `Superseded` or `Retired`), `subject_type`, and tags. This is deterministic database work, not model work, and it does most of the pruning.
- **Semantic ranking second.** Within the pre-filtered set, an embedding-based similarity ranks units against the task. Embeddings are produced through a capability adapter, so the embedding provider is as swappable as the generation provider — the vector store holds a `model_version` per embedding and re-embeds on provider change behind the seam.
- **Confidence and recency weighting.** Ranking favors `Established` over `Tentative` units and recently reaffirmed understanding, respecting the Knowledge domain's confidence grading.
- **Bounded output.** The result is a small, explicit set — each unit carried forward with its `id` and `statement` — sized to the reasoning task, not to a context window.

### Retrieved Knowledge Preserves Grounding

Each retrieved unit enters the downstream prompt as an individually-identified, delimited block (see `prompt-strategy.md`). When a later capability relies on it, the resulting claim cites that unit's `id` — and the grounding check verifies the citation against the actual retrieved set (see `explainability.md`). Retrieval and grounding thus reinforce each other: only retrieved, in-scope Knowledge can be cited, and every citation resolves to a real, inspectable unit. This is what makes the system's reasoning auditable rather than a black box that "just knows things."

### Respecting the Knowledge Lifecycle

The AI layer is a *consumer* of Knowledge, never an autonomous author of it. It may, through the pipeline, *propose* new or superseding Knowledge as candidates — but promotion to an authoritative Knowledge unit, and any supersession, happens only through a human-authored Learning Event (see `cognitive-pipeline.md`). Retrieval always respects supersession chains: a `Superseded` unit is invisible to reasoning, so stale understanding cannot silently re-enter a Thesis. Memory compounds under human curation, exactly as the Knowledge domain intends.

## Part II — Behavior Profile as a Mirror, Not a Lever

### The Ethical Constraint

The Behavior Profile records how an investor tends to act — patterns like selling winners too early, averaging down into deteriorating theses, over-concentrating after a run of confirmations, or anchoring on entry price. This is among the most sensitive data in the platform, and it admits two opposite uses. Aegis permits exactly one.

> The Behavior Profile is used to surface an investor's own biases *back to them*, so they can decide better. It is never used to manipulate, nudge, or steer them toward a particular action.

### Reflection, Not Persuasion

The `reflect.behavioral_pattern` capability turns the profile into *self-awareness*, not *direction*. When the pipeline prepares a ReasoningBundle for a pending Decision, reflection may surface an observation of the form: "You are considering adding to a position after a contradiction was flagged. Historically, in similar situations, you have averaged down into theses that later weakened. This is a pattern worth examining." It names the pattern, cites the past Decisions that established it, and stops. It offers no recommended action. It does not push toward buy or sell. Its entire purpose is to make a latent bias visible at the moment it is most likely to operate, so the human's own judgment can account for it.

### Structural Safeguards

The mirror-not-lever principle is enforced, not merely stated:

- **No prescriptive output.** The reflection capability's output contract carries an observed pattern, its supporting past Decisions, and a neutral prompt to reflect — with **no action field, no recommendation, no directional score.** A contract with nowhere to put "you should buy" cannot deliver it.
- **Cited to the investor's own history.** Every reflection cites the specific prior Decisions and Learning Events that constitute the pattern; the investor can inspect the basis, exactly as with any other grounded claim.
- **Symmetric by construction.** Reflections are surfaced whenever a relevant pattern is present, independent of which direction the investor is leaning — the system does not selectively withhold a mirror to encourage one outcome.
- **Downstream of the human boundary.** Reflection informs the investor before they decide; it never gates, blocks, or auto-adjusts a Decision. The investor remains the sole actor.

### Behavior Data Never Leaves as Identity

Like all sensitive inputs, Behavior Profile data crossing the provider boundary is tokenized and scoped by the Gateway's redaction guardrail (see `evaluation-and-guardrails.md`). The provider sees an abstract behavioral pattern to reason over, never the investor's identity.

## Model-Agnosticism

Both memory disciplines are expressed as capabilities over canonical domain objects — Knowledge, Behavior Profile, Decision, Learning Event — with contracts free of any provider concept. Retrieval, embedding, and reflection are each served by swappable adapters and gated by the same evaluation harness as every other capability. The memory model does not know the name of the model reasoning over it, and swapping that model changes nothing in how Knowledge is retrieved or how bias is reflected. Memory is a property of the domain; the model is a replaceable engine that reasons over it.
