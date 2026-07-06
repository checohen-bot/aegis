# The Feature Lifecycle

*Volume IX — Execution Playbook · Chapter 2*

This chapter walks a single feature through the full Aegis lifecycle — from a business need to a released, learned-from capability — using one concrete example so that every stage is tangible rather than abstract. The lifecycle is fixed: **Business Need → RFC → ADR → Domain Model → Implementation → Tests → Docs → Review → Release → Learning.** No feature skips stages; small features move through them quickly, large ones slowly, but the sequence is invariant.

Our worked example: **"Give the investor the ability to record a Decision, with its reasoning, and have that Decision be explainable later."**

## Stage 1 — Business Need

Everything starts as intent expressed in mission terms, owned by the founder. Here the need is: *the investor made a real choice about capital, and Aegis must capture not just the choice but why it was made, so decision quality can be judged later against the Capital Mission it served.* The need is written down in the language of the domain — it references Decision, reasoning, Evidence, and explainability — not in the language of implementation. A need that cannot be stated in domain terms is not yet ready to become a feature.

## Stage 2 — RFC

The need becomes a **Request for Comments**: a short, structured proposal that turns intent into a considered shape. The Decision-recording RFC states the problem, the proposed user-visible behavior ("the investor records a Decision, attaches reasoning and referenced Evidence, and can later retrieve the full rationale"), the domain objects touched (Decision, Evidence, Observation, Capital Mission for the evaluation frame), the alternatives considered, and the open questions. The RFC is where disagreement is cheap. The founder validates that the RFC serves the mission and uses the correct meaning of "Decision"; engineering validates that it is buildable within the architecture. An RFC is approved when both are satisfied.

## Stage 3 — ADR

If the feature requires or sets an *architectural* choice, that choice is captured in an **Architecture Decision Record** before code. For our example, the ADR might record: "A Decision is an aggregate root; its reasoning and Evidence references are stored with mandatory provenance (model/prompt version if AI-assisted, inputs current at the time); Decisions are immutable once recorded and are superseded, never edited." This ADR is binding. If it overrides an architectural principle it says so explicitly. Features that fit cleanly within existing ADRs need no new one — but the check is deliberate, not skipped.

## Stage 4 — Domain Model

Now the Decision object is modeled precisely, in the same form as every canonical object in Volume III: definition, why it exists, key attributes, invariants, relationships, lifecycle/state, and aggregate boundary. For our feature: a Decision carries `id`, `rationale`, references to the `Evidence` it rests on, the `Capital Mission`/`Thesis` it serves, provenance, and `decided_at`. Its invariants are enforceable — a recorded Decision MUST carry a rationale and at least the mission frame against which it will be judged; an explainable Decision MUST retain its Evidence references immutably. The model is settled before any table is created.

## Stage 5 — Implementation

Engineering builds the feature within its module boundary. The Decision module owns its persistence and exposes a published interface — no other module reaches into its tables. Recording a Decision emits a domain event (a fact: "a Decision was recorded") that the Knowledge and Learning layers may later react to. The implementation honors replaceability: any AI assistance flows through the capability gateway so the model and prompt version are recorded as provenance, not hard-wired.

## Stage 6 — Tests

Tests are written to the invariants, not to the implementation. For the Decision feature: a Decision cannot be recorded without a rationale; its Evidence references are retrievable unchanged after the fact; the explainability query returns the full provenance chain; the emitted event carries the correct payload. Tests encode the *promises* of the feature so that future refactors are safe. The walking-skeleton discipline applies — at least one test proves the slice end-to-end.

## Stage 7 — Docs

The feature is documented where it will be found: the domain object in Volume III, any architectural choice in its ADR, and any user-facing behavior in the appropriate volume. Documentation is part of the feature, not a follow-up. An undocumented Decision-recording capability is not done, because a future engineer or the founder must be able to learn what it means and why, from the repository alone.

## Stage 8 — Review

Review checks the feature against the Definition of Done (Chapter 5): architectural consistency (boundaries respected, events used correctly), decision quality (does it model Decision faithfully), repository quality, maintainability, reliability, explainability (can the rationale be retrieved and trusted), and long-term evolution (can Decision be extended without breakage). Review is not a rubber stamp on working code; it is the gate that protects the qualities the company actually measures.

## Stage 9 — Release

The feature ships through CI/CD, which enforces the gates automatically: it builds, tests pass, boundaries hold, docs are present. Release is boring by design — the pipeline, not a human, certifies that the merge is safe.

## Stage 10 — Learning

The lifecycle closes where the product's own philosophy points: learning. Once investors record real Decisions, those Decisions become inputs to Learning Events — did the recorded reasoning hold up against outcomes and the Capital Mission's success definition? What the platform learns about decision quality feeds back into the product, and what *we* learn about building the feature feeds back into the next RFC. A feature is not finished when it ships; it is finished when we have learned from it. That closing loop is why the sequence exists.
