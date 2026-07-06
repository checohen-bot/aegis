# Ubiquitous Language

This is the shared vocabulary of Aegis. Engineers, product, and the founder must use these terms identically — in code, in conversation, in the UI, and in this Bible. Names of the fifteen canonical objects are frozen and defined in their own documents; this reference fixes the **verbs and distinctions** that connect them so that a sentence means exactly one thing to everyone.

## Core Framing Terms

**Adaptive Quality Investing (AQI).** The methodology Aegis is built on: improving the *quality of capital-allocation decisions*, not predicting prices. "Quality" refers to the soundness of the process and reasoning; a good decision can have a bad outcome and vice versa.

**Decision quality.** A property of the *reasoning and process* behind a choice, assessed independently of its market outcome. The platform optimizes this, not returns.

**Capital allocation.** Any deployment of capital across opportunities. V1 is long-term public equity, but the language is domain-neutral so future domains reuse it unchanged.

## The Central Distinctions

**Observation vs. Evidence.** An **Observation** is an unevaluated noted change ("revenue growth decelerated this quarter") — raw, not yet judged. **Evidence** is a sourced fact that has been evaluated for relevance and credibility and bears on a specific Thesis. An Observation becomes Evidence only by being **evaluated**.

**Evidence vs. Knowledge.** **Evidence** is thesis-bound and often transient. **Knowledge** is durable, curated understanding distilled from many Evidence items and Observations, retained independently of any single Thesis.

**Thesis vs. Case.** An **Investment Thesis** is a falsifiable *belief* about why a Company is a good investment. An **Investment Case** is an *argument*, backed by Evidence, that supports or challenges that belief. A Thesis is what you believe; a Case is how you argue it.

**Risk vs. Catalyst.** A **Risk** is a way the Thesis could be *wrong* (a failure mode). A **Catalyst** is an anticipated *event* expected to move the Thesis's value or standing, in either direction. Risks are dangers; Catalysts are scheduled or conditional turning points.

## Canonical Verbs

**Form a thesis.** Create a new Investment Thesis with a stated, falsifiable belief and its falsification condition. Emits `ThesisFormed`.

**Invalidate a thesis.** Record that a Thesis has been proven false — its falsification condition has been met, a ThesisBreaking Risk has materialized, or its supporting Evidence has collapsed. Invalidation is a deliberate, recorded judgment, not mere doubt; it transitions the Thesis to an invalidated state, prompts a Decision review, and triggers a Learning Event. Invalidation is not deletion — the Thesis and its history remain.

**Confirm / challenge a thesis.** To **confirm** is to add Evidence that strengthens the belief; to **challenge** is to add Evidence that weakens it. Neither is invalidation; both adjust conviction.

**Evaluate an observation.** Assess a raw Observation for credibility and relevance, promoting it to Evidence (or discarding it). This is the gate between raw signal and thesis-bearing fact.

**Distill knowledge.** Synthesize one or more Evidence items and Observations into a durable Knowledge unit, or supersede an existing one.

**Trigger a catalyst.** Record that an anticipated event has occurred, creating an Observation and enabling comparison of the pre-registered expectation to the actual outcome. The Catalyst's pre-registered expected direction is immutable — this is what makes calibration honest.

**Materialize a risk.** Record that a previously identified failure mode has actually occurred, based on confirming signals. A materialized ThesisBreaking Risk forces an invalidation review.

**Make a decision.** Commit a buy, sell, hold, or resize choice *with recorded reasoning* and cited Theses/Cases. Emits `DecisionMade`. A Decision is immutable once committed.

**Resize a holding.** A Decision that changes the *size* of an existing position without closing it — adding to (scaling in) or trimming (scaling out) a Holding. Distinct from **open** (establish a new Holding) and **close** (exit entirely). "Rebalance" is a resize (or set of resizes) driven by a Policy band rather than a new judgment.

**Hold.** A deliberate, recorded Decision to take no size change after review — an active choice, not the absence of one. Aegis records holds so that inaction is auditable.

**Capture a learning.** Create a Learning Event: compare a pre-registered expectation to the actual outcome, attribute the result (skill, luck, process gap, knowledge gap, behavioral error, or correct-process-bad-outcome), and distill a forward-applicable lesson. Emits `LearningCaptured`.

**Attribute an outcome.** Assign the cause of a result across skill vs. luck vs. process. Crucially, a good outcome from a poor process and a poor outcome from a sound process are both first-class and must be labeled honestly.

**Enforce / breach a policy.** To **enforce** is to evaluate a Policy against a Decision at decision time (permit, warn, override, or block). A **breach** is a Decision that violates an Active Policy — a hard-blocked action prevented, or a soft-blocked action overridden with recorded justification. Breaches feed the Behavior Profile.

**Govern.** A Capital Mission **governs** Portfolios and parents Policies — it sets the intent and constraints against which everything else is judged. Suitability and success are always assessed *relative to the governing Mission*.

## Usage Rules

1. Never use "risk" loosely to mean volatility or price drawdown; a Risk is a named failure mode of a Thesis.
2. Never say "delete" for auditable objects; say **invalidate**, **retire**, **close**, or **supersede** as appropriate.
3. "Belief" maps to Thesis; "argument" maps to Case; "fact" maps to Evidence; "note" maps to Observation. Use them precisely.
4. "Learning" is always a captured Learning Event, not casual reflection.
5. A "good decision" refers to decision quality (process), never to a profitable outcome.
