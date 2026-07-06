# Engineering Principles

*Volume VII — Engineering · Chapter 1*

These principles govern how we build, not what we build. Volume IV constrains
the *structure* of Aegis; this chapter constrains the *craft*. They apply to
every line of Python and TypeScript, every test, every migration, every script.
Where an engineering choice conflicts with one of these principles, either the
choice changes or an ADR is written to override it visibly. Silent violation is
a defect, caught in review.

## Principles We Hold

**1. Maintainability.** Code is read far more often than it is written and lives
far longer than the context that produced it. We optimise for the engineer who
inherits this file in eighteen months with none of today's memory. Small
modules, honest names, short functions, and boundaries that match Volume IV's
module map. A change should be local: touching Thesis validation must not
require understanding Capital allocation.

**2. Correctness.** Aegis advises on capital-bearing decisions. Wrong is worse
than slow and far worse than absent. Correctness is established by tests
(Chapter 4), by typed contracts, and by making illegal states unrepresentable —
prefer a value object that cannot hold an invalid quantity over a validated
primitive. Critical investment logic — Thesis validation, Decision recording,
Capital allocation — carries the highest bar.

**3. Clarity.** The reader should learn the domain from the code, not decode the
framework. Business intent belongs in domain language; technical mechanism stays
at module edges. If a reviewer must ask "what does this do?", the code has
failed before any bug is found. Clever is a liability; obvious is an asset.

**4. Observability.** A system you cannot see is a system you cannot operate.
Every module emits structured logs, metrics, and OpenTelemetry traces as a
condition of being shippable, not as a later enhancement. Provenance and audit
trails (Volume IV, Chapter 4) are part of this discipline: an unexplainable
Decision is unshippable.

**5. Scalability.** We build for the load we can justify, with headroom, not for
imagined web-scale. The Modular Monolith scales vertically and by careful use of
Redis and read paths first. Scaling decisions are measured against real numbers
and recorded, never assumed.

**6. Security.** We handle financial data and act on user capital. Least
privilege, secrets never in source, input validated at boundaries, dependencies
audited, and no user data in logs. Security is reviewed on every PR, not
delegated to a quarterly pass.

**7. Testability.** Code that is hard to test is badly designed. Dependencies
are injected, side effects are pushed to edges, and pure domain logic is kept
pure. If you cannot test a unit without a database, a network, or the clock, the
boundary is wrong — fix the design, not the test.

**8. Replaceability.** The architectural discipline of Volume IV applies to
craft: depend on interfaces and events, never concrete implementations. An LLM
provider, market-data vendor, or broker adapter is swapped by rewriting one
adapter. Model-agnostic AI is enforced through the Capability Gateway, never by
importing a vendor SDK into domain code.

**9. Determinism where possible.** Given the same inputs, code should produce the
same outputs. Injected clocks, seeded randomness, explicit ordering, and
idempotent handlers. AI calls are inherently non-deterministic; we quarantine
that non-determinism behind the gateway and record model and prompt versions so
results remain explainable and reproducible in intent.

## Anti-Patterns We Refuse

**Premature optimization.** Correct and clear first; fast when a measurement
demands it. Optimisation without a profiler and a number is speculation, and
speculation that obscures clarity is a net loss.

**Hidden behaviour and magic.** No metaprogramming that hides control flow, no
decorators with surprising side effects, no import-time work, no implicit global
state. Behaviour a reader cannot trace from the call site does not belong in
Aegis.

**Vendor lock-in.** No vendor concept leaks past an adapter. The domain never
knows which LLM, which broker, or which data vendor is in use. If swapping a
vendor touches domain code, the boundary has failed.

**Unnecessary abstraction.** An abstraction earns its place with two concrete
users or a boundary named in Volume IV. Interfaces with a single implementation
and no replacement story are noise. Delete speculative generality.

**Over-engineering.** Build the feature in the RFC, not the platform you imagine
following it. Configuration options nobody requested, plugin systems with no
plugins, and frameworks-within-frameworks are all forms of the same waste.

**Microservices without justification.** Aegis is a Modular Monolith by
deliberate decision (Volume IV). Extracting a service is an architectural change
requiring an RFC and ADR that demonstrate an independent scaling, deployment, or
failure-isolation need which module boundaries cannot satisfy. Distributed
systems are a cost, not a badge.

## How These Are Applied

Principles are enforced where work happens: in code review (Chapter 7), where a
reviewer names the principle a change violates; in CI (Chapter 5), which
mechanises the checkable subset; and in ADRs, which record every conscious
override. A new engineer is not expected to memorise this list — they are
expected to recognise, over their first weeks, that every convention in the
repository is one of these principles made concrete.
