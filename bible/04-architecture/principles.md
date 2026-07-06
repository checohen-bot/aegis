# Architectural Principles

*Volume IV — System Architecture · Chapter 1*

These principles govern every structural decision in Aegis. They are not
aspirational slogans; they are constraints. When a design choice conflicts with
one of these principles, the design changes or an Architecture Decision Record
(ADR) is written to consciously and visibly override the principle. Silent
violation is a defect.

## 1. Business-First Design

Architecture serves the domain, not the reverse. Aegis exists to improve the
*quality of investment decisions* for individual investors practicing Adaptive
Quality Investing. The structure of the system therefore mirrors the structure
of the problem: modules are drawn around canonical domain concepts — Portfolio,
Holding, Company, Investment Thesis, Investment Case, Evidence, Observation,
Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior
Profile, Policy — not around technical layers or infrastructure conveniences.
A newcomer reading the module map should learn the business, not the framework.
Technical concerns (caching, transport, serialization) are subordinate details
that live at module edges, never at their center.

## 2. Replaceability Over Reuse

Every external dependency and every internal module is designed to be replaced.
This is the defining discipline behind the Modular Monolith: we accept the
operational simplicity of a single deployable, but we refuse the internal
entanglement that usually accompanies it. Concretely — a module depends on
*interfaces and events*, never on another module's concrete implementation or
its tables. An LLM provider, a market-data vendor, or the broker (IBKR) can be
swapped by rewriting one adapter, not by touching domain logic. Replaceability
is verified, not assumed: if you cannot describe how a component would be
removed, its boundary is wrong.

## 3. Explicit Boundaries

Boundaries that are not enforced do not exist. Aegis draws hard lines between
modules and makes crossing them deliberate and visible. Cross-module
communication happens only through published interfaces (synchronous, in-process
calls against a stable contract) or domain events (asynchronous facts on the
event bus). There is no shared-table access, no reaching into another module's
internals, no ambient global state standing in for a contract. Each module owns
its domain objects and its persistence; the boundary is the API, and the API is
the promise. Chapter 5 (*Module Boundaries*) specifies the enforcement rules.

## 4. Explainability as a First-Class Concern

Aegis advises humans on high-stakes, capital-bearing decisions. An answer the
user cannot interrogate is worse than no answer. Explainability is therefore an
architectural property designed in from the first line, never a reporting
feature bolted on later. Every Decision, every AI-produced Observation or
Knowledge artifact, and every material recommendation must carry its provenance:
the Evidence it rests on, the Thesis or Policy it serves, the model and prompt
version that produced it, and the inputs that were current at the time. This
requirement shapes data models (provenance is a mandatory field, not an
afterthought), the AI Capability Gateway (which records model, version, and
inputs for every call), and the event schema (events are the audit trail). If a
feature cannot explain itself, it is not shippable.

## 5. Determinism Where Possible

Probabilistic components (LLMs, ranking heuristics) are isolated and bounded.
The domain core — portfolio accounting, thesis state transitions, policy
evaluation, risk and position math — is deterministic, testable, and free of
model calls. AI is used to *propose, summarize, and surface*; the domain
*decides and records* according to explicit rules. This separation keeps the
system auditable, keeps tests meaningful, and ensures that the same inputs
produce the same domain outcomes regardless of which model version was live.
Non-determinism is quarantined behind the AI Capability Gateway and always
lands in the domain as reviewable Evidence or Observations, never as silent
state mutation.

## 6. Model-Agnosticism

No module may hardcode against a specific LLM provider's SDK, endpoint, or
prompt dialect. All AI capability access flows through a single abstraction —
the AI Capability Gateway — which exposes intent-shaped operations
(*summarize this evidence*, *extract catalysts from this filing*) rather than
provider-shaped ones. Providers are configuration and adapters behind that
gateway. This protects Aegis from vendor lock-in, from pricing and capability
shifts, and from provider outages, and it makes A/B evaluation of models a
routing decision rather than a code change.

## 7. Microservices Are Deferred, Not Rejected

We deliberately build a Modular Monolith. Microservices impose distributed-
systems cost — network partitions, eventual consistency, deployment
choreography, and cross-service debugging — that a pre-scale product cannot
justify and that would slow the very domain iteration Aegis depends on. By
enforcing strict internal boundaries *now*, we retain the option to extract any
module into a service *later*, when — and only when — a specific, evidenced
pressure (independent scaling, isolation, or team topology) justifies it, and
an ADR records the decision. Extraction is an outcome earned by boundary
discipline, not a starting posture. Event sourcing and CQRS are deferred on the
same terms.
